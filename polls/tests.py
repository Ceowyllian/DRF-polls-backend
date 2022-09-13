from django.test import TestCase

from .seeder import run

class TestQuestionModel(TestCase):

    def setUp(self):
        run()
