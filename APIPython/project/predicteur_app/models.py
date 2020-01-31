from django.db import models

# Create your models here.
      
class Incident(models.Model):
    
    active=models.FloatField()
    incident_state=models.FloatField()
    resolved_at=models.FloatField()
    opened_at=models.FloatField()
    number=models.FloatField()
    sys_mod_count=models.FloatField()
    u_priority_confirmation=models.FloatField()
   
    
    duree=models.FloatField(null=True)

    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
            return f'Un incident avec {self.active}'
