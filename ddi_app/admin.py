from django.contrib import admin

from ddi_app.models import UserProfile, Test

# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'date_birth', 'about_user']


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'description', 'attempts', 'attempt_passed']

#
# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ['test', 'question']


# @admin.register(Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ['question', 'answer']
