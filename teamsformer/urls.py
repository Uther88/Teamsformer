from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.auth.views import logout



urlpatterns = [
    # Site
    url(r'^(?:index.+)?$', views.index, name='index'),
    url(r'^profile/$', views.profile, name='profile'),
    # Teams views
    url(r'^teams/search/$', views.teams_search, name='teams_search'),
    url(r'^teams/my/$', views.my_teams, name='my_teams'),
    url(r'^teams/(?P<pk>[0-9]+)$', views.team_view, name='team_view'),
    url(r'^teams/claim/(?P<pk>[0-9]+)$', views.claim_to_team, name='claim_to_team'),
    url(r'^teams/claim/(?P<pk>[0-9]+)/accept$', views.accept_claim, name='accept_claim'),
    url(r'^teams/claim/(?P<pk>[0-9]+)/refuse$', views.refuse_claim, name='refuse_claim'),
    url(r'^teams/unclaim/(?P<pk>[0-9]+)$', views.team_unclaim, name='team_unclaim'),
    url(r'^teams/create/$', views.team_create, name='team_create'),
    url(r'^teams/edit/(?P<pk>[0-9]+)$', views.team_edit, name='team_edit'),
    url(r'^teams/delete/(?P<pk>[0-9]+)$', views.team_delete, name='team_delete'),
    url(r'^teams/leave/(?P<pk>[0-9]+)$', views.team_leave, name='team_leave'),
    url(r'^teams/invites$', views.my_invites, name='my_invites'),
    url(r'^teams/invites/accept/(?P<pk>[0-9]+)$', views.accept_invite, name='accept_invite'),
    url(r'^teams/invites/deny/(?P<pk>[0-9]+)$', views.deny_invite, name='deny_invite'),
    # Messages views
    url(r'^messages/$', views.my_messages, name='my_messages'),
    url(r'^messages/dialog/(?P<pk>[0-9]+)$', views.dialog_view, name='dialog_view'),
    url(r'^messages/new/(?P<pk>[0-9]+)$', views.new_message, name='new_message'),
    url(r'^messages/send/(?P<pk>[0-9]+)$', views.send_message, name='send_message'),
    # Contacts views
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^contacts/search/$', views.search_teammate, name='search_teammate'),
    url(r'^contacts/add/(?P<pk>[0-9]+)$', views.add_to_contacts, name='add_to_contacts'),
    url(r'^contacts/invite/(?P<pk>[0-9]+)$', views.invite_to_team, name='invite_to_team'),
    url(r'^contacts/remove/(?P<pk>[0-9]+)$', views.remove_from_contacts, name='remove_from_contacts'),
    url(r'^contacts/user/(?P<pk>[0-9]+)$', views.user_view, name='user_view'),
    url(r'^logout/$', logout, {'next_page': 'index'}, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

