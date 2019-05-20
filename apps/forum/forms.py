from .models import Topic, Board, Comments
from django import forms


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('title', 'content', 'board')


class BoardList(forms.Form):
    board = forms.IntegerField(
        widget=forms.Select(
            attrs={'name': 'skills', 'class': 'ui fluid search dropdown'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(BoardList, self).__init__(*args, **kwargs)
        self.fields['board'].widget.choices = Board.objects.all().values_list('id', 'name')


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('content', 'topic')






