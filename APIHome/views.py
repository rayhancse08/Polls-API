from django.shortcuts import render,HttpResponse
from .models import Poll,Vote,Choice
from rest_framework import generics
from .serializers import PollSerializer,VoteSerializer,ChoiceSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404,get_list_or_404
from rest_framework import permissions

# Create your views here.

def home(request):
    return HttpResponse("This is test")

class PollViewSet(viewsets.ModelViewSet):                                   #viewset when both(list,detail)view classes have same serializer.
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def destroy(self, request, *args, **kwargs):                            #define destroy method for delete poll
        poll=Poll.objects.get(pk=self.kwargs['pk'])                         #get poll pk
        if not request.user==poll.created_by:                               # check requested user create poll or not.If not raise an error
            raise PermissionError("You can not delete this post")
        return super().destroy(request,*args,**kwargs)                      #call parent class destry method after prefiltering



class ChoiceList(generics.ListCreateAPIView):                               #display and create choice list.
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])          # filter pollwise choice list.
        return queryset
    '''
    def get(self, request, *args, **kwargs):
        choice = get_list_or_404(Choice,poll_id=self.kwargs['pk'])
        data=ChoiceSerializer(choice).data
        return Response(data)
    '''

    def post(self, request, *args, **kwargs):                                 # method for creating new choice
       poll = Poll.objects.get(pk=self.kwargs["pk"])
       if not request.user == poll.created_by:                                 # only poll creator can create choice.
         raise PermissionError("You can not create choice for this poll.")
       return super().post(request, *args, **kwargs)                            # call super class post method


class ChoiceDetail(APIView):
    serializer_class = ChoiceSerializer


    def get(self,request,*args,**kwargs):                                       #get method for retriving data
        choice=get_object_or_404(Choice,id=self.kwargs['choice_pk'],poll_id=self.kwargs['pk'])
        data=ChoiceSerializer(choice).data                                      #serialize data
        return Response(data)
 
    
    def put(self,request,pk,choice_pk):
        choice = get_object_or_404(Choice, id=choice_pk, poll_id=pk)
        serializer = ChoiceSerializer(choice,data=request.data)                             #serialize data
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)                                                #save and response data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):                                                  #delete method for deleting object
        choice = Choice.objects.filter(id=self.kwargs["choice_pk"],poll_id=self.kwargs["pk"])    #get object
        choice.delete()                                                                          # delete object
        #return super().destroy(request,*args,*kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)



#class for creating vote.
class CreateVote(APIView):

    def get(self, request, pk, choice_pk):                                                      #get poll id,choice_id and create vote.
        #voted_by = request.data.get("voted_by")
        voted_by=self.request.user.id
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly)
    serializer_class = UserSerializer

    def post(self,request):
        self.username=request.data.get('username')
        self.password=request.data.get('password')
        user=authenticate(username=self.username,password=self.password)
        if user:
            return Response({"token":user.auth_token.key})
        else:
            return Response({'error':'Wrong Credintial'},status=status.HTTP_400_BAD_REQUEST)