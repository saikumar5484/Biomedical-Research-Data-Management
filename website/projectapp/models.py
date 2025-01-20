# # projectapp/models.py
# from django.db import models

# class Project(models.Model):
#     sno = models.IntegerField()
#     year = models.IntegerField()
#     document_link = models.URLField()
#     project_id = models.CharField(max_length=100,unique=True)
#     project_details = models.TextField()

#     def __str__(self):
#         return self.project_id

# class Review(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Link to the user who submitted the review
#     rating = models.PositiveIntegerField()
#     review_text = models.TextField(null=True, blank=True)

from datetime import timezone
from django.db import models


class Project(models.Model):
    sno = models.IntegerField()
    year = models.IntegerField()
    document_link = models.URLField()
    project_id = models.CharField(max_length=100, unique=True)
    project_details = models.TextField()

    def __str__(self):
        return self.project_id


class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Link to the user who submitted the review
    rating = models.PositiveIntegerField()
    review_text = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return f"Review for {self.project.project_id} by {self.user.username}"
    
   
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name
    

# models.py
from django.db import models
from django.utils import timezone

class UploadData(models.Model):
    sno = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    doc_link = models.FileField(upload_to='documents/')
    project_id = models.CharField(max_length=50)
    project_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

