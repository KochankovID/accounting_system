from django.contrib import admin

from .models import Employee, Order, Equipment, Profession

admin.site.register(Employee)
admin.site.register(Order)
admin.site.register(Equipment)
admin.site.register(Profession)
