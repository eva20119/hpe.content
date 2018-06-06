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
    template = ViewPageTemplateFile("template/en_cover.pt")
    def __call__(self):
        return self.template()


class EnMindGasStation(BrowserView):
    template = ViewPageTemplateFile('template/en_mind_gas_station.pt')
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
                if obj.lang == 'English':
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


class EnPublicizePressure(BrowserView):
    template = ViewPageTemplateFile('template/en_publicize_pressure.pt')
    def __call__(self):
        if api.user.is_anonymous():
            self.request.response.redirect('%s/user_login'%api.portal.get().absolute_url())
            return 
        return self.template()


class EnEatBlog(BrowserView):
    template = ViewPageTemplateFile('template/en_eat_blog.pt')
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
            if tmp['activity_date'] == '2018-04-10 09:00':
                self.condition_1 = True
            elif tmp['activity_date'] == '2018-04-19 09:00':
                self.condition_2 = True
            elif tmp['activity_date'] == '2018-04-12 12:00':
                self.condition_3 = True
            elif tmp['activity_date'] == '2018-04-26 12:00':
                self.condition_4 = True
        return self.template()


class EnTestPressure(BrowserView):
    template = ViewPageTemplateFile('template/en_test_pressure.pt')
    def __call__(self):
        if api.user.is_anonymous():
            self.request.response.redirect('%s/user_login'%api.portal.get().absolute_url())
            return 
        return self.template()


class EnCalculatePressure(BrowserView):
    template = ViewPageTemplateFile('template/en_calculate_pressure.pt')
    def __call__(self):
        request = self.request
        answer1_1 = request.get('answer1_1')
        answer1_2 = request.get('answer1_2')
        answer1_3 = request.get('answer1_3')
        answer1_4 = request.get('answer1_4')
        answer1_5 = request.get('answer1_5')
        answer1_6 = request.get('answer1_6')
        answer2_1 = request.get('answer2_1')
        answer2_2 = request.get('answer2_2')
        answer2_3 = request.get('answer2_3')
        answer2_4 = request.get('answer2_4')
        answer2_5 = request.get('answer2_5')
        answer2_6 = request.get('answer2_6')
        answer2_7 = request.get('answer2_7')
        personal_pressure = (int(answer1_1) + int(answer1_2) + int(answer1_3) + int(answer1_4) + int(answer1_5) + int(answer1_6)) / 6
        work_pressure = (int(answer2_1) + int(answer2_2) + int(answer2_3) + int(answer2_4) + int(answer2_5) + int(answer2_6) + int(answer2_7)) / 7

        user = api.user.get_current().getUserName()
        execSql  = SqlObj()

        execStr = """INSERT INTO pressure(user, personal_pressure, work_pressure) 
                VALUES('{}', '{}', '{}')""".format(user, personal_pressure, work_pressure)
        execSql.execSql(execStr)

        self.personal_pressure = personal_pressure
        self.work_pressure = work_pressure

        return self.template()


class EnUserProfile(BrowserView):
    template = ViewPageTemplateFile('template/en_profile.pt')
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
            if tmp['category']  ==  '食在有道理':
                category = 'FOOD MAKES SENSE'
            elif tmp['category'] == '肌力動次動':
                category = 'Strength training: Move it! move it!'
            elif tmp['category'] == '防癌你我他':
                category = 'Power Of Prevention'

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


class EnReservation(BrowserView):
    template = ViewPageTemplateFile('template/en_reservation.pt')
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
                # 填入第一次的開始後結束時間
                timeList.append([startTime, (obj.date + datetime.timedelta(minutes = 20)).strftime('%H:%M')])  
                for i in range(1, 6):
                    minutes = i*20
                    # 此處縮排vscode顯示似乎有問題
                    reservation_start_time = obj.date + datetime.timedelta(minutes = minutes)
		    reservation_end_time = reservation_start_time + datetime.timedelta(minutes = 20)
                    timeList.append([reservation_start_time.strftime('%H:%M'), reservation_end_time.strftime('%H:%M')])
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
                        alternateMsg = 'Open Alternate'
                    else:
                        alternate = 'disabled'
                        alternateMsg = 'No Vacancy'  
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
            self.user_reservation_msg = 'You haved booked %s' %user_reservation_date
            self.already_reservation = True

        self.reservationList = reservationList

        return self.template()


