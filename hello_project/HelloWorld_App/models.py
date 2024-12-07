from django.db import models
from django.utils import timezone

# Create your models here.
#class Library(models.Model): #ORM
#    content = models.TextField()
class Library(models.Model):
    STATUS_CHOICES = [
        (1, 'To Be Read'),   # TBR
        (2, 'Current'),      # Current
        (3, 'Read'),         # Read
    ]
    content = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.content} ({self.get_status_display()})"