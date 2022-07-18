from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('edit-user/', views.EditUserView.as_view(), name='edit-user'),
    path('author/<str:pk>/', views.AuthorView.as_view(), name='author'),

    path('course-info/<str:pk>/', views.CourseInfoView.as_view(), name='course-info'),
    path('join-course/<str:pk>/', views.JoinCourseView.as_view(), name='join-course'),
    path('under-construction/', views.UnderConstructionView.as_view(),
         name='under-construction'),

    path('course/<str:pk>/', views.CourseMainView.as_view(), name='course-main'),
    path('course/<str:pk>/<str:pk2>/', views.CourseView.as_view(), name='course'),
    path('course-create/', views.CourseCreateView.as_view(), name='course-create'),
    path('course-edit/<str:pk>/', views.CourseEditView.as_view(), name='course-edit'),

    path('req-del/<str:pk>/', views.ReqDelView.as_view(), name='req-del'),
    path('skill-del/<str:pk>/', views.SkillDelView.as_view(), name='skill-del'),
    path('chapter-del/<str:pk>/', views.ChapterDelView.as_view(), name='chapter-del'),

    path('chapter-edit/<str:pk>/',
         views.ChapterEditView.as_view(), name='chapter-edit'),
    path('lesson-add/<str:pk>/', views.LessonAddView.as_view(), name='lesson-add'),
    path('lesson-del/<str:pk>/', views.LessonDelView.as_view(), name='lesson-del'),

    path('search/', views.SearchView.as_view(), name='search'),
]
