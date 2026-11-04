"""
Mengubah primary key Project dari integer menjadi UUID dan menambah
project_image_url, TANPA kehilangan data proyek dan relasi star yang sudah ada.

Langkah: simpan data lama ke memori -> hapus tabel lama -> buat tabel baru
(UUID) -> masukkan kembali data lama dengan UUID baru. Migrasi berjalan dalam
satu transaksi, jadi jika gagal di tengah jalan semua perubahan dibatalkan.
"""
import uuid

from django.conf import settings
from django.db import migrations, models

_backup = {"projects": []}


def backup_projects(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    _backup["projects"] = [
        {
            "title": p.title,
            "description": p.description or "",
            "tech_stack": p.tech_stack or "",
            "thumbnail": p.thumbnail.name if p.thumbnail else None,
            "project_url": p.project_url or "",
            "source_url": p.source_url or "",
            "started_at": p.started_at,
            "is_ongoing": p.is_ongoing,
            "ended_at": p.ended_at,
            "is_featured": p.is_featured,
            "created_at": p.created_at,
            "starred_by": list(p.starred_by.values_list("pk", flat=True)),
        }
        for p in Project.objects.all()
    ]


def restore_projects(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    for data in _backup["projects"]:
        starred_by = data.pop("starred_by")
        created_at = data.pop("created_at")
        project = Project.objects.create(**data)
        # auto_now_add menimpa created_at saat create, jadi dikembalikan manual.
        Project.objects.filter(pk=project.pk).update(created_at=created_at)
        project.starred_by.set(starred_by)
    _backup["projects"] = []


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_education_starred_by_alter_project_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(backup_projects, migrations.RunPython.noop),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('tech_stack', models.CharField(help_text='Pisahkan setiap teknologi dengan koma, contoh: Django, PostgreSQL, React', max_length=255)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='projects/')),
                ('project_url', models.URLField(blank=True, help_text='Link demo/live project (opsional)')),
                ('project_image_url', models.URLField(blank=True)),
                ('source_url', models.URLField(blank=True, help_text='Link repository/source code (opsional)')),
                ('started_at', models.DateField(blank=True, null=True)),
                ('is_ongoing', models.BooleanField(default=False)),
                ('ended_at', models.DateField(blank=True, null=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('starred_by', models.ManyToManyField(blank=True, related_name='starred_projects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-is_featured', '-started_at'],
            },
        ),
        migrations.RunPython(restore_projects, migrations.RunPython.noop),
    ]
