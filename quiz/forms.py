from django import forms

from quiz import models


class SelectedAnswersForm(forms.ModelForm):
    class Meta:
        model = models.SelectedAnswer
        fields = ['question', 'answer']
        widgets = {'answer': forms.RadioSelect()}

    def __init__(self, *args, **kwargs):
        super(SelectedAnswersForm, self).__init__(*args, **kwargs)
        self.fields['answer'].queryset = models.Answer.objects.filter(
            question=self.initial.get('question')
        )
        self.fields['question'].disabled = True
