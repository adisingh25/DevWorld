from django.shortcuts import render, redirect
from .models import Profile,Skill
# Create your views here.
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User

from django.contrib import messages
from .forms import CutsomUserCreationForm,ProfileForm,SkillForm,MessageForm
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from .utils import searchProfiles,paginateProfiles




def loginUser(request):
    page = 'login'

    if request.user.is_authenticated :   # if the user is already authenticated then do not show him that page
        return redirect('profiles')


    if request.method == 'POST':
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username not found!!')
        
        user = authenticate(request, username=username, password = password)

        if user is not None:
            login(request, user)            # creates a session for that user in the session database and adds the session to the cookies of our browser.
            #return redirect('profiles')
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')   
        # send the user to the 'next page' if 'next' is mentioned in the url (action parameter of the form) else to his account page
        else :
            messages.error(request,'Credentials are wrong')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)   # deletes the session from our database
    print('logged out')
    messages.success(request, 'User was logged out!!')
    return redirect('login')




def registerUser(request):
    page = 'register'
    form = CutsomUserCreationForm()

    if request.method == 'POST':
        form = CutsomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Instead of saving the form right away, we are holding a temporary instance of it 
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')
            login(request,user)    # login the user once he is  registered
            return redirect('edit-account')
        
        else:
            messages.error(request, 'User account was not created successfully')


    context = {'page':page, 'form' : form}
    return render(request, 'users/login_register.html', context=context)

def profiles(request):

    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    
    context = {'profiles' : profiles, 'search_query' : search_query, 'custom_range': custom_range}
    return render(request, 'users/profiles.html', context = context)

def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")        # exclude those skills which have no description
    otherSkills = profile.skill_set.filter(description="")              # Returns all those skills that have no description
    context = {'profile' : profile, 'topSkills' : topSkills, 'otherSkills' : otherSkills}
    return render(request, 'users/user-profile.html', context= context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile          # once the user is logged in, we can always access it using 'request.user'
    skills = profile.skill_set.all()  
    projects = profile.project_set.all()     
    context = {'profile' : profile, 'skills' : skills, 'projects':projects}
    return render(request, 'users/account.html', context=context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    context = {'form' : form}
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            form.save()
            return redirect('account')
        # else:
        #     return redirect('edit-account')


    return render(request, 'users/profile_form.html', context=context)



@login_required(login_url='login')
def createSkill(request):
    form  = SkillForm()
    context= {'form' : form}
    profile = request.user.profile

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')
        
    return render(request, 'users/skill_form.html', context=context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_object.html', context)



@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()  
    # 'messages' here is the renamed version that we have done in model.py for the message model (recipient field)

    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests' : messageRequests, 'unreadCount' : unreadCount}
    return render(request, 'users/inbox.html', context = context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)    # recipent is referred as 'messages' in the "Message" model that we had created 
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)

