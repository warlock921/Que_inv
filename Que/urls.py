#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-30 09:47:19
# @Author  : warlock921 (caoyu921@163.com)
# @Link    : http://example.org
# @Version : $Id$

from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.display_Que,name="display_Que"),
	url(r'(?P<que_id>\d)',views.display_Que_content,name="display_Que_content"),
]