from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import models
from .models import Account, SystemConfig, OperationLog

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('account_id', 'username', 'email', 'real_name', 'phone', 'avatar', 'user_type', 'status', 'create_time', 'update_time')
        read_only_fields = ('account_id', 'create_time', 'update_time')

class AccountCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Account
        fields = ('account_id', 'username', 'password', 'email', 'first_name', 'last_name', 
                 'phone', 'user_type', 'create_time', 'update_time')
        read_only_fields = ('account_id', 'create_time', 'update_time')
    
    def create(self, validated_data):
        # 创建用户
        user_data = {
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
            'email': validated_data.pop('email'),
            'first_name': validated_data.pop('first_name', ''),
            'last_name': validated_data.pop('last_name', '')
        }
        user = User.objects.create_user(**user_data)
        
        # 创建账户
        account = Account.objects.create(
            user=user,
            phone=validated_data.get('phone', ''),
            role=validated_data.get('role', 'user')
        )
        
        return account

class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('phone', 'user_type')
    
    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)
        instance.user_type = validated_data.get('user_type', instance.user_type)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=255)
    user_type = serializers.IntegerField(default=1)
    
    def validate(self, attrs):
        """验证登录信息"""
        username = attrs.get('username')
        password = attrs.get('password')
        user_type = attrs.get('user_type', 1)
        
        # 查找用户（支持用户名或手机号登录）
        try:
            if user_type == 2:  # 管理员登录
                account = Account.objects.get(
                    username=username,
                    user_type=2
                )
            else:  # 普通用户登录
                account = Account.objects.get(
                    models.Q(username=username) | models.Q(phone=username),
                    user_type=user_type
                )
        except Account.DoesNotExist:
            raise serializers.ValidationError("用户名或密码错误")
        
        # 验证密码
        if not account.check_password(password):
            raise serializers.ValidationError("用户名或密码错误")
        
        # 检查账户状态
        if account.status != 1:
            raise serializers.ValidationError("账户已被禁用")
        
        attrs['account'] = account
        return attrs


class RegisterSerializer(serializers.Serializer):
    """注册序列化器"""
    
    username = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(min_length=6)
    confirm_password = serializers.CharField()
    real_name = serializers.CharField(max_length=50)
    email = serializers.EmailField(required=False, allow_blank=True)
    
    def validate_username(self, value):
        """验证用户名"""
        if Account.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value
    
    def validate_phone(self, value):
        """验证手机号"""
        import re
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError("请输入正确的手机号")
        
        if Account.objects.filter(phone=value).exists():
            raise serializers.ValidationError("手机号已被注册")
        return value
    
    def validate(self, attrs):
        """验证数据"""
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("两次输入的密码不一致")
        return attrs
    
    def create(self, validated_data):
        """创建用户"""
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        
        account = Account(**validated_data)
        account.set_password(password)
        account.save()
        return account


class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料序列化器"""
    
    class Meta:
        model = Account
        fields = [
            'account_id', 'username', 'real_name', 'phone', 'email', 'avatar',
            'register_time', 'last_login_time', 'user_type'
        ]
        read_only_fields = ['account_id', 'username', 'register_time', 'last_login_time', 'user_type']


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=6)
    confirm_password = serializers.CharField()
    
    def validate(self, attrs):
        """验证数据"""
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("两次输入的新密码不一致")
        return attrs
    
    def validate_old_password(self, value):
        """验证旧密码"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("原密码错误")
        return value


class SystemConfigSerializer(serializers.ModelSerializer):
    """系统配置序列化器"""
    
    class Meta:
        model = SystemConfig
        fields = '__all__'
        read_only_fields = ['config_id', 'create_time', 'update_time']


class OperationLogSerializer(serializers.ModelSerializer):
    """操作日志序列化器"""
    
    account_username = serializers.CharField(source='account.username', read_only=True)
    
    class Meta:
        model = OperationLog
        fields = '__all__'
        read_only_fields = ['log_id', 'create_time']

