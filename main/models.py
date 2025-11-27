from django.db import models
from django.contrib.auth.models import User

class Media(models.Model):
    MEDIA_TYPES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]
    
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='photo')
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title or f"{self.media_type.title()} {self.id}"
    
    def is_image(self):
        return self.media_type == 'photo'
    
    def is_video(self):
        return self.media_type == 'video'
    
    def file_extension(self):
        return self.file.name.split('.')[-1].lower()
