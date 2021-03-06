from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .forms import UserForm, TeamForm, MessageForm
from .models import Team, User, Claim, Dialog, Message, Invite
from django.db.models import Q
from django.core.urlresolvers import resolve
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation, DisallowedRedirect

from .models import ROLES


# Base index
def index(request):
    if request.user.is_authenticated:
        return redirect(profile)
    else:
        return render(request, 'teamsformer/index.html')


# View for users profile editing
@login_required()
def profile(request):
    form = UserForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'teamsformer/profiles/profile.html', {'form': form})


# View for searching of teams
@login_required()
def teams_search(request):
    query = request.GET.get('q')
    if query is not None:
        teams = Team.objects.filter(subjects__icontains=query)
    else:
        teams = Team.objects.all()
    return render(request, 'teamsformer/teams/teams-search.html', {'teams': teams})


# View for viewing a single team
@login_required()
def team_view(request, pk):
    select_team = Team.objects.get(pk=pk)
    return render(request, 'teamsformer/teams/team.html', {'team': select_team})


# View for creating the team
@login_required()
def team_create(request):
    contact_list = request.user.contact_list.all()
    form = TeamForm(request.POST or None, request.FILES or None)
    for role in ROLES:
        form.fields[role[0].lower()].queryset = User.objects.filter(
            Q(pk=request.user.pk) & Q(role=role[0]) | Q(role=role[0]) & Q(pk__in=contact_list)
        )
    if form.is_valid():
        team = form.save()
        team.admin = request.user
        form.save()
        return redirect('my_teams')
    return render(request, 'teamsformer/teams/team-create.html', {'form': form})


# View for editing the team
@login_required()
def team_edit(request, pk):
    editable_team = Team.objects.get(pk=pk)
    contact_list = request.user.contact_list.all()
    if editable_team.admin == request.user:
        form = TeamForm(request.POST or None, request.FILES or None, instance=editable_team)
        for role in ROLES:
            form.fields[role[0].lower()].queryset = User.objects.filter(
                Q(pk=request.user.pk) & Q(role=role[0]) | Q(role=role[0]) & Q(pk__in=contact_list)
            )
        if form.is_valid():
            form.save()
            return redirect('my_teams')
        return render(request, 'teamsformer/teams/team-edit.html', {'form': form})
    else:
        raise PermissionError("You are not an admin of this team!")


# View for deleting the team
@login_required()
def team_delete(request, pk):
    if request.method == 'POST':
        removed_team = Team.objects.get(pk=pk)
        if removed_team.admin == request.user:
            removed_team.delete()
        else:
            raise PermissionError("You are not an admin of this team!")
        return redirect(my_teams)
    else:
        raise SuspiciousOperation('Method %s not allowed, use POST!' % request.method)


# View for viewing teams where user admin and member
@login_required()
def my_teams(request):
    own_teams = Team.objects.filter(admin=request.user)
    member_teams = Team.objects.filter(
        Q(developer=request.user) | Q(investor=request.user) | Q(salesperson=request.user)
    )
    return render(request, 'teamsformer/teams/my-teams.html',
                    {'own_teams': own_teams, 'member_teams': member_teams})


# View for leaving of team
@login_required()
def team_leave(request, pk):
    if request.method == "POST":
        target_team = get_object_or_404(Team, pk=pk)
        for team in (request.user.teams_developer, request.user.teams_investor, request.user.teams_salesperson):
            if target_team in team.all():
                team.remove(target_team)
        return redirect('my_teams')
    else:
        raise SuspiciousOperation('Method %s not allowed, use POST!' % request.method)


# View for viewing all dialogs
@login_required()
def my_messages(request):
    dialogs = Dialog.objects.filter(users=request.user).order_by('-updated_date')
    return render(request, 'teamsformer/message/my-messages.html', {'dialogs': dialogs})


# View for viewing a single dialog
@login_required()
def dialog_view(request, pk):
    dialog = get_object_or_404(Dialog, pk=pk)
    recipient = dialog.users.exclude(pk=request.user.pk).get()
    dialog.messages.order_by('created_date')
    for message in dialog.messages.all():
        message.read()
    form = MessageForm(request.POST or None)
    return render(request, 'teamsformer/message/dialog-view.html', {
        'dialog': dialog, 'form': form, 'recipient': recipient})


