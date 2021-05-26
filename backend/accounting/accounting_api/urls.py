from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import EmployeerRegisterView, EquipmentCRUDView, ProfessionCRUDView, OrderCRUDView

router = DefaultRouter()
router.register('equipments', EquipmentCRUDView, basename='equipment')
router.register('professions', ProfessionCRUDView, basename='profession')
router.register('orders', OrderCRUDView, basename='order')

urlpatterns = [
    path('register/', EmployeerRegisterView.as_view(), name='employee_register'),
    *router.urls
]
