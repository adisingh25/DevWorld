from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProjects(request):

    search_query = ''

    if request.GET.get('text'):
        search_query = request.GET.get('text')

    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )
    return projects, search_query

def paginateProjects(request, projects, results):

    page = request.GET.get('page')
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:                    # when we are at the base url (show page number 1)
        page = 1
        projects = paginator.page(page)
    except EmptyPage:                           # if we access page number 1000 which does not exist
        page = paginator.num_pages
        projects = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)       # decide the range of pages that we see on the wepage. Eg- ...9 10 11 12 13(Current Page) 14 15 16 17
                                                      # rolling window for the pages that we are accessing 
    return custom_range, projects
