import datetime

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sites.models import Site
from django.core import mail
from django.core.exceptions import ImproperlyConfigured
from django.core.handlers.wsgi import WSGIRequest
from django.test import Client
from django.test import TestCase

from registration import signals
from registration.backends import get_backend

from registration2 import forms
from registration2.admin import RegistrationAdmin
from registration2.backends.default import DefaultBackend
from registration2.models import RegistrationProfile

class _MockRequestClient(Client):
    """
    A ``django.test.Client`` subclass which can return mock
    ``HttpRequest`` objects.
    
    """
    def request(self, **request):
        """
        Rather than issuing a request and returning the response, this
        simply constructs an ``HttpRequest`` object and returns it.
        
        """
        environ = {
            'HTTP_COOKIE': self.cookies,
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'REMOTE_ADDR': '127.0.0.1',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': '80',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1,0),
            'wsgi.url_scheme': 'http',
            'wsgi.errors': self.errors,
            'wsgi.multiprocess':True,
            'wsgi.multithread': False,
            'wsgi.run_once': False,
            'wsgi.input': None,
            }
        environ.update(self.defaults)
        environ.update(request)
        request = WSGIRequest(environ)

        # We have to manually add a session since we'll be bypassing
        # the middleware chain.
        session_middleware = SessionMiddleware()
        session_middleware.process_request(request)
        return request


def _mock_request():
    """
    Construct and return a mock ``HttpRequest`` object; this is used
    in testing backend methods which expect an ``HttpRequest`` but
    which are not being called from views.
    
    """
    return _MockRequestClient().request()


