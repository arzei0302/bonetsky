from rest_framework import viewsets
from .models import Test, Question, SpecialistCategory, Specialist, UserTestResult
from .serializers import (TestSerializer, QuestionSerializer, SpecialistCategorySerializer, SpecialistSerializer, UserTestResultSerializer)
from django.shortcuts import render, redirect
from django.http import Http404
from django.utils import timezone




def index(request):
    return render(request, 'mainapp/index.html')


def list_test(request):
    тесты = Test.objects.all()
    return render(request, 'mainapp/list_test.html', {'тесты': тесты})


def start_test(request, test_id):
    тест = Test.objects.get(pk=test_id)
    вопросы = Question.objects.filter(test=тест)
    return render(request, 'mainapp/start_test.html', {'тест': тест, 'вопросы': вопросы})


def send_test(request, test_id):
    if request.method == 'POST':
        тест = Test.objects.get(pk=test_id)
        вопросы = Question.objects.filter(test=тест)
        пользователь = Specialist.objects.get(id=request.user.id)
        баллы = 0
        ответы = {}
        for вопрос in вопросы:
            ответ = request.POST.get(f'вопрос_{вопрос.id}', '')
            if ответ == вопрос.correct_answer:
                баллы += 1
            ответы[вопрос.id] = ответ
        результат = UserTestResult(user=пользователь, test=тест, score=баллы, answers=ответы, start_time=timezone.now())
        результат.save()
        return redirect('result_test', result_id=результат.id) 
    return redirect('mainapp/list_test')


def result_test(request, result_id):
    try:
        результат = UserTestResult.objects.get(pk=result_id)
    except UserTestResult.DoesNotExist:
        raise Http404("Результат теста не найден")
    return render(request, 'mainapp/result_test.html', {'результат': результат})


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class SpecialistCategoryViewSet(viewsets.ModelViewSet):
    queryset = SpecialistCategory.objects.all()
    serializer_class = SpecialistCategorySerializer

class SpecialistViewSet(viewsets.ModelViewSet):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer

class UserTestResultViewSet(viewsets.ModelViewSet):
    queryset = UserTestResult.objects.all()
    serializer_class = UserTestResultSerializer
