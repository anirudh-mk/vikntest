import uuid
from email.policy import default

from django.db import models

# Create your models here.
class Test(models.Model):
    id = models.AutoField(primary_key=True, default=uuid.uuid4())
    voucher_no = models.CharField(max_length=50, default="")
    voucher_date = models.DateField(auto_now_add=True)

