from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

EXPIRATION_DAYS = 1

class Picture(models.Model):
    image = models.ImageField(upload_to='pictures/')
    created_at = models.DateTimeField(default=timezone.now)
    delete_password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.delete_password = make_password(raw_password)

    def check_delete_password(self, raw_password):
        return check_password(raw_password, self.delete_password)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(days=EXPIRATION_DAYS)

    def expires_at(self):
        return self.created_at + timezone.timedelta(days=EXPIRATION_DAYS)

    def time_remaining(self):
        remaining = self.expires_at() - timezone.now()
        if remaining.total_seconds() <= 0:
            return None
        days = remaining.days
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes = remainder // 60
        return {'days': days, 'hours': hours, 'minutes': minutes}
