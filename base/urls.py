from django.urls import path
from . import views

urlpatterns = [
    path('',views.homePage, name="home"),
    path('submit_message',views.submit_message, name="submit_message"),

    path('project_list',views.project_list,name="project_list"),
    path('add_project',views.addProject, name="add_project"),
    path('edit_project/<str:pk>',views.editProject, name="edit_project"),
    path('delete_project/<str:pk>',views.deleteProject.as_view(), name="delete_project"),
    path('project-detail/<str:pk>',views.projectPage, name="project"),
    
    path('edit_aboutMe/<str:pk>',views.editAboutMe, name="edit_AboutMe"),
    
    path('add_skill',views.addSkill, name="add_skill"),
    path('edit_Skill/<str:pk>', views.editSkill, name="edit_skill"),
    path('delete_skill/<str:pk>', views.deleteSkill.as_view(), name="delete_skill"),

    
    path('inbox',views.inboxPage, name="inbox"),
    path('update_is_read',views.update_is_read, name="update_is_read"),
    path('delete_message/<str:pk>',views.deleteMessage.as_view(), name="delete_message"),
    path('delete_all_message',views.deleteAllMessage.as_view(), name="delete_all_messages"),
]
