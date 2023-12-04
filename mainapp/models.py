from django.db import models
from django.utils import timezone
from django.urls import reverse


class Test(models.Model):
    name = models.CharField(max_length=50, verbose_name='ТЕСТ')
    
    class Meta:
        verbose_name = " ТЕСТ"
        verbose_name_plural = "ТЕСТЫ"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('start_test', args=[str(self.id)])
    
    
class SpecialistCategory(models.Model):
    category = models.CharField(max_length=50, verbose_name='ОТДЕЛЫ:') 
    
    class Meta:
        verbose_name = "КАТЕГОРИЯ СПЕЦИАЛИСТА"
        verbose_name_plural = "КАТЕГОРИИ СПЕЦИАЛИСТОВ"

    def __str__(self):
        return self.category
    

class Specialist(models.Model):
    name = models.CharField(max_length=50, verbose_name='ФИО')
    phone = models.CharField(max_length=20, verbose_name='НОМЕР ТЕЛЕФОНА')
    telegram_chat_id = models.BigIntegerField(verbose_name='ID ТЕЛЕГРАММ', unique=True)
    category = models.ForeignKey(SpecialistCategory, on_delete=models.CASCADE, verbose_name='ОТДЕЛ')
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='ДАТА РЕГИСТРАЦИИ')
    
    class Meta:
        verbose_name = "СПЕЦИАЛИСТ"
        verbose_name_plural = "СПЕЦИАЛИСТЫ"

    def __str__(self):
        return self.name
    

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='ТЕСТЫ')
    text = models.TextField(verbose_name='ВОПРОСЫ')
    answer_choices = models.JSONField(verbose_name='ВАРИАНТЫ ОТВЕТОВ', help_text='Сохранить варианты ответов как JSON, ["Ответ 1", "Ответ 2", "Ответ 3"]')
    correct_answer = models.CharField(max_length=255, help_text="ТЕКСТ ПРАВИЛЬНОГО ОТВЕТА", verbose_name='ПРАВИЛЬНЫЕ ОТВЕТЫ')
    
    class Meta:
        verbose_name = "ВОПРОС"
        verbose_name_plural = "ВОПРОСЫ"

    def __str__(self):
        return self.text


class UserTestResult(models.Model):
    user = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(verbose_name='БАЛЛЫ')
    answers = models.JSONField(default=dict, verbose_name='ОТВЕТЫ ПОЛЬЗОВАТЕЛЯ')
    start_time = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "РЕЗУЛЬТАТ"
        verbose_name_plural = "РЕЗУЛЬТАТЫ"

    def __str__(self):
        return f"{self.user.name} - {self.score} БАЛЛОВ"
