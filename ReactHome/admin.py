from django.contrib import admin
from .models import Feeds, Comments

# Register your models here.

class FeedsAdmin(admin.ModelAdmin):
    list_filter = ['author']
    list_display = ['author__username', 'slug']
    search_fields = ['author__username', 'slug']
    readonly_fields = ['author',]

    class Meta:
        model = Feeds

admin.site.register(Feeds, FeedsAdmin)

class CommentsAdmin(admin.ModelAdmin):
    list_filter = ['author', 'post']
    list_display = ['author', 'post']
    search_fields = ['author__username', 'post']
    readonly_fields = ['id']

    class Meta:
        model = Comments
admin.site.register(Comments, CommentsAdmin)