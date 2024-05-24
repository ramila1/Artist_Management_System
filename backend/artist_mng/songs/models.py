from django.db import models
from users.models import CustomUser
from django.utils import timezone

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_artist': True})
    release_date = models.DateField()
    duration = models.CharField(max_length=10)
    lyrics = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
    

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        super().delete()
