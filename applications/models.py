from django.db import models
from django.contrib.auth.models import User

# Create your models here.


STATUS_CHOICES = [
    ('Applied', 'Applied'),
    ('Rejected', 'Rejected'),
    ('Pending', 'Pending'),
    ('Interview', 'Interview'),
]


FIELD_TYPES = [
    ('text', 'Text'),
    ('number', 'Number'),
    ('date', 'Date'),
    ('select', 'Select'),
]

class JobApplications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Applied' )
    notes = models.TextField(blank=True)
    applied_on = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company}-{self.position}"




class CustomColumn(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    options = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


    def __str__(self):
        return self.name



class JobCustomValue(models.Model):
    job = models.ForeignKey(JobApplications, on_delete=models.CASCADE, related_name='custom_values')
    column = models.ForeignKey(CustomColumn, on_delete=models.CASCADE)
    value = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('job', 'column')