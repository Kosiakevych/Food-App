from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import PasswordChangeForm

from base.models import List_of_Dish
from base.serializers import List_of_Dish_Serializer
from change_file_name import handle_uploaded_file
from .models import UserProfile, FavoriteRecipe
from .serializers import UserProfileSerializer, FavoriteRecipeSerializer, CreateList_of_Dish_Serializer, \
    UserRegistrationSerializer
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import requests
from rest_framework.generics import CreateAPIView
from drf_yasg.utils import swagger_auto_schema

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from accounts.utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from django.shortcuts import render, redirect
from django.contrib import messages


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Send activation email to the user
            user_get = UserProfile.objects.get(user=user)

            send_activation_email(user_get, request)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('authentication/user_activation_letter.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    if not settings.TESTING:
        EmailThread(email).start()


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_profile(self, request):
        # getting the UserProfile object for the current user
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            # creating a UserProfile object for the current user if it doesn't exist
            user_profile = UserProfile(user=request.user)
            user_profile.save()
        return user_profile

    @swagger_auto_schema(  # Documentation
        operation_summary="Get user personal info",
        operation_description='<b>You need to be authorized</b>',
        responses={200: UserProfileSerializer()},
        tags=["Accounts"])
    def get(self, request):
        user_profile = self.get_user_profile(request)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    @swagger_auto_schema(  # Documentation
        operation_summary="Change user personal info",
        operation_description='<b>You need to be authorized and put in data info like this</b>',
        responses={200: UserProfileSerializer()},
        tags=["Accounts"])
    def put(self, request):
        user_profile = self.get_user_profile(request)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            avatar = request.data.get('avatar')
            if avatar:
                filename = avatar.name
                new_filename = handle_uploaded_file(avatar, filename, "media/avatars")
                user_profile.avatar = new_filename
                user_profile.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(  # Documentation
        operation_summary="Change Password",
        operation_description='<b>You need to be authorized and put users old password, and new one twice\n'
                              'Like this:</b>\n{\n'
                              '"old_password": "old_password_here",\n'
                              '"new_password1": "new_password_here",\n'
                              ' "new_password2": "new_password_here"\n}',
        responses={200: "Success"},
        tags=["Accounts"])
    def post(self, request):
        form = PasswordChangeForm(request.user, request.data)
        if form.is_valid():
            form.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class AddFavoriteRecipeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Add a dish to user's favorite recipes",
        responses={
            200: "Returns the serialized favorite recipe object",
            404: "If the dish with provided id is not found",
        },
        tags=["Accounts"])
    def post(self, request, dish_id):
        dish = get_object_or_404(List_of_Dish, id=dish_id)
        user = request.user
        favorite_recipe = FavoriteRecipe(user=user, dish=dish)
        favorite_recipe.save()
        serializer = FavoriteRecipeSerializer(favorite_recipe)
        return Response(serializer.data)


class RemoveFavoriteRecipeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Remove a dish from user's favorite recipes",
        responses={
            204: "The dish is successfully removed from the favorite recipes",
            404: "If the dish with provided id is not found",
        },
        tags=["Accounts"])
    def delete(self, request, dish_id):
        dish = get_object_or_404(List_of_Dish, id=dish_id)
        user = request.user
        try:
            favorite_recipe = FavoriteRecipe.objects.get(user=user, dish=dish)
        except FavoriteRecipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        favorite_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteRecipesAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get user's favorite recipes",
        responses={
            200: List_of_Dish_Serializer(many=True),
        },
        tags=["Accounts"])
    def get(self, request):
        user = request.user
        favorite_recipes = FavoriteRecipe.objects.filter(user=user).select_related('dish')
        dishes = [recipe.dish for recipe in favorite_recipes]
        serializer = List_of_Dish_Serializer(dishes, many=True)
        return Response(serializer.data)


def user_activation(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = UserProfile.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect('/regform/')
        # return redirect(reverse('login'))

    return render(request, 'authentication/activation_failed.html', {"user": user})


def activate(request, uid, token):
    url = "http://127.0.0.1:8000/auth/users/activation/"

    data = {
        'uid': uid,
        'token': token
    }
    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("Activation successful!")
    else:
        print("Activation failed.")
    return HttpResponse("Activation successful!")
    # return redirect("success")


class CreateList_of_DishAPIView(CreateAPIView):
    """
        Create a new dish object.
    """
    serializer_class = CreateList_of_Dish_Serializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Create a new dish object",
        request_body=CreateList_of_Dish_Serializer,
        responses={
            201: "Created",
            400: "Bad request"
        },
        tags=["Accounts"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
