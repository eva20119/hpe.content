# -*- coding: utf-8 -*- 
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
from plone.namedfile.field import NamedBlobImage
from plone import namedfile
from Products.CMFPlone.utils import safe_unicode
import base64
from db.connect.browser.views import SqlObj
import datetime

class EnCover(BrowserView):
    template = ViewPageTemplateFile('tmeplate/en_cover.pt')
    def __call__(self):
        return self.template()