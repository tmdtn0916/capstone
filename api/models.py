from django.db import models

class StoryRequest(models.Model):
    keywords = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keywords
