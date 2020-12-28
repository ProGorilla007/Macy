from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.TextField



$ git config --global user.name "Your name here"
$ git config --global user.email "your_email@example.com"

git remote add origin https://github.com/ProGorilla007/Macy.git

git remote -v
sfdafds