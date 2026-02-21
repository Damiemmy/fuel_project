# # core/management/commands/import_truckstops.py
# import csv
# from decimal import Decimal
# from django.core.management.base import BaseCommand
# from core.models import TruckStop

# class Command(BaseCommand):
#     help = "Import truck stop data from CSV"

#     def add_arguments(self, parser):
#         parser.add_argument(
#             "--file",
#             type=str,
#             help="Path to the CSV file",
#             required=True
#         )

#     def handle(self, *args, **options):
#         file_path = options["file"]
#         created_count = 0
#         updated_count = 0

#         with open(file_path, newline='', encoding="utf-8") as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 # Parse data
#                 opis_id = int(row["OPIS Truckstop ID"])
#                 name = row["Truckstop Name"]
#                 address = row["Address"]
#                 city = row["City"]
#                 state = row["State"].upper()  # just in case
#                 latitude = float(row.get("Latitude", 0))
#                 longitude = float(row.get("Longitude", 0))
#                 retail_price = Decimal(row["Retail Price"])

#                 # Update or create record
#                 obj, created = TruckStop.objects.update_or_create(
#                     opis_truckstop_id=opis_id,
#                     defaults={
#                         "name": name,
#                         "address": address,
#                         "city": city,
#                         "state": state,
#                         "latitude": latitude,
#                         "longitude": longitude,
#                         "retail_price": retail_price,
#                     },
#                 )
#                 if created:
#                     created_count += 1
#                 else:
#                     updated_count += 1

#         self.stdout.write(
#             self.style.SUCCESS(
#                 f"Import finished! Created: {created_count}, Updated: {updated_count}"
#             )
#         )



# core/management/commands/import_truckstops.py
import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from core.models import TruckStop, RackPrice  # <-- import RackPrice

class Command(BaseCommand):
    help = "Import truck stop data from CSV"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            help="Path to the CSV file",
            required=True
        )

    def handle(self, *args, **options):
        file_path = options["file"]
        created_count = 0
        updated_count = 0
        rack_created_count = 0

        with open(file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # TruckStop fields
                opis_id = int(row["OPIS Truckstop ID"])
                name = row["Truckstop Name"]
                address = row["Address"]
                city = row["City"]
                state = row["State"].upper()
                latitude = float(row.get("Latitude", 0))
                longitude = float(row.get("Longitude", 0))

                # RackPrice fields
                rack_id = int(row["Rack ID"])
                retail_price = Decimal(row["Retail Price"])

                # Update or create TruckStop
                truckstop_obj, created = TruckStop.objects.update_or_create(
                    opis_truckstop_id=opis_id,
                    defaults={
                        "name": name,
                        "address": address,
                        "city": city,
                        "state": state,
                        "latitude": latitude,
                        "longitude": longitude,
                    },
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

                # Create or update RackPrice
                rack_obj, rack_created = RackPrice.objects.update_or_create(
                    truckstop=truckstop_obj,
                    rack_id=rack_id,
                    defaults={"retail_price": retail_price}
                )
                if rack_created:
                    rack_created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"TruckStops imported! Created: {created_count}, Updated: {updated_count}\n"
                f"RackPrices imported! Created: {rack_created_count}"
            )
        )