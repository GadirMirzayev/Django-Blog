from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from stories.models import (
    Story,
    Recipe,
    Category,
    Contact,
    Comment,
    CommentStory,
    Subscriber,
    Tag
)

# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'created_at')
    search_fields = ('full_name', 'email', 'subject', 'message')


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'category',)
    search_fields = ('title', 'description',)
    list_filter = ('category',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'category',)
    search_fields = ('title', 'description',)
    list_filter = ('category',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(CommentStory)
class CommentStoryAdmin(admin.ModelAdmin):
    list_display = ('text', 'email', 'website',)
    search_fields = ('text', 'email','message',)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    search_fields = ('email',)


class CategoryAdmin(TranslationAdmin):
    list_display = ('id','title',)
    search_fields = ('id','title',)


class TagAdmin(TranslationAdmin):
    list_display = ('id','title',)
    search_fields = ('id','title',)

admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)