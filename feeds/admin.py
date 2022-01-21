from django.contrib import admin
from .models import Feeds, Comments

# Register your models here.

class FeedsAdmin(admin.ModelAdmin):
    list_filter = ['author']
    list_display = ['author', 'slug', 'posted_on']
    search_fields = ['author', 'slug', 'body']
    
    class Meta:
        model = Feeds

admin.site.register(Feeds, FeedsAdmin)

class CommentsAdmin(admin.ModelAdmin):
    list_filter = ['author', 'post']
    list_display = ['author', 'post', 'comment']
    search_fields = ['author__username', 'post', 'comment']

    class Meta:
        model = Comments
admin.site.register(Comments, CommentsAdmin)

