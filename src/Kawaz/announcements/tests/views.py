# -*- coding: utf-8 -*-
#
# Created:        2010/11/16
# Author:        alisue
#
from django.test import TestCase
from django.core.urlresolvers import reverse

from libwaz.test.userset import UserSet
from ..models import Announcement

class AnnouncementViewTest(TestCase):
    def setUp(self):
        self.userset = UserSet()
        for i in xrange(200):
            Announcement.objects.create(
                title='title%s'%i,
                body='body%s'%i
            )
        
    def test_list_view(self):
        response = self.client.get(reverse('announcements-announcement-list'))
        self.assertEqual(response.status_code, 200)
    
    def test_detail_view(self):
        response = self.client.get(reverse('announcements-announcement-detail', kwargs={'object_id': 1}))
        self.assertEqual(response.status_code, 200)
    
    def test_archive_year_view(self):
        response = self.client.get(reverse('announcements-announcement-archive-year', kwargs={'year': 2010}))
        self.assertEqual(response.status_code, 200)
    def test_archive_month_view(self):
        for month in xrange(1, 12):
            response = self.client.get(reverse('announcements-announcement-archive-month', kwargs={'year': 2010, 'month': month}))
            self.assertEqual(response.status_code, 200)
    def test_create_view(self):
        data = {'title': 'Hello', 'body': 'world'}
        # 外部ユーザーはアクセス不可
        response = self.client.get(reverse('announcements-announcement-create'))
        self.assertRedirects(response, reverse('auth_login'))
        response = self.client.post(reverse('announcements-announcement-create'), data)
        self.assertRedirects(response, reverse('auth_login'))
        # 一般ユーザーはアクセス不可能
        self.assertEqual(self.userset.login_user(self.client), True)
        response = self.client.get(reverse('announcements-announcement-create'))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('announcements-announcement-create'), data)
        self.assertEqual(response.status_code, 403)
        # スタッフユーザーはアクセス可能
        self.assertEqual(self.userset.login_staff(self.client), True)
        response = self.client.get(reverse('announcements-announcement-create'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('announcements-announcement-create'), data)
        self.assertRedirects(response, reverse('announcements-announcement-detail', kwargs={'object_id': Announcement.objects.count()}))
        self.assertEqual(Announcement.objects.filter(title='Hello').exists(), True)
        # スーパーユーザーはアクセス可能
        self.assertEqual(self.userset.login_admin(self.client), True)
        response = self.client.get(reverse('announcements-announcement-create'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('announcements-announcement-create'), data)
        self.assertRedirects(response, reverse('announcements-announcement-detail', kwargs={'object_id': Announcement.objects.count()}))
        self.assertEqual(Announcement.objects.filter(title='Hello').exists(), True)
    
    def test_update_view(self):
        data = {'title': 'Hello', 'body': 'world'}
        # 外部ユーザーはアクセス不可
        response = self.client.get(reverse('announcements-announcement-update', kwargs={'object_id': 1}))
        self.assertRedirects(response, reverse('auth_login'))
        response = self.client.post(reverse('announcements-announcement-update', kwargs={'object_id': 1}), data)
        self.assertRedirects(response, reverse('auth_login'))
        # 一般ユーザーはアクセス不可能
        self.assertEqual(self.userset.login_user(self.client), True)
        response = self.client.get(reverse('announcements-announcement-update', kwargs={'object_id': 1}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('announcements-announcement-update', kwargs={'object_id': 1}), data)
        self.assertEqual(response.status_code, 403)
        # スタッフユーザーはアクセス可能
        self.assertEqual(self.userset.login_staff(self.client), True)
        response = self.client.get(reverse('announcements-announcement-update', kwargs={'object_id': 1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('announcements-announcement-update', kwargs={'object_id': 1}), data)
        self.assertRedirects(response, reverse('announcements-announcement-detail', kwargs={'object_id': 1}))
        self.assertEqual(Announcement.objects.filter(title='Hello', pk=1).exists(), True)
        # スーパーユーザーはアクセス可能
        self.assertEqual(self.userset.login_admin(self.client), True)
        response = self.client.get(reverse('announcements-announcement-update', kwargs={'object_id': 1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('announcements-announcement-update', kwargs={'object_id': 1}), data)
        self.assertRedirects(response, reverse('announcements-announcement-detail', kwargs={'object_id': 1}))
        self.assertEqual(Announcement.objects.filter(title='Hello', pk=1).exists(), True)

    def test_delete_view(self):
        # 外部ユーザーはアクセス不可
        response = self.client.get(reverse('announcements-announcement-delete', kwargs={'object_id': 1}))
        self.assertRedirects(response, reverse('auth_login'))
        response = self.client.post(reverse('announcements-announcement-delete', kwargs={'object_id': 1}))
        self.assertRedirects(response, reverse('auth_login'))
        # 一般ユーザーはアクセス不可能
        self.assertEqual(self.userset.login_user(self.client), True)
        response = self.client.get(reverse('announcements-announcement-delete', kwargs={'object_id': 1}))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('announcements-announcement-delete', kwargs={'object_id': 1}))
        self.assertEqual(response.status_code, 403)
        # スタッフユーザーはアクセス可能
        self.assertEqual(self.userset.login_staff(self.client), True)
        response = self.client.get(reverse('announcements-announcement-delete', kwargs={'object_id': 1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('announcements-announcement-delete', kwargs={'object_id': 1}))
        self.assertRedirects(response, reverse('announcements-announcement-list'))
        self.assertEqual(Announcement.objects.filter(pk=1).exists(), False)
        # スーパーユーザーはアクセス可能
        self.assertEqual(self.userset.login_admin(self.client), True)
        response = self.client.get(reverse('announcements-announcement-delete', kwargs={'object_id': 2}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('announcements-announcement-delete', kwargs={'object_id': 2}))
        self.assertRedirects(response, reverse('announcements-announcement-list'))
        self.assertEqual(Announcement.objects.filter(pk=2).exists(), False)
    
    def test_invalid_detail_view(self):
        response = self.client.get(reverse('announcements-announcement-detail', kwargs={'object_id': 0}))
        self.assertEqual(response.status_code, 404)
    def test_invalid_update_view(self):
        self.assertEqual(self.userset.login_staff(self.client), True)
        response = self.client.get(reverse('announcements-announcement-update', kwargs={'object_id': 0}))
        self.assertEqual(response.status_code, 404)
        response = self.client.post(reverse('announcements-announcement-update', kwargs={'object_id': 0}))
        self.assertEqual(response.status_code, 404)
    def test_invalid_delete_view(self):
        self.assertEqual(self.userset.login_staff(self.client), True)
        response = self.client.get(reverse('announcements-announcement-delete', kwargs={'object_id': 0}))
        self.assertEqual(response.status_code, 404)
        response = self.client.post(reverse('announcements-announcement-update', kwargs={'object_id': 0}))
        self.assertEqual(response.status_code, 404)