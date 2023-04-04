from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(Project)
# admin.site.register(Subtask)
admin.site.register(Stats)
admin.site.register(Mode)