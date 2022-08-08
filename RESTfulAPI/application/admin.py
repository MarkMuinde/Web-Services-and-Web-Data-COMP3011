from django.contrib import admin
from .models import Module, Professor, Rating

#Register tables
admin.site.register(Module) 
admin.site.register(Professor) 
admin.site.register(Rating)
