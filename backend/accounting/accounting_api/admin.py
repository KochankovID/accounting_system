from django.contrib import admin

from .models import Employee, Order, Equipment, Profession, EmployeeEquipment


class EquipmentInline(admin.TabularInline):
    model = EmployeeEquipment


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    inlines = [
        EquipmentInline,
    ]


admin.site.register(Order)
admin.site.register(Equipment)
admin.site.register(Profession)
