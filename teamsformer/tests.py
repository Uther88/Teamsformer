from django.test import TestCase, Client
from .models import Team, User, Dialog, Message, Invite, Claim
from .forms import UserForm, TeamForm
import datetime
from .settings import DATABASES, BASE_DIR
import os.path
from pkg_resources import require, DistributionNotFound
from teamsformer import views


# Base testing case with basic fixtures and settings
class CustomTestCase(TestCase):
    fixtures = ['test_fixtures.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username="TestUser1", password="12345")


# System tests

# Test DB existing
class TestDatabase(TestCase):

    def test_exists_db(self):
        self.db = DATABASES['default']['NAME']
        self.assertTrue(
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
        self.assertFalse(
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
        self.assertFalse(
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
        self.assertFalse(
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
        self.assertFalse(
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
        self.assertFalse(
            Claim.objects.filter(pk=self.claim.pk).exists()
        )


"""                         Integrated tests                          """


class TestIndexView(CustomTestCase):

    def setUp(self):
        self.client = Client()

    def test_index_for_unauthorized_enter(self):
        response = self.client.get('/index/')

        # check response status
        self.assertEqual(
            response.status_code, 200
        )
        # check template name
        self.assertIn(
            'index.html', response.templates[0].name
        )
        # check view function
        self.assertEqual(
            response.resolver_match.func, views.index
        )

    def test_index_for_authorized_enter(self):
        login = self.client.login(
            username="TestUser1", password="12345"
        )
        response = self.client.get('/index/', follow=True)

        # check for authorize user
        self.assertEqual(
            login, True
        )
        # check response status
        self.assertEqual(
            response.status_code, 200
        )
        # check template name
        self.assertIn(
            'profile.html', response.templates[0].name
        )


class TestProfileView(CustomTestCase):

    def test_profile_entry(self):
        response = self.client.get('/profile/')

        # check response status
        self.assertEqual(
            response.status_code, 200
        )
        # check on the availability form in context
        self.assertIn(
            'form', response.context
        )
        # check for equal of form name
        self.assertEqual(
            str(response.context['form']), 'UserForm'
        )
        # check for existing user in form instance
        self.assertEqual(
            response.context['form'].instance.username, 'TestUser1'
        )
        # check view function
        self.assertEqual(
            response.resolver_match.func, views.profile
        )
        # check template name
        self.assertIn(
            'profile.html', response.templates[0].name
        )


class TestTeamsSearch(CustomTestCase):

    def test_view_response(self):
        response = self.client.get(
            '/teams/search/', {'q': 'test'}
        )
        # check status code
        self.assertEqual(
            response.status_code, 200
        )
        # check on the availability of context
        self.assertEqual(
            'test', response.context['teams'][0].subjects
        )
        # check view function
        self.assertEqual(
            response.resolver_match.func, views.teams_search
        )
        # check template name
        self.assertIn(
            'teams-search.html', response.templates[0].name
        )


class TestTeamView(CustomTestCase):

    def test_team_view(self):
        team = Team.objects.get(title='TestTeam')
        response = self.client.get(
            '/teams/%s' % team.pk
        )
        # check status code
        self.assertEqual(
            response.status_code, 200
        )
        #  check on the availability of context
        self.assertEqual(
            team, response.context['team']
        )
        # check view function
        self.assertEqual(
            response.resolver_match.func, views.team_view
        )
        # check template name
        self.assertIn(
            'team.html', response.templates[0].name
        )


class TestTeamCreateView(CustomTestCase):

    def test_team_create_view_response(self):
        response = self.client.get('/teams/create/')
        user1 = response.context['user']
        user2 = User.objects.get(username="TestUser2")
        user1.contact_list.add(user2)

        # check status code
        self.assertEqual(
            response.status_code, 200
        )
        # check context
        self.assertEqual(
            response.context['form'].__class__, TeamForm
        )
        # check for existing investor user from contact list in form querysets
        self.assertIn(
            user2.username, str(response.context['form']['investor'])
        )
        # check view function
        self.assertEqual(
            response.resolver_match.func, views.team_create
        )
        # check template name
        self.assertIn(
            'team-create.html', response.templates[0].name
        )

    def test_team_create(self):
        response = self.client.post('/teams/create/', follow=True,
                                    data={
                                        'title': 'TestTeam2',
                                        'subjects': 'test',
                                        'description': 'test'
                                    })
        # check status code
        self.assertEqual(
            response.status_code, 200
        )
        # check for existing of created team
        self.assertTrue(
            Team.objects.filter(title="TestTeam2").exists()
        )
        # check for created team admin
        self.assertEqual(
            Team.objects.get(title="TestTeam2").admin, response.context['user']
        )
        # check for redirect after successful creating the team
        self.assertEqual(
            response.request['PATH_INFO'], '/teams/my/'
        )


class TestTeamEditView(CustomTestCase):

    def test_team_edit_view_response(self):
        team = Team.objects.get(title="TestTeam")
        response = self.client.get(
            '/teams/edit/%s' % team.pk
        )
        user1 = response.context['user']
        user2 = User.objects.get(username="TestUser2")
        user1.contact_list.add(user2)

        # check status code
        self.assertEqual(
            response.status_code, 200
        )
        # check target team in response context
        self.assertEqual(
            response.context['form'].__class__, TeamForm
        )
        # check for team instance
        self.assertEqual(
            team, response.context['form'].__dict__['instance']
        )
        # check for team admin
        self.assertEqual(
            response.context['user'], response.context['form'].__dict__['instance'].admin
        )
        # check for existing investor user from contact list in form querysets
        self.assertIn(
            user2.username, str(response.context['form']['investor'])
        )
        # check view function
        self.assertEqual(
            response.resolver_match.func, views.team_edit
        )
        # check template name
        self.assertIn(
            'team-edit.html', response.templates[0].name
        )

    def test_team_modify(self):
        self.team = Team.objects.get(title="TestTeam")
        response = self.client.post('/teams/edit/%s' % self.team.pk,
                                    follow=True, data={'title': 'ModifyTeam'})
        self.team.refresh_from_db()

        # check status code
        self.assertEqual(
            response.status_code, 200
        )
        # check for redirect after successful modify the team
        self.assertEqual(
            response.request['PATH_INFO'], '/teams/my/'
        )
        # check for changing team title
        self.assertEqual(
            self.team.title, 'ModifyTeam'
        )


class TestTeamDeleteView(CustomTestCase):

    def test_team_delete_view(self):
        team = Team.objects.get(title="TestTeam")
        response = self.client.post(
            '/teams/delete/%s' % team.pk, follow=True
        )
        wrong_response = self.client.get(
            '/teams/delete/%s' % team.pk, follow=True
        )

        # check response status code
        self.assertEqual(
            response.status_code, 200
        )
        # check for deleting target team
        self.assertFalse(
            Team.objects.filter(title="TestTeam").exists()
        )
        # check for successful redirect after deleting team
        self.assertTrue(
            response.redirect_chain
        )
        self.assertIn(
            '/teams/my/', response.redirect_chain[0]
        )
        # check for bad request if request method is GET
        self.assertEqual(
            wrong_response.status_code, 400
        )


class TestMyTeamsView(CustomTestCase):

    def test_my_teams(self):
        response = self.client.get('/teams/my/')
        user = response.context['user']
        team = Team.objects.get(title="TestTeam")
        team.developer.add(user)

        # check response status code
        self.assertEqual(
            response.status_code, 200
        )
        # check for view function
        self.assertEqual(
            response.resolver_match.func, views.my_teams
        )
        # check template
        self.assertIn(
            'my-teams.html', response.templates[0].name
        )
        # check on the availability of context
        self.assertIn(
            'own_teams', response.context
        )
        self.assertIn(
            'member_teams', response.context
        )
        # check for existing for admin-user in own teams queryset
        self.assertEqual(
            team.admin, user
        )
        # check for existing for member-user in member teams queryset
        self.assertTrue(
            team.developer.filter(pk=user.pk).exists()
        )


class TestTeamLeaveView(CustomTestCase):

    def test_team_leave(self):
        response = self.client.get
