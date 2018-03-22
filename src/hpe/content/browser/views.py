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


class Cover(BrowserView):
    template = ViewPageTemplateFile('template/cover.pt')
    def __call__(self):
        
        return self.template()


class Login(BrowserView):
    template = ViewPageTemplateFile('template/login.pt')
    def __call__(self):
        return self.template()


class Upload(BrowserView):
    template = ViewPageTemplateFile('template/upload.pt')
    def __call__(self):
        request = self.request
        # 暫且先轉到首頁
        abs_url = api.portal.get().absolute_url()
        request.response.redirect(abs_url)
        return  
        
        if api.user.is_anonymous():
            request.response.redirect('%s/user_login'%abs_url)
            return
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
        
        user = api.user.get_current().getProperty('email')
        execSql = SqlObj()
        execStr = """SELECT * FROM bicycle_picture WHERE user='{}'""".format(user)
        result = execSql.execSql(execStr)
        verify_data = []
        not_verify_data = []
        
        for item in result:
            tmp = dict(item)
            verify = tmp['verify']
            place = tmp['place']
            user = tmp['user']
            data = tmp['data']
            event = tmp['event']
            date = tmp['date']
            if verify == 0:
                not_verify_data.append({
                    'data': data,
                    'event': event,
                    'date': date,
                    'place': place
                })
            elif verify == 1:
                verify_data.append({
                    'data': data,
                    'event': event,
                    'date': date,
                    'place': place
                })
        self.verify_data = verify_data
        self.not_verify_data = not_verify_data

        return self.template()


class EatBlog(BrowserView):
    template = ViewPageTemplateFile('template/eat_blog.pt')
    def __call__(self):
        if api.user.is_anonymous():
            self.request.response.redirect('%s/user_login'%api.portal.get().absolute_url())
            return        
        user = api.user.get_current().getProperty('email')
        execSql = SqlObj()
        execStr = 'SELECT * from activity where category="%s" and user="%s"' %('食在有道理',user)
        result = execSql.execSql(execStr)
        self.condition_1 = False
        self.condition_2 = False
        self.condition_3 = False
        self.condition_4 = False
        for item in result:
            tmp = dict(item)
            # if tmp['activity_date'] == '2018-04-10 09:30':
            if tmp['activity_date'] == '2018-03-21 10:00':
                self.condition_1 = True
            elif tmp['activity_date'] == '2018-04-12 09:30':
                self.condition_2 = True
            elif tmp['activity_date'] == '2018-04-12 12:30':
                self.condition_3 = True
            elif tmp['activity_date'] == '2018-04-26 12:30':
                self.condition_4 = True
        return self.template()


class MindGasStation(BrowserView):
    template = ViewPageTemplateFile('template/mind_gas_station.pt')
    def __call__(self):
        portal = api.portal.get()
        if api.user.is_anonymous():
            self.request.response.redirect('%s/user_login'%portal.absolute_url())
            return
        else:
            data = []
            brain = api.content.find(context=portal['article'], Type="File")
            for item in brain:
                url = item.getURL()
                obj = item.getObject()
                img = '%s/@@images/img/preview' %url
                file = '%s/@@display-file/file/%s' %(url, obj.file.filename)
                description = obj.description
                tmp = description.split('\r')
                des_content = ''
                if description:
                    for text in tmp:
                        des_content += '. ' + text.strip() + '<br>'

                data.append({
                    'img': img,
                    'file': file,
                    'text': des_content
                })
            self.data = data
        return self.template()


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
        
        user = api.user.get_current().getProperty('email')
        event = request.get('event')
        place = request.get('place')
        data = request.get('b64_image').split(',')[1]
        
        execSql = SqlObj()
        execStr = """INSERT INTO bicycle_picture(user, event, place, data) VALUES('{}',
            '{}','{}','{}')""".format(user, event, place, data)
        execSql.execSql(execStr)
        # b64_image = request.get('b64_image').split(',')[1]
        # image_title = request.get('image')
        # event = request.get('event')
        # place = request.get('place')
        # news = api.content.create(
        #     type='BicyclePicture',
        #     container=portal,
        #     title='news1',
        #     event=event,
        #     place=place,
        #     image=namedfile.NamedBlobImage(data=base64.b64decode(b64_image), filename=safe_unicode(image_title))
        # )


