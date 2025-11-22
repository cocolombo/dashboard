from django.contrib import admin
from .models import Page, Widget, Link

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ('title', 'page', 'order')
    list_filter = ('page',)

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'widget', 'order')
    list_filter = ('widget__page', 'widget')
