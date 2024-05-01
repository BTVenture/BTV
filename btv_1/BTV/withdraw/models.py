from django.db import models

import uuid


class Withdraw_History(models.Model):
    withdraw_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('authenticate.User_Model', on_delete=models.CASCADE)
    amount = models.IntegerField(blank=False, null=False)
    request_date = models.DateTimeField(auto_now_add=True)
    account_number = models.TextField(blank=True, null=True)
    ifsc_code = models.TextField(blank=True, null=True)
    status_choices = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"
