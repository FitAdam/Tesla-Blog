from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    """The blog post."""
    title = models.CharField(max_length=150)
    header_image = models.ImageField(null=True, blank=True, upload_to="images/")
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        """Return a string representation of the model."""
        return self.title
