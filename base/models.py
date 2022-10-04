from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.dispatch import receiver
from django.db.models.signals import post_delete


# Create your models here.
class UserProfile(models.Model):
    name = models.CharField(max_length=200, null=True)
    about = models.TextField(null=True, default="Uzupełnij informacje o sobie")
    registration_date = models.DateTimeField(auto_now_add=True, null=True)
    avatar = models.ImageField(
        null=True, default="media/profile.jpg", upload_to='media/profile_images/')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.name:
            return self.name
        return self.username


@receiver(post_delete, sender=UserProfile)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:  # just in case user is not specified
        instance.user.delete()


class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    image = models.ImageField(
        null=True, default="media/default-course.png", upload_to='media/course_images/')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    members = models.ManyToManyField(User, related_name='members', blank=True)

    def __str__(self):
        return self.course_name


class Requirement(models.Model):
    requirement = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.requirement


class LearnedSkill(models.Model):
    skill = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.skill


class Chapter(models.Model):
    chapter_name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.chapter_name[:50]


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    video = models.FileField(validators=[FileExtensionValidator(
        allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])], upload_to='media/videos/')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.lesson_name


class Comment(models.Model):
    comment_body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.comment_body[:50]
