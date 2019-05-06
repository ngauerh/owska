from django.forms import widgets

from .models import Topic, Board
from django import forms


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('title', 'content', 'board')


class BoardList(forms.Form):
    board = forms.IntegerField(
        widget=forms.Select()
    )

    def __init__(self, *args, **kwargs):
        super(BoardList, self).__init__(*args, **kwargs)
        self.fields['board'].widget.choices = Board.objects.all().values_list('id', 'name')





