# -*- coding: utf-8 -*-
from django import forms

from django.conf import settings
from django.forms.util import flatatt, to_current_timezone
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils import datetime_safe, formats
from django.utils.html import escape, conditional_escape
from django.utils.translation import ugettext, ugettext_lazy
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.safestring import mark_safe
from django.forms import Media

from xadmin.util import vendor

from ELITEUADMIN.settings import Constant

FILE_INPUT_CONTRADICTION = object()

class ImagePreviewInput(forms.FileInput):
    @property
    def media(self):
        '上传前 预览图片'
        media = Media()
        media.add_js(['js/previrew-image-before-upload.js'])
        # media.add_css({'screen': files})
        return media

    def render(self, name, value, attrs=None):
        template = u'''
                <a href="%(img_uri)s" target="view_window">
                <img src="%(img_uri)s"  width="200" height="200"></img>
                </a>
                <div class="preview" hidden="hidden"></div>
                %(input)s
            '''
        self.attrs['onchange'] = 'previewImg(this)'
        substitutions = {
            'img_uri': value.url if hasattr(value, 'url') else 'https://coding.net/static/fruit_avatar/Fruit-3.png',
            'input': super(ImagePreviewInput, self).render(name, value, attrs),
        }
        return mark_safe(template % substitutions)

class ImageInput(forms.FileInput):
    initial_text = ugettext_lazy('Currently')
    input_text = ugettext_lazy('Change')
    clear_checkbox_label = ugettext_lazy('Clear')

    template_with_initial = u'%(initial_text)s: %(initial)s %(clear_template)s<br />%(input_text)s: %(input)s'
    # template_with_initial = u'%(initial_text)s: %(initial)s %(clear_template)s<br /><div>%(input_text)s: %(input)s</div>'

    template_with_clear = u'%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

    def clear_checkbox_name(self, name):
        """
        Given the name of the file input, return the name of the clear checkbox
        input.
        """
        return name + '-clear'

    def clear_checkbox_id(self, name):
        """
        Given the name of the clear checkbox input, return the HTML id for it.
        """
        return name + '_id'

    def render(self, name, value, attrs=None):
        '加上id和内联显示'
        attrs = {'style': "display:inline", 'id': 'id_'+name}
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'''
            <a href="%(img_uri)s" target="view_window">
                <img src="%(img_uri)s"  width="200" height="200"></img>
            </a>
            <div class="preview" hidden="hidden"></div>
            %(input)s
            '''

        substitutions['input'] = super(ImageInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            # substitutions['initial'] = (u'<a href="%s">%s</a>' % (escape(value.url), escape(force_unicode(value))))
            substitutions['initial'] = (u'<img src="%s"  width="150" height="150"></img>' % (escape(value.url)))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = forms.CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)

    def value_from_datadict(self, data, files, name):
        upload = super(ImageInput, self).value_from_datadict(data, files, name)
        if not self.is_required and forms.CheckboxInput().value_from_datadict(
            data, files, self.clear_checkbox_name(name)):
            if upload:
                # If the user contradicts themselves (uploads a new file AND
                # checks the "clear" checkbox), we return a unique marker
                # object that FileField will turn into a ValidationError.
                return FILE_INPUT_CONTRADICTION
            # False signals to clear any existing value, as opposed to just None
            return False
        return upload

class CertificateImageInput(forms.FileInput):
    @property
    def media(self):
        '上传前 预览图片'
        media = Media()
        media.add_js(['js/previrew-image-before-upload.js'])
        # media.add_css({'screen': files})
        return media

    def render(self, name, value, attrs=None):
        # 下面这种方式可以去掉后面再增加类, 就是禁止 crispy添加的类
        attrs.update({'class': ''})
        # 添加执行图片预览的函数调用
        self.attrs['onchange'] = 'previewImg(this)'
        auth_value = int(self.attrs.pop('auth_value', Constant.TeacherCertificateNotPass))
        if auth_value == Constant.TeacherCertificatePass:
            template = u'''
                <a href="%(img_uri)s" target="view_window">
                <img src="%(img_uri)s"  width="200" height="200"></img>
                </a>
                <div class="preview" hidden="hidden"></div>
                %(input)s
                <button name="certificate_pass" data-certificate="%(certificate_name)s" class="btn btn-default" disabled="disabled" >通过审核</button>
                <button name="certificate_not" data-certificate="%(certificate_name)s" class="btn btn-default">未通过审核</button>
            '''
        else:
            template = u'''
                <a href="%(img_uri)s" target="view_window">
                <img src="%(img_uri)s"  width="200" height="200"></img>
                </a>
                <div class="preview" hidden="hidden"></div>
                %(input)s
                <button name="certificate_pass" data-certificate="%(certificate_name)s" class="btn btn-default">通过审核</button>
                <button name="certificate_not" data-certificate="%(certificate_name)s" class="btn btn-default" disabled="disabled" >未通过审核</button>
            '''
        # if attrs.get('')
        substitutions = {
            # 'img_uri': 'https://coding.net/static/fruit_avatar/Fruit-3.png',
            # 'img_uri': value if value else 'https://coding.net/static/fruit_avatar/Fruit-3.png',
            'img_uri': 'https://coding.net/static/fruit_avatar/Fruit-3.png',
            # 下面的位置不能颠倒，因为要把 certificate_name 弹出来使用， 所以不能颠倒
            'certificate_name': self.attrs.pop('certificate_name', ''),
            'input': super(CertificateImageInput, self).render(name, value, attrs),
        }
        if value and hasattr(value, "url"):
            substitutions['img_uri'] = value.url
        return mark_safe(template % substitutions)

class NoLabelImageInput(forms.FileInput):
    @property
    def media(self):
        '上传前 预览图片'
        media = Media()
        media.add_js(['js/previrew-image-before-upload.js'])
        # media.add_css({'screen': files})
        return media

    def render(self, name, value, attrs=None):
        attrs.update({'class': ''})
        # 添加执行图片预览的函数调用
        self.attrs['onchange'] = 'previewImg(this)'
        template = u'''
            <a href="%(img_uri)s" target="view_window">
            <img src="%(img_uri)s"  width="230" height="230"></img>
            </a>
            <div class="preview" hidden="hidden"></div>
            %(input)s
        '''
        substitutions = {
            # 'img_uri': 'https://coding.net/static/fruit_avatar/Fruit-3.png',
            'img_uri': value.url if value else 'https://coding.net/static/fruit_avatar/Fruit-3.png',
            'input': super(NoLabelImageInput, self).render(name, value, attrs),
        }
        return mark_safe(template % substitutions)

