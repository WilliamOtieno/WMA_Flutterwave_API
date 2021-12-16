from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            if User.objects.filter(username='william').exists():
                pass
            else:
                user = User.objects.create(username='william', email='jimmywilliamotieno@gmail.com',
                                           first_name='William', last_name='Jimmy', phone_number='254719383956')
                user.set_password('1234')
                user.is_active = True
                user.is_staff = True
                user.is_superuser = True  # To access django admin
                user.save()

                self.stdout.write(self.style.SUCCESS('Successfully Created Demo User'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(e))
