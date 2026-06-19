import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from Administrator.models import tbl_adminregistration, tbl_creditmaster

def seed():
    # Admin seeding
    if not tbl_adminregistration.objects.filter(adminregistration_email='admin@edutrack.com').exists():
        tbl_adminregistration.objects.create(
            adminregistration_name='EduTrack-X Admin',
            adminregistration_contact='9876543210',
            adminregistration_email='admin@edutrack.com',
            adminregistration_password='admin123'
        )
        print("Default admin created successfully (admin@edutrack.com / admin123).")
    else:
        print("Admin already exists.")

    # Credit Master seeding
    credits = [
        ('SEC', 3),
        ('VAC', 2),
        ('MDC', 3),
        ('Minor', 4),
        ('Internship', 4),
        ('Project', 6),
        ('Add-on', 2),
        ('Workshop', 1),
        ('Certificate', 2)
    ]
    for category, val in credits:
        if not tbl_creditmaster.objects.filter(creditmaster_category=category).exists():
            tbl_creditmaster.objects.create(
                creditmaster_category=category,
                creditmaster_credit=val,
                creditmaster_status=1
            )
            print(f"Credit rule for {category} ({val} credits) created.")
        else:
            print(f"Credit rule for {category} already exists.")

if __name__ == '__main__':
    seed()
