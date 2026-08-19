from django.urls import path

from notes import views

urlpatterns = [
    path('', views.note_list, name='note_list'),
]
