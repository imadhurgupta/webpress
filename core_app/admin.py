from django.contrib import admin
from .models import Website, Page, Plugin, Template

admin.site.register(Website)
admin.site.register(Page)
admin.site.register(Plugin)
admin.site.register(Template)
