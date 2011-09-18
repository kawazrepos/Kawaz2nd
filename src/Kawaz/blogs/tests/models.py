# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/26
#
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User

from ..models import Category, Entry

import datetime

class EntryModelTest(TestCase):
    def setUp(self):
        self.james = User.objects.create_user('james', 'james@test.com', 'james')
        self.emily = User.objects.create_user('emily', 'emily@test.com', 'emily')
    def test_create_model(self):
        new_category = Category.objects.create(
            label='category',
        )
        new_obj = Entry.objects.create(
            pub_state='public',
            title='title',
            body='body',
            category=new_category,
            author=self.james,
            publish_at=datetime.datetime.now(),
            publish_at_date=datetime.date.today(),
        )
        self.assertTrue(Entry.objects.filter(title='title').exists())
        found_obj = Entry.objects.get(title='title')
        self.assertEqual(new_obj, found_obj)
    def test_create_invalid_model(self):
        self.assertRaises(IntegrityError, Entry.objects.create, 
            pub_state='public',
            title=None,
            body='body',
            author=self.james,
            publish_at=datetime.datetime.now(),
            publish_at_date=datetime.date.today(),
        )
        Entry.objects.create(
            pub_state='public',
            title='title',
            body='body',
            publish_at=datetime.datetime(2000, 1, 1, 0, 0, 0),
            publish_at_date=datetime.datetime(2000, 1, 1),
            author=self.james,
        )
        # 日付,著者が同じためエラーが発生する
        self.assertRaises(IntegrityError, Entry.objects.create, 
            pub_state='public',
            title='title',
            body='body',
            publish_at=datetime.datetime(2000, 1, 1, 0, 0, 0),
            publish_at_date=datetime.datetime(2000, 1, 1),
            author=self.james,
        )
        # 日付が違うためエラーが発生しない
        Entry.objects.create(
            pub_state='public',
            title='title',
            body='body',
            publish_at=datetime.datetime(2000, 1, 2, 0, 0, 0),
            publish_at_date=datetime.datetime(2000, 1, 2),
            author=self.james,
        )
        # 著者が違うためエラーが発生しない
        Entry.objects.create(
            pub_state='public',
            title='title',
            body='body',
            publish_at=datetime.datetime(2000, 1, 1, 0, 0, 0),
            publish_at_date=datetime.datetime(2000, 1, 1),
            author=self.emily,
        )
    def test_update_model(self):
        new_category = Category.objects.create(
            label='category',
        )
        new_category2 = Category.objects.create(
            label='category2',
        )
        Entry.objects.create(
            pub_state='public',
            title='title',
            body='body',
            category=new_category,
            author=self.james,
            publish_at=datetime.datetime.now(),
            publish_at_date=datetime.date.today(),
        )
        found_obj = Entry.objects.get(title='title')
        found_obj.title = 'title2'
        found_obj.body = 'body2'
        found_obj.category = new_category2
        found_obj.save()
        found_obj2 = Entry.objects.get(title='title2')
        self.assertEqual(found_obj2.body.raw, 'body2')
        self.assertEqual(found_obj2.category, new_category2)
    
    def test_invalid_update_model(self):
        new_category = Category.objects.create(
            label='category',
        )
        Entry.objects.create(
            pub_state='public',
            title='title',
            body='body',
            category=new_category,
            author=self.james,
            publish_at=datetime.datetime.now(),
            publish_at_date=datetime.date.today(),
        )
        found_obj = Entry.objects.get(title='title')
        found_obj.title = None
        found_obj.body = 'body2'
        self.assertRaises(IntegrityError, found_obj.save)
        
    def test_delete_model(self):
        Entry.objects.create(
            pub_state='public',
            title='title',
            body='body',
            author=self.james,
            publish_at=datetime.datetime.now(),
            publish_at_date=datetime.date.today(),
        )
        found_obj = Entry.objects.get(title='title')
        found_obj.delete()
        self.assertTrue(not Entry.objects.filter(title='title').exists())