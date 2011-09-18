# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/12
#
from django.test import TestCase
from django.db import IntegrityError
from ..models import Announcement

class AnnouncementModelTest(TestCase):
    
    def test_create_model(self):
        new_obj = Announcement.objects.create(
            title='title',
            body='body',
            sage=True,
        )
        self.assertTrue(Announcement.objects.filter(title='title').exists())
        found_obj = Announcement.objects.get(title='title')
        self.assertEqual(new_obj, found_obj)
    
    def test_create_invalid_model(self):
        self.assertRaises(IntegrityError, Announcement.objects.create, 
            title=None,
            body='body',
            sage=True,
        )
        self.assertRaises(IntegrityError, Announcement.objects.create,
            pk = 1,
            title='title',
            body='body',
            sage=True,
        )
    
    def test_update_model(self):
        Announcement.objects.create(
            title='title',
            body='body',
            sage=True,
        )
        found_obj = Announcement.objects.get(title='title')
        found_obj.title = 'AAAAA'
        found_obj.body = 'BBBBB'
        found_obj.sage = False
        found_obj.save()
        self.assertTrue(Announcement.objects.filter(title='AAAAA').exists())
        found_obj2 = Announcement.objects.get(title='AAAAA')
        self.assertEqual(found_obj, found_obj2)
    
    def test_update_invalid_model(self):
        Announcement.objects.create(
            title='title',
            body='body',
            sage=True,
        )
        found_obj = Announcement.objects.get(title='title')
        found_obj.title = None
        self.assertRaises(IntegrityError, found_obj.save)
        
    def test_delete_model(self):
        Announcement.objects.create(
            title='title',
            body='body',
            sage=True,
        )
        found_obj = Announcement.objects.get(title='title')
        found_obj.delete()
        self.assertTrue(not Announcement.objects.filter(title='title').exists())