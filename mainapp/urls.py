from django.urls import path, include
from mainapp.views import index, list_test, start_test, send_test, result_test
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register(r'tests', views.TestViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'specialist-categories', views.SpecialistCategoryViewSet)
router.register(r'specialists', views.SpecialistViewSet)
router.register(r'user-test-results', views.UserTestResultViewSet)


urlpatterns = [
    path('api/', include(router.urls)), 
    path('', index, name='home'),  # http://127.0.0.1:8000/   
    
    
    path('list_test/', list_test, name='list_test'),
    path('start_test/<int:test_id>/', start_test, name='start_test'),
    path('send_test/<int:test_id>/', send_test, name='send_test'),
    path('result_test/<int:result_id>/', result_test, name='result_test'),
    
]