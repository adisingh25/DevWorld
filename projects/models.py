from django.db import models
import uuid
from users.models import Profile
# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)  #if the owner is deleted, delete the project also 
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="icon.svg")   # This is present in static/images folder or directory
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)        # this is many to many relationship i.e one Project can have many tags
    votes_total = models.IntegerField(default=0, null=True, blank=True)
    votes_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 
    # we are overidding the default id that would have been given by the database and 
    #also setting this field as our primary key and preventing anyone to alter our values

    def __str__(self):
        return self.title                # python way to show the Object in DB, using Title as the identifier.
    
    class Meta:
        ordering = ['-votes_ratio', '-votes_total', '-created']          # store and retrive on the basis of date of creation (lastest one will be at the top)


    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url
    

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes/totalVotes) * 100
        self.votes_total = totalVotes
        self.votes_ratio = ratio
        self.save()


    @property
    def reviewers(self):                      # gives all the people's id who have voted for this project
        queryset = self.review_set.all().values_list('owner__id', flat=True)         # 'flat' ensures that we get a true list and not an object
        return queryset

        
    



class Review(models.Model):
    #TUPLE/ENUM 
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE) # Delete the review once the Project is deleted # Foreign Key establishes a one to many relationship
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE) #Makes this field a drop-down menu 
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 

    class Meta:
        unique_together = [['owner', 'project']]    
        # the owner and project combination remains unique together
        # ensures only one review from one profile 

    def __str__(self):
        return self.value     
    





class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 

    def __str__(self):
        return self.name  