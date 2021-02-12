from django import template
from djangoplicity.blog.models import Category

register = template.Library()


@register.inclusion_tag('blog/categories_list.html')
def list_blog_categories():
    return {
        "categories": Category.objects.all()
    }
