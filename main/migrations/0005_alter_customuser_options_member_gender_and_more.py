# Generated by Django 5.1 on 2024-11-15 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_alter_member_membership_date_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={"verbose_name": "User", "verbose_name_plural": "Users"},
        ),
        migrations.AddField(
            model_name="member",
            name="gender",
            field=models.CharField(
                choices=[("male", "Male"), ("female", "Female")],
                default="male",
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="beneficiary",
            name="full_name",
            field=models.CharField(max_length=255, verbose_name="FullName"),
        ),
        migrations.AlterField(
            model_name="beneficiary",
            name="id_number",
            field=models.CharField(max_length=20, verbose_name="ID Number"),
        ),
        migrations.AlterField(
            model_name="beneficiary",
            name="relationship_type",
            field=models.CharField(
                choices=[
                    ("spouse", "Spouse"),
                    ("child", "Child"),
                    ("parent", "Parent"),
                    ("principal", "Principal"),
                    ("nominee", "Nominee"),
                ],
                max_length=50,
                verbose_name="Relationship Type",
            ),
        ),
        migrations.AlterField(
            model_name="member",
            name="date_of_birth",
            field=models.DateField(null=True, verbose_name="Date Of Birth"),
        ),
        migrations.AlterField(
            model_name="member",
            name="hit_ec_number",
            field=models.CharField(
                max_length=20, null=True, verbose_name="HIT EC Number"
            ),
        ),
        migrations.AlterField(
            model_name="member",
            name="id_number",
            field=models.CharField(max_length=20, null=True, verbose_name="ID Number"),
        ),
        migrations.AlterField(
            model_name="member",
            name="phone_number",
            field=models.CharField(
                max_length=15, null=True, verbose_name="Phone Number"
            ),
        ),
    ]
