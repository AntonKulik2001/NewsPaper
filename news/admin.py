from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('categoryType', 'title', 'dateCreation', 'rating')
    list_filter = ('categoryType', 'rating', 'dateCreation')



admin.site.register(Post, PostAdmin)
admin.site.register(Category)
