from django import forms

class NewTask(forms.Form):
    DATEPICKER = {
        'type': 'text',
        'class': 'form-control',
        'id': 'datetimepicker4',
        'placeholder': 'Enter date for task'
    }
    TIMEPICKER = {
        'type': 'text',
        'class': 'form-control',
        'id': 'datetimepicker3',
        'placeholder': 'Enter time for task'
    }
    TASK_STATUS = (
        ('P', 'Pending'),
        ('D', 'Done'),
        ('M', 'Missed'),
    )
    task = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Enter task description'
        }
    ))
    date = forms.DateField(widget=forms.DateInput(
        attrs=(DATEPICKER)
    ))
    time = forms.TimeField(widget=forms.TimeInput(
        attrs=(TIMEPICKER)
    ))
    status = forms.ChoiceField(
        choices=TASK_STATUS,
        widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ),
        help_text='Please choose task status'
    )