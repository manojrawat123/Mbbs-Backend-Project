from django import forms
from .models import CollegeInfo

class CollegeInfoForm(forms.ModelForm):
    class Meta:
        model = CollegeInfo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.college_extra_info:
            self.fields.pop('college_extra_info')
        if self.instance and self.instance.colege_fee_info:
            self.fields.pop('colege_fee_info')
