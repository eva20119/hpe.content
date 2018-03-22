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
        select_date = request.get('select_date[]')
        if type(select_date) == str:
            select_date = [select_date]
        event = request.get('event')
        user = api.user.get_current().getProperty('email')
        execSql = SqlObj()
        for activity in select_date:
            
            # 寫進活動列表
            execStr = """INSERT INTO activity(user,category,activity_date) VALUES('{}','{}'
                ,'{}')""".format(user, event, activity)
            execSql.execSql(execStr)
            # 寫進log
            log = '參加報名'
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
            step = context.step
            now_time = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
            # 介再開始和結束的時間內且role要是讀者
            if now >= start and now <= end:
                execSql = SqlObj()
                execStr = """SELECT * FROM activity WHERE user='{}' AND 
                    activity_date='{}'""".format(email, start_date)
                result = execSql.execSql(execStr)
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
                        execStr = """UPDATE activity SET is_end = 1,step='{}',finish_time='{}' WHERE 
                            user='{}' AND activity_date='{}'
                            """.format(step, now.strftime('%Y-%m-%d %H:%M:%S'), email, start_date)
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
                return '開始時間,結束時間或會員權限有問題'
        else:
            return '權限不足'

class CancelActivity(BrowserView):
    def __call__(self):
        request = self.request
        activity_date = request.get('activity_date')
        category = request.get('category')
        user = api.user.get_current().getProperty('email')
        execSql = SqlObj()

        execStr = """DELETE FROM activity WHERE user='{}' AND activity_date='{}'
            """.format(user, activity_date)
        execSql.execSql(execStr)

        execStr = """INSERT INTO log(user,log,category) VALUES('{}','{}','{}')
            """.format(user, '取消參加活動', category)
        execSql.execSql(execStr)

        request.response.redirect('%s/profile' %api.portal.get().absolute_url())