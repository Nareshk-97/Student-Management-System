from django.urls import path 
from .views import mentor_list, mentor_dashboard, mentor_create, mentor_delete, mentor_detail, mentor_update

urlpatterns = [
    path("mentor-list/", mentor_list, name="mentor_list"),
    path('mentor-dashboard/', mentor_dashboard, name='mentor_dashboard'),
    path('create/', mentor_create, name='mentor_create'),
    path('<int:pk>/', mentor_detail, name='mentor_detail'),
    path('<int:pk>/update/', mentor_update, name='mentor_update'),
    path('<int:pk>/delete/', mentor_delete, name='mentor_delete')
] 

