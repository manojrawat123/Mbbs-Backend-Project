from django.contrib import admin
from .models import Account,User,UserTestInfo,UserTransactionTable,UserProfile

# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display= ['id']

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(UserTestInfo)
admin.site.register(UserTransactionTable)
