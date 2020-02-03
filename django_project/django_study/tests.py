from django.contrib.auth.models import User


user = User.objects.create_superuser('Schuyler', 'caishunweiking@126.com', '123456')