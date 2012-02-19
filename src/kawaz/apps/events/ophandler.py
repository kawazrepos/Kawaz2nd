# vim: set fileencoding=utf8:
"""
Kawaz Event Object Permission Handler

CLASS:
    EventObjectPermHandler - Object Permission Handler class of Event


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
__VERSION__ = "0.1.0"
from object_permission import site
from object_permission.handlers import ObjectPermHandler

from kawaz.core import get_children_group

from models import Event

class EventObjectPermHandler(ObjectPermHandler):
    """Object permission handler of Kawaz Event"""

    def get_author(self):
        """get author of profile instance"""
        return getattr(self.instance, 'author')
    def get_pub_state(self):
        """get pub_state of profile instance"""
        return getattr(self.instance, 'pub_state')

    def setup(self):
        """setup function"""
        self.watch('author')
        self.watch('pub_state')

    def updated(self, attr):
        children = get_children_group()
        # Profile owner has manager permission
        self.manager(self.get_author())
        # Depend on pub_state
        if self.get_pub_state() == 'public':
            # Everyone can view
            self.viewer(children)
            self.viewer(None)
            self.viewer('anonymous')
        elif self.get_pub_state() == 'protected':
            # Children can view
            self.viewer(children)
            self.reject(None)
            self.reject('anonymous')
        else:
            # No one can view
            self.reject(children)
            self.reject(None)
            self.reject('anonymous')
site.register(Event, EventObjectPermHandler)
