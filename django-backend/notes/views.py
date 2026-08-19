from django.shortcuts import render
from rest_framework import generics

from notes.models import Note
from notes.serializers import NoteSerializer

# Create your views here.

# View for looking at how django html templates work,
# not for use with vue
def note_list(request):
    notes = Note.objects.all()
    notes_dict = {"notes": notes}
    return render(request, 'notes/list.html', notes_dict)

class NotesListView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer