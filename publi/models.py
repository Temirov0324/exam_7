from django.db import models

# Create your models here.

class Publication(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image=models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"

    def __str__(self):
        return self.title