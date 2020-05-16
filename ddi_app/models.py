from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile', verbose_name='user')
    first_name = models.CharField(verbose_name='first name', max_length=30, blank=True)
    last_name = models.CharField(verbose_name='last name', max_length=150, blank=True)
    date_birth = models.DateField(format('%Y-%m-%d'), null=True, blank=True)
    about_user = models.TextField(blank=True, null=True)

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
    attempt_passed = models.SmallIntegerField(default=0, verbose_name='number of passed attempts')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'test'
        verbose_name_plural = 'tests'


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='question_test', verbose_name='test')
    question = models.CharField(max_length=1500, verbose_name='question')

    class Meta:
        verbose_name = 'question'
        verbose_name_plural = 'questions'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_question', verbose_name='answer')
    answer = models.CharField(max_length=1500, verbose_name='answer')
    answer_variant = models.BooleanField(default=False, verbose_name='answer variant')

    class Meta:
        verbose_name = 'answer'
        verbose_name_plural = 'answers'

