from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('', views.api_overview),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', views.UserApiView.as_view()),
    path('transfer/', views.TransferAPIView.as_view()),   
    path('made-transfer-receipts/', views.MadeTransferReceipts.as_view(), name="made_transfers_list"),
    path('made-transfer-receipts/<int:pk>/', views.MadeTransferReceipts.as_view(), name="made_transfer_detail"),
    path('incoming-transfer-receipts/', views.IncomingTransferReceipts.as_view(), name="incoming_transfers_list"),
    path('incoming-transfer-receipts/<int:pk>/', views.IncomingTransferReceipts.as_view(), name="incoming_transfer_detail"),
]