from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class TopsisAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_file = models.CharField(max_length=400)
    weights = models.CharField(max_length=255)
    impacts = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class TopsisResult(models.Model):
    analysis = models.ForeignKey(TopsisAnalysis, on_delete=models.CASCADE)
    topsis_score = models.TextField()  # Store as text or JSON if you want to store arrays
    rank = models.TextField()

    def __str__(self):
        return f"Result for {self.analysis}"