from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, CreateAdminView, ListAdminView, UpdateAdminView, DetailAdminView, CommAdminView, ModelAdminView, ModelFormAdminView

from .plugins import CreateAdminViewFormPlugin, UpdateAdminViewFormPlugin, CreateAdminViewFormLayoutPlugin, UpdateAdminViewFormLayoutPlugin, ListAdminViewFormListPlugin, ListAdminViewQueryPlugin, get_breadcrumb_method_Plugin

site.register_plugin(CreateAdminViewFormPlugin, CreateAdminView)
site.register_plugin(CreateAdminViewFormLayoutPlugin, CreateAdminView)

site.register_plugin(UpdateAdminViewFormPlugin, UpdateAdminView)
site.register_plugin(UpdateAdminViewFormLayoutPlugin, UpdateAdminView)

site.register_plugin(ListAdminViewFormListPlugin, ListAdminView)
site.register_plugin(ListAdminViewQueryPlugin, ListAdminView)

site.register_plugin(get_breadcrumb_method_Plugin, ModelFormAdminView)











