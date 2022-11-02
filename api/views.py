import jwt
from rest_framework.permissions import IsAuthenticated, AllowAny
from pointsTransfer.settings import SECRET_KEY
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Receipt, User
from .serializers import ReceiptSerializer, TransferDataSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_400_BAD_REQUEST, 
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN
)

# Create your views here.

# Endpoint list
@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Transfer': '/transfer/<int:pk>/',
        'Made-transfers':'/made_transfers_receipts/<int:user_id>/',
        'Made-transfer-detail':'/receipt-detail/<int:user_id>/<int:pk>/',
        'Incoming-transfers':'/made-transfer-receipts/<int:user_id>/',
        'Incoming-transfer-detail':'/receipt-detail/<int:user_id>/<int:pk>/',
        'User-view':'/user/',
    }
    return Response(api_urls)

# -------------------- TRANSFER ---------------------------------

# Endpoint to send data to perform transfer and create a receipt
class TransferAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, user_id, format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        token = token.split(' ')
        decode_payload = jwt.decode(token[1], SECRET_KEY, algorithms=["HS256"])
        user = get_object_or_404(User, pk=user_id)

        if decode_payload.get('user_id') == user_id:
            serializer = TransferDataSerializer(data=request.data)
        
            if serializer.is_valid():
                transfer_value = serializer.validated_data.get('transfer_value')
                if int(transfer_value) > user.balance:
                    return Response(
                        {"message": "Saldo insuficiente"},
                        status=HTTP_400_BAD_REQUEST
                        )
                elif int(transfer_value) <= 0:
                    return Response(
                        {"message": "Digite um valor válido."}, 
                        status=HTTP_400_BAD_REQUEST
                        )
                else:      
                    enrollment = serializer.validated_data.get('transfer_user')
                    try: 
                        transfer_user = User.objects.get(enrollment=enrollment)
                    except:
                        return Response(
                            {"message": "Código de matrícula inválido"}, 
                            status=HTTP_400_BAD_REQUEST
                            )

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
                    "message": "Há erros de validação", 
                    "errors": serializer.errors
                }, 
                status=HTTP_400_BAD_REQUEST
                )
        else: 
            return Response({'message': 'Não autorizado'}, status=HTTP_403_FORBIDDEN)

# ------------------ INCOMING RECEIPTS -------------------------

# Endpoint to list all incoming receipts for a user
@api_view(['GET'])
def incoming_transfer_receipts(request, user_id):
    permission_classes = (IsAuthenticated, )
    token = request.META.get('HTTP_AUTHORIZATION')
    token = token.split(' ')
    decode_payload = jwt.decode(token[1], SECRET_KEY, algorithms=["HS256"])
    user = get_object_or_404(User, pk=user_id)

    if decode_payload.get('user_id') == user_id:
        receipt = Receipt.objects.filter(transfer_user=user.enrollment)
        serializer = ReceiptSerializer(receipt, many=True)

        return Response(serializer.data, status=HTTP_200_OK)
    else: 
        return Response({'message': 'Não autorizado'}, status=HTTP_403_FORBIDDEN)

# Endpoint to list a specefic incoming receipt for a user  
@api_view(['GET'])
def incoming_transfer_receipt_detail(request, user_id, pk):
    permission_classes = (IsAuthenticated, )
    token = request.META.get('HTTP_AUTHORIZATION')
    token = token.split(' ')
    decode_payload = jwt.decode(token[1], SECRET_KEY, algorithms=["HS256"])
    user = get_object_or_404(User, pk=user_id)

    if decode_payload.get('user_id') == user_id:
        try:
            user_receipts = Receipt.objects.filter(transfer_user=user.enrollment)
            for i in user_receipts:
                if pk == i.id:
                    receipt = Receipt.objects.get(pk=pk)
            serializer = ReceiptSerializer(receipt, many=False)
            return Response(serializer.data, status=HTTP_200_OK)
        except:
            return Response(
                { 'message': 'Comprovante não encontrado.'}, 
                status=HTTP_404_NOT_FOUND
                )
    else:
         return Response({'message': 'Não autorizado'}, status=HTTP_403_FORBIDDEN)

# ------------------ MADE RECEIPTS -------------------------

# Endpoint to list all made receipts for a user
@api_view(['GET'])
def made_transfer_receipts(request, user_id):
    permission_classes = (IsAuthenticated, )
    token = request.META.get('HTTP_AUTHORIZATION')
    token = token.split(' ')
    decode_payload = jwt.decode(token[1], SECRET_KEY, algorithms=["HS256"])
    user = get_object_or_404(User, pk=user_id)

    if decode_payload.get('user_id') == user_id:
        receipt = Receipt.objects.filter(user=user.enrollment)
        serializer = ReceiptSerializer(receipt, many=True)

        return Response(serializer.data, status=HTTP_200_OK)
    else: 
        return Response({'message': 'Não autorizado'}, status=HTTP_403_FORBIDDEN)
    
# Endpoint to list a specefic made receipt for a user
@api_view(['GET'])
def made_transfer_receipt_detail(request, user_id, pk):
    token = request.META.get('HTTP_AUTHORIZATION')
    token = token.split(' ')
    decode_payload = jwt.decode(token[1], SECRET_KEY, algorithms=["HS256"])
    user = get_object_or_404(User, pk=user_id)

    if decode_payload.get('user_id') == user_id:
        try:
            user_receipts = Receipt.objects.filter(user=user.enrollment)
            for i in user_receipts:
                if pk == i.id:
                    receipt = Receipt.objects.get(pk=pk)
            serializer = ReceiptSerializer(receipt, many=False)
            return Response(serializer.data, status=HTTP_200_OK)
        except:
            return Response(
                { 'message': 'Comprovante não encontrado.'}, 
                status=HTTP_404_NOT_FOUND
                )
    else:
         return Response({'message': 'Não autorizado'}, status=HTTP_403_FORBIDDEN)

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