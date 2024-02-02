from django.urls import path
from Notes import views

urlpatterns = [
    path('choose_account', views.choose_account, name='choose_account'),
    path('student', views.register_student, name='student'),
    path('choisir_ue', views.choisir_ue, name='choisir_ue'),
    path('teacher', views.register_teacher, name='teacher'),
    path('login_student', views.login_student, name='login_student'),
    path('login_teacher', views.login_teacher, name='login_teacher'),
    path('mainstudent', views.mainstudent, name='mainstudent'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('mainteacher/<str:code>/', views.mainteacher, name='mainteacher'),
    path('click_ue', views.click_ue, name='click_ue'),
    path('choisir_ec', views.choisir_ec, name='choisir_ec'),
    path('student_user_profil', views.student_user_profil, name='student_user_profil'),
    path('teacher_user_profil', views.teacher_user_profil, name='teacher_user_profil'),
]