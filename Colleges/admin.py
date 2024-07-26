from django.contrib import admin
from .models import College,CollegeInfo,CollegeMedia,University,FeeStructure
from .forms import CollegeInfoForm
# Register your models here.

class CollegeAdmin(admin.ModelAdmin):
    prepopulated_fields= {'college_slug': ('college_name',)}


class CollegeInfoAdmin(admin.ModelAdmin):
    list_filter = ['college', 'college_extra_info', 'colege_fee_info']
    search_fields = ['college__name', 'college_extra_info__name']

admin.site.register(CollegeInfo, CollegeInfoAdmin)

admin.site.register(College,CollegeAdmin)
admin.site.register(CollegeMedia)
admin.site.register(University)
admin.site.register(FeeStructure)