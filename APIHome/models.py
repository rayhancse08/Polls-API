from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#Model for poll

class Poll(models.Model):
    question=models.CharField(max_length=100)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    pub_date=models.DateField(auto_now=True)
    def __str__(self):
        return self.question

#Model for choice.

class Choice(models.Model):
    poll=models.ForeignKey(Poll,related_name='choices',on_delete=models.CASCADE)
    choice_text=models.CharField(max_length=100)
    def __str__(self):
        return self.choice_text

#Model for vote.

class Vote(models.Model):
    choice=models.ForeignKey(Choice,related_name='votes',on_delete=models.CASCADE)
    poll=models.ForeignKey(Poll,on_delete=models.CASCADE)
    voted_by=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        unique_together=("poll","voted_by")    # combine poll and voted_by.

    def __str__(self):
        return 'Poll: {0} and {1} vote is {2}'.format(self.poll,self.voted_by,self.choice)





