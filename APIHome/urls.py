from django.urls import path
from APIHome import views
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls


schema_view = get_swagger_view(title='Polls API')
router=DefaultRouter()
router.register('polls',views.PollViewSet,base_name='polls')
urlpatterns=[
    path('',views.home),
    #path('poll/',views.PoolList.as_view(),name='poll_list'),
    path('poll/<int:pk>/choice/',views.ChoiceList.as_view(),name='choice_list'),
    path('poll/<int:pk>/choice/<int:choice_pk>/vote/',views.CreateVote.as_view(),name='create_vote'),
    path('choice/',views.ChoiceList.as_view(),name='choice_list'),
    path('vote/',views.CreateVote.as_view(),name='create_vote'),
    path('users/',views.UserCreate.as_view(),name='user_create'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('swagger-docs/', schema_view),
    path('docs/', include_docs_urls(title='Polls API')),

]
urlpatterns+=router.urls


