from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_center', views.add_center, name='add_center'),
    path('delete_center', views.delete_center, name='delete_center'),
    path('add_enterprise', views.add_enterprise, name='add_enterprise'),
    path('delete_enterprise', views.delete_enterprise, name='delete_enterprise'),
    path('add_models', views.add_models, name='add_models'),
    path('delete_models', views.delete_models, name='delete_models'),
    path('add_staffs', views.add_staff, name='add_staff'),
    path('delete_staff', views.delete_staff, name='delete_staff'),
    path('alter_enterprise_info', views.alter_enterprise_info, name='alter_enterprise_info'),
    path('alter_models_info', views.alter_models_info, name='alter_models_info'),
    path('alter_staff_info', views.alter_staff_info, name='alter_staff_info'),
    path('select_center_info', views.select_center_info, name='select_center_info'),
    path('select_enterprise_info', views.select_enterprise_info, name='select_enterprise_info'),
    path('select_models_info', views.select_model_info, name='select_models_info'),
    path('select_staff_info', views.select_staff_info, name='select_staff_info'),
    path('stockIn', views.stockIn, name='stockIn'),
    path('placeOrder', views.placeOrder, name='placeOrder'),
    path('updateOrder', views.updateOrder, name='updateOrder'),
    path('deleteOrder', views.deleteOrder, name='deleteOrder'),
    path('getAllStaffCount', views.getAllStaffCount, name='getAllStaffCount'),
    path('getContractCount', views.getContractCount, name='getContractCount'),
    path('getOrderCount', views.getOrderCount, name='getOrderCount'),
    path('getNeverSoldProductCount', views.getNeverSoldProductCount, name='getNeverSoldProductCount'),
    path('getFavoriteProductModel', views.getFavoriteProductModel, name='getFavoriteProductModel'),
    path('getAvgStockByCenter', views.getAvgStockByCenter, name='getAvgStockByCenter'),
    path('getContractInfo', views.getContractInfo, name='getContractInfo'),
    path('test_input', views.test_input, name='test_input'),
    path('test_output', views.test_output, name='test_output'),
    path('getProductByNumber', views.getProductByNumber, name='getProductByNumber')
]
