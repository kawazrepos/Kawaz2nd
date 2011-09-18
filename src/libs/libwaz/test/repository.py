# -*- coding: utf-8 -*-
'''
Created on 2011/05/07

@author: miio
'''

import os
import pysvn

class SvnTestRepository(object):
       
    def __init__(self):
        self.created_path = []
        self.client       = pysvn.Client()
        
    def set_repository_base_path(self,path):
        self.base_path = path
        
    def create_master(self,name):
        u'''
            Create svn master repository.
            Return create master repository directory path.
        '''
        repository_master_path = os.path.join(self.base_path,name)
        os.system("svnadmin create " + repository_master_path)
        self.created_path.append(repository_master_path)
        return repository_master_path
        
    def create_checkout(self,master_name,target_name):
        u'''
            Checkout svn repository from master repository.
            Return checkout repository directory path.
         '''
        repository_master_path = os.path.join(self.base_path,master_name)
        repository_path        = os.path.join(self.base_path,target_name)
        os.system("mkdir " + repository_path)
        self.client.checkout(url = "file://" + repository_master_path, path = repository_path)
        self.created_path.append(repository_path)
        return repository_path
        
    def touch_and_commit_file(self,file_path,commit_message):
        u'''
            Touch file and commit.
         '''
        os.system("touch " + file_path)
        self.client.add(file_path)
        self.client.checkin([file_path], commit_message)
        
    def delete(self):
        u'''
            Delete all from created master repository and created checkout repository and directories.
         '''
        for result in self.created_path:
            os.system("rm -r " + result)
