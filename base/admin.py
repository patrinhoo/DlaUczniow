from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Category, Course, Requirement, LearnedSkill, Chapter, Lesson, Comment


admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Requirement)
admin.site.register(LearnedSkill)
admin.site.register(Chapter)
admin.site.register(Lesson)
admin.site.register(Comment)
