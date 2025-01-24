from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for the User Model
    """
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )
    class Meta:
        model = get_user_model()
        fields = [
            "username", "email", 'first_name', 'last_name',
            'password', 'password2', 'city', 'state', 'address',
            'phone'
        ]
    def validate(self, data):
        """
        Perform cross-field validation and complex checks
        """
        # Ensure the data from the two password fields match.
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                "password": "Passwords do not match"
        })
        
        User = get_user_model()
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({
                "username": "Username already exists"
            })
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({
                "email": "Email already exists"
            })
        # Use Django's password validator to check password strength
        try:
            validate_password(data['password'])
        except Exception as e:
            raise serializers.ValidationError({
                "password": str(e)
            })

        # You can also add additional cross-field validation here if necessary
        return data
    
    def create(self, validated_data):
        """
        Create a new user from validated data.
        """
        # Pop password2 since it's not needed
        validated_data.pop('password2')
        password = validated_data.pop('password')

        User = get_user_model()
        try:
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
        except Exception as e:
            raise serializers.ValidationError({
                "error": "User can not be created."
            })
        return user