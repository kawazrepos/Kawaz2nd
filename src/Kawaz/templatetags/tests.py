"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
    def test_youtube_perser(self):
        """
        Tests detection as YouTube Video.
        """
        from templatetags import viewer
        sample = r'http://www.youtube.com/watch?v=iHLT-QWQvWc'
        self.assertTrue(viewer.viewer(sample))

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

