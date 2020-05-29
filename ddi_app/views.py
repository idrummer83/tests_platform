from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.db.models import Count, F, Value


from ddi_app.forms import UserProfileForm, CommentForm

from ddi_app.models import UserProfile, Test, QuestionAnswer, UserStatistic, Comment

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
        context['tests_list'] = Test.objects.filter(user_id=self.request.user.id)
        context['user_profile'] = UserProfile.objects.filter(user_id=self.request.user.id).first()
        return context


@login_required
def home(request):
    return render(request, 'home.html')


class CreateTestPage(TemplateView):
    template_name = 'create_test_page.html'


class CreateQuestionPage(TemplateView):
    template_name = 'create_question_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test_id'] = kwargs['pk']
        return context


def create_test(request, pk):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        attempts = request.POST['attempts']

        Test.objects.create(user_id=pk, title=title, description=description, attempts=attempts).save()
        last = Test.objects.all().last()

        return redirect('/create_question_page/{}'.format(last.id))


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

        return redirect('/create_question_page/{}'.format(pk))


class TestView(TemplateView):
    template_name = 'test_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = Test.objects.filter(id=kwargs['pk']).first()
        context['comments'] = Comment.objects.filter(test_id=kwargs['pk'])
        return context


class TestsListView(TemplateView):
    template_name = 'tests_list_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # UserStatistic.objects.filter(user_stat_id=kwargs['pk'])
        context['tests_list'] = Test.objects.order_by('date')
        return context


class PassTestPage(TemplateView):
    template_name = 'pass_test_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = Test.objects.filter(id=kwargs['pk']).first()
        context['questions_list'] = QuestionAnswer.objects.filter(test_id=kwargs['pk'])
        return context


def test_answer(request, pk):
    # current_user = request.user.id
    test = Test.objects.filter(id=pk).only('attempts').first()
    print('t', test.attempts)
    # answ = UserStatistic.objects.filter(user_stat_id=request.user.id, test_id=pk).only('answer_attempt_passed').first()
    qw_answ = QuestionAnswer.objects.filter(test_id=pk).only('answer_1_status', 'answer_2_status', 'answer_3_status', 'answer_4_status')
    attempt_passed = 0
    try:
        answ = UserStatistic.objects.filter(user_stat_id=request.user.id, test_id=pk).only(
            'answer_attempt_passed').first()
        attempt_passed = answ.answer_attempt_passed
        print('111', attempt_passed)
    except AttributeError:
        print('not exist')
    else:
        attempt_passed = 1
        print('222', attempt_passed)

    # if test.attempts > answ.answer_attempt_passed:
    #     print('go')
    # else:
    #     print('passed')

    # TODO Destroy this HORROR (((( !!!!!
    if request.method == 'POST':
        qqq = []
        for q_id in request.POST.getlist('question_id'):
            qwe = []
            for i in range(1, 5):
                s = '{}_answer_{}_status'.format(q_id, i)
                if request.POST.get(s) == 'on':
                    qwe.append(('{}'.format(q_id),'answer_{}_status'.format(i), True))
            qqq.append(qwe)
        result = []
        for x in qqq:
            answer = vars(qw_answ.filter(id=int(x[0][0])).first())

            if answer[x[0][1]] is x[0][2]:
                result.append('question id-{} passed'.format(int(x[0][0])))
        percent = (len(result)/qw_answ.count())*100
        UserStatistic.objects.create(test_id=pk, user_stat_id=request.user.id,
                                     answer_attempt_passed=attempt_passed,
                                     answer_percent=percent, correct_answer_number=len(result)).save()
    return redirect('/result_page/{}'.format(pk))


class ResultPage(TemplateView):
    template_name = 'result_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result'] = UserStatistic.objects.filter(test_id=kwargs['pk']).last()
        return context


class Filter(TemplateView):
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
                context['tests_list'] = search_result
                return context
        context['tests_list'] = tests_list
        return context


class CommentView(FormView):
    template_name = "comment_page.html"
    form_class = CommentForm

    def form_valid(self, form):
        user = self.request.user.id
        comment = form.cleaned_data['comment']
        Comment.objects.create(user_id=user, test_id=self.kwargs['pk'], comment=comment).save()
        return redirect('/test_page/{}'.format(self.kwargs['pk']))

    def form_invalid(self, form):
        return super().form_valid(form)