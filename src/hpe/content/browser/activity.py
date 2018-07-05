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
import time


class UpdateActivity(BrowserView):
    def __call__(self):
        request = self.request

        # 檢查是否已完整填寫員工資料
        current = api.user.get_current()
#        import pdb; pdb.set_trace()
        if not (current.getProperty('en_name') and current.getProperty('officephone') and current.getProperty('cellphone')):
            return 'loseData'

        select_date = request.get('select_date[]')
        if type(select_date) == str:
            select_date = [select_date]
        event = request.get('event')
        user = api.user.get_current().getProperty('email')
        step = request.get('step')
        special = request.get('special[0][]')
        execSql = SqlObj()
        if select_date:
            for activity in select_date:

                # 寫進活動列表
                execStr = """INSERT INTO activity(user,category,activity_date,step) VALUES('{}','{}'
                    ,'{}','{}')""".format(user, event, activity,step)
                execSql.execSql(execStr)
                # 寫進log
                log = '報名%s' %activity
                execStr = """INSERT INTO log(user,category,log) VALUES('{}','{}','{}')
                    """.format(user, event, log)
                execSql.execSql(execStr)

        # 防癌你我他的三選一
        if special:
            execStr = """INSERT INTO activity(user,category,activity_date,step, note) VALUES('{}','{}'
                ,'{}','{}','{}')""".format(user, event, special[0],step, special[1])
            execSql.execSql(execStr)
            # 寫進log
            log = '報名%s' % special[0]
            execStr = """INSERT INTO log(user,category,log) VALUES('{}','{}','{}')
                """.format(user, event, log)
            execSql.execSql(execStr)
        return 'success'


class EventHandl(BrowserView):
    def __call__(self):
        request = self.request
        context = self.context
        worker_roles = api.user.get_current().getRoles()
        if 'Reader' in worker_roles:
            email = request.get('email')
            start = time.mktime(context.start.timetuple())
            end = time.mktime(context.end.timetuple())
            now = time.time()
            user_name = api.user.get(username=email).getProperty('fullname')
            start_date = context.start.strftime('%Y-%m-%d %H:%M')
            category = context.title
            step = context.step
            now_time = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
            # 介再開始和結束的時間內且role要是讀者
            if now >= start-14400 and now <= end:
                execSql = SqlObj()
                execStr = """SELECT * FROM activity WHERE user='{}' AND
                    activity_date='{}'""".format(email, start_date)
                result = execSql.execSql(execStr)
                # 若沒報名就幫他現場報名
                if not result:
                    execStr = """INSERT INTO activity(user,category,activity_date,is_first
                        ,check_in_time,step) VALUES('{}','{}','{}',1,'{}', '{}')
                        """.format(email, category, start_date, now_time, step)
                    execSql.execSql(execStr)
                    log = "%s 現場報名 %s %s" %(user_name, category, start_date)
                    execStr = """INSERT INTO log(user,category,log) VALUES('{}','{}','{}')
                        """.format(email, category, log)
                    execSql.execSql(execStr)
                    return '現場報名成功'
                else:
                    tmp = dict(result[0])
                    if tmp['is_first'] == 0 and tmp['is_end'] == 0 and tmp['check_in_time'] == None:
                        execStr = """UPDATE activity SET is_first = 1,check_in_time='{}' WHERE user='{}' AND
                            activity_date='{}'""".format(now_time, email, start_date)
                        execSql.execSql(execStr)
                        execStr = """INSERT INTO log(user,category,log) VALUES('{}','{}','{}')
                            """.format(email, '活動進行', '%s 活動參加' %now_time)
                        execSql.execSql(execStr)
                        return '%s %s 報到成功' %(user_name, now_time)
                    elif tmp['is_first'] == 1 and tmp['is_end'] == 0 and tmp['check_in_time'] and tmp['finish_time'] == None:
                        check_in_time = datetime.datetime.strptime(tmp['check_in_time'], '%Y-%m-%d %H:%M:%S')
                        now = datetime.datetime.now()
                        time_delta = now - check_in_time
                        if time_delta.total_seconds() > 60:
                            execStr = """UPDATE activity SET is_end = 1,finish_time='{}' WHERE
                                user='{}' AND activity_date='{}'
                                """.format(now.strftime('%Y-%m-%d %H:%M:%S'), email, start_date)
                            execSql.execSql(execStr)
                            execStr = """INSERT INTO log(user,category,log) VALUES('{}','{}','{}')
                                """.format(email, '活動進行', '%s活動完成'%now.strftime('%Y-%m-%d %H:%M:%S') )
                            execSql.execSql(execStr)
                            return '%s %s 活動完成' %(user_name, now_time)
                        else:
                            return '%s 您已報到過   請勿重複報到' %user_name
                    elif tmp['is_first'] == 1 and tmp['is_end'] == 1:
                        return '%s 您已完成活動  請勿再報到' %user_name
            else:
                return '活動尚未開始'
        else:
            return '權限不足'


