from django.db import models
from accounts.models import CustomUser

class PhotoModel(models.Model):
    id = models.BigAutoField(primary_key=True) 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    likes = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class LikeModel(models.Model):
    id = models.BigAutoField(primary_key=True) 
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    photo = models.ForeignKey(PhotoModel,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    id = models.BigAutoField(primary_key=True) 
    follower = models.ForeignKey(CustomUser,related_name='followers',on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser,related_name='following',on_delete=models.CASCADE)



