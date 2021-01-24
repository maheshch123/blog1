from planety.models import Post,Profile,Comment
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class UserCreateSearilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
         ]
        extra_kwargs = {'password':
                            {'write_only':True},
                            'email': {'write_only':True},
                            'username':{'write_only':True}}
    def create(self,validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        user_obj = User(
            username = username,
            email = email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data 



class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'