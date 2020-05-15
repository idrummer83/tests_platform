from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView

from ddi_app.forms import UserProfileForm

from ddi_app.models import UserProfile

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

            UserProfile.objects.create(user_id=pk, first_name=first_name, last_name=last_name, date_birth=date_birth,
                                       about_user=about_user).save()

            return redirect('/')
        else:
            # messages.error(request, form.errors)
            return redirect('/signup/')
    else:
        form = UserProfileForm()
    return render(request, 'profile.html', {'form': form})

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('/')
#     else:
#         form = SignUpForm()
#     return render(request, 'registration/signup.html', {'form': form})


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['user_profile'] = UserProfile.objects.filter(id=kwargs['user'].id)
        return context


@login_required
def home(request):
    return render(request, 'home.html')
