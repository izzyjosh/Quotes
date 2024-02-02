from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
        path("",views.UserList.as_view(),name="user-list"),
        path("user_detail/<uuid:pk>/",views.UserDetail.as_view(),name="user-detail"),
        path('api-token-auth/', auth_views.obtain_auth_token,name="obtain-token"),
        path("signup/",views.RegisterUser.as_view(),name="signup"),
        path("notes/",views.NoteView.as_view(),name="notes"),
        path("notes-details/<int:pk>/",views.NoteDetail.as_view(),name="note-detail"),
        ]


urlpatterns = format_suffix_patterns(urlpatterns)
