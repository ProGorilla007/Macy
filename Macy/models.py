from django.db import models
import uuid


class User(models.Model):
    my_id = uuid.uuid4()
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=4)


class Links(models.Model):
    MEDIA_CHOICES = [
        ('TWT', 'Twitter'),
        ('INS', 'Instagram'),
        ('TIK', 'TikTok'),
        ('FBK', 'Facebook'),
        ('YTB', 'Youtube'),
        ('LNE', 'LINE'),
        ('MIS', 'Other'),
    ]

    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE)

    media_choice = models.CharField(
        max_length=3,
        choices=MEDIA_CHOICES,
        default='MIS',
    )

    link = models.URLField(max_length=255)


# ***git set up command cheat list***
# $ git config --global user.name "Your name here"
# $ git config --global user.email "your_email@example.com"
# git remote add origin https://github.com/ProGorilla007/Macy.git
# git remote -v
