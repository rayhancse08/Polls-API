from rest_framework import serializers
from .models import Poll,Choice,Vote
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

#serialize Vote model

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vote
        fields='__all__'

#serialize Choice model

class ChoiceSerializer(serializers.ModelSerializer):
    vote=VoteSerializer(many=True,required=False,read_only=True)
    class Meta:
        model=Choice
        fields='__all__'

#Serialize Poll model

class PollSerializer(serializers.ModelSerializer):
    choice=ChoiceSerializer(many=True,required=False,read_only=True)
    class Meta:
        model=Poll
        fields='__all__'

#Serialize User model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username','password')
        extra_kwargs={'password':{'write_only':True}}
    def create(self, validated_data):                                       #override customize create behaviour
        user=User(
            username=validated_data['username'],                           #validate user

        )
        user.set_password(validated_data['password'])                    #validate password
        user.save()
        Token.objects.create(user=user)                                 #create token for respective user.
        return user
