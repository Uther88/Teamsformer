from django.contrib import admin
from .models import User, Team, Claim, Message, Dialog, Invite
admin.site.register(User)
admin.site.register(Team)
admin.site.register(Claim)
admin.site.register(Message)
admin.site.register(Dialog)
admin.site.register(Invite)