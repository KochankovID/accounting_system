from django.db import models

from accounting import settings


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_info',
                                null=False)
    profession = models.ForeignKey('Profession', on_delete=models.SET_NULL, related_name='staff', null=True)

    first_name = models.CharField(max_length=256, null=False, blank=False)
    second_name = models.CharField(max_length=256, null=False, blank=False)

    equipment = models.ManyToManyField('Equipment', related_name='owner', through='EmployeeEquipment',
                                       through_fields=('employee', 'equipment'))

    subordinates = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='boss')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profession(models.Model):
    name = models.CharField(max_length=256)


class EmployeeEquipment(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)


class Equipment(models.Model):
    name = models.CharField(max_length=256, null=False)
    type = models.CharField(max_length=256, null=False)
    price = models.IntegerField(null=False)
    period = models.DurationField(null=False)


class OrderEquipment(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)


class Order(models.Model):
    ACTIVE = 'AC'
    RESOLVED = 'RS'

    STATE_CHOICES = [
        ('AC', 'Active'),
        ('RS', 'Resolved'),
    ]

    employee_id = models.ForeignKey('Employee', related_name='orders', null=False, on_delete=models.CASCADE)
    equipment_id = models.ManyToManyField('Equipment', related_name='orders', through='OrderEquipment',
                                          through_fields=('order', 'equipment'))

    state = models.CharField(max_length=2, choices=STATE_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