class EnMuscleActivity(BrowserView):
    template = ViewPageTemplateFile('template/en_muscle_activity.pt')
    def __call__(self):
        if api.user.is_anonymous():
            self.request.response.redirect('%s/user_login'%api.portal.get().absolute_url())
            return        
        user = api.user.get_current().getProperty('email')
        execSql = SqlObj()
        execStr = 'SELECT * from activity where category="%s" and user="%s"' %('肌力動次動',user)
        result = execSql.execSql(execStr)
        self.condition_1 = False
        self.condition_2 = False
        self.condition_3 = False
        self.condition_4 = False
        for item in result:
            tmp = dict(item)
            if tmp['activity_date'] == '2018-05-03 10:30':
                self.condition_1 = True
            elif tmp['activity_date'] == '2018-05-10 10:30':
                self.condition_2 = True
            elif tmp['activity_date'] == '2018-05-08 10:30':
                self.condition_3 = True
        return self.template()


class EnAntiCancerView(BrowserView):
    template = ViewPageTemplateFile('template/en_anti_cancer_view.pt')
    def __call__(self):
        if api.user.is_anonymous():
            self.request.response.redirect('%s/user_login'%api.portal.get().absolute_url())
            return
        user = api.user.get_current().getProperty('email')
        execSql = SqlObj()
        execStr = 'SELECT * from activity where category="%s" and user="%s"' %('防癌你我他',user)
        result = execSql.execSql(execStr)
        self.condition_1 = False
        self.condition_2 = False
        self.condition_3 = False
        self.condition_4 = False
        for item in result:
            tmp = dict(item)
            if tmp['activity_date'] == '2018-06-14 12:00':
                self.condition_1 = True
            elif tmp['activity_date'] == '2018-06-21 15:30' or tmp['activity_date'] == '2018-06-21 14:30':
                self.condition_2 = True
            elif tmp['activity_date'] == '2018-06-26 12:00':
                self.condition_3 = True
            elif tmp['activity_date'] == '2018-06-21 12:15' or tmp['activity_date'] == '2018-06-21 11:00' or tmp['activity_date'] == 0:
                self.condition_4 = True
        return self.template()


class EnTestCancerView(BrowserView):
    template = ViewPageTemplateFile('template/en_test_cancer_view.pt')
    def __call__(self):
        return self.template()


class EnTestCancer(BrowserView):
    template = ViewPageTemplateFile('template/en_test_cancer.pt')
    def __call__(self):
        return self.template()


class EnAnalysisCancer(BrowserView):
    template = ViewPageTemplateFile('template/en_analysis_cancer.pt')
    def __call__(self):
        request = self.request
        if api.user.is_anonymous():
            request.response.redirect('%s/user_login'%api.portal.get().absolute_url())
            return   
        q1 = request.get('q1')
        q2 = request.get('q2').replace('\xe2\x80\x99', "'")
        q3 = request.get('q3').replace('\xef\xbc\x8c', ',').replace('\xe2\x89\xa6', '<=').replace('\xe2\x89\xa7', '>=').replace('\xef\xbc\x9c', '<')
        q4 = request.get('q4')
        q5 = request.get('q5')
        q6 = request.get('q6')
        execSql = SqlObj()
        user = api.user.get_current().getProperty('email')
        execStr = """INSERT INTO anti_cancer(`user`, `q1`, `q2`, `q3`, `q4`, `q5`, `q6`)
            VALUES('{}','{}',"{}",'{}','{}','{}','{}')""".format(user, q1, q2, q3, q4, q5, q6)
        execSql.execSql(execStr)
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.q5 = q5
        self.q6 = q6
        return self.template()

