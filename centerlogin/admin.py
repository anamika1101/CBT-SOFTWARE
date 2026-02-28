from django.contrib import admin
from .models import CenterStudent, ExamAssignment


@admin.register(CenterStudent)
class CenterStudentAdmin(admin.ModelAdmin):
    list_display = ("roll_no", "name", "email", "phone", "course", "status", "center")
    search_fields = ("roll_no", "name", "email", "phone")
    list_filter = ("status", "center")


@admin.register(ExamAssignment)
class ExamAssignmentAdmin(admin.ModelAdmin):
    list_display = ("student", "test", "status", "score", "center", "assigned_at")
    search_fields = ("student__name", "student__roll_no", "test__test_name")
    list_filter = ("status", "center")
