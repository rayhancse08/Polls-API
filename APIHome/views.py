from django.shortcuts import render,HttpResponse
from .models import Poll,Vote,Choice
from rest_framework import generics
from .serializers import PollSerializer,VoteSerializer,ChoiceSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth import authenticate
# Create your views here.
def home(request):

    return HttpResponse("This is test page")
'''
class PoolList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
'''

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    def destroy(self, request, *args, **kwargs):
        poll=Poll.objects.get(pk=self.kwargs['pk'])
        if not request.user==poll.created_by:
            raise PermissionError("You can not delete this post")
        return super().destroy(request,*args,**kwargs)

class ChoiceList(generics.ListCreateAPIView):

    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
        return queryset
    serializer_class = ChoiceSerializer


    def post(self, request, *args, **kwargs):
       poll = Poll.objects.get(pk=self.kwargs["pk"])
       if not request.user == poll.created_by:
         raise PermissionError("You can not create choice for this poll.")
       return super().post(request, *args, **kwargs)


class CreateVote(APIView):
    def get(self, request, pk, choice_pk):
        voted_by=request.data.get("voted_by")
        #voted_by=self.get("voted_by")
        data={'choice':choice_pk,'poll':pk,'voted_by':voted_by}
        serializer=VoteSerializer(data=data)
        if serializer.is_valid():
            vote=serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = ()
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        user=authenticate(username=username,password=password)
        if user:
            return Response({"token":user.auth_token.key})
        else:
            return Response({'error':'Wrong Credintial'},status=status.HTTP_400_BAD_REQUEST)