from django.db import models
from account.models import MyUser
from vote.models import VoteModel


class Post(VoteModel, models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=50, verbose_name="Title")
    url = models.SlugField(max_length=150, unique=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created date")

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comment')

    def __str__(self):
        return str(self.comment)

