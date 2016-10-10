from django.test import TestCase, Client
from .models import Team, User, Dialog, Message, Invite, Claim
from .forms import UserForm
import datetime
from .settings import DATABASES, BASE_DIR
import os.path
from pkg_resources import require, DistributionNotFound
from teamsformer import views


# System tests

# Test DB existing
class TestDatabase(TestCase):
    def test_exists_db(self):
        self.db = DATABASES['default']['NAME']
        self.assertEqual(
            os.path.exists(self.db), True
        )


# Test requirements from requirements.txt
class TestRequirements(TestCase):
    def test_requirements(self):
        try:
            requirements = open(BASE_DIR + '/requirements.txt')
        except FileNotFoundError as e:
            self.fail(e)
        try:
            require(requirements)
        except DistributionNotFound as e:
            self.fail(e)


# Unit tests

class TestUser(TestCase):
    def test_str(self):
        self.user = User(username="TestUser")
        self.assertEqual(str(self.user), "TestUser")

    def test_new_messages(self):
        self.user = User.objects.create(username='TestUser')
        self.message = Message.objects.create(sender=self.user, recipient=self.user)
        self.user.received_messages.add(self.message)
        self.assertEqual(
            type(self.user.new_messages()), int
        )
        self.assertEqual(
            self.user.new_messages(), 1
        )


class TestDialog(TestCase):
    def test_str(self):
        self.user1 = User.objects.create(username="TestUser1")
        self.user2 = User.objects.create(username="TestUser2")
        self.dialog = Dialog.objects.create()
        self.dialog.users.add(self.user1, self.user2)
        self.assertEqual(
            str(self.dialog), 'Dialog for TestUser1 and TestUser2'
        )

    def test_update_date(self):
        self.past_date = datetime.datetime.now() - datetime.timedelta(hours=1)
        self.dialog = Dialog(
            created_date=self.past_date, updated_date=self.past_date
        )
        self.dialog.update_date()
        self.assertNotEqual(
            self.dialog.updated_date, self.dialog.created_date
        )


class TestMessage(TestCase):
    def test_str(self):
        self.user1 = User.objects.create(username="TestUser1")
        self.user2 = User.objects.create(username="TestUser2")
        self.message = Message(
            sender=self.user1,recipient=self.user2, text="Test message"
        )
        self.assertEqual(
            str(self.message), 'From TestUser1 to TestUser2'
        )

    def test_reading(self):
        self.user1 = User.objects.create(username="TestUser1")
        self.user2 = User.objects.create(username="TestUser2")
        self.message = Message.objects.create(
            sender=self.user1, recipient=self.user2, text="Test message"
        )
        self.message.read()
        self.assertEqual(
            self.message.is_new, False
        )


class TestTeam(TestCase):
    def test_str(self):
        self.team = Team(title="Test team")
        self.assertEquals(
            str(self.team), 'Test team'
        )

    def test_member_list(self):
        self.user = User.objects.create(
            username="TestUser", role="developer"
        )
        self.team = Team.objects.create(
            title="Tes team", subjects="Test Team", description="Test Team"
        )
        self.team.developer.add(self.user)
        self.assertEqual(
            type(self.team.get_members()), list
        )
        self.assertIn(
            self.user.pk, self.team.get_members()
        )


class TestInvite(TestCase):
    def test_str(self):
        self.user = User(username="TestUser")
        self.team = Team(title="Test team")
        self.invite = Invite(user=self.user, team=self.team)
        self.assertEqual(
            str(self.invite), 'TestUser to Test team'
        )

    def test_accept(self):
        self.user = User.objects.create(
            username="TestUser", role="developer"
        )
        self.team = Team.objects.create(
            title="Test team", description="Test team", subjects="Test team"
        )
        self.invite = Invite.objects.create(
            user=self.user, team=self.team, comment="Test invite"
        )
        self.invite.accept()
        self.assertIn(
            self.user, self.team.developer.all()
        )
        self.assertEqual(
            Invite.objects.filter(pk=self.team.pk).exists(), False
        )

    def test_deny(self):
        self.user = User.objects.create(
            username="TestUser", role="developer"
        )
        self.team = Team.objects.create(
            title="Test team", description="Test team", subjects="Test team"
        )
        self.invite = Invite.objects.create(
            user=self.user, team=self.team, comment="Test invite"
        )
        self.invite.deny()
        self.assertEqual(
            Invite.objects.filter(pk=self.team.pk).exists(), False
        )


class TestClaim(TestCase):
    def test_str(self):
        self.user = User(username="TestUser")
        self.team = Team(title="Test team")
        self.claim = Claim(user=self.user, team=self.team)
        self.assertEqual(
            str(self.claim), 'TestUser to Test team'
        )

    def test_approve(self):
        self.user = User.objects.create(
            username="TestUser", role="developer"
        )
        self.team = Team.objects.create(
            title="Test team", description="Test team", subjects="Test team"
        )
        self.claim = Claim.objects.create(
            user=self.user, team=self.team, comment="Test claim"
        )
        self.claim.approve()
        self.assertIn(
            self.user, self.team.developer.all()
        )
        self.assertEqual(
            Claim.objects.filter(pk=self.claim.pk).exists(), False
        )

    def test_deny(self):
        self.user = User.objects.create(
            username="TestUser", role="developer"
        )
        self.team = Team.objects.create(
            title="Test team", description="Test team", subjects="Test team"
        )
        self.claim = Claim.objects.create(
            user=self.user, team=self.team, comment="Test claim"
        )
        self.claim.deny()
        self.assertEqual(
            Claim.objects.filter(pk=self.claim.pk).exists(), False
        )


# Integrate tests
class TestIndexView(TestCase):
    # load base data
    fixtures = ['test_fixtures.json']

    # configure http-client
    def setUp(self):
        self.client = Client()

    def test_index_for_unauthorized_enter(self):
        response = self.client.get('/index/')

        # check response status
        self.assertEqual(response.status_code, 200)
        # check template name
        self.assertIn('index.html', response.templates[0].name)
        # check view function
        self.assertEqual(response.resolver_match.func, views.index)

    def test_index_for_authorized_enter(self):
        login = self.client.login(username="TestUser1", password="12345")
        response = self.client.get('/index/', follow=True)

        # check for authorize user
        self.assertEqual(login, True)
        # check response status
        self.assertEqual(response.status_code, 200)
        # check template name
        self.assertIn('profile.html', response.templates[0].name)


class TestProfileView(TestCase):
    # load base data
    fixtures = ['test_fixtures.json']

    # configure http-client
    def setUp(self):
        self.client = Client()
        self.client.login(username="TestUser1", password="12345")

    def test_profile_entry(self):
        response = self.client.get('/profile/')

        # check response status
        self.assertEqual(response.status_code, 200)
        # check for existing form in response context
        self.assertIn('form', response.context)
        # check for equal of form name
        self.assertEqual(str(response.context['form']), 'UserForm')
        # check for existing user in form instance
        self.assertEqual(response.context['form'].instance.username, 'TestUser1')