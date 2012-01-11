# vim: set fileencoding=utf8:
"""
Kawaz Profile Object Permission Handler

CLASS:
    ProfileObjectPermHandler - Object Permission Handler class of Profile


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

from models import Profile

class ProfileObjectPermHandler(ObjectPermHandler):
    """Object permission handler of Kawaz Profile"""

    def get_user(self):
        """get user of profile instance"""
        return getattr(self.instance, 'user')
    def get_pub_state(self):
        """get pub_state of profile instance"""
        return getattr(self.instance, 'pub_state')

    def setup(self):
        """setup function"""
        self.watch('pub_state')

    def updated(self, attr):
        # Profile owner has manager permission
        self.manager(self.get_user())
        # Authenticated user can view
        self.viewer(None)
        # Anonymous user is depend on pub_state
        if self.get_pub_state() == 'public':
            self.viewer('anonymous')
        else:
            self.reject('anonymous')
site.register(Profile, ProfileObjectPermHandler)
