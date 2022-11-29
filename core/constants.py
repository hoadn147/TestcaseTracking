from django.db import models

class parentTabChoices(models.TextChoices):
        Unit  = 'UNIT'
        Complete =  'COMPLETE'
        Component = 'COMPONENT'
        Domain = 'DOMAIN'

parent_tab_name = ['UNIT', 'COMPLETE', 'COMPONENT', 'DOMAIN']


class testCaseResult(models.TextChoices):
        true = 'Pass'
        false=  'False' 
        
test_case_result = ['Pass' , 'False']