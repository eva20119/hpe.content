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

class BicyclePictureView(BrowserView):
    template = ViewPageTemplateFile("template/BicyclePictureView.pt")
    def __call__(self):
        event_brain = api.content.find(portal_type="EventList")
        place_brain = api.content.find(portal_type="PlaceList")
        eventList = []
        placeList = []
        
        for brain in event_brain:
            eventList.append(brain.Title)

        for brain in place_brain:
            placeList.append(brain.Title)

        self.eventList = eventList
        self.placeList = placeList

        return self.template()


class UploadBicyclePicture(BrowserView):
    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()
        alsoProvides(request, IDisableCSRFProtection)

        b64_image = request.get('b64_image').split(',')[1]
        image_title = request.get('image')
        event = request.get('event')
        place = request.get('place')
        news = api.content.create(
            type='BicyclePicture',
            container=portal,
            title='news1',
            event=event,
            place=place,
            image=namedfile.NamedBlobImage(data=base64.b64decode(b64_image), filename=safe_unicode(image_title))
        )


class Reservation(BrowserView):
    template = ViewPageTemplateFile("template/reservation.pt")
    def __call__(self):
        brains = api.content.find(portal_type='Reservation')
        reservationList = []
        user = api.user.get_current().getUserName()
        user_reservation_date = api.user.get(user).getProperty('reservation_date')
        self.aleard_reservation = False

        if not user_reservation_date:
            for item in brains:
                obj = item.getObject()
                title = obj.title
                startDate = obj.date.strftime('%Y/%m/%d')
                startTime = obj.date.strftime('%H:%M')

                timeList = []
                timeList.append([startTime])  
                for i in range(1, 6):
                    minutes = i*20
                    time = obj.date + datetime.timedelta(minutes = minutes)               
                    timeList.append([time.strftime('%H:%M')])
                peroid1 = obj.peroid1
                peroid2 = obj.peroid2
                peroid3 = obj.peroid3
                peroid4 = obj.peroid4
                peroid5 = obj.peroid5
                peroid6 = obj.peroid6
                alternate = obj.alternate
                ####若前6個時間都預約滿才開放候補####
                if peroid1 and peroid2 and peroid3 and peroid4 and peroid5 and peroid6:
                    alternate = 'enable'
                    alternateMsg = '開放候補'
                # elif alternate:
                #     alternate = 'disabled'
                #     alternateMsg = '候補以滿'
                else:
                    alternate = 'not_open'
                ###用來判斷有沒有預定 ###
                tmp_peroid = {
                    'peroid1': peroid1,
                    'peroid2': peroid2,
                    'peroid3': peroid3,
                    'peroid4': peroid4,
                    'peroid5': peroid5,
                    'peroid6': peroid6
                }

                for k,v in tmp_peroid.items():
                    index = int(k.split('peroid')[1])
                    peroid = 'peroid%s' %index
                    index = index - 1
                    if not v:
                        timeList[index].append('enable %s' %peroid)
                    else:
                        timeList[index].append('disabled %s' %peroid)                              
                
                #######################
                reservationList.append({
                    'title': title,
                    'timeList': timeList,
                    'startDate': startDate,
                    'peroid1': peroid1,
                    'peroid2': peroid2,
                    'peroid3': peroid3,
                    'peroid4': peroid4,
                    'peroid5': peroid5,
                    'peroid6': peroid6,
                    'alternate': alternate,
                    'alternateMsg': alternateMsg
                })
        else:
            self.user_reservation_msg = '您以預約%s' %user_reservation_date
            self.aleard_reservation = True

        self.reservationList = reservationList

        return self.template()


class UpdateReservation(BrowserView):
    def __call__(self):
        request = self.request
        peroid = request.get('peroid')
        start_date = request.get('start_date')
        time = request.get('time')
        user = api.user.get_current().getUserName()
        brain = api.content.find(portal_type="Reservation")
        flag = False
        peroid_flag = ''

        for item in brain:
            obj = item.getObject()
            date = obj.date.strftime('%Y/%m/%d')
            if start_date == date:
                if peroid == 'peroid1' and not obj.peroid1:
                    obj.peroid1 = user
                    flag = True
                    peroid_flag = 'peroid1'
                elif peroid == 'peroid2' and not obj.peroid2:
                    obj.peroid2 = user
                    flag = True
                    peroid_flag = 'peroid2'
                elif peroid == 'peroid3' and not obj.peroid3:
                    obj.peroid3 = user
                    flag = True
                    peroid_flag = 'peroid3'
                elif peroid == 'peroid4' and not obj.peroid4:
                    obj.peroid4 = user
                    flag = True
                    peroid_flag = 'peroid4'
                elif peroid == 'peroid5' and not obj.peroid5:
                    obj.peroid5 = user
                    flag = True
                    peroid_flag = 'peroid5'
                elif peroid == 'peroid6' and not obj.peroid6:
                    obj.peroid6 = user
                    flag = True
                    peroid_flag = 'peroid6'
                elif peroid == 'alternate':
                    if obj.alternate:
                        obj.alternate +=',%s' %user
                    else:
                        obj.alternate = user
                    flag = True
                    peroid_flag = 'alternate'
        ####防止同時預約，導致前者被覆蓋####
        if flag == True:
            api.user.get(user).setMemberProperties(mapping={
                    'reservation_date': '%s  %s' %(start_date, time),
                    'peroid': peroid_flag
            })
            return 'success'
        else:
            return 'error'


