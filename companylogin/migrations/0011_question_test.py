from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("companylogin", "0010_rename_centers_center_rename_questions_question_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="test",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="companylogin.test",
            ),
        ),
    ]

