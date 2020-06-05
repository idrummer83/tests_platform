from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from ddi_app.forms import UserProfileForm, CommentForm

from ddi_app.models import UserProfile, Test, QuestionAnswer, UserStatistic, Comment

# Create your views here.


class BasePageView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


@login_required(login_url='accounts/login')
def updateprofile(request, pk):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            date_birth = form.cleaned_data['date_birth']
            about_user = form.cleaned_data['about_user']
            photo = form.cleaned_data['photo']
            fs = FileSystemStorage()
            fs.save(photo.name, photo)

            user_exist = UserProfile.objects.filter(user_id=pk).first()

            if user_exist:
                UserProfile.objects.update(user_id=pk, first_name=first_name, last_name=last_name, date_birth=date_birth,
                                       about_user=about_user, photo=photo)
            else:
                UserProfile.objects.create(user_id=pk, first_name=first_name, last_name=last_name, date_birth=date_birth,
                                       about_user=about_user, photo=photo).save()

            return redirect('/accounts/profile/')
        else:
            messages.error(request, form.errors)
            return redirect('/signup/')
    else:
        form = UserProfileForm()
    return render(request, 'profile.html', {'form': form})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tests_list'] = Test.objects.filter(user_id=self.request.user.id, complete=True)
        context['user_profile'] = UserProfile.objects.filter(user_id=self.request.user.id).first()
        return context


class CreateTestPage(LoginRequiredMixin, TemplateView):
    template_name = 'create_test_page.html'


class CreateQuestionPage(LoginRequiredMixin, TemplateView):
    template_name = 'create_question_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test_questions'] = QuestionAnswer.objects.filter(test_id=kwargs['pk']).count()
        context['test_id'] = kwargs['pk']
        return context


@login_required(login_url='accounts/login')
def create_test(request, pk):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        attempts = request.POST['attempts']

        Test.objects.create(user_id=pk, title=title, description=description, attempts=attempts).save()
        last = Test.objects.all().last()

        return redirect('/create_question_page/{}'.format(last.id))


@login_required(login_url='accounts/login')
def create_question(request, pk):
    if request.method == 'POST':
        question = request.POST['question']
        answer_1 = request.POST['answer_1']
        answer_1_status = request.POST.get('answer_1_status', False)
        if answer_1_status == 'on':
            answer_1_status = True
        else:
            answer_1_status = False

        answer_2 = request.POST['answer_2']
        answer_2_status = request.POST.get('answer_2_status', False)
        if answer_2_status == 'on':
            answer_2_status = True
        else:
            answer_2_status = False

        answer_3 = request.POST['answer_3']
        answer_3_status = request.POST.get('answer_3_status', False)
        if answer_3_status == 'on':
            answer_3_status = True
        else:
            answer_3_status = False

        answer_4 = request.POST['answer_4']
        answer_4_status = request.POST.get('answer_4_status', False)
        if answer_4_status == 'on':
            answer_4_status = True
        else:
            answer_4_status = False

        QuestionAnswer.objects.create(test_id=pk, question=question, answer_1=answer_1,
                                      answer_1_status=answer_1_status, answer_2=answer_2,
                                      answer_2_status=answer_2_status, answer_3=answer_3,
                                      answer_3_status=answer_3_status, answer_4=answer_4,
                                      answer_4_status=answer_4_status).save()
        test_min_question = Test.objects.filter(id=pk).values_list('question_min_number', flat=True).first()
        question_count = QuestionAnswer.objects.filter(test_id=pk).count()
        if test_min_question < question_count:
            Test.objects.filter(id=pk).update(complete=True)

        return redirect('/create_question_page/{}'.format(pk))


class TestView(LoginRequiredMixin, TemplateView):
    template_name = 'test_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_denied = UserStatistic.objects.filter(test_denied=True).values_list('test_id', flat=True)
        test_denied = Test.objects.filter(id=kwargs['pk']).first()

        denied = False
        if test_denied.id in id_denied:
            denied = True

        context['denied'] = denied
        context['test'] = Test.objects.filter(id=kwargs['pk']).first()
        context['comments'] = Comment.objects.filter(test_id=kwargs['pk'])
        return context


