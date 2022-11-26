from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .constants import parentTabChoices, parent_tab_name


class User(AbstractBaseUser):

    username = models.CharField(max_length=50, null=False, unique=True)

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = "user"

    def create_relative_parent_tab(self):  # new
        parent_tab = []
        for tab in parent_tab_name:
            parent_tab.append(
                ParentTab(user_id=self.id, tab_name=tab)
            )
        ParentTab.objects.bulk_create(parent_tab)


class ParentTab(models.Model):
    tab_name = models.CharField(
        choices=parentTabChoices.choices, max_length=10, null=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='parent_tab')

    class Meta:
        db_table = "parent_tab"
        unique_together = ['tab_name', 'user']


class subTab(models.Model):
    testcase_id = models.TextField(max_length=255, null=False)
    req_id = models.TextField(max_length=255, null=False)
    testcase_result = models.TextField(max_length=255, null=False)
    parent_tab = models.ForeignKey(
        ParentTab, on_delete=models.CASCADE, related_name='sub_tab', null=False)

    def save(self, *args, **kwargs):  # new
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        db_table = "sub_tab"
        unique_together = [["testcase_id", "req_id"]]


class requirementFilter(models.Model):
    parent_tab = models.ForeignKey(
        ParentTab, on_delete=models.CASCADE, related_name='requirement_filter')
    req_id = models.TextField(max_length=255, null=False)
    filter_name = models.TextField(max_length=100, null=False)

    class Meta:
        db_table = "requirement_filter"
        unique_together = ['filter_name', 'parent_tab']
        
