from django.core.exceptions import ObjectDoesNotExist
from django.db import models

class OrderField(models.PositiveIntegerField):
    
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)
    
    
    def pre_save(self, model_instace, add):
        if getattr(model_instace, self.get_attname()) is None:
            try:
                qs = self.model.objects.all()
                
                if self.for_fields:
                    query = {
                        field: getattr(model_instace, field)
                        for field in self.for_fields
                    }
                    
                    qs = qs.filter(**query)
                
                last_item = qs.latest(self.get_attname())    
                value = getattr(last_item, self.get_attname()) + 1
                
            except ObjectDoesNotExist:
                value = 0
                
            setattr(model_instace, self.attname, value)
            return value
    
        else:               
            return super().pre_save(model_instace, add)