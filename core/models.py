from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .constants import parentTabChoices


class User(AbstractBaseUser):

    username = models.CharField(max_length=50, null=False, unique=True)
    
    USERNAME_FIELD = 'username'

    class Meta:
        db_table = "user"


class subTab(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    testcase_id = models.TextField(max_length= 255,null=False)
    req_id = models.TextField(max_length=255,null=False)
    testcase_result = models.TextField(max_length=255, null=False)
    parent_tab = models.CharField(
        choices=parentTabChoices.choices, max_length=10, null=False)
    filter_id = models.IntegerField(null=True)
    
    def save(self, *args, **kwargs):  # new
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        db_table = "sub_tab"
        unique_together = [["testcase_id", "req_id"]]


class requirementFilter(models.Model):
    req_id = models.TextField(max_length=255,null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    filter_name = models.TextField(max_length=100, null=False, unique=True )

    class Meta:
        db_table = "requirement_filter"
