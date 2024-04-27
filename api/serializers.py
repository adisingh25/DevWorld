# serializer converts the python data[python objects and list] to JSON Data

from rest_framework import serializers
from projects.models import Project,Tag,Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'



class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)                #only a single owner on each project i.e many = False
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'                                # we can also explicitly specify the fields that we want to serialize

    
    def get_reviews(self, obj):                           # this has to start with 'get' compulsorily
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

# By default, it will only serialize the Project and not other tables associated with like tags,owners etc.
# Instead of showing the actual values, it will just show us the 'id' of those (id of tag and owner)
# To deal with this, we need to add 'nested serializers'.
        






