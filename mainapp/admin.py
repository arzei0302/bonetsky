from django.contrib import admin
from .models import Test, Specialist, Question, SpecialistCategory, UserTestResult
from django.core.management import call_command
from django import forms
from django.contrib import admin
from django.contrib.admin import helpers
from django.shortcuts import render
from .models import Specialist, Test

class TestChoiceForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    test_choice = forms.ModelChoiceField(Test.objects.all(), label='Выберите тест')


def send_test_link(modeladmin, request, queryset):
    form = None
    if 'apply' in request.POST:
        form = TestChoiceForm(request.POST)
        if form.is_valid():
            test_id = form.cleaned_data['test_choice'].id
            specialist_ids = queryset.values_list('id', flat=True)
            call_command('send_test_link', test_id, *specialist_ids)
            modeladmin.message_user(request, "Ссылки на тест успешно отправлены.")
            return
        else:
            modeladmin.message_user(request, "Пожалуйста, выберите тест.")

    if not form:
        form = TestChoiceForm(initial={'_selected_action': request.POST.getlist('_selected_action')})
    
    return render(request, 'mainapp/send_test_link_form.html', {'items': queryset, 'form': form, 'title': 'Отправить ссылку на тест'})


class SpecialistAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'telegram_chat_id', 'category', 'timestamp',]
    list_display_links = ['name', 'phone', 'telegram_chat_id', 'category', 'timestamp',]
    search_fields = ['name', 'phone', 'telegram_chat_id',]
    actions = [send_test_link]
admin.site.register(Specialist, SpecialistAdmin)

@admin.register(UserTestResult)
class UserTestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'score', 'answers', 'timestamp', 'start_time']
    list_display_links = ['user', 'test', 'score', 'answers',]
    search_fields = ['user',]
   
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['name',]
    search_fields = ['name',]
    
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'test', 'answer_choices', 'correct_answer',]
    list_display_links = ['text', 'test', 'answer_choices', 'correct_answer',]
    search_fields = ['text', 'test', 'answer_choices', 'correct_answer', ]
    
@admin.register(SpecialistCategory)
class SpecialistCategoryAdmin(admin.ModelAdmin):
    list_display = ['category',]
    list_display_links = ['category',]
    

    
    

