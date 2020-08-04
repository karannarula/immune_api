import django_tables2 as tables
from .models import Users

class UsersTable(tables.Table):
	
    class Meta:
        model = Users

        template_name = 'django_tables2/bootstrap.html'