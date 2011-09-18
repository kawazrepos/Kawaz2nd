# -*- coding: utf-8 -*-
#
# Author:          miio
# Date:            2011/02/23
# Mail:            info@miio.info
#
from django.test import TestCase
from django.core.urlresolvers import reverse

from libwaz.test.userset import UserSet
from ..models import Component,Version,Product,Report
from django.contrib.auth.models import Group
import datetime
import hashlib
from time import time

class ProductViewTest(TestCase):
    def setUp(self):
        self.userset = UserSet()
        self.james = UserSet.create_user('james')
        self.emily = UserSet.create_user('emily')
        self.peter = UserSet.create_user('peter')
        self.alice = UserSet.create_user('alice')
        self.assertTrue(1)
        self.dproduct = self.new_product()
        
    def new_product(self):
        self.product_name = 'label'+hashlib.sha384(str(time())).hexdigest()
        return Product.objects.create(
            label=self.product_name,
            body='body'+self.product_name,
            rules='rules'+self.product_name,
            group=Group.objects.create(name='children'+self.product_name),
        )
    def new_component(self,product):
        self.component_name='dummy_coponent'+hashlib.sha384(str(time())).hexdigest()
        return Component.objects.create(
            label=self.component_name,
            product=product
        )
    def new_version(self,product):
        self.version_name = 'dummy_version'+hashlib.sha384(str(time())).hexdigest()
        return Version.objects.create(
            label=self.version_name,
            product=product
        )
        
#ProductTest
#主にレスポンスを確認      
    def test_get_product_list(self):
        u'''
        プロダクト一覧を取得
        '''
        response = self.client.get(reverse('bugwaz-product-list'))
        self.assertEqual(response.status_code, 200)
        
    def test_get_product_detail(self):
        u'''
        プロダクト詳細を取得
        '''
        response = self.client.get(reverse('bugwaz-product-detail', kwargs = {'object_id': self.dproduct.id}))
        self.assertEqual(response.status_code, 200)
        
    def test_get_not_found_product_detail(self):
        u'''
        存在しないプロダクトの時は404エラー
        '''
        response = self.client.get(reverse('bugwaz-product-detail', kwargs = {'object_id': 0}))
        self.assertEqual(response.status_code, 404)
        
       
# ComponentTest
# 主にレスポンスを確認
    def test_get_component_list(self):
        u'''
        プロダクトキーからコンポーネント一覧を取得する。
        '''
        product = self.new_product()
        component = self.new_component(product)
        response = self.client.get(reverse('bugwaz-component-list', kwargs = {'product': product.id}))
        self.assertEqual(response.status_code, 200) 
        
    def test_get_not_found_component_list(self):
        u'''
        存在しないプロダクトからコンポーネント一覧を取得しようとすると404エラー
        '''
        response = self.client.get(reverse('bugwaz-component-list', kwargs = {'product': 0}))
        self.assertEqual(response.status_code, 404)
        
    def test_get_component_detail(self):
        u'''
        コンポーネントの詳細を取得
        プロダクトIDとコンポーネントIDで取得
        '''
        product = self.new_product()
        component = self.new_component(product)
        response = self.client.get(reverse('bugwaz-component-detail', kwargs = {'product': product.id,'object_id': component.id}))
        self.assertEqual(response.status_code, 200) 
        
    def test_get_not_found_component_detail(self):
        u'''
        存在しないプロダクト・コンポーネントを取得しようとすると404エラー
        '''
        response = self.client.get(reverse('bugwaz-component-detail', kwargs = {'product': 0,'object_id': 0}))
        self.assertEqual(response.status_code, 404) 
        
        u'''
        プロダクトは存在するが、存在しないコンポーネントの詳細を取得しようとするとエラー
        '''
        product = self.new_product()
        response = self.client.get(reverse('bugwaz-component-detail', kwargs = {'product': product.id,'object_id': 0}))
        self.assertEqual(response.status_code, 404) 
        
        u'''
        コンポーネントは存在するが、間違ったプロダクトIDを指定すると404エラー
        '''
        component = self.new_component(product)
        response = self.client.get(reverse('bugwaz-component-detail', kwargs = {'product': 0,'object_id': component.id}))
        self.assertEqual(response.status_code, 404)   
             
# VersionTest
# 主にレスポンスを確認
    def test_get_version_list(self):
        u'''
        プロダクトキーからバージョン一覧を取得する。
        '''
        product = self.new_product()
        response = self.client.get(reverse('bugwaz-version-list', kwargs = {'product': product.id}))
        self.assertEqual(response.status_code, 200) 
    def test_get_not_found_version_list(self):
        response = self.client.get(reverse('bugwaz-version-list', kwargs = {'product': 0}))
        self.assertEqual(response.status_code, 404)
        
    def test_get_version_detail(self):
        u'''
        バージョンの詳細を取得
        プロダクトIDとバージョンIDで取得
        '''
        product = self.new_product()
        version = self.new_version(product)
        response = self.client.get(reverse('bugwaz-version-detail', kwargs = {'product': product.id,'object_id': version.id}))
        self.assertEqual(response.status_code, 200) 
        
    def test_get_not_found_version_detail(self):
        u'''
        存在しないプロダクトからバージョン一覧を取得しようとすると404エラー
        '''
        response = self.client.get(reverse('bugwaz-version-detail', kwargs = {'product': 0,'object_id': 0}))
        self.assertEqual(response.status_code, 404) 
        
        u'''
        プロダクトは存在するが、存在しないバージョンの詳細を取得しようとするとエラー
        '''
        product = self.new_product()
        response = self.client.get(reverse('bugwaz-version-detail', kwargs = {'product': product.id,'object_id': 0}))
        self.assertEqual(response.status_code, 404) 
        
        u'''
        バージョンは存在するが、間違ったプロダクトIDを指定すると404エラー
        '''
        version = self.new_version(product)
        response = self.client.get(reverse('bugwaz-version-detail', kwargs = {'product': 0,'object_id': version.id}))
        self.assertEqual(response.status_code, 404) 