# View for creating and sending new messages
@login_required()
def send_message(request, pk):
    sender = request.user
    recipient = get_object_or_404(User, pk=pk)
    text = request.POST.get('text')
    back = request.POST.get('back')
    try:
        dialog = Dialog.objects.get(users=sender.pk and recipient.pk)
        dialog.update_date()
    except ObjectDoesNotExist:
        dialog = Dialog.objects.create()
        dialog.users.add(sender, recipient)
    Message.objects.create(
        sender=sender, recipient=recipient, dialog=dialog, text=text
    )
    try:
        if resolve(back):
            return redirect(back)
    except Http404 as e:
        raise DisallowedRedirect(e)


# View for claiming to teams
@login_required()
def claim_to_team(request, pk):
    target_team = Team.objects.get(pk=pk)
    if not target_team.claims.all() & request.user.claims_to_teams.all():
        Claim.objects.create(
            user=request.user,
            team=target_team,
            comment="Hi! I am a %s, please take me to your team" % request.user.role
        )
    return redirect('team_view', pk=pk)


# View for unclaiming to team
@login_required()
def team_unclaim(request, pk):
    back = request.GET.get('back')
    target_team = get_object_or_404(Team, pk=pk)
    if target_team.claims.all() & request.user.claims_to_teams.all():
        Claim.objects.get(user=request.user, team=target_team).delete()
    if resolve(back):
        return HttpResponseRedirect(back)


# View for accepting the claim to team
@login_required()
def accept_claim(request, pk):
    claim = get_object_or_404(Claim, pk=pk)
    if claim.team.admin == request.user:
        request.user.contact_list.add(claim.user)
        claim.approve()
    return redirect('team_view', pk=claim.team.pk)


# View for refusing a claim to team
@login_required()
def refuse_claim(request, pk):
    claim = get_object_or_404(Claim, pk=pk)
    if claim.team.admin == request.user:
        claim.deny()
    return redirect('team_view', pk=claim.team.pk)


# View for contact list
@login_required()
def contacts(request):
    if request.user.is
    contact_list = request.user.contact_list.all()
    return render(request, 'teamsformer/contacts/contacts.html', {'contact_list': contact_list})


# View for adding users to contact list
@login_required()
def add_to_contacts(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    request.user.contact_list.add(target_user)
    back = request.GET.get('back')
    if resolve(back):
        return HttpResponseRedirect(back)


# View for removing users from contact list
@login_required()
def remove_from_contacts(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    request.user.contact_list.remove(target_user)
    return redirect('contacts')


# View for searching teammates to your team
@login_required()
def search_teammate(request):
    form = MessageForm(request.POST or None)
    query = request.GET.get('q')
    if query is not None:
        users = User.objects.filter(
            Q(username=query) | Q(role__icontains=query) | Q(skills__icontains=query) | Q(about__icontains=query))
    else:
        users = User.objects.exclude(pk=request.user.pk)
    return render(request, 'teamsformer/contacts/search-teammate.html', {'users': users, 'form': form})


# View for inviting users to team
@login_required()
def invite_to_team(request, pk):
    team_pk = request.POST.get('team')
    text = request.POST.get('text')
    back = request.GET.get('back')
    target_user = get_object_or_404(User, pk=pk)
    target_team = get_object_or_404(Team, pk=team_pk)
    if request.user == target_team.admin and\
            not Invite.objects.filter(user=target_user, team=target_team).exists():
            Invite.objects.create(user=target_user, team=target_team, comment=text)
    if resolve(back):
        return HttpResponseRedirect(back)


# View for viewing a new invites to team
@login_required()
def my_invites(request):
    invites = Invite.objects.filter(user=request.user)
    return render(request, 'teamsformer/teams/my-invites.html',
                  {'invites': invites})


# View for accepting invite to team
@login_required()
def accept_invite(request, pk):
    invite = get_object_or_404(Invite, pk=pk)
    invite.accept()
    return redirect('my_invites')


# View for deny invite to team
@login_required()
def deny_invite(request, pk):
    invite = get_object_or_404(Invite, pk=pk)
    invite.deny()
    return redirect('my_invites')


# View for viewing the users
@login_required()
def user_view(request, pk):
    form = MessageForm(request.POST or None)
    target_user = get_object_or_404(User, pk=pk)
    return render(request, 'teamsformer/contacts/user-view.html',
                  {'target_user': target_user, 'form': form})


