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
from django.contrib.sites.models import Site
from rest_framework import serializers

from djangoplicity.archives.utils import get_instance_archives_urls

from djangoplicity.blog.models import AuthorDescription, Category, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )


class AuthorDescriptionSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='author.name')
    photo = serializers.SerializerMethodField(read_only=True)
    static_photo = serializers.ReadOnlyField(source='author.static_photo')

    def get_photo(self, obj):
        if obj.author and obj.author.photo:
            return get_instance_archives_urls(obj.author.photo)

    class Meta:
        model = AuthorDescription
        fields = ('name', 'description', 'photo', 'static_photo')


class PostSerializer(serializers.ModelSerializer):
    authors = AuthorDescriptionSerializer(source='authordescription_set', many=True)
    banner = serializers.SerializerMethodField(read_only=True)
    category = CategorySerializer(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)

    def get_banner(self, obj):
        return get_instance_archives_urls(obj.banner)

    def get_url(self, obj):
        url = obj.get_absolute_url()
        return 'https://{}{}'.format(Site.objects.get_current().domain, url)

    class Meta:
        model = Post
        fields = ('slug', 'url', 'title', 'subtitle', 'banner', 'authors', 'category', 'lede', 'release_date')
