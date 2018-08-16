from django.urls import path
from APIHome import views
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls


schema_view = get_swagger_view(title='Polls API')                                                   #is used for swagger-docs path
router=DefaultRouter()
router.register('polls',views.PollViewSet,base_name='polls')
                                                                                                    #route poll viewset using router.
urlpatterns=[

    path('polls/<int:pk>/choice/',views.ChoiceList.as_view(),name='choice_list'),                               #check choice list
    path('polls/<int:pk>/choice/<int:choice_pk>/',views.ChoiceDetail.as_view(),name='choice_detail'),
    path('polls/<int:pk>/choice/<int:choice_pk>/vote/',views.CreateVote.as_view(),name='create_vote'),          #create vote url
    path('users/',views.UserCreate.as_view(),name='user_create'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('swagger-docs/', schema_view),
    path('docs/', include_docs_urls(title='Polls API')),

]
urlpatterns+=router.urls                                                                                    #add router urls in urlpatterns


