# -*- coding: utf-8 -*-
#
# eso-blog
# Copyright (c) 2007-2017, European Southern Observatory (ESO)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the European Southern Observatory nor the names
#      of its contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
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

from django.utils.translation import ugettext_noop as _

from djangoplicity.archives.contrib.browsers import ListBrowser
from djangoplicity.archives.contrib.queries.defaults import AllPublicQuery, \
    EmbargoQuery
from djangoplicity.archives.options import ArchiveOptions

from djangoplicity.blog.queries import PostTagQuery
from djangoplicity.blog.models import Tag
from djangoplicity.blog.views import PostDetailView


class PostOptions(ArchiveOptions):
    slug_field = 'slug'
    urlname_prefix = 'blog'
    template_name = 'archives/post/detail.html'
    detail_view = PostDetailView
    select_related = ('banner', )
    prefetch_related = ('tags', 'authordescription_set__author')

    class Queries(object):
        default = AllPublicQuery(browsers=('normal', ), verbose_name=_('Blog Posts'), feed_name='default', select_related=['category'])
        staging = EmbargoQuery(browsers=('normal', ), verbose_name=_('Blog Posts (Staging)'))
        tag = PostTagQuery(browsers=('normal', ), relation_field='tags', url_field='slug', title_field='name', use_category_title=True, verbose_name='%s')
        category = PostTagQuery(browsers=('normal', ), relation_field='category', url_field='slug', title_field='name', use_category_title=True, verbose_name='%s')

    class Browsers(object):
        normal = ListBrowser()

    @staticmethod
    def extra_context( obj, lang=None ):
        return {
            'tags': Tag.objects.order_by('name')
        }

    @staticmethod
    def feeds():
        from djangoplicity.blog.feeds import PostFeed
        return {
            '': PostFeed,
        }
