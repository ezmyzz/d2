from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    objects = None
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def update_rating(self):
        user = self.id_user

        post_list = Post.objects.filter(id_author=self, type=Post.article)

        post_rating_list = post_list.values("rating")
        result = 3 * (sum(item["rating"] for item in post_rating_list))

        comment_rating_list = Comment.objects.filter(id_user=user).values("rating")
        result += sum(item["rating"] for item in comment_rating_list)

        for post in post_list:
            comment_in_post = Comment.objects.filter(id_post=post).values("rating")
            result += sum(item["rating"] for item in comment_in_post)

        self.rating = result
        self.save()


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=128, unique=True)


class Post(models.Model):
    objects = None
    article = "AR"
    news = "NW"
    POST_TYPE = [(article, 'Статья'), (news, 'Новость')]

    id_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=POST_TYPE, default=article)
    created = models.DateTimeField(auto_now_add=True)
    id_post_category = models.ManyToManyField(Category, through="PostCategory")
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField()

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        result = self.text[:124] + "..."
        return result


class PostCategory(models.Model):
    objects = None
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    objects = None
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField()

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
