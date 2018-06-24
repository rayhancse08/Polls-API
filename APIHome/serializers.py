from rest_framework import serializers
from .models import Poll,Choice,Vote
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vote
        fields='__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    #vote=VoteSerializer(many=True,required=False)
    class Meta:
        model=Choice
        fields='__all__'

class PollSerializer(serializers.ModelSerializer):
    choice=ChoiceSerializer(many=True,required=False,read_only=True)
    class Meta:
        model=Poll
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username','password')
        extra_kwargs={'password':{'write_only':True}}
    def create(self, validated_data):
        user=User(
            username=validated_data['username'],

        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
