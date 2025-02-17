from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.fields import ArrayField
from django.db.models.functions import Lower

# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    preferences = models.JSONField(default=dict, blank=True)
    verified = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(Lower('email'), name="email_lower_idx")  # Case-insensitive unique email
        ]

# Property Listings
class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, db_index=True)  # Indexed for faster queries
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    available_from = models.DateField()
    amenities = models.JSONField(default=dict, blank=True)
    images = ArrayField(models.TextField(), blank=True, default=list)  # PostgreSQL optimized array field
    created_at = models.DateTimeField(auto_now_add=True)

# User Matches
class Match(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')]

    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_sent')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_received')
    compatibility_score = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Messages with Real-time Support
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# Reviews
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Payments (Future Feature)
class Payment(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')]

    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_made')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [GinIndex(fields=['status'])]  # Fast filtering

