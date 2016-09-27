from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.db.models import Q
from select_multiple_field.models import SelectMultipleField


# Roles
D = "Developer"
I = "Investor"
S = "Sales person"
ROLES = (
    (D, 'Developer'),
    (I, 'Investor'),
    (S, 'Sales person'),
)


# Custom user model
class User(AbstractUser):
    role = models.CharField('User role',
                            max_length=40,
                            default=None,
                            choices=ROLES,
                            blank=True,
                            null=True
                            )
    skills = models.TextField('Skills',
                              default=None,
                              blank=True,
                              null=True
                              )
    about = models.TextField('Other information',
                             default=None,
                             blank=True,
                             null=True
                             )
    avatar = models.ImageField(max_length=255, upload_to='users/avatars/',
                               blank=True
                               )
    contact_list = models.ManyToManyField('self', blank=True)

    class Meta:
        verbose_name = "Custom user"
        verbose_name_plural = "Custom users"

    def new_messages(self):
        return self.received_messages.filter(is_new=True).count()


# Model of teams
class Team(models.Model):
    title = models.CharField('Team', max_length=40, unique=True)
    subjects = models.CharField('Subject', max_length=50, default=None, blank=True)
    description = models.TextField('Team details', blank=True, default=None)
    image = models.ImageField('Team image', upload_to='teams/images/', blank=True)

    admin = models.ForeignKey(User, related_name='teams_admin', null=True)
    developer = models.ManyToManyField(User, related_name='teams_developer', blank=True)
    investor = models.ManyToManyField(User, related_name='teams_investor', blank=True)
    sales_person = models.ManyToManyField(User, related_name='teams_sales_person', blank=True)
    created_date = models.DateTimeField('Created data', default=datetime.now)
    needs = SelectMultipleField(max_length=50, choices=ROLES,
                              blank=True, null=True
                             )

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return self.title

    def get_members(self):
        members = (self.developer.all(),
                   self.investor.all(),
                   self.sales_person.all()
                   )
        members_list = []
        for queryset in members:
            for user in queryset:
                members_list.append(user.pk)
        return members_list


# Model of dialogs between users
class Dialog(models.Model):
    users = models.ManyToManyField(User, related_name="dialogs")
    created_date = models.DateTimeField('Created date', auto_now_add=True)
    updated_date = models.DateTimeField('Updated date', auto_now=True)

    class Meta:
        verbose_name = "Dialog"
        verbose_name_plural = "Dialogs"

    def __str__(self):
        return 'Dialog for ' + self.users.all()[0].username + ' and ' + self.users.all()[1].username

    def update_date(self):
        self.updated_date = datetime.now()
        self.save()


# Model of messages
class Message(models.Model):
    sender = models.ForeignKey(User, related_name="send_messages", max_length=40, null=True)
    recipient = models.ForeignKey(User, related_name="received_messages", max_length=40, null=True)
    dialog = models.ForeignKey(Dialog, related_name='messages', null=True)
    text = models.TextField('Text of message', default=None, max_length=400)
    created_date = models.DateTimeField('Created data', auto_now_add=True)
    is_new = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-created_date']

    def __str__(self):
        return 'From ' + self.sender.username + ' to ' + self.recipient.username

    def read(self):
        if self.is_new is True:
            self.is_new = False
            self.save()


# Model of invites users to teams
class Invite(models.Model):
    user = models.ForeignKey(User, related_name="invites_to_teams", null=True)
    team = models.ForeignKey(Team, related_name="invited_users", null=True)
    created_date = models.DateTimeField('Date of invite', auto_now_add=True)
    comment = models.TextField(max_length=255, default=None, blank=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Invite"
        verbose_name_plural = "Invites"
        ordering = ['-created_date']

    def __str__(self):
        return self.user.username + ' to ' + self.team.title

    def accept(self):
        self.accepted = True
        if self.user.role == 'Developer':
            self.team.developer.add(self.user)
        elif self.user.role == 'Investor':
            self.team.investor == self.user
        elif self.user.role == 'Sales person':
            self.team.sales_person.add(self.user)
        self.delete()

    def deny(self):
        self.delete()


# Model of claims users to teams
class Claim(models.Model):
    user = models.ForeignKey(User, related_name="claims_to_teams", null=True)
    team = models.ForeignKey(Team, related_name="claims", null=True)
    approved = models.BooleanField(default=False)
    comment = models.TextField(max_length=255, default=None, blank=True)
    created_date = models.DateTimeField('Created date', auto_now_add=True)

    class Meta:
        verbose_name = "Claim"
        verbose_name_plural = "Claims"

    def __str__(self):
        return self.user.username + '_to_' + self.team.title

    def approve(self):
        self.approved = True
        if self.user.role == 'Developer':
            self.team.developer.add(self.user)
        elif self.user.role == 'Investor':
            self.team.investor == self.user
        elif self.user.role == 'Sales person':
            self.team.sales_person.add(self.user)
