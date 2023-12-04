from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import ProfilePicture, Project, Skill, Message, Skill, AboutMe, Language, Technology
from .forms import ProjectForm, MessageForm, SkillForm, AboutForm
from django.views.generic.edit import DeleteView
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

#  Custom function
from .func import calculate_unread_messages

# Create your views here.

'''
    Home Page functions or class
'''
def homePage(request):
    profile_pic = ProfilePicture.objects.order_by('-created_at').first()

    projects = Project.objects.all()
    val = False
    if Project.objects.all().count() > 6:
        projects = Project.objects.all()[:6]
        val = True

    about_me = AboutMe.objects.all()


    detailedSkills = Skill.objects.exclude(body='').order_by('created_at')
    skills = Skill.objects.filter(body='')

    
    unreadMessages = calculate_unread_messages()
    dot = True if unreadMessages > 0 else False


    form = MessageForm()
    message = ''


    context = {
        'profile_pic':profile_pic,
        'projects':projects,
        'about_me':about_me,
        'detailedSkills' : detailedSkills,
        'skills' : skills,
        'val':val,
        'unreadMessages':unreadMessages,
        'form':form,
        'dot':dot,
        'message' : message,
        'room_name':"broadcast",
    }

    return render(request,'base/home.html',context)

def submit_message(request):
    form = MessageForm()
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            unreadMessages = Message.objects.filter(is_read = False).count()
            message = "Your Message Has been Sent!"
            return JsonResponse({'message':message,'unreadMessages':unreadMessages})


