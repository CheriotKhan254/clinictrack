import pandas as pd
from django.core.management.base import BaseCommand

from clinic.models import Facility, LandRecord


def find_column(df, *keywords):
    """
    Find a column whose name (lowercased) contains ALL given keywords.
    Returns the column name or None if not found.
    """
    for col in df.columns:
        lower = str(col).lower()
        if all(k in lower for k in keywords):
            return col
    return None


class Command(BaseCommand):
    help = "Import facilities and land data from an Excel file into Facility and LandRecord."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            default="/home/user/Downloads/HEALTH 13062025-1.xlsx",
            help="Path to the Excel file to import.",
        )

    def handle(self, *args, **options):
        path = options["file"]
        self.stdout.write(f"Reading Excel file: {path}")

        df = pd.read_excel(path)

        # Try to automatically detect important columns based on keywords.
        facility_col = (
            find_column(df, "facility", "name")
            or find_column(df, "public", "utility")
            or find_column(df, "health", "facility")
        )

        subcounty_col = find_column(df, "sub", "county")
        ward_col = find_column(df, "ward")
        location_col = find_column(df, "village") or find_column(df, "location")

        # Land size (acres / hectares / size)
        land_size_col = (
            find_column(df, "land", "acre")
            or find_column(df, "land", "ha")
            or find_column(df, "land", "size")
        )

        # Land use description
        land_use_col = find_column(df, "land", "use") or find_column(df, "current", "use")

        # Dispute status column (e.g. "Disputed/ undisputed")
        dispute_col = None
        for col in df.columns:
            if "disputed" in str(col).lower():
                dispute_col = col
                break

        if facility_col is None:
            raise RuntimeError("Could not find a column for facility/public utility name.")

        self.stdout.write("Detected columns:")
        self.stdout.write(f"  Facility name: {facility_col}")
        self.stdout.write(f"  Subcounty:     {subcounty_col}")
        self.stdout.write(f"  Ward:          {ward_col}")
        self.stdout.write(f"  Location:      {location_col}")
        self.stdout.write(f"  Land size:     {land_size_col}")
        self.stdout.write(f"  Land use:      {land_use_col}")
        self.stdout.write(f"  Dispute:       {dispute_col}")

        created_facilities = 0
        created_land_records = 0

        for _, row in df.iterrows():
            name_raw = row.get(facility_col)
            if pd.isna(name_raw):
                continue
            name = str(name_raw).strip()
            if not name:
                continue

            subcounty = str(row.get(subcounty_col, "") or "").strip() if subcounty_col else ""
            ward = str(row.get(ward_col, "") or "").strip() if ward_col else ""
            location = str(row.get(location_col, "") or "").strip() if location_col else ""

            # Land size
            acreage = 0.0
            if land_size_col:
                size_raw = row.get(land_size_col, 0)
                try:
                    acreage = float(size_raw) if size_raw not in (None, "") else 0.0
                except Exception:
                    acreage = 0.0

            # Land use
            land_use = ""
            if land_use_col:
                land_use = str(row.get(land_use_col, "") or "").strip()

            # Dispute / undisputed
            dispute_status = ""
            if dispute_col:
                dispute_raw = str(row.get(dispute_col, "") or "").strip().lower()
                if "disputed" in dispute_raw and "un" not in dispute_raw:
                    dispute_status = "Disputed"
                elif "undisputed" in dispute_raw or "not disputed" in dispute_raw:
                    dispute_status = "Undisputed"

            facility, fac_created = Facility.objects.get_or_create(
                name=name,
                subcounty=subcounty,
                ward=ward,
                defaults={"location": location},
            )
            if fac_created:
                created_facilities += 1

            LandRecord.objects.create(
                facility=facility,
                acreage=acreage,
                land_use=land_use,
                dispute_status=dispute_status,
            )
            created_land_records += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Facilities created: {created_facilities}, land records created: {created_land_records}"
            )
        )

