from rest_framework import serializers
from create_user.models import Users,Location


class UserSerializers(serializers.ModelSerializer):
	class Meta:
		model = Users
		fields = ('created','title','user_id','logged_in','email')



class LocationSerializers(serializers.ModelSerializer):
	class Meta:
		model = Location
		fields = ('latitude','longitude','email_id','created','index','status_bit','name')