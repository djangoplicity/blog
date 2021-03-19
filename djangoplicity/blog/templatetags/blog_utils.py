from django import template
from django.utils.html import format_html
from djangoplicity.blog.models import Category
from random import randint

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
        '<div class="blog-video-wrapper {html_class}">'
            '<video id="{id}" src="{src}" loop="loop" muted="muted" preload="auto" width="100%"></video>'
            '<div class="blog-video-mute-control" onclick="toggleVideoMute({id})"><i class="fa fa-volume-off"></i></div>'
        '</div>',
        src=src,
        html_class=html_class,
        id=randint(0, 100000)
    )


@register.simple_tag
def dyk(text):
    if not text:
        return ''
    return format_html('<div class="dyk"><span class="dyk__title">#DYK</span><p>{}</p></div>', text)
