from django.contrib import admin

from ddi_app.models import UserProfile, Test, UserStatistic, QuestionAnswer

# Register your models here.


class UserStatisticAdmin(admin.TabularInline):
    model = UserStatistic


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'date_birth', 'about_user']
    inlines = [
        UserStatisticAdmin,
    ]


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'description', 'attempts', 'date']


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['test', 'question']
