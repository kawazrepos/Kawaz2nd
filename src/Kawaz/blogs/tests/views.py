# -*- coding: utf-8 -*-
#
# Created:        2010/11/16
# Author:        alisue
#
from django.test import TestCase
from django.core.urlresolvers import reverse

from libwaz.test.userset import UserSet
from ..models import Entry

import datetime

class EntryViewTest(TestCase):
    def setUp(self):
        self.userset = UserSet()
        self.james = UserSet.create_user('james')
        self.emily = UserSet.create_user('emily')
        self.peter = UserSet.create_user('peter')
        self.alice = UserSet.create_user('alice')
        for i in xrange(1, 100):
            Entry.objects.create(
                pub_state='public',
                title='title%s'%i,
                body='body%s'%i,
                author=self.james,
                publish_at=datetime.datetime.now(),
                publish_at_date=datetime.date.today(),
            )
        for i in xrange(1, 100):
            Entry.objects.create(
                pub_state='protected',
                title='title%s'%i,
                body='body%s'%i,
                author=self.emily,
                publish_at=datetime.datetime.now(),
                publish_at_date=datetime.date.today(),
            )
        for i in xrange(1, 100):
            Entry.objects.create(
                pub_state='private',
                title='title%s'%i,
                body='body%s'%i,
                author=self.peter,
                publish_at=datetime.datetime.now(),
                publish_at_date=datetime.date.today(),
            )
        for i in xrange(1, 100):
            Entry.objects.create(
                pub_state='draft',
                title='title%s'%i,
                body='body%s'%i,
                author=self.alice,
                publish_at=datetime.datetime.now(),
                publish_at_date=datetime.date.today(),
            )
    def test_list_view(self):
        response = self.client.get(reverse('blogs-entry-list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('blogs-entry-list', kwargs={'author': self.james.username}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('blogs-entry-list', kwargs={'author': self.emily.username}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('blogs-entry-list', kwargs={'author': self.peter.username}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('blogs-entry-list', kwargs={'author': self.alice.username}))
        self.assertEqual(response.status_code, 200)
    def test_draft_list_view(self):
        # 外部ユーザーは閲覧不可
        response = self.client.get(reverse('blogs-entry-draft-list', kwargs={'author': self.james.username}))
        self.assertRedirects(response, "%s?next=%s"%(reverse('auth_login'), reverse('blogs-entry-draft-list', kwargs={'author': self.james.username})))
        self.userset.login(self.client, self.james)
        response = self.client.get(reverse('blogs-entry-draft-list', kwargs={'author': self.james.username}))
        self.assertEqual(response.status_code, 200)
    
    def test_archive_year_view(self):
        kwargs = {
            'year': 2010,
        }
        response = self.client.get(reverse('blogs-entry-archive-year', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('blogs-entry-archive-year', kwargs=dict(kwargs, author=self.james.username)))
        self.assertEqual(response.status_code, 200)
    
    def test_archive_month_view(self):
        kwargs = {
            'year': 2010,
            'month': 1,
        }
        response = self.client.get(reverse('blogs-entry-archive-month', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('blogs-entry-archive-month', kwargs=dict(kwargs, author=self.james.username)))
        self.assertEqual(response.status_code, 200)
    def test_archive_day_view(self):
        kwargs = {
            'year': 2010,
            'month': 1,
            'day': 1,
        }
        response = self.client.get(reverse('blogs-entry-archive-day', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('blogs-entry-archive-day', kwargs=dict(kwargs, author=self.james.username)))
        self.assertEqual(response.status_code, 200)
    def test_archive_today_view(self):
        response = self.client.get(reverse('blogs-entry-archive-today'))
        self.assertEqual(response.status_code, 200)
        kwargs = {
            'author': self.james.username,
        }
        response = self.client.get(reverse('blogs-entry-archive-today', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
    def test_detail_view(self):
        kwargs = {
            'year': datetime.date.today().strftime('%Y'),
            'month': datetime.date.today().strftime('%m'),
            'day': datetime.date.today().strftime('%d'),
            'slug': 'title1',
        }
        # Jamesの日記は外部ユーザーでも閲覧可能
        response = self.client.get(reverse('blogs-entry-detail', kwargs=dict(kwargs, author=self.james.username)))
        self.assertEqual(response.status_code, 200)
        # Emilyの日記は内部ユーザー専用
        response = self.client.get(reverse('blogs-entry-detail', kwargs=dict(kwargs, author=self.emily.username)))
        self.assertRedirects(response, "%s?next=%s"%(reverse('auth_login'), reverse('blogs-entry-detail', kwargs=dict(kwargs, author=self.emily.username))))
        self.userset.login(self.client, self.emily)
        response = self.client.get(reverse('blogs-entry-detail', kwargs=dict(kwargs, author=self.emily.username)))
        self.assertEqual(response.status_code, 200)
        # Peterの日記は彼専用
        response = self.client.get(reverse('blogs-entry-detail', kwargs=dict(kwargs, author=self.peter.username)))
        self.assertEqual(response.status_code, 403)
        self.userset.login(self.client, self.peter)
        response = self.client.get(reverse('blogs-entry-detail', kwargs=dict(kwargs, author=self.peter.username)))
        self.assertEqual(response.status_code, 200)
        # Aliceの日記は書きかけなので blogs-entry-detail では NotFound
        response = self.client.get(reverse('blogs-entry-detail', kwargs=dict(kwargs, author=self.alice.username)))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('blogs-entry-draft-detail', kwargs={'author': self.alice.username, 'object_id': self.alice.blog_entries.all()[0].pk}))
        self.assertEqual(response.status_code, 403)
        self.userset.login(self.client, self.alice)
        response = self.client.get(reverse('blogs-entry-draft-detail', kwargs={'author': self.alice.username, 'object_id': self.alice.blog_entries.all()[0].pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_draft_detail_view(self):
        # 外部ユーザーは閲覧不可
        response = self.client.get(reverse('blogs-entry-draft-detail', kwargs={'author': self.alice.username, 'object_id': self.alice.blog_entries.all()[0].pk}))
        self.assertRedirects(response, "%s?next=%s"%(reverse('auth_login'), reverse('blogs-entry-draft-detail', kwargs={'author': self.alice.username, 'object_id': self.alice.blog_entries.all()[0].pk})))
        self.userset.login(self.client, self.alice)
        response = self.client.get(reverse('blogs-entry-draft-detail', kwargs={'author': self.alice.username, 'object_id': self.alice.blog_entries.all()[0].pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_create_view(self):
        kwargs = {'author': self.james}
        data = {'pub_state': 'public', 'title': 'Hello', 'body': 'world'}
        data2 = {'pub_state': 'public', 'title': 'Hello2', 'body': 'world2'}
        # 外部ユーザーはアクセス不可
        response = self.client.get(reverse('blogs-entry-create', kwargs=kwargs))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('blogs-entry-create', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 302)
        # Emilyはアクセス不可能
        self.assertEqual(self.userset.login(self.client, self.emily), True)
        response = self.client.get(reverse('blogs-entry-create', kwargs=kwargs))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('blogs-entry-create', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 403)
        # Jamesはアクセス可能
        self.assertEqual(self.userset.login(self.client, self.james), True)
        response = self.client.get(reverse('blogs-entry-create', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('blogs-entry-create', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.filter(title='Hello').exists(), True)
        # スタッフユーザーはアクセス不可能
        self.assertEqual(self.userset.login_staff(self.client), True)
        response = self.client.get(reverse('blogs-entry-create', kwargs=kwargs))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('blogs-entry-create', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 403)
        # スーパーユーザーはアクセス可能
        self.assertEqual(self.userset.login_admin(self.client), True)
        response = self.client.get(reverse('blogs-entry-create', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('blogs-entry-create', kwargs=kwargs), data2)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.filter(title='Hello2').exists(), True)

    def test_update_view(self):
        kwargs = {
            'author': self.james.username,
            'object_id': 1,
        }
        data = {'pub_state': 'public', 'title': 'Hello', 'body': 'world'}
        # 外部ユーザーはアクセス不可
        response = self.client.get(reverse('blogs-entry-update', kwargs=kwargs))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('blogs-entry-update', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 302)
        # Emilyはアクセス不可能
        self.assertEqual(self.userset.login(self.client, self.emily), True)
        response = self.client.get(reverse('blogs-entry-update', kwargs=kwargs))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('blogs-entry-update', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 403)
        # Jamesはアクセス可能
        self.assertEqual(self.userset.login(self.client, self.james), True)
        response = self.client.get(reverse('blogs-entry-update', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('blogs-entry-update', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.filter(title='Hello', pk=1).exists(), True)
        # スタッフユーザーはアクセス不可能
        self.assertEqual(self.userset.login_staff(self.client), True)
        response = self.client.get(reverse('blogs-entry-update', kwargs=kwargs))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('blogs-entry-update', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 403)
        # スーパーユーザーはアクセス可能
        self.assertEqual(self.userset.login_admin(self.client), True)
        response = self.client.get(reverse('blogs-entry-update', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('blogs-entry-update', kwargs=kwargs), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.filter(title='Hello', pk=1).exists(), True)
        
    def test_delete_view(self):
        kwargs = {
            'author': self.james.username,
            'object_id': 1,
        }
        kwargs2 = {
            'author': self.james.username,
            'object_id': 2,
        }
        # 外部ユーザーはアクセス不可
        response = self.client.get(reverse('blogs-entry-delete', kwargs=kwargs))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('blogs-entry-delete', kwargs=kwargs))
        self.assertEqual(response.status_code, 302)
        # Emilyはアクセス不可能
        self.assertEqual(self.userset.login(self.client, self.emily), True)
        response = self.client.get(reverse('blogs-entry-delete', kwargs=kwargs))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('blogs-entry-delete', kwargs=kwargs))
        self.assertEqual(response.status_code, 403)
        # Jamesはアクセス可能
        self.assertEqual(self.userset.login(self.client, self.james), True)
        response = self.client.get(reverse('blogs-entry-delete', kwargs=kwargs))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('blogs-entry-delete', kwargs=kwargs))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.filter(pk=1).exists(), False)
        # スタッフユーザーはアクセス不可能
        self.assertEqual(self.userset.login_staff(self.client), True)
        response = self.client.get(reverse('blogs-entry-delete', kwargs=kwargs2))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('blogs-entry-delete', kwargs=kwargs2))
        self.assertEqual(response.status_code, 403)
        # スーパーユーザーはアクセス可能
        self.assertEqual(self.userset.login_admin(self.client), True)
        response = self.client.get(reverse('blogs-entry-delete', kwargs=kwargs2))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('blogs-entry-delete', kwargs=kwargs2))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.filter(pk=2).exists(), False)