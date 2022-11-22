from django.db import models

class parentTabChoices(models.TextChoices):
        Unit  = 'UNIT'
        Complete =  'COMPLETE'
        Component = 'COMPONENT'
        Domain = 'DOMAIN'