from django.db import models
from django.utils import timezone

class Submission(models.Model):
    # example fields; adjust to your project (E-Hospitality: patient_name, email, issue, etc.)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.name} <{self.email}> @ {self.created_at.isoformat()}"