class TestsListView(LoginRequiredMixin, TemplateView):
    template_name = 'tests_list_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_denied = UserStatistic.objects.filter(user_stat_id=kwargs['pk'],test_denied=True).values_list('test_id', flat=True)
        user_stat_list = UserStatistic.objects.filter(user_stat_id=kwargs['pk']).exclude(test_id__in=id_denied).values_list('test_id', flat=True)

        context['passed_tests_list'] = Test.objects.filter(id__in=user_stat_list).order_by('date').reverse()
        context['tests_denied'] = Test.objects.filter(id__in=id_denied).order_by('date').reverse()
        context['all_tests_list'] = Test.objects.filter(complete=True).order_by('date').reverse()

        return context


class PassTestPage(LoginRequiredMixin, TemplateView):
    template_name = 'pass_test_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = Test.objects.filter(id=kwargs['pk']).first()
        context['questions_list'] = QuestionAnswer.objects.filter(test_id=kwargs['pk'])
        return context


@login_required(login_url='accounts/login')
def test_answer(request, pk):
    qw_answ = QuestionAnswer.objects.filter(test_id=pk).only('answer_1_status', 'answer_2_status', 'answer_3_status', 'answer_4_status')
    try:
        answ = UserStatistic.objects.filter(user_stat_id=request.user.id, test_id=pk).only(
            'answer_attempt_passed').last()
        attempt_passed = answ.answer_attempt_passed
        attempt_passed += 1
    except AttributeError:
        attempt_passed = 1

    if request.method == 'POST':
        wrap_lst_answers = []

        for q_id in request.POST.getlist('question_id'):
            list_answers = []
            for i in range(1, 5):
                s = '{}_answer'.format(q_id)
                if request.POST.get(s) == 'on':
                    list_answers.append(('{}'.format(q_id),'answer_{}_status'.format(i), True))
            wrap_lst_answers.append(list_answers)
        result = []
        try:
            for x in wrap_lst_answers:
                answer = vars(qw_answ.filter(id=int(x[0][0])).first())

                if answer[x[0][1]] is x[0][2]:
                    result.append('question id-{} passed'.format(int(x[0][0])))
        except:
            messages.error(request, 'Empty or excess point, remind you - every question has only ONE answer.')
            return redirect('/pass_test_page/{}'.format(pk))

        percent = (len(result)/qw_answ.count())*100

        att = False
        attempts = Test.objects.filter(id=pk).only('attempts').first()
        if attempts.attempts == attempt_passed:
            att = True
        UserStatistic.objects.create(test_id=pk, user_stat_id=request.user.id, test_denied=att,
                                     answer_attempt_passed=attempt_passed,
                                     answer_percent=percent, correct_answer_number=len(result)).save()

    return redirect('/result_page/{}'.format(pk))


class ResultPage(TemplateView, LoginRequiredMixin):
    template_name = 'result_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result'] = UserStatistic.objects.filter(test_id=kwargs['pk']).last()
        return context


class Filter(LoginRequiredMixin, TemplateView):
    template_name = "tests_list_page.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Filter, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tests_list = Test.objects.all()
        if self.request.method == 'GET':
            if self.request.GET.get('search'):
                search_text = self.request.GET.get('search')
                search_result = Test.objects.filter(title__icontains=search_text)
                context['all_tests_list'] = search_result
                return context
        context['all_tests_list'] = tests_list
        return context


class CommentView(LoginRequiredMixin, FormView):
    template_name = "comment_page.html"
    form_class = CommentForm

    def form_valid(self, form):
        user = self.request.user.id
        comment = form.cleaned_data['comment']
        Comment.objects.create(user_id=user, test_id=self.kwargs['pk'], comment=comment).save()
        return redirect('/test_page/{}'.format(self.kwargs['pk']))

    def form_invalid(self, form):
        return super().form_valid(form)