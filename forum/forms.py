from .models import Topic
from django import forms


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'
