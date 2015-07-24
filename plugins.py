# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.forms.models import modelform_factory
import copy
from xadmin.sites import site
from xadmin.util import get_model_from_relation, vendor
from xadmin.views import BaseAdminPlugin, CreateAdminView, ListAdminView, UpdateAdminView, DetailAdminView, CommAdminView, ModelAdminView, ModelFormAdminView
from xadmin.layout import Layout


class CreateAdminViewFormPlugin(BaseAdminPlugin):

    def init_request(self, *args, **kwargs):
        return hasattr(self.admin_view, 'form_add')

    def get_model_form(self, __, **kwargs):
        self.admin_view.form = self.admin_view.form_add
        return __(**kwargs)


class UpdateAdminViewFormPlugin(BaseAdminPlugin):

    def init_request(self, *args, **kwargs):
        return hasattr(self.admin_view, 'form_change')

    def get_model_form(self, __, **kwargs):
        self.admin_view.form = self.admin_view.form_change
        return __(**kwargs)


class UpdateAdminViewFormLayoutPlugin(BaseAdminPlugin):

    def init_request(self, *args, **kwargs):
        return hasattr(self.admin_view, 'form_layout_change')

    def get_form_layout(self, __):
        self.admin_view.form_layout = self.admin_view.form_layout_change
        return __()


class CreateAdminViewFormLayoutPlugin(BaseAdminPlugin):

    def init_request(self, *args, **kwargs):
        return hasattr(self.admin_view, 'form_layout_add')

    def get_form_layout(self, __):
        self.admin_view.form_layout = self.admin_view.form_layout_add
        return __()

class ListAdminViewFormListPlugin(BaseAdminPlugin):

    def init_request(self, *args, **kwargs):
        if hasattr(self.admin_view, 'form_list_query'):
            self.instance_forms()
            return True
        return False

    def instance_forms(self):
        self.admin_view.form_list_query_obj = self.admin_view.form_list_query(**self.get_form_datas())

    def get_form_datas(self):
        if self.request.method == 'GET':
            initial = dict(self.request.GET.items())
            return {'initial': initial}
        else:
            return {'data': self.request.POST, 'files': self.request.FILES}

    def get_media(self, media):
        media += self.admin_view.form_list_query.media
        media.add_js(['js/string-format.js', ])
        return media

    def get_context(self, context):
        context.update({
            'homeindex': self.admin_view.get_admin_url('index'),
            'form_list_query': self.admin_view.form_list_query_obj,
        })
        return context


class ListAdminViewQueryPlugin(BaseAdminPlugin):

    def init_request(self, *args, **kwargs):
        return hasattr(self.admin_view, 'get_list_queryset_method')

    def get_list_queryset(self, __):
        return self.admin_view.get_list_queryset_method()

class get_breadcrumb_method_Plugin(BaseAdminPlugin):

    def init_request(self, *args, **kwargs):
        return hasattr(self.admin_view, 'get_breadcrumb_method')

    def get_breadcrumb(self, __):
        bcs = self.admin_view.get_breadcrumb_method()
        return bcs if bcs else __()





