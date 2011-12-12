# -*- coding: utf-8 -*-
#
# src/Kommonz/fields/thumbnailfield/exceptions.py
# created by giginet on 2011/11/12
#
class DuplicatePatterNameException(Exception):
    def __init__(self, pattern_name):
        self.pattern_name = pattern_name
    
    def __str__(self):
        return 'Pattern name "%s" have been already defined.' % self.pattern_name

