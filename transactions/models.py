from django.db import models

class Transaction(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    amount = models.FloatField()
    type = models.CharField(max_length=255)
    parent = models.ForeignKey('self', related_name= 'child',on_delete=models.DO_NOTHING, null=True, blank=True)
    transaction_sum = models.FloatField(editable=False, default=0)

    def __str__(self):
        return f"id: {self.id},\n amount: {self.amount},\n type: {self.type}"

    def to_json(self):
        response = {}
        response["amount"] = self.amount
        response["type"] = self.type
        if(self.parent):
            response["parent_id"] = self.parent_id
        return response
    
    def parent_id(self):
        if(self.parent):
            self.patent.id
        else:
            return None
    
    def save(self, *args, **kwargs):
        delta_amount = 0.0
        first_update = kwargs.pop("first_update", True)
        if(self.transaction_sum == 0.0):
             self.transaction_sum = self.amount
             delta_amount = self.amount
        super().save(*args, **kwargs)
        if(first_update):
            self.custom_post_save_operations(delta_amount)

    def custom_post_save_operations(self, delta_amount):
        if(self.parent and delta_amount!=0.0):
            self.parent.transaction_sum += delta_amount
            self.parent.save(first_update=False)
            self.parent.custom_post_save_operations(delta_amount)
