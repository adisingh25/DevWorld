from django.shortcuts import render,redirect

# Create your views here.


from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm,ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import searchProjects,paginateProjects
from django.contrib import messages

from django.core.paginator import Paginator


# def projects(request):
#     return HttpResponse('Here are the project')
# def project(request, pk):
#     return HttpResponse('Here is your project ' + str(pk))






def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)

    
    context = {'projects': projects,
               'search_query': search_query, 'custom_range': custom_range}
    
    return render(request, 'projects/projects.html', context=context)     # This ensures that we pick the template from the project folder (not from the global template folder)

def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    tags = projectObj.tags.all()
    context = {'project' : projectObj, 'tags' : tags, 'form' : form}

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount                     # property over the model 'Project', called to update the count for each project in the database

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', pk=projectObj.id)
        
    
    return render(request, 'projects/single-project.html',context=context)




@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile      # get the current user profile 
    form = ProjectForm()
    context = {'form' : form}

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        form = ProjectForm(request.POST, request.FILES)       # 'request.FILES' has user uploaded images 
        if form.is_valid:
            project = form.save(commit=False)
            project.owner = profile
            project.save()


            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')       # this is the account page of the user 

    return render(request, 'projects/project_form.html', context=context)




@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk) # Find the project of the current user 
    form = ProjectForm(instance=project)    # Form is pre-filled with some values 
    context = {'form' : form, 'project' : project}

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()  #allowing users to enter the tags on their own and we add those
        form = ProjectForm(request.POST,request.FILES,instance=project)  # This informs which project needs to be updated
        if form.is_valid:
            form.save()             
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)    # create this tag if this tag is not available in our "Tags" table
                project.tags.add(tag)
            # return redirect('project', project.id)       # this is the specific projects page which has been updated.
            return redirect('account')

    return render(request, 'projects/project_form.html', context=context)


@login_required(login_url='login')
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    context = {'object' : project.title}

    if request.method == 'POST':
        project.delete()
        return redirect('projects')


    return render(request, 'delete_object.html', context=context)