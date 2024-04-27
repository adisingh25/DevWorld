from django.forms import ModelForm 
from .models import Project,Review
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'featured_image', 'demo_link', 'source_link']
        
        # Removed 'tags' from the above list 
        widgets = {
            'tags' : forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        
        # Using a for loop to set the class for each field
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'input'})

        #self.fields['title'].widget.attrs.update({'class' : 'input', 'placeholder' : 'Add a title'})
            

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {                                          #custom labels
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})