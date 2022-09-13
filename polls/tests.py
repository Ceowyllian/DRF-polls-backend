from django.test import TestCase

import seeder


class TestQuestionModel(TestCase):

    def setUp(self):
        seeder.run()
