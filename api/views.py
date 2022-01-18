from rest_framework import views, generics, permissions, status
from rest_framework.response import Response
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, AccessToken
from . import serializer
from .models import Leads, Subscription, User
from django.db.utils import IntegrityError
from itertools import islice
import datetime
import random
from django.utils import timezone



class RegisterView(views.APIView):
    class_serializer = serializer.RegisterSerializer
    def post(self, request):
        serializer = self.class_serializer(data=request.data)
        if serializer.is_valid():
            machine_uid = serializer.validated_data.pop('machine_uid', None)
            user = serializer.save()
            if user:
                try:
                    Subscription.objects.create(user=user, machine_uid=machine_uid)
                    return Response({"message": "Registred successfuly"}, status=status.HTTP_201_CREATED)
                except IntegrityError:
                    return Response({'message': 'You already signed up with this machine, kindly use you registred account or contact us.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = f'({list(serializer.errors.keys())[0]}) {list(serializer.errors.values())[0][0]}'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):
    serializer_class = serializer.LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                refresh = RefreshToken(serializer.validated_data['refresh'])
                refresh.blacklist()
                return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
            except TokenError:
                return Response({'message': 'Token is invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = f'({list(serializer.errors.keys())[0]}) {list(serializer.errors.values())[0][0]}'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(generics.GenericAPIView):
    serializer_class = serializer.PasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            data = serializer.validated_data
            if user.check_password(data['old_password']):
                user.set_password(data['new_password'])
                user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'password is incorrect.'}, status=status.HTTP_409_CONFLICT)
        else:
            message = f'({list(serializer.errors.keys())[0]}) {list(serializer.errors.values())[0][0]}'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


class ForgetPassword(generics.GenericAPIView):
    serializer_class = serializer.ForgetPasswordSerializer 
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                token = get_token_for_user(user)["access"] 
                email_body = 'Hi '+ user.username + '\nPlease enter the code below into your Veriblaster App instead to set your password\n\n' + token + '\n\nBest Regards,\nVeriblaster Team'
                data = {'email_body': email_body, 'email_subject': 'Veriblaster (Reset password)', "to_email": [user.email]}
                email_message = EmailMessage(subject=data["email_subject"], body=data["email_body"], to=data["to_email"])
                email_message.send()
                return Response({'message': 'Please check your email to reset password'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            message = f'({list(serializer.errors.keys())[0]}) {list(serializer.errors.values())[0][0]}'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
    

class LinkForgetPasswordReset(generics.GenericAPIView):
    serializer_class = serializer.TokenSerializer 
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                user_id = AccessToken(data["token"])['user_id']
                user = User.objects.filter(id=user_id).first()
                if user:
                    user.set_password(data["new_password"])
                    user.save()
                    return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Password reset link is invalid'}, status=status.HTTP_404_NOT_FOUND)
            except TokenError: 
                return Response({"message": "Code is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = f'({list(serializer.errors.keys())[0]}) {list(serializer.errors.values())[0][0]}'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


class OrderLeadsView(generics.GenericAPIView):
    serializer_class = serializer.OrderLeadsSerialier
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            user_sub = Subscription.objects.filter(user=request.user, machine_uid=validated_data["machine_uid"]).first()
            if user_sub:
                if user_sub.expire >= timezone.now():
                    if user_sub.leads_orderd_date is None or (timezone.now() >= (user_sub.leads_orderd_date + datetime.timedelta(days=7))):
                        user_sub.leads_orderd_date = timezone.now()
                        user_sub.save()
                        items_leads = list(Leads.objects.all())
                        if len(items_leads) > 2000:
                            random_items = random.sample(items_leads, 2000)
                        else:
                            random_items = items_leads
                        data = [obj.phone for obj in random_items]
                        return Response({'data': data}, status=status.HTTP_200_OK)
                    else:
                        return Response({'message': 'You cant order more then 1 time in a week for each machine.'}, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({'message': 'Account Expired, please contact us for Subscription.'}, status=status.HTTP_410_GONE)
            else:
                return Response({'message': 'Account with the machine not exists.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            message = f'({list(serializer.errors.keys())[0]}) {list(serializer.errors.values())[0][0]}'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


class CheckUserActivationView(views.APIView):
    serializer_class = serializer.OrderLeadsSerialier
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            user_sub = Subscription.objects.filter(user=request.user, machine_uid=validated_data["machine_uid"]).first()
            if user_sub:
                if user_sub.expire >= timezone.now():
                    return Response({'message': 'Account Activated', 'data': {'expire_on': user_sub.expire}}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Account Expired, please contact us for Subscription.'}, status=status.HTTP_410_GONE)
            else:
                return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            message = f'({list(serializer.errors.keys())[0]}) {list(serializer.errors.values())[0][0]}'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


class AddNewMachineView(views.APIView): 
    serializer_class = serializer.OrderLeadsSerialier
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            try:
                print(validated_data["machine_uid"])
                Subscription.objects.create(user=request.user, machine_uid=validated_data["machine_uid"])
                return Response({"message": "New Machine added successfully."}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'message': 'You already signed up with this machine, kindly use you registred account or contact us.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = f'({list(serializer.errors.keys())[0]}) {list(serializer.errors.values())[0][0]}'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


'''
Admin Part
'''
class AdminUploadLeadsView(generics.GenericAPIView):
    serializer_class = serializer.LeadsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        token_user_email = request.user
        if token_user_email.is_superuser:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                leads = data['leads']
                batch_size = 100
                objs = (Leads(phone=lead) for lead in leads)
                while True:
                    batch = list(islice(objs, batch_size))
                    if not batch:
                        break
                    Leads.objects.bulk_create(batch, batch_size)
                return Response({'message': 'Leads uploaded successfully'}, status=status.HTTP_201_CREATED)
            else:
                message = f'({list(serializer.errors.keys())[0]}) {list(serializer.errors.values())[0][0]}'
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        

class UsersSubscriptionView(generics.GenericAPIView):
    serializer_class = serializer.SubscriptionsSerialier
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        token_user_email = request.user
        if token_user_email.is_superuser:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                subscriptions = data["subscriptions"]
                ids_not_exists = {"ids_not_exists": []}
                machine_ids_objects = []
                for info in subscriptions:
                    machine_obj = Subscription.objects.filter(machine_uid=info["uid"]).first()
                    if machine_obj:
                        expire = machine_obj.expire + datetime.timedelta(days=(30*info["months_number"])+1)
                        machine_obj.expire = expire
                        machine_ids_objects.append(machine_obj)                       
                    else:
                        ids_not_exists["ids_not_exists"].append(info["uid"])
                if machine_ids_objects:
                    Subscription.objects.bulk_update(machine_ids_objects, ['expire'])
                return Response({'message': 'Accounts Activated', 'data': [], 'errors': ids_not_exists}, status=status.HTTP_200_OK)
            else:
                message = f'({list(serializer.errors.keys())[0]}) {list(serializer.errors.values())[0][0]}'
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_403_FORBIDDEN)


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'access': str(refresh.access_token)}