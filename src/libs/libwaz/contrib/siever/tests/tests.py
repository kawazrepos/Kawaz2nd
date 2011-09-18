import datetime
import os

from django.conf import settings
from django.test import TestCase

from ..filterset import FilterSet
from .. import filters

from models import User, Comment, Book, Restaurant, Article, STATUS_CHOICES


class GenericViewTests(TestCase):
    urls = 'django_filters.tests.test_urls'
    fixtures = ['test_data']
    template_dirs = [
        os.path.join(os.path.dirname(__file__), 'templates'),
    ]

    def setUp(self):
        self.old_template_dir = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = self.template_dirs

    def tearDown(self):
        settings.TEMPLATE_DIRS = self.old_template_dir

    def test_generic_view(self):
        response = self.client.get('/books/')
        for b in ['Ender&#39;s Game', 'Rainbox Six', 'Snowcrash']:
            self.assertContains(response, b)

class InheritanceTest(TestCase):
    def test_inheritance(self):
        class F(FilterSet):
            class Meta:
                model = Book

        class G(F):
            pass
        self.assertEqual(set(F.base_filters), set(G.base_filters))

class ModelInheritanceTest(TestCase):
    def test_abstract(self):
        class F(FilterSet):
            class Meta:
                model = Restaurant

        self.assertEquals(set(F.base_filters), set(['name', 'serves_pizza']))

        class F(FilterSet):
            class Meta:
                model = Restaurant
                fields = ['name', 'serves_pizza']

        self.assertEquals(set(F.base_filters), set(['name', 'serves_pizza']))


class DateRangeFilterTest(TestCase):
    def test_filter(self):
        a = Article.objects.create(published=datetime.datetime.today())
        class F(FilterSet):
            published = filters.DateRangeFilter()
            class Meta:
                model = Article
        f = F({'published': '2'})
        self.assertEqual(list(f), [a])


class FilterSetForm(TestCase):
    def test_prefix(self):
        class F(FilterSet):
            class Meta:
                model = Restaurant
                fields = ['name']
        self.assert_('blah-prefix' in unicode(F(prefix='blah-prefix').form))

class AllValuesFilterTest(TestCase):
    fixtures = ['test_data']

    def test_filter(self):
        class F(FilterSet):
            username = filters.AllValuesFilter()
            class Meta:
                model = User
                fields = ['username']
        form_html = ('<tr><th><label for="id_username">Username:</label></th>'
            '<td><select name="username" id="id_username">\n'
            '<option value="aaron">aaron</option>\n<option value="alex">alex'
            '</option>\n<option value="jacob">jacob</option>\n</select></td>'
            '</tr>')
        self.assertEqual(unicode(F().form), form_html)
        self.assertEqual(list(F().qs), list(User.objects.all()))
        self.assertEqual(list(F({'username': 'alex'})), [User.objects.get(username='alex')])
        self.assertEqual(list(F({'username': 'jose'})), list(User.objects.all()))

class InitialValueTest(TestCase):
    fixtures = ['test_data']

    def test_initial(self):
        class F(FilterSet):
            status = filters.ChoiceFilter(choices=STATUS_CHOICES, initial=1)
            class Meta:
                model = User
                fields = ['status']
        self.assertEqual(list(F().qs), [User.objects.get(username='alex')])
        self.assertEqual(list(F({'status': 0})), list(User.objects.filter(status=0)))


class RelatedObjectTest(TestCase):
    fixtures = ['test_data']
    
    def test_foreignkey(self):
        class F(FilterSet):
            class Meta:
                model = Article
                fields = ['author__username']
        self.assertEqual(F.base_filters.keys(), ['author__username'])
        form_html = ('<tr><th><label for="id_author__username">Username:</label>'
            '</th><td><input type="text" name="author__username" '
            'id="id_author__username" /></td></tr>')
        self.assertEqual(str(F().form), form_html)
        self.assertEqual(F({'author__username': 'alex'}).qs.count(), 2)
        self.assertEqual(F({'author__username': 'jacob'}).qs.count(), 1)

        class F(FilterSet):
            author__username = filters.AllValuesFilter()
            class Meta:
                model = Article
                fields = ['author__username']
            
        form_html = ('<tr><th><label for="id_author__username">Author  '
            'username:</label></th><td><select name="author__username" '
            'id="id_author__username">\n<option value="alex">alex</option>\n'
            '<option value="jacob">jacob</option>\n</select></td></tr>')
        self.assertEqual(str(F().form), form_html)


class MultipleChoiceFilterTest(TestCase):
    fixtures = ['test_data']

    def test_all_choices_selected(self):
        class F(FilterSet):
            class Meta:
                model = User
                fields = ["status"]
        
        self.assertEqual(list(F({"status": [0, 1]}).qs), list(User.objects.all()))

class MultipleLookupTypesTest(TestCase):
    fixtures = ['test_data']
    
    def test_no_GET_params(self):
        class F(FilterSet):
            published = filters.DateTimeFilter(lookup_type=['gt', 'lt'])
            class Meta:
                model = Article
                fields = ['published']
        
        self.assertEqual(list(F({}).qs), list(Article.objects.all()))