from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView

from ddi_app.forms import UserProfileForm

from ddi_app.models import UserProfile, Test, Answer

# Create your views here.


class BasePageView(TemplateView):
    template_name = 'index.html'


def updateprofile(request, pk):
    if request.method == 'POST':
        form = UserProfileForm(request.POST or None)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            date_birth = form.cleaned_data['date_birth']
            about_user = form.cleaned_data['about_user']

            user_exist = UserProfile.objects.filter(user_id=pk).first()

            if user_exist:
                UserProfile.objects.update(user_id=pk, first_name=first_name, last_name=last_name, date_birth=date_birth,
                                       about_user=about_user)
            else:
                UserProfile.objects.create(user_id=pk, first_name=first_name, last_name=last_name, date_birth=date_birth,
                                       about_user=about_user).save()

            return redirect('/accounts/profile/')
        else:
            # messages.error(request, form.errors)
            return redirect('/signup/')
    else:
        form = UserProfileForm()
    return render(request, 'profile.html', {'form': form})


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.filter(user_id=self.request.user.id).first()
        return context


@login_required
def home(request):
    return render(request, 'home.html')


class CreateTestPage(TemplateView):
    template_name = 'create_test_page.html'


class CreateAnswersPage(TemplateView):
    template_name = 'create_answers_page.html'


def create_test(request, pk):
    if request.method == 'POST':
        user = request.POST['user_id']
        title = request.POST['title']
        description = request.POST['description']
        attempts = request.POST['attempts']

        Test.objects.create(user_id=user, title=title, description=description, attempts=attempts).save()

        return redirect('/create_answers_page/')


def create_answers(request):
    if request.method == 'POST':
        user = request.POST['user_id']
        title = request.POST['title']
        description = request.POST['description']
        attempts = request.POST['attempts']

        Answer.objects.create(user=user, title=title, description=description, attempts=attempts).save()

        return redirect('/create_answers_page/')