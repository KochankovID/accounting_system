from collections import OrderedDict

from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, CharField

from accounting_api.models import Employee, Equipment, Profession, Order
from authentication.serializers import RegistrationSerializer


class EquipmentSerializer(ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'


class ProfessionSerializer(ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    employee_id = PrimaryKeyRelatedField(queryset=Employee.objects.all())
    equipment_id = PrimaryKeyRelatedField(many=True, queryset=Equipment.objects.all(), required=False)

    class Meta:
        model = Order
        fields = '__all__'


class EmployeerRegistrationSerializer(ModelSerializer):
    user = RegistrationSerializer()
    equipment = PrimaryKeyRelatedField(many=True, required=False, queryset=Equipment.objects.all())

    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data: OrderedDict):
        user = User.objects.create_user(**validated_data['user'])

        del validated_data['user']
        employee = Employee.objects.create(user_id=user.id, **validated_data)
        return employee
