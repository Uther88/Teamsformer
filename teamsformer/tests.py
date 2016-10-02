from django.test import TestCase
from .models import Team, User, Dialog, Message, Invite, Claim
import datetime
from .settings import DATABASES, BASE_DIR
import os.path
from pkg_resources import require, DistributionNotFound
from .views import index

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


class TestUser(TestCase):
    def test_str(self):
        self.user = User(username="TestUser")
        self.assertEqual(str(self.user), "TestUser")

    def test_new_messages(self):
        self.user = User.objects.create(username='TestUser')
        self.message = Message.objects.create(
            recipient=self.user, text="testing message")
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
            username="TestUser", role="Developer"
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
            username="TestUser", role="Developer"
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
            username="TestUser", role="Developer"
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
            username="TestUser", role="Developer"
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
            username="TestUser", role="Developer"
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