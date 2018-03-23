# -*- coding: utf-8 -*-
from plone import api
from hpe.content import _
import qrcode
from plone.namedfile.field import NamedBlobImage
from plone import namedfile
import base64
from db.connect.browser.views import SqlObj
from zope.globalrequest import getRequest


def firstLogin(event):
    portal = api.portal.get()
    user = api.user.get_current().getProperty('email')
    abs_url = portal.absolute_url()
    url = 'http://696d405b.ngrok.io/hpe/event/event_handl?email=%s' %(user)
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make_image().save('user.png')
    img = open('user.png', 'rb')
    b64_img = base64.b64encode(img.read())
    execSql = SqlObj()
    execStr = """INSERT INTO user_picture(user, picture_data) 
            VALUES('{}', '{}')""".format(user, b64_img)

    execSql.execSql(execStr)

    img.close()
    api.portal.show_message(message=_(u'Dear colleagues, please provide basic information if this is the first time you log in. Thank you'), request=portal.REQUEST, type='info')


def userLogin(event):
    request = getRequest()
    language = request.get('language')
    abs_url = api.portal.get().absolute_url()
    if language == 'chinese':
        request.response.redirect(abs_url)
    elif language == 'english':
        request.response.redirect('%s/en_cover' %abs_url)


def userLogout(event):
    request = getRequest()
    abs_url = api.portal.get().absolute_url()

    request.response.redirect(abs_url)