from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Question, Choice

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'surveys/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]



# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'surveys/index.html', context)

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Andai id jok bolgonduktan, Senin Suroon jok!")
#     return render(request, 'surveys/detail.html', {'question':question})

class DetailView(generic.DetailView):
    model = Question
    template_name= 'surveys/detail.html'

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'surveys/detail.html', {'question':question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'surveys/results.html'

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'surveys/results.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'surveys/detail.html', {'question': question, 'error_message':"You didn't select a choice."})
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('surveys:results', args=(question.id,)))
    return HttpResponse("You're voting on question %s." % question_id)