class CancelActivity(BrowserView):
    def __call__(self):
        request = self.request
        activity_date = request.get('activity_date')
        category = request.get('category')
        lang = request.get('lang')
        user = api.user.get_current().getProperty('email')
        execSql = SqlObj()

        execStr = """DELETE FROM activity WHERE user='{}' AND activity_date='{}'
            """.format(user, activity_date)
        execSql.execSql(execStr)

        execStr = """INSERT INTO log(user,log,category) VALUES('{}','{}','{}')
            """.format(user, '取消%s' %activity_date , category)
        execSql.execSql(execStr)
        if lang == 'Chinese':
            request.response.redirect('%s/profile' %api.portal.get().absolute_url())
        if lang == 'English':
	    request.response.redirect('%s/en_profile' %api.portal.get().absolute_url())


class ShowActivityStatus(BrowserView):
    template = ViewPageTemplateFile('template/show_activity_status.pt')
    def __call__(self):
        request = self.request
        abs_url = api.portal.get().absolute_url()
        roles = api.user.get_current().getRoles()
        if api.user.is_anonymous() or 'Manager' not in roles:
	        request.response.redirect('%s/user_login' %abs_url)
	        return
        return self.template()


class GetEventData(BrowserView):
    template = ViewPageTemplateFile('template/event_result.pt')
    template1 = ViewPageTemplateFile('template/event_result_for_cancer.pt')
    template2 = ViewPageTemplateFile('template/event_result_for_bicycle.pt')
    img_preview = ViewPageTemplateFile('template/img_preview.pt')
    def __call__(self):
        request = self.request
        date = request.get('date')
        event = request.get('event')
        execSql = SqlObj()

        all_users = api.user.get_users()
        user_data = {}
        for item in all_users:
            email = item.getProperty('email')
            user_id = item.getProperty('user_id')
            cellphone = item.getProperty('cellphone')
            location = item.getProperty('location')
            officephone = item.getProperty('officephone')
            fullname = item.getProperty('fullname')
            en_name = item.getProperty('en_name')
            user_data[email] = {
                'user_id': user_id,
                'cellphone':cellphone,
                'en_name': en_name,
                'location': location,
                'officephone':officephone,
                'fullname': fullname
            }
        if event == '樂活騎單車':
            if date == 'audit':
                execStr = """SELECT * FROM bicycle_picture WHERE is_check = 0 Limit 15 """
            elif date == 'complete' or date == 'img_preview':
                execStr = """SELECT * FROM bicycle_picture WHERE is_check = 1  ORDER BY complete_time ASC"""
        else:
            execStr = """SELECT * FROM activity WHERE category = '{}' AND activity_date = '{}'
                ORDER BY sing_up_time""".format(event, date)
        result = execSql.execSql(execStr)
        data = []
        if event == '樂活騎單車':
            for item in result:
                tmp = dict(item)
                user_email = tmp['user']
                location = tmp['location']
                want_award = tmp['want_award']
                img = tmp['img']
                image_title = tmp['image_title']
                is_check = tmp['is_check']
                id = tmp['id']
                upload_time = tmp['upload_time']
                if user_data.has_key(user_email):
                    user_list = user_data[user_email]
                    data.append([
                        user_list['user_id'], user_email, user_list['fullname']
                        , user_list['en_name'], user_list['officephone'], user_list['cellphone']
                        , user_list['location'], location, want_award, img, image_title, is_check, id, upload_time
                    ])
        else:
            for item in result:
                tmp = dict(item)
                activity_date = tmp['activity_date']
                sing_up_time = tmp['sing_up_time']
                user_email = tmp['user']
                category= tmp['category']
                note = tmp['note']
                if user_data.has_key(user_email):
                    user_list = user_data[user_email]
                    data.append([
                        category ,activity_date, user_list['user_id'], user_email, user_list['fullname']
                        , user_list['en_name'], user_list['officephone'], user_list['cellphone']
                        , user_list['location'], sing_up_time, note
                    ])
        self.data = data


        if date == '2018-06-21 12:15' or date == '2018-06-21 11:00' or date == '0':
            return self.template1()
        elif date == 'img_preview':
            return self.img_preview()
        elif event == '樂活騎單車':
            return self.template2()
        else:
            return self.template()
