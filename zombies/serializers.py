from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

Usuario = get_user_model()


class UsuarioSerializer(serializers.ModelSerializer):
    """Datos publicos del usuario (nunca incluye la contrasena)."""

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'mic',
                  'gt_xbox', 'steam', 'psn', 'plutonium']
        read_only_fields = fields


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_username(self, value):
        value = value.strip()
        if Usuario.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError('Este nombre de usuario ya existe.')
        return value

    def validate_email(self, value):
        value = value.strip()
        if Usuario.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Este correo ya está registrado.')
        return value

    def validate(self, attrs):
        # Aplica los validadores de AUTH_PASSWORD_VALIDATORS de settings.py
        user = Usuario(username=attrs['username'], email=attrs['email'])
        try:
            validate_password(attrs['password'], user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return attrs

    def create(self, validated_data):
        return Usuario.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # username o correo
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs['identifier'].strip()
        password = attrs['password']

        username = identifier
        if '@' in identifier:
            match = Usuario.objects.filter(email__iexact=identifier).first()
            if match:
                username = match.username
        else:
            match = Usuario.objects.filter(username__iexact=identifier).first()
            if match:
                username = match.username

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password,
        )
        if user is None or not user.is_active:
            raise serializers.ValidationError('Usuario o contraseña incorrectos.')

        attrs['user'] = user
        return attrs
