from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("realtime_actions", "0003_rename_installation_id_fcm_token"),
    ]

    operations = [
        migrations.DeleteModel(
            name="FirebaseInstallation",
        ),
    ]
