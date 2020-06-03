from django.db import models
from django.contrib.auth.models import User

from datetime import date

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile', verbose_name='user')
    first_name = models.CharField(verbose_name='first name', max_length=30, blank=True)
    last_name = models.CharField(verbose_name='last name', max_length=150, blank=True)
    date_birth = models.DateField(format('%Y-%m-%d'), null=True, blank=True)
    about_user = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'user profile'
        verbose_name_plural = 'users profile'


class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_user', verbose_name='user')
    title = models.CharField(max_length=500, verbose_name='title')
    description = models.TextField(max_length=2000, verbose_name='description')
    attempts = models.SmallIntegerField(default=2, verbose_name='number of attempts')
    question_min_number = models.SmallIntegerField(default=5, verbose_name='minimal number of questions')
    complete = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'test'
        verbose_name_plural = 'tests'


class QuestionAnswer(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='question_test', verbose_name='test')
    question = models.CharField(max_length=1500, verbose_name='question')
    answer_1 = models.CharField(max_length=1500, verbose_name='answer1')
    answer_1_status = models.BooleanField(default=False, verbose_name='answer1 variant')
    answer_2 = models.CharField(max_length=1500, verbose_name='answer2')
    answer_2_status = models.BooleanField(default=False, verbose_name='answer2 variant')
    answer_3 = models.CharField(max_length=1500, verbose_name='answer3')
    answer_3_status = models.BooleanField(default=False, verbose_name='answer3 variant')
    answer_4 = models.CharField(max_length=1500, verbose_name='answer4')
    answer_4_status = models.BooleanField(default=False, verbose_name='answer4 variant')

    class Meta:
        verbose_name = 'question'
        verbose_name_plural = 'questions'


class UserStatistic(models.Model):
    test_id = models.SmallIntegerField(verbose_name='test answer')
    user_stat = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_stat', verbose_name='user_statistic')
    answer_attempt_passed = models.SmallIntegerField(default=0, verbose_name='number of passed attempts')
    test_denied = models.BooleanField(default=False, verbose_name='test_denied')
    answer_percent = models.SmallIntegerField(verbose_name='answer in percents')
    correct_answer_number = models.SmallIntegerField(verbose_name='correct_answer_number')
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'user statistic'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment', verbose_name='user_comment')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test_comment', verbose_name='test_comment')
    comment = models.TextField(verbose_name='user comment')

    class Meta:
        verbose_name = 'user comment'