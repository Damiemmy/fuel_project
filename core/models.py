from django.db import models

# Create your models here.

class TruckStop(models.Model):
    opis_truckstop_id = models.PositiveIntegerField(
        unique=True,
        db_index=True
    )

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    city = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=2, db_index=True)

    latitude = models.FloatField()
    longitude = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["latitude", "longitude"]),
        ]
        ordering = ["name"]  # or city, not price

    def __str__(self):
        return f"{self.name} - {self.city}, {self.state}"

    def save(self, *args, **kwargs):
        self.state = self.state.upper()
        super().save(*args, **kwargs)

class RackPrice(models.Model):
    truckstop = models.ForeignKey(
        TruckStop,
        on_delete=models.CASCADE,
        related_name="rack_prices"
    )
    rack_id = models.PositiveIntegerField(db_index=True)
    retail_price = models.DecimalField(max_digits=10, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("truckstop", "rack_id")
        indexes = [
            models.Index(fields=["rack_id"]),
            models.Index(fields=["retail_price"]),
        ]

    def __str__(self):
        return f"{self.truckstop.name} - Rack {self.rack_id}"