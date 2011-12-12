# -*- coding: utf-8 -*-
#
# src/Kommonz/thumbnailfield/models.py
# created by giginet on 2011/11/06
#
import os, shutil
from django.db.models.fields.files import ImageField
from django.db.models import signals
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from widgets import DelAdminFileWidget
from forms import ThumbnailFormField
from exceptions import DuplicatePatterNameException
from utils import get_thumbnail_filename, create_thumbnail, convert_patterns_dict

class ThumbnailField(ImageField):
    def __init__(self, *args, **kwargs):
        thumbnail_size_patterns = kwargs.pop('thumbnail_size_patterns', ())
        self.thumbnail_size_patterns = convert_patterns_dict(thumbnail_size_patterns)
        super(ThumbnailField, self).__init__(*args, **kwargs) 

    def _rename_resize_image(self, sender, instance, created, **kwargs):
        '''
        Renames the image, and calls methods to resize and create the thumbnail
        '''
        if getattr(instance, self.name):
            filename = getattr(instance, self.name).path
            ext = os.path.splitext(filename)[1].lower().replace('jpg', 'jpeg')
            dst = self.generate_filename(instance, '%s_%s%s' % (self.name, instance._get_pk_val(), ext))
            dst_fullpath = os.path.join(settings.MEDIA_ROOT, dst)
            if created or os.path.abspath(filename) != os.path.abspath(dst_fullpath):
                if 'fixtures' in filename:
                    if not os.path.exists(os.path.dirname(dst_fullpath)):
                        os.makedirs(os.path.dirname(dst_fullpath))
                        shutil.copyfile(filename, dst_fullpath)
                elif os.path.exists(filename):
                    os.rename(filename, dst_fullpath)
                create_thumbnail(dst_fullpath, dst_fullpath, self.thumbnail_size_patterns)
                setattr(instance, self.attname, dst)
                instance.save()

    def _set_thumbnails(self, instance=None, **kwargs):
        '''
        Creates a "thumbnail" object as attribute of the ImageField instance
        Thumbnail attribute will be of the same class of original image, so
        "path", "url"... properties can be used
        '''
        if getattr(instance, self.name):
            filename = self.generate_filename(instance, os.path.basename(getattr(instance, self.name).path))
            for pattern_name, pattern_size in self.thumbnail_size_patterns.iteritems():
                if hasattr(getattr(instance, self.name), pattern_name):
                    raise DuplicatePatterNameException(pattern_name)
                thumbnail_filename = get_thumbnail_filename(filename, pattern_name)
                thumbnail_type = self.attr_class(instance, self, thumbnail_filename)
                setattr(getattr(instance, self.name), pattern_name, thumbnail_type)

    def formfield(self, **kwargs):
        '''
        Specify form field and widget to be used on the forms
        '''
        kwargs['widget'] = DelAdminFileWidget
        kwargs['form_class'] = ThumbnailFormField
        return super(ImageField, self).formfield(**kwargs)

    def save_form_data(self, instance, data):
        '''
            Overwrite save_form_data to delete images if "delete" checkbox
            is selected
        '''
        if data == '__deleted__':
            filename = getattr(instance, self.name).path
            if os.path.exists(filename):
                os.remove(filename)
            for pattern_name in self.pattern_names:
                thumbnail_filename = get_thumbnail_filename(filename, pattern_name)
                if os.path.exists(thumbnail_filename):
                        os.remove(thumbnail_filename)
            setattr(instance, self.name, None)
        else:
            super(ImageField, self).save_form_data(instance, data)

    def get_db_prep_save(self, value):
        '''
            Overwrite get_db_prep_save to allow saving nothing to the database
            if image has been deleted
        '''
        if value:
            return super(ImageField, self).get_db_prep_save(value)
        else:
            return u''

    def contribute_to_class(self, cls, name):
        '''
        Call methods for generating all operations on specified signals
        '''
        super(ImageField, self).contribute_to_class(cls, name)
        signals.post_save.connect(self._rename_resize_image, sender=cls)
        signals.post_init.connect(self._set_thumbnails, sender=cls)

