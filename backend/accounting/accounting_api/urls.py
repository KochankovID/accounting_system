from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import EmployeerCRUDView, EquipmentCRUDView, ProfessionCRUDView, OrderCRUDView, EmployeerGetInfoView

router = DefaultRouter()
router.register('employees', EmployeerCRUDView, basename='employee')
router.register('info_employees', EmployeerGetInfoView, basename='info_employee')
router.register('equipments', EquipmentCRUDView, basename='equipment')
router.register('professions', ProfessionCRUDView, basename='profession')
router.register('orders', OrderCRUDView, basename='order')

urlpatterns = [
    *router.urls
]
