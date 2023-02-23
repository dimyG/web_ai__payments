from django.db import models


class Payment(models.Model):
    user_id = models.IntegerField(null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.date} {self.pk}| user: {self.user_id} amount: {self.amount}'


