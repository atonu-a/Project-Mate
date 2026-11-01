from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("realtime_actions", "0002_firebaseinstallation"),
    ]

    operations = [
        migrations.RenameField(
            model_name="firebaseinstallation",
            old_name="installation_id",
            new_name="fcm_token",
        ),
        migrations.AlterField(
            model_name="firebaseinstallation",
            name="fcm_token",
            field=models.CharField(max_length=4096, unique=True),
        ),
    ]
