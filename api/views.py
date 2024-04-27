
from rest_framework.response import Response
from .serializers import ProjectSerializer
from rest_framework.decorators import api_view, permission_classes
from projects.models import Project,Review,Tag
from rest_framework.permissions import IsAuthenticated, IsAdminUser

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]
    return Response(routes)



# getting all the projects
@api_view(['GET'])               # our decorators
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)   # coverting to JSON data (many=True means we are serializing many object)
    return Response(serializer.data)




# getting a single project
@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request,pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile                            # this comes from the token that we will pass and not from the session based logic
    data = request.data 

    review, created = Review.objects.get_or_create(        # Try to fetch the review of the project from the ownwer.
        owner=user,                                        # If not found then, create a new review with the owner
        project=project,    
    )

    review.value = data['value']
    review.save()

    project.getVoteCount                                  # To update the vote count and vote_ratio

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)



@api_view(['DELETE'])
def removeTag(request):
    tagId = request.data['tag']
    projectId = request.data['project']

    project = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id=tagId)

    project.tags.remove(tag)

    return Response('Tag was deleted!')