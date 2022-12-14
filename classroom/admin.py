from django.contrib import admin
from .models import Class

# Register your models here.
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'invitation_code', 'created_by', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name',)
    raw_id_fields = ('created_by', 'students')
    list_per_page = 20
    date_hierarchy = "created_on"
