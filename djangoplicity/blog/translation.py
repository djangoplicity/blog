from modeltranslation.translator import register, TranslationOptions
from .models import Category, Author


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'slug', 'footer',)
    # The slug is required because it's used in the URL
    required_languages = {'default': ('slug',)}


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('biography',)
