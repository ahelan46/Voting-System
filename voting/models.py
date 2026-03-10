from django.db import models
from .utils import generate_qr

class Voter(models.Model):
    name = models.CharField(max_length=100)
    voter_id = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=10)
    has_scanned = models.BooleanField(default=False)
    has_voted = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            qr_path = generate_qr(self.voter_id)
            self.qr_code = qr_path
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
        return self.voter_id


class Party(models.Model):
    party_name = models.CharField(max_length=100)

    def __str__(self):
        return self.party_name


class Vote(models.Model):
    voter = models.OneToOneField(Voter, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)


class VotingSession(models.Model):
    is_active = models.BooleanField(default=False)

