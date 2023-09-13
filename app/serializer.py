from rest_framework import serializers
from django.core.exceptions import ValidationError
from app.models import CustomUser
# from django.forms import CheckboxInput
from rest_framework_simplejwt.tokens import RefreshToken, TokenBackendError


class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = CustomUser
        fields = ("__all__")
        
class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    is_doctor = serializers.BooleanField(style={'input_type':'checkbox-class'})
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'confirm_password','is_doctor']
        extra_fields = [
            ({'input_type' : 'password'}),
            ({'confirm_password': {'read_only': True}}),
        ]


    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        email = data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("User with this email already exists, please confirm this is you.")

        if password != confirm_password:
            raise ValidationError({"err" : "Password doesn't match!"})
        return data



    def create(self, validated_data):
        
        user = CustomUser.objects.create_user( 
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_doctor = validated_data.get('is_doctor')
            
        )

        return user

    



class LoginSerializer(serializers.ModelSerializer):
    

    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type':{'password'}})
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    

# update user details
class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name', 'username']



class BlockUsers(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['is_active']



class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()
    


    default_error_messages = {
        "bad_token" : ('Token is expired or invalid, or You must be logged out from this site')
    }
    
    def validate(self, attrs):

        self.refresh = attrs['token']
        print(attrs.get('token'))
        print(self.refresh)
        return attrs

    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenBackendError:
            self.fail('bad_token')
