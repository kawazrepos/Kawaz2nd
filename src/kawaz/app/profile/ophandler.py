# vim: set fileencoding=utf8:
"""
Kawaz Profile Object Permission Handler

CLASS:
    Skill - A skill
    ProfileManager - A profile manager
    Profile - A profile
    Service - A service


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
from observer import watch
from object_permission import site
from object_permission.handlers import ObjectPermHandlerBase

from models import Profile

class ProfileObjectPermHandler(ObjectPermHandlerBase):
    def created(self):
        # Watch pub_state
        self._pub_state_watcher = \
                watch(self.obj, 'pub_state', self._pub_state_updated)
        self.updated()
    def updated(self):
        # Profile owner has manager permission
        self.mediator.manager(self.obj.user)
        # Authenticated user can view
        self.mediator.viewer(None)
        # Anonymous user is depend on pub_state
        if self.obj.pub_state == 'public':
            self.mediator.viewer('anonymous')
        else:
            self.mediator.reject('anonymous')
    def deleted(self):
        self._pub_state_watcher.unwatch()

    def _pub_state_updated(self, sender, obj, attr):
        self.updated()
site.register(Profile, ProfileObjectPermHandler)
