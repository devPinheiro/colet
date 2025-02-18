from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Lower

# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    preferences = models.JSONField(default=dict, blank=True)
    verified = models.BooleanField(default=False)

    # FIX: Resolve reverse accessor clashes
    groups = models.ManyToManyField(
        "auth.Group", related_name="api_user_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="api_user_permissions", blank=True
    )

    class Meta:
        indexes = [
            models.Index(Lower('email'), name="email_lower_idx")
        ]

# Property Listings
class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, db_index=True)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    available_from = models.DateField()
    amenities = models.JSONField(default=dict, blank=True)
    images = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Matches
class Match(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')]

    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_sent')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_received')
    compatibility_score = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
