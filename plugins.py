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
from xadmin.views.base import inclusion_tag


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


class TitlePlugin(BaseAdminPlugin):

    def init_request(self, *args, **kwargs):
        return hasattr(self.admin_view, 'breadcrumb_dict')

    def get_breadcrumb(self, __):
        if isinstance(self.admin_view, (CreateAdminView, UpdateAdminView)) and 'title_list' in self.admin_view.breadcrumb_dict and 'title_form' in self.admin_view.breadcrumb_dict:
            return [
                {'title': '首页', 'url': self.admin_view.get_admin_url('index')},
                {'title': self.admin_view.breadcrumb_dict['title_list'], 'url': self.admin_view.model_admin_url('changelist')},
                {'title': self.admin_view.breadcrumb_dict['title_form']}
            ]
        if isinstance(self.admin_view, ListAdminView) and 'title_list' in self.admin_view.breadcrumb_dict:
            return [
                {'title': u'首页', 'url': self.admin_view.get_admin_url('index')},
                {'title': self.admin_view.breadcrumb_dict['title_list']},
            ]
        return __()

    def get_context(self, context):
        if isinstance(self.admin_view, CreateAdminView) and 'title_form' in self.admin_view.breadcrumb_dict:
            context.update({'title': u'增加 %s' % self.admin_view.breadcrumb_dict['title_form']})
        if isinstance(self.admin_view, UpdateAdminView) and 'title_form' in self.admin_view.breadcrumb_dict:
            context.update({'title': u'修改 %s' % self.admin_view.breadcrumb_dict['title_form']})
        if isinstance(self.admin_view, ListAdminView) and 'title_list' in self.admin_view.breadcrumb_dict:
            context.update({'title': self.admin_view.breadcrumb_dict['title_list']})
        return context


class CustomPaginationPlugin(BaseAdminPlugin):

    def init_request(self, *args, **kwargs):
        return hasattr(self.admin_view, 'pagination_name')
        
    @inclusion_tag('manage_pagination.html')
    def block_custom_pagination(self, context, nodes, page_type='normal'):
        """
        Generates the series of links to the pages in a paginated list.
        """
        ALL_VAR = 'all'
        DOT = '.'
        paginator, page_num = self.admin_view.paginator, self.admin_view.page_num

        pagination_required = (
            not self.admin_view.show_all or not self.admin_view.can_show_all) and self.admin_view.multi_page
        if not pagination_required:
            page_range = []
        else:
            ON_EACH_SIDE = {'normal': 5, 'small': 3}.get(page_type, 3)
            ON_ENDS = 2

            # If there are 10 or fewer pages, display links to every page.
            # Otherwise, do some fancy
            if paginator.num_pages <= 10:
                page_range = range(paginator.num_pages)
            else:
                # Insert "smart" pagination links, so that there are always ON_ENDS
                # links at either end of the list of pages, and there are always
                # ON_EACH_SIDE links at either end of the "current page" link.
                page_range = []
                if page_num > (ON_EACH_SIDE + ON_ENDS):
                    page_range.extend(range(0, ON_EACH_SIDE - 1))
                    page_range.append(DOT)
                    page_range.extend(
                        range(page_num - ON_EACH_SIDE, page_num + 1))
                else:
                    page_range.extend(range(0, page_num + 1))
                if page_num < (paginator.num_pages - ON_EACH_SIDE - ON_ENDS - 1):
                    page_range.extend(
                        range(page_num + 1, page_num + ON_EACH_SIDE + 1))
                    page_range.append(DOT)
                    page_range.extend(range(
                        paginator.num_pages - ON_ENDS, paginator.num_pages))
                else:
                    page_range.extend(range(page_num + 1, paginator.num_pages))

        need_show_all_link = self.admin_view.can_show_all and not self.admin_view.show_all and self.admin_view.multi_page
        return {
            'cl': self.admin_view,
            'pagination_required': pagination_required,
            'show_all_url': need_show_all_link and self.admin_view.get_query_string({ALL_VAR: ''}),
            'page_range': map(self.admin_view.get_page_number, page_range),
            'ALL_VAR': ALL_VAR,
            '1': 1,
            # 'pre_page': '?p=%s' % (self.admin_view.page_num-1),
            # 'next_pare': '?p=%s' % (self.admin_view.page_num+1),
            'page_name': self.admin_view.pagination if hasattr(self.admin_view, 'pagination') else u'记录',
        }


class FormSetPlugin(BaseAdminPlugin):

    def init_request(self, *args, **kwargs):
        return hasattr(self.admin_view, 'form_set_dict')

    def get_context(self, context):
        if isinstance(self.admin_view, CreateAdminView):
            for key in self.admin_view.form_set_dict:
                if key.startswith('form_set_add'):
                    context.update({key: self.admin_view.form_set_dict[key]})
        if isinstance(self.admin_view, UpdateAdminView):
            for key in self.admin_view.form_set_dict:
                if key.startswith('form_set_change'):
                    helper = 'helper_%s' % key
                    context.update({key: self.admin_view.form_set_dict[key], helper: self.admin_view.form_set_dict[helper]})
                    'pass'
        # if isinstance(self.admin_view, ListAdminView):
        #     for key in self.admin_view.form_set_dict:
        #         if key.startswith('form_set_list'):
        #             context.update({key: self.admin_view.form_set_dict[key]})
        return context

