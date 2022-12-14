from django.contrib import admin
from .models import Assignment, Question, GradedAssignment


# Register your models here.

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'classroom', 'created_on')
    date_hierarchy = 'created_on'
    list_per_page = 20
    raw_id_fields = ('classroom',)
    list_filter = ('created_on',)


@admin.register(GradedAssignment)
class GradedAssignmentAdmin(admin.ModelAdmin):
    list_display = ('marks_obtained', 'assignment', 'user', 'submitted')
    list_per_page = 20
    list_filter = ('submitted',)
    raw_id_fields = ('assignment', 'user')

    def marks_obtained(self, obj):
        return f"{obj.marks} out of {obj.total_marks}"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'assignment')
    list_per_page = 20
    raw_id_fields = ('assignment',)
