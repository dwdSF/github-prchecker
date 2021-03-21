'''
#  тут могли бы быть тесты, но я очень устал
#  Update: передохнул, напишем немного тестов
'''
from .models import Check
from django.test import Client, TestCase
from django.urls import reverse


class TestCheck(TestCase):
    ''' Health tests of the authorization and verification page '''

    def setUp(self):
        self.client = Client()
        self.check = Check.objects.create(
            project_name='test',
            stars_number=100,
            url='test url',
            merged_prs=[('test_merged_prs.com/testing', 2)],
            not_merged_prs=[],
            username='melevir'
        )

    def test_check_page(self):
        text = 'Enter username'
        response = self.client.get(reverse('info'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text)

    def test_check_post_ajax(self):
        message = b'{"message": "success"}'
        response = self.client.post(reverse('info'),
                                    {'username': self.check.username},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertContains(response, message)

    def test_check_get_ajax(self):
        response = self.client.get(reverse('info_data'),
                                   {'username': self.check.username},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.check.project_name)
        self.assertContains(response, self.check.url)
        self.assertContains(response, self.check.stars_number)
