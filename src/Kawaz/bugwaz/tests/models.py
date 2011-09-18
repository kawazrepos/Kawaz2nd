# -*- coding: utf-8 -*-
#
# Author:          miio
# Date:            2011/02/19
# Mail:            info@miio.info
#
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User,Group

from ..models import Component,Version,Product,Report

import datetime
import hashlib
from time import time


class EntryModelTest(TestCase):
    def setUp(self):
        self.james = User.objects.create_user('james', 'james@test.com', 'james')
        self.emily = User.objects.create_user('emily', 'emily@test.com', 'emily')
    
    def new_product(self):
        self.product_name = 'label'+hashlib.sha384(str(time())).hexdigest()
        return Product.objects.create(
            label=self.product_name,
            body='body'+self.product_name,
            rules='rules'+self.product_name,
            group=Group.objects.create(name='children'+self.product_name),
        )  
    def test_create_products(self):
        u'''
        プロダクトが正常に作れるか検証
        '''
        obj=self.new_product()
        found_obj = Product.objects.get(label=self.product_name)
        self.assertEqual(obj, found_obj)

    def test_delete_products(self):
        u'''
        プロダクトを正常に削除できるか検証
        '''
        obj = self.new_product()
        obj.delete()
        self.assertFalse(Product.objects.filter(label='label').exists())          
        
    def test_product_get_absolute_url(self):
        u'''
        プロダクトのURLを取得できるか検証（例：/bugwaz/1/）
        '''
        obj = self.new_product()
        self.assertEqual('/bugwaz/1/',obj.get_absolute_url())
        
    def test_product_get_report_bug_url(self):
        u'''
        プロダクトのURLを取得できるか検証（例：/bugwaz/1/reports/create/）
        '''
        obj = self.new_product()
        self.assertEqual('/bugwaz/1/reports/create/',obj.get_report_bug_url())
        
    def new_component(self):
        self.component_name='dummy_coponent'+hashlib.sha384(str(time())).hexdigest()
        return Component.objects.create(
            label=self.component_name,
            product=self.new_product()
        )
        
    def test_create_component(self):
        u'''
        プロダクトのコンポーネントを生成できるか検証
        '''
        obj = self.new_component()
        found_obj= Component.objects.get(label=self.component_name)
        self.assertEqual(obj, found_obj)
        
    def test_component_get_absolute_url(self):
        u'''
        プロダクトのコンポーネントのURLを取得できるか検証（例：/bugwaz/1/components/1/）
        '''
        obj = self.new_component()
        self.assertEqual('/bugwaz/1/components/1/',obj.get_absolute_url())
        
    def test_delete_component(self):
        u'''
        プロダクトのコンポーネントを正常に削除できるか検証
        '''
        obj = self.new_component()
        obj.delete()
        self.assertFalse(Component.objects.filter(label='dummy_component').exists()) 
         
    def new_version(self):
        self.version_name = 'dummy_version'+hashlib.sha384(str(time())).hexdigest()
        return Version.objects.create(
            label=self.version_name,
            product=self.new_product()
        )
        
    def test_create_version(self):
        u'''
        プロダクトのバージョンを生成できるか検証
        '''
        obj = self.new_version()
        found_obj= Version.objects.get(label=self.version_name)
        self.assertEqual(obj, found_obj)

    def test_delete_version(self):
        u'''
        プロダクトのバージョンを正常に削除できるか検証
        '''
        obj = self.new_version()
        obj.delete()
        self.assertFalse(Component.objects.filter(label=self.version_name).exists())

    def test_component_get_version_url(self):
        u'''
        プロダクトのバージョンのURLを取得できるか検証（例：/bugwaz/1/versions/1/）
        '''
        obj = self.new_version()
        self.assertEqual('/bugwaz/1/versions/1/',obj.get_absolute_url())
        
    def new_report(self,product):
        self.report_name = 'label'+hashlib.sha384(str(time())).hexdigest()
        return Report.objects.create(
                product = product,
                label=self.report_name,
                body='body'+self.report_name,
                author=self.emily,
            )
        
    def test_report_create(self):
        u'''
        レポートの生成チェック
        '''
        obj = self.new_report(self.new_product())
        found_obj=Report.objects.get(label=self.report_name)
        self.assertEqual(obj,found_obj)
        
    def test_report_get_absolute_url(self):
        u'''
        プロダクトに対するレポートのURLを取得できるか検証（例：/bugwaz/1/reports/1/）
        '''
        prod = self.new_product()
        obj = self.new_report(prod)
        self.assertEqual('/bugwaz/1/reports/1/',obj.get_absolute_url())
        u'''
        更に同一のプロダクトで新しいレポートを生成すると、/bugwaz/1/reports/2/になることを検証
        '''
        obj = self.new_report(prod)
        self.assertEqual('/bugwaz/1/reports/2/',obj.get_absolute_url())
        u'''
        レポートの削除してからレポートを作っても消した分は穴抜きとなり、詰まることはない
        /bugwaz/1/reports/2/ の状態で削除した次に追加すると /bugwaz/1/reports/3/になる。
        '''
        obj = self.new_report(prod)
        Report.objects.get(label=self.report_name).delete()
        obj = self.new_report(prod)
        self.assertEqual('/bugwaz/1/reports/3/',obj.get_absolute_url())
        
    def test_report_many_get_absolute_url(self):
        u'''
        レポートを生成した後、更に同一のプロダクトで新しいレポートを生成すると、/bugwaz/1/reports/2/になることを検証
        '''
        prod = self.new_product()
        obj = self.new_report(prod)
        self.assertEqual('/bugwaz/1/reports/1/',obj.get_absolute_url())
        obj = self.new_report(prod)
        self.assertEqual('/bugwaz/1/reports/2/',obj.get_absolute_url())

    def test_report_delete_get_absolute_url(self):
        u'''
        レポートを正しく削除できることを検証
        '''
        prod = self.new_product()
        obj = self.new_report(prod)
        Report.objects.get(label=self.report_name).delete()
        self.assertFalse(Report.objects.filter(label=self.report_name).exists())
        
    def test_report_recreate_get_absolute_url(self):
        prod = self.new_product()
        u'''
        直前のレポートを削除してから生成すると、レポートIDは変わらない。
        /bugwaz/1/reports/1/の状態で削除して次に追加すると/bugwaz/1/reports/1/になる
        '''       
        obj = self.new_report(prod)
        self.assertEqual('/bugwaz/1/reports/1/',obj.get_absolute_url())
        Report.objects.get(label=self.report_name).delete()
        obj = self.new_report(prod)
        self.assertEqual('/bugwaz/1/reports/1/',obj.get_absolute_url())
              
        u'''
        直前以外のレポートの削除してからレポートを作っても消した分は穴抜きとなり、詰まることはない
        /bugwaz/1/reports/4/ の状態で/bugwaz/1/reports/2/を削除した次に追加すると /bugwaz/1/reports/5/になる。
        '''
        obj = self.new_report(prod)
        obj = self.new_report(prod)
        sec_name = self.report_name
        obj = self.new_report(prod)
        obj = self.new_report(prod)
        Report.objects.get(label=sec_name).delete()
        Report.objects.get(label=self.report_name).delete()

        obj = self.new_report(prod)
        self.assertEqual('/bugwaz/1/reports/5/',obj.get_absolute_url())

    def test_checkreport(self):
        u'''
        仕様化テスト　残骸
        '''
        obj = self.new_report(self.new_product())  
        obj.join(self.emily)
        print(Report.objects.get(label=self.report_name).charges)
        
    def test_join_report(self):
        u'''
        レポートの担当として加入
        '''
        obj = self.new_report(self.new_product())
        obj.join(self.emily)
        
    def test_join_self_report(self):
        u'''
        自身のレポートに担当として加入
        '''
        obj = self.new_report(self.new_product())
        obj.join(self.james)
        
    def test_quit_no_join_report(self):
        u'''
        非担当のレポートから担当を外れる
        '''
        obj = self.new_report(self.new_product())
        obj.quit(self.james)
        
    def test_quit_join_report(self):
        u'''
        担当中のレポートから担当を外れる
        '''
        obj = self.new_report(self.new_product())
        obj.join(self.james)
        obj.quit(self.james)
        
    def test_quit_self_joined_report(self):
        u'''
        自身の担当中のレポートから担当を外れる
        '''
        obj = self.new_report(self.new_product())
        obj.join(self.emily)
        obj.quit(self.emily)
    
#
# 未テスト項目
# Reportのsave(libwaz側からのModelらしく、リクエストが扱えるModelぽそう？)
# 全Modelsのmodify_object_permission(アクセス権限らしい)
# 各種限界値分解(主に文字列制限があるところに対して)
# Report担当が正しく登録されているかの確認
# 