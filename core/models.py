from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .constants import parentTabChoices


class User(AbstractBaseUser):

    username = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = "user"


class subTab(models.Model):

    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    testcase_id = models.IntegerField(null=False)
    req_id = models.IntegerField(null=False)
    testcase_result = models.TextField(max_length=255, null=False)
    parent_tab = models.CharField(
        choices=parentTabChoices.choices, max_length=10, null=False)

    class Meta:
        db_table = "sub_tab"
        unique_together = [["testcase_id", "req_id"],
                           ["user_id", "parent_tab"]]


class requirementFilter(models.Model):
    req_id = models.IntegerField(null=False)
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)

    class Meta:
        db_table = "requirement_filter"
