from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = (Q(first_person=user) | Q(second_person=user)) & Q(blocked=False)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    blocked = models.BooleanField(default=False)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']
        
    def __str__(self):
        return f"{self.first_person} & {self.second_person}'s Thread"


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.thread} - {self.user}'s message"
    

class ReportContact(models.Model):
    complainant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_complainant')
    offender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_offender')
    subject = models.CharField(max_length=50)
    reason = models.TextField()
    evidence = models.ImageField(upload_to='report_pictures')
    timestamp = models.DateTimeField(auto_now_add=True)
    