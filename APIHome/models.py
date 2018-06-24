from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Poll(models.Model):
    question=models.CharField(max_length=100)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    pub_date=models.DateField(auto_now=True)
    def __str__(self):
        return self.question

class Choice(models.Model):
    poll=models.ForeignKey(Poll,related_name='choices',on_delete=models.CASCADE)
    choice_text=models.CharField(max_length=100)
    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    choice=models.ForeignKey(Choice,related_name='votes',on_delete=models.CASCADE)
    poll=models.ForeignKey(Poll,on_delete=models.CASCADE)
    voted_by=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        unique_together=("poll","voted_by")

'''     
class User(models.Model):
    user=models.CharField(max_length = 50,primary_key=True)
    password=models.CharField(max_length = 50)
    class Meta:
      db_table = "User"

'''




