# Generated by Django 5.1 on 2024-10-29 07:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("first_name", models.CharField(max_length=30)),
                ("last_name", models.CharField(max_length=30)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Member",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("membership_date", models.DateField(auto_created=True)),
                ("phone_number", models.CharField(max_length=15)),
                ("date_of_birth", models.DateField()),
                ("id_number", models.CharField(max_length=20)),
                ("hit_ec_number", models.CharField(max_length=20)),
                ("residential_address", models.TextField()),
                ("employment_position", models.CharField(max_length=100)),
                ("extension", models.CharField(max_length=100)),
                ("fax", models.CharField(max_length=100)),
                ("department", models.CharField(max_length=100)),
                ("employment_duration", models.CharField(max_length=50)),
                ("office_number", models.CharField(max_length=50)),
                ("principal_beneficiary_name", models.CharField(max_length=100)),
                ("principal_beneficiary_cell", models.CharField(max_length=100)),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "Inactive")],
                        default="active",
                        max_length=50,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Beneficiary",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(max_length=255)),
                ("id_number", models.CharField(max_length=20)),
                (
                    "relationship_type",
                    models.CharField(
                        choices=[
                            ("spouse", "Spouse"),
                            ("child", "Child"),
                            ("parent", "Parent"),
                            ("principal", "Principal"),
                            ("nominee", "Nominee"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "proof_of_relationship",
                    models.FileField(null=True, upload_to="beneficiary_proofs/"),
                ),
                ("deceased", models.BooleanField(default=False)),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="beneficiaries",
                        to="main.member",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Trustee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("position", models.CharField(max_length=255)),
                ("role", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PaymentHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("payment_date", models.DateField(auto_created=True)),
                ("period", models.DateField()),
                (
                    "amount_paid",
                    models.DecimalField(decimal_places=2, default=2, max_digits=6),
                ),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.member"
                    ),
                ),
                (
                    "recorded_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="main.trustee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EventLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("event", models.TextField()),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("delete", "Delete"),
                            ("create", "Create"),
                            ("update", "Update"),
                            ("other", "Other"),
                        ],
                        max_length=20,
                    ),
                ),
                ("event_date", models.DateTimeField(auto_now_add=True)),
                (
                    "trustee",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="main.trustee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Claim",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_filed", models.DateField(auto_now_add=True)),
                (
                    "amount_claimed",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("approved", "Approved"),
                            ("rejected", "Rejected"),
                        ],
                        default="pending",
                        max_length=50,
                    ),
                ),
                ("proof_of_claim", models.FileField(upload_to="claims/")),
                ("description", models.TextField(blank=True)),
                ("approval_date", models.DateTimeField(blank=True, null=True)),
                (
                    "beneficiary",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="main.beneficiary",
                    ),
                ),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.member"
                    ),
                ),
                (
                    "approved_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.trustee",
                    ),
                ),
            ],
        ),
    ]
