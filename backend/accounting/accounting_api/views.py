from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from accounting_api.models import Equipment, Profession, Order
from accounting_api.serializers import EmployeerRegistrationSerializer, EquipmentSerializer, ProfessionSerializer, \
    OrderSerializer


class EmployeerRegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmployeerRegistrationSerializer


class EquipmentCRUDView(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ProfessionCRUDView(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class OrderCRUDView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
