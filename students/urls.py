from django.urls import path
from .views import student_list, student_dashboard, student_detail, student_create, student_delete, student_update

urlpatterns = [
    path("student-list/", student_list, name="student_list"),
    path('student-dashboard/', student_dashboard, name = 'student_dashboard'),
    path('create/', student_create, name='student_create'),
    path('<int:pk>/', student_detail, name='student_detail'),
    path('<int:pk>/update/', student_update, name='student_update'),
    path('<int:pk>/delete/', student_delete, name='student_delete')
]
