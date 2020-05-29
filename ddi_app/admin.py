from django.contrib import admin

from ddi_app.models import UserProfile, Test, UserStatistic, QuestionAnswer

# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'date_birth', 'about_user']


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'description', 'attempts', 'date']


@admin.register(UserStatistic)
class UserStatisticAdmin(admin.ModelAdmin):
    list_display = ['test_id', 'user_stat', 'answer_attempt_passed', 'answer_percent', 'correct_answer_number', 'date']


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['test', 'question']