class DefaultRegistrationBackendTests(TestCase):
    """
    Test the default registration backend.

    Running these tests successfully will require two templates to be
    created for the sending of activation emails; details on these
    templates and their contexts may be found in the documentation for
    the default backend.

    """
    backend = DefaultBackend()
    
    def setUp(self):
        """
        Create an instance of the default backend for use in testing,
        and set ``ACCOUNT_ACTIVATION_DAYS`` if it's not set already.

        """
        self.old_activation = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', None)
        if self.old_activation is None:
            settings.ACCOUNT_ACTIVATION_DAYS = 7 # pragma: no cover

    def tearDown(self):
        """
        Yank out ``ACCOUNT_ACTIVATION_DAYS`` back out if it wasn't
        originally set.

        """
        if self.old_activation is None:
            settings.ACCOUNT_ACTIVATION_DAYS = self.old_activation # pragma: no cover

    def test_registration(self):
        """
        Test the registration process: registration creates a new
        inactive account and a new profile with activation key,
        populates the correct account data and sends an activation
        email.

        """
        new_user = self.backend.register(_mock_request(),
                                         username='bob',
                                         email='bob@example.com')

        # Details of the returned user must match what went in.
        self.assertEqual(new_user.username, 'bob')
        self.assertEqual(new_user.email, 'bob@example.com')

        # New user must not be active.
        self.failIf(new_user.is_active)

        # A registration profile was created, and an activation email
        # was sent.
        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_registration_no_sites(self):
        """
        Test that registration still functions properly when
        ``django.contrib.sites`` is not installed; the fallback will
        be a ``RequestSite`` instance.
        
        """
        Site._meta.installed = False
        new_user = self.backend.register(_mock_request(),
                                         username='bob',
                                         email='bob@example.com',
                                        )

        self.assertEqual(new_user.username, 'bob')
        self.assertEqual(new_user.email, 'bob@example.com')

        self.failIf(new_user.is_active)

        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        
        Site._meta.installed = True

    def test_valid_activation(self):
        """
        Test the activation process: activating within the permitted
        window sets the account's ``is_active`` field to ``True`` and
        resets the activation key.

        """
        valid_user = self.backend.register(_mock_request(),
                                           username='alice',
                                           email='alice@example.com',
                                           )

        valid_profile = RegistrationProfile.objects.get(user=valid_user)
        
        self.assertEqual(valid_profile.activation_key, RegistrationProfile.UNTREATED)
        
        # Accept
        self.backend.accept(_mock_request(), valid_profile)

        activated = self.backend.activate(_mock_request(),
                                          valid_profile.activation_key,
                                          password='swordfish')
        self.assertEqual(activated.username, valid_user.username)
        self.failUnless(activated.check_password('swordfish'))
        self.failUnless(activated.is_active)

        # Fetch the profile again to verify its activation key has
        # been reset.
        valid_profile = RegistrationProfile.objects.get(user=valid_user)
        self.assertEqual(valid_profile.activation_key,
                         RegistrationProfile.ACTIVATED)

    def test_valid_activation_untreated(self):
        """
        Test the activation process: activating within the permitted
        window sets the account's ``is_active`` field to ``True`` and
        resets the activation key.

        """
        valid_user = self.backend.register(_mock_request(),
                                           username='alice',
                                           email='alice@example.com',
                                           )

        invalid_profile = RegistrationProfile.objects.get(user=valid_user)
        self.assertEqual(invalid_profile.activation_key, RegistrationProfile.UNTREATED)
        
        self.failIf(self.backend.activate(_mock_request(),
                                          invalid_profile.activation_key,
                                          password='swordfish'))

    def test_valid_activation_rejected(self):
        """
        Test the activation process: activating within the permitted
        window sets the account's ``is_active`` field to ``True`` and
        resets the activation key.

        """
        valid_user = self.backend.register(_mock_request(),
                                           username='alice',
                                           email='alice@example.com',
                                           )

        invalid_profile = RegistrationProfile.objects.get(user=valid_user)
        self.assertEqual(invalid_profile.activation_key, RegistrationProfile.UNTREATED)
        
        self.backend.reject(_mock_request(), invalid_profile, reason='somehow')
        self.assertEqual(invalid_profile.activation_key, RegistrationProfile.REJECTED)

        self.failIf(self.backend.activate(_mock_request(),
                                          invalid_profile.activation_key,
                                          password='swordfish'))

    def test_invalid_activation_expired(self):
        """
        Test the activation process: trying to activate outside the
        permitted window fails, and leaves the account inactive.

        """
        expired_user = self.backend.register(_mock_request(),
                                             username='bob',
                                             email='bob@example.com',
                                             )
        # Accept
        expired_user.date_joined = expired_user.date_joined - datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        expired_user.save()
        expired_profile = RegistrationProfile.objects.get(user=expired_user)
        self.backend.accept(_mock_request(), expired_profile)
        self.failIf(self.backend.activate(_mock_request(),
                                          expired_profile.activation_key,
                                          password='secret'))
        self.failUnless(expired_profile.activation_key_expired())

    def test_allow(self):
        """
        Test that the setting ``REGISTRATION_OPEN`` appropriately
        controls whether registration is permitted.

        """
        old_allowed = getattr(settings, 'REGISTRATION_OPEN', True)
        settings.REGISTRATION_OPEN = True
        self.failUnless(self.backend.registration_allowed(_mock_request()))

        settings.REGISTRATION_OPEN = False
        self.failIf(self.backend.registration_allowed(_mock_request()))
        settings.REGISTRATION_OPEN = old_allowed

    def test_form_class(self):
        """
        Test that the default form class returned is
        ``registration.forms.RegistrationForm``.

        """
        self.failUnless(self.backend.get_form_class(_mock_request()) is forms.RegistrationForm)

    def test_post_registration_redirect(self):
        """
        Test that the default post-registration redirect is the named
        pattern ``registration_complete``.

        """
        self.assertEqual(self.backend.post_registration_redirect(_mock_request(), User()),
                         ('registration_complete', (), {}))

    def test_registration_signal(self):
        """
        Test that registering a user sends the ``user_registered``
        signal.
        
        """
        def receiver(sender, **kwargs):
            self.failUnless('user' in kwargs)
            self.assertEqual(kwargs['user'].username, 'bob')
            self.failUnless('request' in kwargs)
            self.failUnless(isinstance(kwargs['request'], WSGIRequest))
            received_signals.append(kwargs.get('signal'))

        received_signals = []
        signals.user_registered.connect(receiver, sender=self.backend.__class__)

        self.backend.register(_mock_request(),
                              username='bob',
                              email='bob@example.com',
                              )

        self.assertEqual(len(received_signals), 1)
        self.assertEqual(received_signals, [signals.user_registered])

    def test_activation_signal_success(self):
        """
        Test that successfully activating a user sends the
        ``user_activated`` signal.
        
        """
        def receiver(sender, **kwargs):
            self.failUnless('user' in kwargs)
            self.assertEqual(kwargs['user'].username, 'bob')
            self.failUnless('request' in kwargs)
            self.failUnless(isinstance(kwargs['request'], WSGIRequest))
            received_signals.append(kwargs.get('signal'))

        received_signals = []
        signals.user_activated.connect(receiver, sender=self.backend.__class__)

        new_user = self.backend.register(_mock_request(),
                                         username='bob',
                                         email='bob@example.com',
                                         )
        profile = RegistrationProfile.objects.get(user=new_user)
        self.backend.accept(_mock_request(), profile)
        self.backend.activate(_mock_request(), profile.activation_key, password='secret')

        self.assertEqual(len(received_signals), 1)
        self.assertEqual(received_signals, [signals.user_activated])

    def test_activation_signal_failure(self):
        """
        Test that an unsuccessful activation attempt does not send the
        ``user_activated`` signal.
        
        """
        receiver = lambda sender, **kwargs: received_signals.append(kwargs.get('signal'))

        received_signals = []
        signals.user_activated.connect(receiver, sender=self.backend.__class__)

        new_user = self.backend.register(_mock_request(),
                                         username='bob',
                                         email='bob@example.com',
                                         )
        new_user.date_joined -= datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS + 1)
        new_user.save()
        profile = RegistrationProfile.objects.get(user=new_user)
        self.backend.activate(_mock_request(), profile.activation_key, password='secret')

        self.assertEqual(len(received_signals), 0)

    def test_email_send_action(self):
        """
        Test re-sending of activation emails via admin action.
        
        """
        admin_class = RegistrationAdmin(RegistrationProfile, admin.site)
        
        alice = self.backend.register(_mock_request(),
                                      username='alice',
                                      email='alice@example.com',
                                      )
        
        admin_class.resend_activation_email(_mock_request(),
                                            RegistrationProfile.objects.all())
        self.assertEqual(len(mail.outbox), 2) # One on registering, one more on the resend.
        
        RegistrationProfile.objects.filter(user=alice).update(activation_key=RegistrationProfile.ACTIVATED)
        admin_class.resend_activation_email(_mock_request(),
                                            RegistrationProfile.objects.all())
        self.assertEqual(len(mail.outbox), 2) # No additional email because the account has activated.

    def test_email_send_action_no_sites(self):
        """
        Test re-sending of activation emails via admin action when
        ``django.contrib.sites`` is not installed; the fallback will
        be a ``RequestSite`` instance.
        
        """
        Site._meta.installed = False
        admin_class = RegistrationAdmin(RegistrationProfile, admin.site)
        
        alice = self.backend.register(_mock_request(),
                                      username='alice',
                                      email='alice@example.com',
                                      )
        
        admin_class.resend_activation_email(_mock_request(),
                                            RegistrationProfile.objects.all())
        self.assertEqual(len(mail.outbox), 2) # One on registering, one more on the resend.
        
        RegistrationProfile.objects.filter(user=alice).update(activation_key=RegistrationProfile.ACTIVATED)
        admin_class.resend_activation_email(_mock_request(),
                                            RegistrationProfile.objects.all())
        self.assertEqual(len(mail.outbox), 2) # No additional email because the account has activated.
        Site._meta.installed = True

    def test_activation_action(self):
        """
        Test manual activation of users view admin action.
        
        """
        admin_class = RegistrationAdmin(RegistrationProfile, admin.site)

        alice = self.backend.register(_mock_request(),
                                      username='alice',
                                      email='alice@example.com',
                                      )

        admin_class.activate_users(_mock_request(),
                                   RegistrationProfile.objects.all())
        self.failUnless(User.objects.get(username='alice').is_active)

