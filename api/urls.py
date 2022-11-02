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
    path('transfer/<int:user_id>/', views.TransferAPIView.as_view()),   
    path('made-transfer-receipts/<int:user_id>/', views.made_transfer_receipts),
    path('made-transfer-receipt-detail/<int:user_id>/<int:pk>/', views.made_transfer_receipt_detail),
    path('incoming-transfer-receipts/<int:user_id>/', views.incoming_transfer_receipts),
    path('incoming-transfer-receipt-detail/<int:user_id>/<int:pk>/', views.incoming_transfer_receipt_detail)
]