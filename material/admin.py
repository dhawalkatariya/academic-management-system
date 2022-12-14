from django.contrib import admin
from .models import Material
# Register your models here.


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('short_message', 'classroom', 'arrived')
    list_filter = ('arrived',)
    date_hierarchy = 'arrived'
    raw_id_fields = ('classroom',)

    def short_message(self, obj):
        if(len(obj.message) <= 100):
            return obj.message
        return obj.message[:100] + '...'
