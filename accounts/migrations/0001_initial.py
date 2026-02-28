# Generated migration for accounts app

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('role', models.CharField(choices=[('COMPANY', 'Company'), ('CENTER', 'Center'), ('ADMIN', 'Admin'), ('STUDENT', 'Student')], default='COMPANY', max_length=20)),
                ('company_id', models.PositiveIntegerField(blank=True, null=True)),
                ('center_id', models.PositiveIntegerField(blank=True, null=True)),
                ('admin_id', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
