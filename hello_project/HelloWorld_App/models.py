from django.db import models
from django.utils import timezone
from django.db.models import Index

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
    author = models.TextField() #new
    genre = models.TextField() #new
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    date_added = models.DateTimeField(default=timezone.now)
    rating = models.FloatField(null=True, blank=True) #new
    review_id = models.ForeignKey('Review', on_delete=models.SET_NULL, null=True, blank=True)#new

    class Meta:
        indexes = [Index(fields=['content']), Index(fields=['author']),]
    def __str__(self):
        return f"{self.content} ({self.get_status_display()})"
    
class Review(models.Model): #all new
    review_id = models.AutoField(primary_key=True)
    review_title = models.TextField()
    review_content = models.TextField()

    def __str__(self):
        return self.review_title