from django.contrib import admin
from .models import Discussion, Response

# Register your models here.


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('problem', 'created_by',
                    'classroom', 'submitted_on', 'solved')
    date_hierarchy = "submitted_on"
    list_filter = ('submitted_on',)
    list_per_page = 20
    search_fields = ('question',)
    raw_id_fields = ('classroom', 'created_by')

    def problem(self, obj):
        if(len(obj.question) <= 100):
            return obj.question
        return obj.question[:100] + '...'


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('short_res', 'by', 'submitted_on')
    list_filter = ('submitted_on',)
    search_fields = ('answer',)
    raw_id_fields = ('discussion', 'by')
    list_per_page = 20

    def short_res(self, obj):
        if(len(obj.answer) <= 100):
            return obj.answer
        return obj.answer[:100] + '...'
