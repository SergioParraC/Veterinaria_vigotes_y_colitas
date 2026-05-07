from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacto',
            name='numero_contacto',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
