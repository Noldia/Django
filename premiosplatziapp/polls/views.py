from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Question

def index(request):
    latst_question_list = Question.objects.all()
    return render(request, "polls/index.html", {
        "latest_question_list": latst_question_list
    })


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {
        "question": question
    })


def results(request, question_id):
    return HttpResponse(f"Result's question number {question_id}")


def vote(request, question_id):
    return HttpResponse(f"Voting question number {question_id}")