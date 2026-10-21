from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to='Posts')
    description=models.CharField(max_length=300)
    created_at=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    comments=models.CharField(max_length=400)
    added_at=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    post_obj=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')

    def __str__(self):
        return self.comments

class Like(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    post_obj=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('owner','post_obj')

class Follow(models.Model):
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
    following=models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers')
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('follower','following')


