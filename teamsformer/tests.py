from django.test import TestCase
from .models import Team
# Create your tests here.


class TeamTest(TestCase):

    def test_str(self):
        team = Team(title="Test Team")
        print('Testing of str method')
        self.assertEquals(
            str(team),
            'Test Team',
            )
