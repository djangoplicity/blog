# -*- coding: utf-8 -*-
#
# eso-blog
# Copyright (c) 2007-2017, European Southern Observatory (ESO)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#   * Neither the name of the European Southern Observatory nor the names
#     of its contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY ESO ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL ESO BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from djangoplicity.archives.contrib.admin.defaults import RenameAdmin, TranslationDuplicateAdmin, SyncTranslationAdmin, \
    ArchiveAdmin
from djangoplicity.contrib import admin as dpadmin

from djangoplicity.blog.models import Author, AuthorDescription, Category, Post, PostProxy, Tag
from djangoplicity.contrib.admin import CleanHTMLAdmin
from modeltranslation.admin import TranslationAdmin


class AuthorAdmin(RenameAdmin, dpadmin.DjangoplicityModelAdmin):
    raw_id_fields = ('photo', )
    richtext_fields = ('biography', )


class AuthorDescriptionInline(admin.TabularInline):
    model = AuthorDescription


class CategoryAdmin(TranslationAdmin):
    list_display = ('name', 'slug', 'view_online')
    fields = ('name', 'slug', 'footer')
    richtext_fields = ('footer', )
    prepopulated_fields = {"slug": ("name",)}

    def view_online(self, obj):
        return format_html('<a href="{}">View online</a>',
            reverse('blog_query_category', args=[obj.slug]))


def view_online_post(post):
    return format_html('<a href="{}">View online</a>', reverse('blog_detail', args=[post.slug]))


class PostAdmin(dpadmin.DjangoplicityModelAdmin, CleanHTMLAdmin, RenameAdmin):
    filter_horizontal = ('authors', 'tags')
    inlines = (AuthorDescriptionInline, )
    list_display = ('slug', 'title', 'category', 'release_date', 'published', view_online_post)
    list_filter = ('category', 'authors', 'tags')
    raw_id_fields = ('banner', )
    readonly_fields = ('last_modified', 'created')
    richtext_fields = ('body', 'discover_box', 'numbers_box', 'profile', 'links')
    search_fields = ('slug', 'title', 'subtitle', 'lede', 'body', 'links', 'discover_box', 'numbers_box')
    fieldsets = (
        (
           None,
           {'fields': ('slug', 'release_date', 'published', ('created', 'last_modified'))}
        ),
        (
            'Content',
            {'fields': ('banner', 'title', 'subtitle', 'lede', 'body',
            ('discover_box', 'numbers_box'), ('profile', 'links'))}
        ),
        (
            'Metadata',
            {'fields': ('category', 'tags')},
        )
    )


class PostProxyAdmin(RenameAdmin, dpadmin.DjangoplicityModelAdmin, TranslationDuplicateAdmin, SyncTranslationAdmin, ArchiveAdmin):
    list_display = PostAdmin.list_display
    fieldsets = (
        (
            'Language',
            {'fields': ('lang', 'source', 'translation_ready',)}
        ),
        (
           None,
           {'fields': ('slug',)}
        ),
        (
            'Publishing',
            {'fields': ('published', 'release_date', ('created', 'last_modified'))}
        ),
        (
            'Content',
            {'fields': ('title', 'subtitle', 'lede', 'body', ('discover_box', 'numbers_box'), ('profile', 'links'))}
        )
    )
    raw_id_fields = ('source',)
    richtext_fields = PostAdmin.richtext_fields
    readonly_fields = ['release_date', 'created', 'last_modified']

    def get_readonly_fields(self, request, obj=None):
        # When we are editing we disallow updating the slug to prevent duplication of the translation (The slug is the PK)
        if obj:
            return self.readonly_fields + ['slug']
        else:
            return super(PostProxyAdmin, self).get_readonly_fields(request, obj)


class TagAdmin(RenameAdmin, dpadmin.DjangoplicityModelAdmin):
    list_display = ('name', 'slug', 'view_online')

    def view_online(self, obj):
        return format_html('<a href="{}">View online</a>',
            reverse('blog_query_tag', args=[obj.slug]))


def register_with_admin(admin_site):
    admin_site.register(Author, AuthorAdmin)
    admin_site.register(Category, CategoryAdmin)
    admin_site.register(Post, PostAdmin)
    if settings.USE_I18N:
        admin_site.register(PostProxy, PostProxyAdmin)
    admin_site.register(Tag, TagAdmin)


register_with_admin(admin.site)
