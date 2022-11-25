import jwt

from pointsTransfer.settings import SECRET_KEY
from .models import Receipt, User
from .serializers import ReceiptSerializer, TransferDataSerializer, UserSerializer

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_400_BAD_REQUEST, 
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
)

# Create your views here.

# Endpoint list
@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Transfer': '/transfer/',
        'Made-transfers':'/made_transfers_receipts/',
        'Made-transfer-detail':'/receipt-detail/<int:pk>/',
        'Incoming-transfers':'/made-transfer-receipts/',
        'Incoming-transfer-detail':'/receipt-detail/<int:pk>/',
        'User-view':'/user/',
    }
    return Response(api_urls)

# -------------------- TRANSFER ---------------------------------

# Endpoint to send data to perform transfer and create a receipt
class TransferAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        try:
            user = request.user
            serializer = TransferDataSerializer(data=request.data)
        
            if serializer.is_valid():
                transfer_value = serializer.validated_data.get('transfer_value')

                if int(transfer_value) > user.balance:
                    return Response({"message": "Saldo insuficiente"},status=HTTP_400_BAD_REQUEST)

                elif int(transfer_value) <= 0:
                    return Response({"message": "Digite um valor válido."}, status=HTTP_400_BAD_REQUEST)

                else:      
                    enrollment = serializer.validated_data.get('transfer_user')
                    try: 
                        transfer_user = User.objects.get(enrollment=enrollment)
                    except:
                        return Response({"message": "Código de matrícula inválido."}, status=HTTP_404_NOT_FOUND)

                    receipt = Receipt (
                        transfer_value = transfer_value,
                        user = user.enrollment,
                        name = user.name,
                        course = user.course,

                        transfer_user = enrollment,  
                        transfer_name = transfer_user.name,
                        transfer_course = transfer_user.course
                    )
                    receipt.save()
                    return Response(serializer.data, status=HTTP_201_CREATED)

            return Response(
                {
                    "message": "Há erros de validação.", 
                    "errors": serializer.errors
                }, status=HTTP_400_BAD_REQUEST)
        except: 
            return Response({'message': 'Erro ao realizar transferência. Tente novamente mais tarde.'}, status=HTTP_400_BAD_REQUEST)

# ------------------ INCOMING RECEIPTS -------------------------

# Endpoint to list all incoming receipts for a user
@api_view(['GET'])
def incoming_transfer_receipts(request):
    permission_classes = (IsAuthenticated, )
    try:
        user = request.user
        receipt = Receipt.objects.filter(transfer_user=user.enrollment)
        serializer = ReceiptSerializer(receipt, many=True)

        return Response(serializer.data, status=HTTP_200_OK)
    except: 
        return Response({'message': 'Não encontrado.'}, status=HTTP_404_NOT_FOUND)

# Endpoint to list a specefic incoming receipt for a user  
@api_view(['GET'])
def incoming_transfer_receipt_detail(request, pk):
    permission_classes = (IsAuthenticated, )
    try:
        user =  request.user
        receipt = Receipt.objects.get(transfer_user=user.enrollment, pk=pk)
        serializer = ReceiptSerializer(receipt, many=False)

        return Response(serializer.data, status=HTTP_200_OK)
    except:
        return Response({ 'message': 'Não encontrado.'}, status=HTTP_404_NOT_FOUND)
       
# ------------------ MADE RECEIPTS -------------------------

# Endpoint to list all made receipts for a user
@api_view(['GET'])
def made_transfer_receipts(request):
    permission_classes = (IsAuthenticated, )
    try:
        user = request.user
        receipt = Receipt.objects.filter(user=user.enrollment)
        serializer = ReceiptSerializer(receipt, many=True)

        return Response(serializer.data, status=HTTP_200_OK)
    except:
        return Response({'message': 'Não encontrado.'}, status=HTTP_404_NOT_FOUND)
    
# Endpoint to list a specefic made receipt for a user
@api_view(['GET'])
def made_transfer_receipt_detail(request, pk):
    permission_classes = (IsAuthenticated, )
    try:
        user = request.user
        receipt = Receipt.objects.get(user=user.enrollment, pk=pk)  
        serializer = ReceiptSerializer(receipt, many=False)

        return Response(serializer.data, status=HTTP_200_OK)
    except:
        return Response({ 'message': 'Não encontrado.'}, status=HTTP_404_NOT_FOUND)
 
# ----------------- USER ------------------------
class UserApiView(APIView):
    permission_classes = (AllowAny,)

    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        data = request.data.get
        user = User(
            username=data('username'), 
            enrollment=data('enrollment'), 
            name=data('name'), 
            course=data('course'), 
            balance=data('balance')
            )
        user.set_password(data('password'))
        user.save()
        serializer = UserSerializer(user, many=False)

        return Response(serializer.data, status=HTTP_201_CREATED)
   
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=HTTP_200_OK)