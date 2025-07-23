from django.db.backends.sqlite3.introspection import DatabaseIntrospection
from django.db.models import Subquery, OuterRef, FilteredRelation, ExpressionWrapper, DecimalField, IntegerField, \
    CharField, BooleanField
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import status
from django.db import connection
from db.models import Test, SalesMaster
from django.db.models import F, Case, When, Value
from django.db.models import F, Window
from django.db.models.functions import Lag, Lead
from drf_spectacular.utils import extend_schema

from utils.utils import VoucherNumberUtils


class AuthUserView(APIView):
    @extend_schema(
        summary="Greet the user",
        description="Returns a Hello, World message",
        responses={200: dict},
        parameters=['username','password']
    )
    def get(self, request):
        voucher_number = VoucherNumberUtils(SalesMaster,'2d97ee99-64d0-4121-ab42-0d1f563c4afa',1,'SI1','SI','','','')._check_voucher_number_gap()
        print(voucher_number)
        # username = request.data['username']
        # password = request.data['password']

        # q = Test.objects.annotate(
        #     next_voucher=Case(When(ExpressionWrapper('voucher_no'+ 1 = 'voucher_no', output_field=IntegerField()), then=F('voucher_no')),)
        # ).order_by('voucher_no')

        # queryset = Test.objects.annotate(
        #     next_voucher=Window(
        #         expression=Lead('voucher_no'),
        #         order_by=F('voucher_no').asc()
        #     )
        # ).annotate(
        #     has_gap=Case(
        #         When(next_voucher__isnull=False, then=~(F('voucher_no') + 1 == F('next_voucher'))),
        #         default=Value(False),
        #         output_field=BooleanField()
        #     ),
        #     expected_next=ExpressionWrapper(F('voucher_no') + 1, output_field=IntegerField())
        # ).filter(has_gap=True).values('expected_next').first()
        #
        # print("First missing voucher:", queryset['expected_next'] if queryset else None)


        

        # if not User.objects.get_username(username):
        #     return Response(data={'error': 'Username does not exist'},status=status.HTTP_404_NOT_FOUND)
        #         email = username
        #         username = User.objects.get(email=email).username
        #         user_id = User.objects.get(email=email).id
        #         user_name_ok = True
        #         user_insts = User.objects.get(email=email)
        #     elif User.objects.filter(username=username).exists():
        #         user_name_ok = True
        #         user_id = User.objects.get(username=username).id
        #         user_insts = User.objects.get(username=username)
        #     if user_insts:
        #         user_email = user_insts.email
        #         password_ok = user_insts.check_password(password)
        #     try:
        #         service = request.data['service']
        #     except:
        #         service = None
        #     # print("user_insts===>",user_insts.username)
        #     user = authenticate(username=username, password=password)
        #     if user:
        #         is_login = True
        #         # if User.objects.filter(username=username).exists():
        #         #     user_ins = User.objects.get(username=username)
        #         if user.is_active == True:
        #             is_verified = True
        #     if user:
        #         login(request, user)
        #         headers = {
        #             'Content-Type': 'application/json',
        #         }
        #
        #         data = {"username":  username, "password": password}
        #         protocol = "http://"
        #         if request.is_secure():
        #             protocol = "https://"
        #
        #         web_host = request.get_host()
        #         request_url = protocol + web_host + "/api/v1/authentication/token/"
        #         response = requests.post(
        #             request_url, headers=headers, data=json.dumps(data))
        #
        #         if response.status_code == 200:
        #             data = response.json()
        #             success = 6000
        #             message = "Login successfully"
        #
        #             access_token = data["access"]
        #             # response_redirect = None
        #             print("service=====>",service)
        #             if service:
        #                 if service == "admin_panel":
        #                     if AdminUsers.objects.filter(user=user,status=False,is_delete=False).exists() or Partner.objects.filter(user=user).exists() or user.is_superuser:
        #                         pass
        #                     else:
        #                         success = 6001
        #                         error_code = 6001
        #                         data = None
        #                         error = "User not found"
        #                         return Response(
        #                             {
        #                                 "success": success,
        #                                 "data": data,
        #                                 "error": error,
        #                                 "error_code": error_code,
        #                                 "user_email": user_email
        #                             },
        #                             status=status.HTTP_200_OK,
        #                         )
        #                 if is_admin == False:
        #                     if AccountCustomerServices.objects.filter(user=user, Service=service).exists():
        #                         acc_service = AccountCustomerServices.objects.filter(
        #                             user=user, Service=service).first()
        #                         acc_service.LastTokenID = access_token
        #                         acc_service.save()
        #                     else:
        #                         AccountCustomerServices.objects.create(
        #                             user=user,
        #                             LastTokenID=access_token,
        #                             Service=service
        #                         )
        #                 admin_SSO = User.objects.get(id=data['user_id'])
        #                 token = RefreshToken.for_user(admin_SSO)
        #                 service_header = {
        #                     'Content-Type': 'application/json',
        #                     'Authorization': f"Bearer {token.access_token}"
        #                 }
        #
        #                 # if service == "otaibi":
        #                 #     service_url = "https://juhaniapi.viknbooks.com/api/v1/users/create"
        #                 #     redirect_response = redirect(f"https://juhaniapi.viknbooks.com/api/v1/users/accounts?sid={access_token}")
        #
        #                 #     # response_service_data = response_service.json()
        #                 #     # response_redirect = response_service_data['response_redirect']
        #                 # elif service == "viknbooks":
        #                 #     service_url = "https://www.testapi.viknbooks.com/api/v9/users/create"
        #                 #     redirect_response = redirect(f"https://www.testapi.viknbooks.com/api/v9/users/accounts?sid={access_token}")
        #                 #     print("printing response...........................................................")
        #                 #     print(redirect_response)
        #                 #     print("printing response...........................................................")
        #
        #                 # if redirect_response.status_code == 302:
        #                 #     response =  Response(
        #                 #     {
        #                 #         'success': 6000,  tokenPlus/users/create-user
        #                 #         'url' : 'https://test.viknbooks.com/dashboard/home'
        #                 #     },
        #                 #     status=status.HTTP_200_OK)
        #                 if service == "viknbooks":
        #                     service = "viknbooks_domain"
        #                 # elif service == "token_plus":
        #                 #     service = "token_plus"
        #                 base_url = getBaseUrl(service)
        #                 service_url = base_url + "users/create-user"
        #                 print("service_url===>",service_url)
        #                 service_data = {
        #                         "id": user.id,
        #                         "role":data['role'],
        #                         "password": password,
        #                         "username": user.username,
        #                         "first_name": user.first_name,
        #                         "last_name": user.last_name,
        #                         "email": user.email,
        #                         "last_login": str(user.last_login),
        #                     }
        #                 # new_data = service_data.update(data)
        #                 response_service = requests.post(
        #                 service_url, headers=service_header, data=json.dumps(service_data))
        #             data["username"] = user.username
        #             data["email"] = user.email
        #
        #             set_recent_activities(request,'Sign in',service)
        #             set_divice_details(request)
        #             create_user_account_service(user)
        #
        #             data["last_login"] = str(user.last_login)
        #
        #             response = Response(
        #                 {
        #                     'success': success,
        #                     'data': data,
        #                     'user_id': data['user_id'],
        #                     'role': data['role'],
        #                     'message': message,
        #                     'error': None,
        #                     'username': username,
        #                     # 'response_redirect':response_redirect
        #                 },
        #                 status=status.HTTP_200_OK)
        #             # response = HttpResponse(access_token)
        #             # two_years = datetime.datetime.now()+datetime.timedelta(days=730)
        #             # response.set_cookie(key='VBID', value={'VBID': access_token, 'is_admin': False}, domain=".localhost",
        #             #                     path='/', expires=two_years, samesite='None', secure=True)
        #
        #             return response
        #         else:
        #             success = 6001
        #             data = None
        #             error = "please contact admin to solve this problem."
        #             return Response(
        #                 {
        #                     'success': success,
        #                     'data': data,
        #                     'error': message,
        #                 },
        #                 status=status.HTTP_200_OK)
        #     else:
        #         success = 6001
        #         error_code = 6001
        #         data = None
        #         if user_name_ok and password_ok == False:
        #             error_code = 6002
        #             error = "Password Incorrect"
        #         elif user_name_ok and is_verified == False:
        #             error = "Please Verify Your Email to Login"
        #             error_code = 6003
        #             data = user_id
        #         else:
        #             error = "User not found"
        #         return Response(
        #             {
        #                 "success": success,
        #                 "data": data,
        #                 "error": error,
        #                 "error_code": error_code,
        #                 "user_email": user_email
        #             },
        #             status=status.HTTP_200_OK,
        #         )
        #
        # else:
        #     message = generate_serializer_errors(serialized._errors)
        #     success = 6001
        #     data = None
        #
        #     return Response(
        #         {
        #             'success': success,
        #             'data': data,
        #             'error': message,
        #         },
        #         status=status.HTTP_200_OK)

        return Response({'data': 'This is a test response'}, status=status.HTTP_200_OK)