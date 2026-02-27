from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

User = get_user_model()

class Command(BaseCommand):
    help = "Delete users who never verified their email (older than 3 days)"

    def handle(self, *args, **kwargs):
        days_threshold = 1
        threshold_date = timezone.now() - timedelta(days=days_threshold)

        # Get all unverified emails
        unverified_emails = EmailAddress.objects.filter(
            verified=False
        )

        # Corresponding users older than threshold
        users_to_delete = User.objects.filter(
            email__in=unverified_emails.values_list('email', flat=True),
            date_joined__lt=threshold_date
        )

        count = users_to_delete.count()
        users_to_delete.delete()
        self.stdout.write(f"Deleted {count} unverified users older than {days_threshold} days")