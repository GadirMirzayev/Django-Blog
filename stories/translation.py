from modeltranslation.translator import translator, TranslationOptions
from stories.models import Category,Tag

class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

translator.register(Category, CategoryTranslationOptions)


class TagTranslationOptions(TranslationOptions):
    fields = ('title',)

translator.register(Tag, TagTranslationOptions)

