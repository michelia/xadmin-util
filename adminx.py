# -*- coding: utf-8 -*-
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, CreateAdminView, ListAdminView, UpdateAdminView, DetailAdminView, CommAdminView, ModelAdminView, ModelFormAdminView

from .plugins import CreateAdminViewFormPlugin, UpdateAdminViewFormPlugin, CreateAdminViewFormLayoutPlugin, UpdateAdminViewFormLayoutPlugin, ListAdminViewQueryFormPlugin, ListAdminViewQueryPlugin, TitlePlugin, CustomPaginationPlugin, FormSetPlugin

site.register_plugin(CreateAdminViewFormPlugin, CreateAdminView)
site.register_plugin(CreateAdminViewFormLayoutPlugin, CreateAdminView)

site.register_plugin(UpdateAdminViewFormPlugin, UpdateAdminView)
site.register_plugin(UpdateAdminViewFormLayoutPlugin, UpdateAdminView)

site.register_plugin(ListAdminViewQueryFormPlugin, ListAdminView)
site.register_plugin(ListAdminViewQueryPlugin, ListAdminView)
site.register_plugin(CustomPaginationPlugin, ListAdminView)


# for create update AdminView
site.register_plugin(FormSetPlugin, ModelFormAdminView)

# for list create update AdminView
site.register_plugin(TitlePlugin, ModelAdminView)













