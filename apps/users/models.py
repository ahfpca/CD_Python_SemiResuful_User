from __future__ import unicode_literals
from django.db import models
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def record_validator(self, postData):
        errors = {}

        # Validate first_name
        first_name = postData['first_name'].strip()
        if len(first_name) < 1:
            errors['first_name'] = "First name is required!"
        elif len(first_name) < 2:
            errors['first_name'] = "First name should have at least 2 characters!"
        if not charCheckName(first_name):
            errors['first_name'] = "First name accept only alhpabeth and space!"

        # Validate last_name
        last_name = postData['last_name'].strip()
        if len(last_name) < 1:
            errors['last_name'] = "Last name is required!"
        elif len(last_name) < 2:
            errors['last_name'] = "Last name should have at least 2 characters!"
        if not charCheckName(last_name):
            errors['last_name'] = "Last name accept only alhpabeth and space!"
        
        # Validate email
        email = postData['email'].strip()
        if len(email) < 1:
            errors['email'] = "Email is required!"
        elif not email_regex.match(email):
            errors['email'] = "Email is not valid!"

        return errors


class User(models.Model):
    user_id = models.AutoField(primary_key = True)
    first_name = models.CharField(max_length = 60)
    last_name = models.CharField(max_length = 60)
    email = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()


def charCheckName(name):
    for c in name:
        if not c.isalpha() and not c.isspace():
            return False

    return True


def charCheckPassword(pwd):
    result = True
    upper = 0
    lower = 0
    number = 0
    nonAlphaNum = 0

    for c in pwd:
        if c.isupper():
            upper += 1
        if c.islower():
            lower += 1
        if c.isnumeric():
            number += 1
        if not c.isspace() and not c.isalnum():
            nonAlphaNum += 1

    if upper == 0 or lower == 0 or number == 0 or nonAlphaNum == 0:
        return False

    return result
