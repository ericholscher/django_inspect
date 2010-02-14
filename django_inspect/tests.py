import datetime

from django.test.testcases import TestCase
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from django_inspect import base

class IntrospectorTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'test')
        self.comment = Comment.objects.create(
            content_type = ContentType.objects.get_for_model(User),
            object_pk = self.user.pk,
            user=self.user,
            user_name = "Joe Somebody",
            user_email = "jsomebody@example.com",
            user_url = "http://example.com/~joe/",
            comment = "First here, too!",
            ip_address = "127.0.0.1",
            site = Site.objects.get_current(),
        )


    def test_basic_content(self):
        ins = base.Inspecter(self.comment)
        self.assertEqual(ins.content.field, 'comment')
        self.assertEqual(ins.content.value, 'First here, too!')

    def test_basic_pub_date(self):
        ins = base.Inspecter(self.comment)
        self.assertEqual(ins.pub_date.field, 'submit_date')

    def test_basic_title(self):
        ins = base.Inspecter(self.comment)
        self.assertEqual(ins.title.field, None)

    def test_basic_ip(self):
        ins = base.Inspecter(self.comment)
        self.assertEqual(ins.ip_address.value, '127.0.0.1')

    def test_basic_user(self):
        ins = base.Inspecter(self.comment)
        self.assertEqual(ins.user.value.username, 'test')

    def test_basic_mapping(self):
        DEFAULT_MAPPINGS = {
        'comments.comment': {
            'content': 'user_name',
            'pub_date': 'submit_date',
             },
        'auth.user': {
            'content': 'username',
            'pub_date': 'last_login',
            },
        }

        user_inspecter = base.Inspecter(self.user, DEFAULT_MAPPINGS)
        self.assertEqual(user_inspecter.content.field, 'username')
        self.assertEqual(user_inspecter.content.value, 'test')

        #Test that the mapping overrides the defaults.
        comment_ins = base.Inspecter(self.comment, DEFAULT_MAPPINGS)
        self.assertEqual(comment_ins.content.field, 'user_name')
        self.assertEqual(comment_ins.content.value, 'Joe Somebody')
