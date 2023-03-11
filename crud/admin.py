from django.contrib import admin
from .models import Tasks

class TaskAdmin(admin.ModelAdmin):
    readonly_fields= ('created',)

admin.site.register(Tasks, TaskAdmin)