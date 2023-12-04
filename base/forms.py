from django.forms import ModelForm
from django import forms
from .models import Project, Message, Skill, AboutMe

class ProjectForm(ModelForm):
    languages = forms.CharField(max_length=255, required=False, label="Programming Languages(comma-separated)")
    technologies = forms.CharField(max_length=255, required=False, label="Technology Used(comma-separated)")

    class Meta:
        model = Project
        fields = ['title','thumbnail','body','source_code','live_website','languages','technologies']

    def __init__(self,*args, **kwargs):
        super(ProjectForm,self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class':'form-control','placeholder':'Title'})
        
        self.fields['body'].widget.attrs.update(
            {'class':'form-control','placeholder':'Description'})

        self.fields['source_code'].widget.attrs.update(
            {'class':'form-control','placeholder':'Source_Code_Link'})

        self.fields['live_website'].widget.attrs.update(
            {'class':'form-control','placeholder':'Live Website URL'})
        
        self.fields['languages'].widget.attrs.update(
            {'class':'form-control','placeholder':'Languages That You used'})
        
        self.fields['technologies'].widget.attrs.update(
            {'class':'form-control','placeholder':'Technologies That You used'})
        
    
    def clean_languages(self):
        languages = self.cleaned_data.get('languages')
        if languages:
            # Split the input by a delimiter (e.g., comma)
            languages_list = [lang.strip() for lang in languages.split(',')]
            return languages_list
        else:
            return []
        
    def clean_technologies(self):
        technologies = self.cleaned_data.get('technologies')
        if technologies:
            # Split the input by a delimiter (e.g., comma)
            technologies_list = [tech.strip() for tech in technologies.split(',')]
            return technologies_list
        else:
            return []


class AboutForm(ModelForm):
    class Meta:
        model = AboutMe
        fields = ['body']

    def __init__(self,*args, **kwargs):
        super(AboutForm,self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update(
            {'class':'form-control','placeholder':'Description'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        exclude = ['is_read']
        labels = {
            'body' : ('Message'),
        }

    def __init__(self,*args, **kwargs):
        super(MessageForm,self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class':'form-control','placeholder':'Keval Prajapati'})
        
        self.fields['email'].widget.attrs.update(
            {'class':'form-control','placeholder':'kevalprajapati1001@gmail.com'})
        
        self.fields['subject'].widget.attrs.update(
            {'class':'form-control','placeholder':'Your Subject'})
        
        self.fields['body'].widget.attrs.update(
            {'class':'form-control','placeholder':'Enter your Message'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['logo']

        labels = {
            'body' : ('Description'),
        }

    def __init__(self,*args, **kwargs):
        super(SkillForm,self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class':'form-control','placeholder':'Title'})
        
        self.fields['body'].widget.attrs.update(
            {'class':'form-control','placeholder':'Description'})