''' 
Add project Function
'''
@login_required(login_url="home")
def addProject(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()  # Save the project first

            # Get the list of languages entered by the user
            languages_list = form.cleaned_data.get('languages')

            # Get the list of technologies entered by the user
            technologies_list = form.cleaned_data.get('technologies')

            # Create Language objects and associate them with the project
            for language_name in languages_list:
                language, created = Language.objects.get_or_create(name=language_name.strip())
                project.languages.add(language)

            for technology_name in technologies_list:
                technology, created = Technology.objects.get_or_create(name=technology_name.strip())
                project.Technologies.add(technology)

            return redirect('home')
    else:
        form = ProjectForm()

    context = {'form': form}
    return render(request, 'base/project_form.html', context)

'''
Edit Project Function
'''
@login_required(login_url="home")
def editProject(request, pk):
    project = get_object_or_404(Project, id=pk)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()  # Save the project first

            # Get the list of languages entered by the user
            languages_list = form.cleaned_data.get('languages')

            # Get the list of technologies entered by the user
            technologies_list = form.cleaned_data.get('technologies')

            # Create Language objects and associate them with the project
            for language_name in languages_list:
                language, created = Language.objects.get_or_create(name=language_name.strip())
                project.languages.add(language)

            for technology_name in technologies_list:
                technology, created = Technology.objects.get_or_create(name=technology_name.strip())
                project.Technologies.add(technology)

            return redirect('home')
            
    else:
        languages = ", ".join([language.name for language in project.languages.all()])
        technologies = ", ".join([technology.name for technology in project.Technologies.all()])
        initial_data = {'languages': languages,'technologies':technologies}
        form = ProjectForm(instance=project, initial=initial_data)

    context = {'form': form}
    return render(request, 'base/update_form.html', context)


'''
Delete Project Class
'''
@method_decorator(login_required(login_url="home"), name="dispatch")
class deleteProject(LoginRequiredMixin,DeleteView):
    model = Project
    success_url = reverse_lazy('home')
    template_name = "base/delete_form.html"

    def delete(self, request, *args, **kwargs):
        project = self.get_object()
        messages.success(request, f"Project '{project.name}' has been deleted successfully.")
        return super().delete(request, *args, **kwargs)



'''
Edit About Me Function
'''
@login_required(login_url="home")
def editAboutMe(request,pk):
    aboutMe = AboutMe.objects.get(id=pk)
    form = AboutForm(instance=aboutMe)

    if request.method == "POST":
        form = AboutForm(request.POST, request.FILES,instance=aboutMe)
        if form.is_valid():
            form.save()
            messages.success(request,'Project Has Been updated!')
            return redirect('home')
    context = {'form':form}
    return render(request,'base/about_form.html',context)

'''
Add Skill Function
'''
@login_required(login_url="home")
def addSkill(request):
    form = SkillForm

    if request.method == "POST":
        form = SkillForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Skill Have Been Added!')
            return redirect('home')
    context = {'form':form}
    return render(request,'base/skill_form.html',context)

'''
EditSkill Function
'''
@login_required(login_url="home")
def editSkill(request,pk):
    
    aboutMe = Skill.objects.get(id=pk)
    form = SkillForm(instance=aboutMe)

    if request.method == "POST":
        form = SkillForm(request.POST, request.FILES,instance=aboutMe)
        if form.is_valid():
            form.save()
            messages.success(request,'Project Has Been updated!')
            return redirect('home')
    context = {'form':form}
    return render(request,'base/edit_skill.html',context)

'''
Delete SKill Class
'''
@method_decorator(login_required(login_url="home"), name="dispatch")
class deleteSkill(LoginRequiredMixin,DeleteView):
    model = Skill
    success_url = reverse_lazy('home')
    template_name = 'base/home.html'

    def get_object(self,queryset=None):
        return get_object_or_404(Skill,pk=self.kwargs['pk'])
    
    def delete(self, request, *args, **kwargs):
        message = self.get_object()
        messages.success(request, f"Message '{message.name}' has been deleted successfully.")
        return super().delete(request, *args, **kwargs)


''' 
Individual Project Page 
'''
def projectPage(request, pk):
    project = Project.objects.get(id=pk)
    languages = project.languages.all()
    Technologies = project.Technologies.all()
    from_project_list = request.GET.get('from_project_list', False)
    context = {
        'project':project,
        'languages':languages,
        'Technologies':Technologies,
        'from_project_list':from_project_list,
    }
    return render(request,'base/project_detail_page.html',context)


'''
Project List Page
'''
def project_list(request):
    projects = Project.objects.all()
    context = {
        'projects':projects,
    }
    return render(request,'base/project_list.html',context)


'''
Inbox Page For Admin
'''
@login_required(login_url="home")
def inboxPage(request):
    inbox = Message.objects.all().order_by('is_read','-created_at')
    unreadMessages = Message.objects.filter(is_read = False).count()
    if Message.objects.all().count() == Message.objects.exclude(is_read=False).count():
        inbox = Message.objects.all().order_by('-created_at')

    context = {
        'inbox' : inbox,
        'unreadMessages' : unreadMessages,
        'room_name':"broadcast",
    }
    return render(request,'base/inbox.html',context)

'''
Updating Is read function when admin view message
'''
def update_is_read(request):    
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        message = Message.objects.get(id=message_id)
        message.is_read = True
        message.save()
        return JsonResponse({'success': 'Message marked as read'})

    return JsonResponse({'error': 'Invalid request method'})


'''
Delete Message Class
'''
@method_decorator(login_required(login_url="home"), name="dispatch")
class deleteMessage(LoginRequiredMixin,DeleteView):
    model = Message
    success_url = reverse_lazy('inbox')
    template_name = 'base/inbox.html'

    def get_object(self,queryset=None):
        return get_object_or_404(Message,pk=self.kwargs['pk'])
    
    def delete(self, request, *args, **kwargs):
        message = self.get_object()
        messages.success(request, f"Message '{message.name}' has been deleted successfully.")
        return super().delete(request, *args, **kwargs)
    
'''
Delete All Message Class
'''
@method_decorator(login_required(login_url="home"), name="dispatch")
class deleteAllMessage(LoginRequiredMixin,DeleteView):
    
    def post(self, request):
        Message.objects.all().delete()
        return redirect('inbox')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, f"All message has been deleted successfully.")
        return super().delete(request, *args, **kwargs)