class ReservationStatus(BrowserView):
    template = ViewPageTemplateFile("template/reservation_status.pt")
    def __call__(self):
        brains = api.content.find(portal_type='Reservation')
        reservationList = []
        for item in brains:
            obj = item.getObject()
            title = obj.title
            startDate = obj.date.strftime('%Y/%m/%d')
            startTime = obj.date.strftime('%H:%M')
            peroid1 = obj.peroid1
            peroid2 = obj.peroid2
            peroid3 = obj.peroid3
            peroid4 = obj.peroid4
            peroid5 = obj.peroid5
            peroid6 = obj.peroid6
            alternate = obj.alternate

            tmp_peroid = [peroid1, peroid2, peroid3, peroid4, peroid5, peroid6]
            
            timeList = []
            # timeList.append([startTime])  
            for i in range(0, 6):
                minutes = i*20
                time = obj.date + datetime.timedelta(minutes = minutes)
                # import pdb;pdb.set_trace()             
                timeList.append( '%s %s' %( time.strftime('%H:%M'), tmp_peroid[i])  )
            
            reservationList.append({
                    'title': title,
                    'timeList': timeList,
                    'startDate': startDate,
                    'alternate': alternate,
                })    
        self.reservationList = reservationList

        return self.template()


class UserProfile(BrowserView):
    template = ViewPageTemplateFile("template/user_profile.pt")
    def __call__(self):
        user_name = api.user.get_current().getUserName()
        user = api.user.get(user_name)

        self.user_id = user.getProperty('id', '')
        self.user_email = user.getProperty('email', '')
        self.user_ch_name = user.getProperty('ch_name', '')
        self.user_en_name = user.getProperty('en_name', '')
        self.user_officephone = user.getProperty('officephone', '')
        self.user_cellphone = user.getProperty('cellphone', '')
        self.user_location = user.getProperty('location', '')

        return self.template()



class UpdateProfile(BrowserView):
    def __call__(self):
        request = self.request
        user_ch_name = request.get('user_ch_name')
        user_en_name = request.get('user_en_name')
        user_email = request.get('user_email')
        user_officephone = request.get('user_officephone')
        user_location = request.get('user_location')
        user_cellphone = request.get('user_cellphone')

        user_name = api.user.get_current().getUserName()
        user = api.user.get(user_name)

        user.setMemberProperties(mapping={
                                            'ch_name': user_ch_name,
                                            'en_name': user_en_name,
                                            'email': user_email,
                                            'officephone': user_officephone,
                                            'location': user_location,
                                            'cellphone': user_cellphone,
                                        })
        request.response.redirect('%s/user_profile' % api.portal.get().absolute_url())
        api.portal.show_message('儲存成功'.decode('utf-8'), self.request, 'info')


class CancelReservation(BrowserView):
    def __call__(self):
        request = self.request
        user_name = api.user.get_current().getUserName()
        user = api.user.get(user_name)
        reservation_date = user.getProperty('reservation_date')[:10]
        peroid = user.getProperty('peroid')
        brain = api.content.find(context=api.portal.get(),Type='Reservation')

        for item in brain:
            obj = item.getObject()
            date = obj.date.strftime('%Y/%m/%d')
            if date == reservation_date:
                alternate = obj.alternate
                flag = False
                if alternate:
                    alternate_user = api.user.get(alternate)

                if peroid == 'peroid1':
                    if alternate:
                        # obj.peroid1 = alternate
                        date = obj.date
                        peroid_flag = 'peroid1'
                        flag = True
                    else:
                        obj.peroid1 = ''
                elif peroid == 'peroid2':
                    if alternate:
                        # obj.peroid2 = alternate
                        date = obj.date + datetime.timedelta(minutes = 20)
                        peroid_flag = 'peroid2'
                        flag = True
                    else:
                        obj.peroid2 = ''
                elif peroid == 'peroid3':
                    if alternate:
                        # obj.peroid3 = alternate
                        date = obj.date + datetime.timedelta(minutes = 40)
                        peroid_flag = 'peroid3'
                        flag = True
                    else:
                        obj.peroid3 = ''
                elif peroid == 'peroid4':
                    if alternate:
                        # obj.peroid4 = alternate
                        date = obj.date + datetime.timedelta(minutes = 60)
                        peroid_flag = 'peroid4'
                        flag = True
                    else:
                        obj.peroid4 = ''
                elif peroid == 'peroid5':
                    if alternate:
                        # obj.peroid5 = alternate
                        date = obj.date + datetime.timedelta(minutes = 80)
                        peroid_flag = 'peroid5'
                        flag = True
                    else:
                        obj.peroid5 = ''
                elif peroid == 'peroid6':
                    if alternate:
                        # obj.peroid6 = alternate
                        date = obj.date + datetime.timedelta(minutes = 100)
                        peroid_flag = 'peroid6'
                        flag = True
                    else:
                        obj.peroid6 = ''
                ####
                # 1.再peroid取消預約 沒候補
                # 2.再peroid取消預約 有候補
                # 3.自己是候補  取消預約
                ####
                # if flag:  
                #     alternate_user.setMemberProperties(mapping={
                #         'reservation_date': date.strftime('%Y/%m/%d  %H:%M'),
                #         'peroid': peroid_flag
                #     })
                user.setMemberProperties(mapping={
                    'reservation_date': '',
                    'peroid': ''
                })
                obj.alternate = ''

        request.response.redirect('%s/reservation' % api.portal.get().absolute_url())