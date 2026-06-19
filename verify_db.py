import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from Administrator.models import tbl_adminregistration, tbl_creditmaster

def verify():
    admins = tbl_adminregistration.objects.all()
    print(f"Total admin registrations: {admins.count()}")
    for admin in admins:
        print(f" - Admin Email: {admin.adminregistration_email}")
        
    rules = tbl_creditmaster.objects.all()
    print(f"Total Credit Master Rules: {rules.count()}")
    for r in rules:
        print(f" - {r.creditmaster_category}: {r.creditmaster_credit} credits")

if __name__ == '__main__':
    verify()
