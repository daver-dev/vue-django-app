from django.urls import path

from notes import views

urlpatterns = [
    path('', views.NotesListView.as_view(), name='notes_api'),
    path('<int:pk>/', views.NoteDetailView.as_view(), name='note_detail')
]