class Reservation(BrowserView):
    template = ViewPageTemplateFile("template/reservation.pt")
    def __call__(self):
        if api.user.is_anonymous():
            self.request.response.redirect('%s/user_login'%api.portal.get().absolute_url())
            return 
        brains = api.content.find(portal_type='Reservation')
        reservationList = []
        user_reservation_date = api.user.get_current().getProperty('reservation_date')
        self.already_reservation = False
        
        # 若以預約就不顯示報名表
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
                alternateMsg = ''
                if peroid1 and peroid2 and peroid3 and peroid4 and peroid5 and peroid6:
                    if alternate == None or len(alternate.split(',')) < 30: 
                        alternate = 'enable'
                        alternateMsg = '開放候補'
                    else:
                        alternate = 'disabled'
                        alternateMsg = '候補以滿'  
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
            self.already_reservation = True

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
            execSql =SqlObj()
            log = '%s %s 預約成功' %(start_date, peroid)
            execStr = """INSERT INTO log(user,category,log) VALUES('{}','{}','{}')
                """.format(user, '預約', log)
            execSql.execSql(execStr)

            api.user.get_current().setMemberProperties(mapping={
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
        roles = api.user.get_current().getRoles()
        abs_url = api.portal.get().absolute_url()
        if 'Manager' not in roles:
            api.portal.show_message('您沒有權限', self.request, 'error')            
            self.request.response.redirect(abs_url)
            return
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
            ####peroid時間， 預約人， 是否預定， 是否可以選取####
            peroidList = []
            timeList = []
            for i in range(0, 6):
                minutes = i*20
                time = obj.date + datetime.timedelta(minutes = minutes)
                if not tmp_peroid[i]:
                    j = i + 1
                    peroidList.append('peroid%s' %j)
                    condition_peroid = 'enable'
                    condition_select = 'enable_selct'
                else:
                    condition_peroid = 'disabled'
                    condition_select = 'disabled_select'

                timeList.append([time.strftime('%H:%M'), tmp_peroid[i], condition_peroid, condition_select])
            ####判斷是否有候補人員####
            if not alternate:
                condition_alternate = False
                alternateList = ''
            else:
                condition_alternate = True
                alternateList = alternate.split(',')

            reservationList.append({
                    'title': title,
                    'timeList': timeList,
                    'startDate': startDate,
                    'alternate': alternateList,
                    'startDateTime': obj.date.strftime('%Y/%m/%d  %H:%M'),
                    'peroidList': peroidList,
                    'condition_alternate': condition_alternate,
                    'condition_peroid': condition_peroid
                })    
        self.reservationList = reservationList

        return self.template()


class UserProfile(BrowserView):
    template = ViewPageTemplateFile("template/user_profile.pt")
    def __call__(self):
        if api.user.is_anonymous():
            self.request.response.redirect('%s/user_login'%api.portal.get().absolute_url())
            return 
        user = api.user.get_current()
        user_email = user.getProperty('email')

        execSql = SqlObj()
        execStr = """SELECT picture_data FROM user_picture WHERE user = '{}'
                 """.format(user_email)
        result = execSql.execSql(execStr)

        self.picture_data = 'data:image/png;base64,%s' %dict(result[0])['picture_data']
        self.user_id = user.getProperty('user_id', '')
        self.user_email = user_email
        self.user_ch_name = user.getProperty('fullname', '')
        self.user_en_name = user.getProperty('en_name', '')
        self.user_cellphone = user.getProperty('cellphone', '')
        self.user_location = user.getProperty('location', '')
        self.user_officephone = user.getProperty('officephone', '')
        
        execStr = """SELECT * FROM activity WHERE user='{}'""".format(user_email)
        result = execSql.execSql(execStr)
        data = []
        for item in result:
            tmp = dict(item)
            category = tmp['category']
            activity_date = tmp['activity_date']
            is_first = tmp['is_first']
            is_end = tmp['is_end']
            step = tmp['step']

            if is_first == 0:
                condition_1 = True
                condition_2 = False
                condition_3 = False
            elif is_first == 1 and is_end == 1:
                condition_1 = False
                condition_2 = True
                condition_3 = False
            elif is_first == 1 and is_end == 0:
                condition_1 = False
                condition_2 = False
                condition_3 = True

            data.append({
                'category': category,
                'activity_date': activity_date,
                'step': step,
                'condition_1': condition_1,
                'condition_2': condition_2,
                'condition_3': condition_3,
            })
        self.data = sorted(data)

        execStr = """SELECT SUM(step) as sum_step FROM `activity` WHERE user='{}' AND is_first=1 
            AND is_end=1""".format(user_email)
        result = execSql.execSql(execStr)
        sum_step = dict(result[0])['sum_step']
        if not sum_step:
            sum_step = 0
        self.sum_step = sum_step 
        return self.template()



class UpdateProfile(BrowserView):
    def __call__(self):
        request = self.request
        user_ch_name = request.get('user_ch_name')
        user_en_name = request.get('user_en_name')
        user_officephone = request.get('user_officephone')
        user_location = request.get('user_location')
        user_cellphone = request.get('user_cellphone')

        user = api.user.get_current()
        user.setMemberProperties(mapping={
                                            'fullname': user_ch_name,
                                            'en_name': user_en_name,
                                            'officephone': user_officephone,
                                            'location': user_location,
                                            'cellphone': user_cellphone,
                                        })
        request.response.redirect('%s/profile' % api.portal.get().absolute_url())
        api.portal.show_message('儲存成功'.decode('utf-8'), self.request, 'info')


class CancelReservation(BrowserView):
    def __call__(self):
        request = self.request
        user = api.user.get_current()        
        user_name = user.getProperty('email')
        reservation_date = user.getProperty('reservation_date')[:10]
        peroid = user.getProperty('peroid')
        brain = api.content.find(context=api.portal.get(),Type='Reservation')

        for item in brain:
            obj = item.getObject()
            date = obj.date.strftime('%Y/%m/%d')
            if date == reservation_date:
                if peroid == 'peroid1':
                    date = obj.date
                    peroid_flag = 'peroid1'
                    obj.peroid1 = ''
                elif peroid == 'peroid2':
                    date = obj.date + datetime.timedelta(minutes = 20)
                    peroid_flag = 'peroid2'
                    obj.peroid2 = ''
                elif peroid == 'peroid3':
                    date = obj.date + datetime.timedelta(minutes = 40)
                    peroid_flag = 'peroid3'
                    obj.peroid3 = ''
                elif peroid == 'peroid4':
                    date = obj.date + datetime.timedelta(minutes = 60)
                    peroid_flag = 'peroid4'
                    obj.peroid4 = ''                        
                elif peroid == 'peroid5':
                    date = obj.date + datetime.timedelta(minutes = 80)
                    peroid_flag = 'peroid5'
                    obj.peroid5 = ''
                elif peroid == 'peroid6':
                    obj.peroid6 = ''
                    date = obj.date + datetime.timedelta(minutes = 100)
                    peroid_flag = 'peroid6'
                elif peroid == 'alternate':
                    alternate_list = obj.alternate.split(',')
                    alternate_list.remove(user_name)
                    obj.alternate = ''
                    for item in alternate_list:
                        if obj.alternate:
                            obj.alternate +=',%s' %item
                        else:
                            obj.alternate = item
                user.setMemberProperties(mapping={
                    'reservation_date': '',
                    'peroid': ''
                })
        execSql =SqlObj()
        execStr = """INSERT INTO log(user,category,log) VALUES('{}','{}','{}')
            """.format(user_name, '預約', '預約取消')
        execSql.execSql(execStr)
        request.response.redirect('%s/reservation' % api.portal.get().absolute_url())


class UpdateAlternate(BrowserView):
    def __call__(self):
        request = self.request
        name = request.get('name')
        peroid = request.get('peroid')
        start_date = request.get('start_date')
        time = request.get('time')
        user = api.user.get(username=name)

        brain = api.content.find(conext=api.portal.get(), Type="Reservation")
        for item in brain:
            obj = item.getObject()
            date = obj.date.strftime('%Y/%m/%d')
            if date == start_date[:10]:
                if peroid == 'peroid1':
                    obj.peroid1 = name
                elif peroid == 'peroid2':
                    obj.peroid2 = name
                elif peroid == 'peroid3':
                    obj.peroid3 = name
                elif peroid == 'peroid4':
                    obj.peroid4 = name
                elif peroid == 'peroid5':
                    obj.peroid5 = name
                elif peroid == 'peroid6':
                    obj.peroid6 = name
                alternate_list = obj.alternate.split(',')
                alternate_list.remove(name)
                obj.alternate = ''
                for item in alternate_list:
                    if obj.alternate:
                        obj.alternate +=',%s' %item
                    else:
                        obj.alternate = item
                user.setMemberProperties(mapping={
                    'reservation_date': '%s %s' %(start_date[:10], time),
                    'peroid': peroid
                })
        return 'success'


class ManagerCancelReservation(BrowserView):
    def __call__(self):
        request = self.request
        peroidList = request.get('peroidList[]', '')
        alternateList = request.get('alternateList[]', '')
        action = request.get('action')
        brain = api.content.find(conext=api.portal.get(), Type="Reservation")
        if type(peroidList) == str:
            peroidList = [peroidList, 'z,z']
        if type(alternateList) == str:
            alternateList = [alternateList, 'z,z']
        if action == 'peroid':
            for data in peroidList:
                start_date = data.split(',')[0]
                user_name = data.split(',')[1]
                user = api.user.get(username=user_name)
                for item in brain:
                    obj = item.getObject()
                    date = obj.date.strftime('%Y/%m/%d')
                    if date == start_date:
                        if obj.peroid1 == user_name:
                            obj.peroid1 = ''
                        elif obj.peroid2 == user_name:
                            obj.peroid2 = ''
                        elif obj.peroid3 == user_name:
                            obj.peroid3 = ''
                        elif obj.peroid4 == user_name:
                            obj.peroid4 = ''
                        elif obj.peroid5 == user_name:
                            obj.peroid5 = ''
                        elif obj.peroid6 == user_name:
                            obj.peroid6 = ''
                    ####用來排除只選一個時抓不到user####
                    if user_name != 'z':
                        user.setMemberProperties(mapping={
                            'reservation_date': '',
                            'peroid': ''
                        })
        elif action == 'alternate':
            for name in alternateList:
                for item in brain:
                    obj = item.getObject()
                    if obj.alternate:
                        obj_alternate = obj.alternate.split(',')
                        if name in obj_alternate:
                            obj_alternate.remove(name)
                            obj.alternate = ''
                            user = api.user.get(username=name)
                            user.setMemberProperties(mapping={
                                'reservation_date': '',
                                'peroid': ''
                            })
                            for user_name in obj_alternate:
                                if obj.alternate:
                                    obj.alternate +=',%s' %user_name
                                else:
                                    obj.alternate = user_name
        return 'success'


class SendMail():
    def send_mail(self):
        api.portal.send_email(
            recipient="ah13441673@gmail.com",
            sender="henry@mingtak.com.tw",
            subject="Trappist",
            body="One for you Bob!",
        )


class Log(BrowserView):
    template = ViewPageTemplateFile('template/log.pt')
    def __call__(self):
        execSql = SqlObj()        
        execStr = """SELECT * FROM log ORDER BY time DESC"""
        self.result = execSql.execSql(execStr)
        
        return self.template()
