from django import template
from django.utils.html import format_html
from djangoplicity.blog.models import Category

register = template.Library()


@register.inclusion_tag('blog/categories_list.html')
def list_blog_categories():
    return {
        "categories": Category.objects.all()
    }


@register.simple_tag
def blog_video(src, **kwargs):
    fullwidth = kwargs.get('fullwidth', 'False') == 'True'
    html_class = 'fullwidth' if fullwidth else ''

    if not src:
        return ''
    return format_html(
        '<video src="{}" class="{}" autoplay="autoplay" loop="loop" muted="muted" width="100%"></video>',
        src, html_class
    )


@register.simple_tag
def dyk(text):
    if not text:
        return ''
    return format_html('<div class="dyk"><span class="dyk__title">#DYK</span><p>{}</p></div>', text)
