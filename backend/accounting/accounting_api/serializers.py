from collections import OrderedDict

from django.contrib.auth.models import User
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, Serializer

from accounting_api.models import Employee, Equipment, Profession, Order, EmployeeEquipment
from authentication.serializers import RegistrationSerializer


class EquipmentSerializer(ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'


class EquipmentWithAmountSerializer(ModelSerializer):
    equipment = EquipmentSerializer()

    class Meta:
        model = EmployeeEquipment
        fields = ('amount', 'equipment')


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
    equipment = PrimaryKeyRelatedField(many=True, required=False, queryset=Equipment.objects.all(), write_only=True)

    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data: OrderedDict):
        user = User.objects.create_user(**validated_data['user'])

        del validated_data['user']
        employee = Employee.objects.create(user_id=user.id, **validated_data)
        return employee


class EmployeerGetInfoSerializer(ModelSerializer):
    user = RegistrationSerializer(read_only=True)
    equipments = EquipmentWithAmountSerializer(many=True, read_only=True, source='employeeequipment_set')
    profession = ProfessionSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'
