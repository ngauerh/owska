from .models import Topic,Board
from django import forms


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('title', 'content', 'board')


class SelectTestForm(forms.Form):
    city = forms.IntegerField(
        widget=forms.Select(
            choices=(
                (1, "BeiJing"),
                (2, "WeiHai"),
                (3, "RuShan"),
            ),
            attrs={
                "class": "form-control",
            }
        ),
        required=True
    )


class BoardList(forms.Form):
    b = forms.IntegerField(
        widget=forms.Select()
    )
    def __init__(self, *args, **kwargs):  # 执行父类的构造方法
        super(SelectTestForm, self).__init__(*args, **kwargs)
        self.fields['admin'].widget.choices = Board.objects.all().values_list('id', 'name')