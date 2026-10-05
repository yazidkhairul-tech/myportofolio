from django.core.exceptions import ValidationError
from django.forms import (
    DateInput,
    ModelForm,
    TextInput,
    Textarea,
    DateTimeInput,
    NumberInput,
)
from django.utils.html import strip_tags

from main.models import Education, Project

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution_name",
            "program",
            "started_at",
            "ended_at",
            "description",
            "score",
        ]

        labels = {
            "institution_name": "Institusi",
            "program": "Program / Jurusan",
            "started_at": "Tanggal Mulai",
            "ended_at": "Tanggal Selesai (kosongkan jika masih berlangsung)",
            "description": "Deskripsi",
            "score": "Nilai Akhir (dari 100)",
        }

        widgets = {
            "institution_name": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                    "maxlength": 255,
                }
            ),
            "program": TextInput(
                attrs={
                    "placeholder": "S1 Ilmu Komputer",
                    "maxlength": 255,
                }
            ),
            "started_at": DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "ended_at": DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalaman studimu",
                    "rows": 3,
                }
            ),
            "score": NumberInput(
                attrs={
                    "placeholder": "88.50",
                    "step": "0.01",
                    "min": 0,
                    "max": 100,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ended_at"].required = False
        self.fields["score"].required = False
        self.fields["description"].required = False

    def clean(self):
        cleaned_data = super().clean()
        started_at = cleaned_data.get("started_at")
        ended_at = cleaned_data.get("ended_at")
        if started_at and ended_at and ended_at < started_at:
            self.add_error("ended_at", "Tanggal selesai tidak boleh lebih awal dari tanggal mulai.")
        return cleaned_data

    def clean_institution_name(self):
        institution_name = strip_tags(self.cleaned_data.get("institution_name", "")).strip()
        if not institution_name:
            raise ValidationError("Nama institusi tidak boleh hanya berisi tag HTML.")
        return institution_name

    def clean_program(self):
        program = strip_tags(self.cleaned_data.get("program", "")).strip()
        if not program:
            raise ValidationError("Program / Jurusan tidak boleh hanya berisi tag HTML.")
        return program

    def clean_description(self):
        return strip_tags(self.cleaned_data.get("description", "")).strip()

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "thumbnail",
            "project_url",
            "source_url",
            "started_at",
            "is_ongoing",
            "ended_at",
            "is_featured",
        ]
        widgets = {
            "description": Textarea(attrs={"rows": 4}),
            "started_at": DateInput(attrs={"type": "date"}),
            "ended_at": DateInput(attrs={"type": "date"}),
        }
        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi",
            "tech_stack": "Tech Stack",
            "thumbnail": "Gambar/Screenshot",
            "project_url": "Link Demo",
            "source_url": "Link Source Code",
            "started_at": "Mulai Dikerjakan",
            "is_ongoing": "Masih Berjalan",
            "ended_at": "Selesai Dikerjakan",
            "is_featured": "Tandai sebagai Featured",
        }
 
    def clean(self):
        cleaned_data = super().clean()
        is_ongoing = cleaned_data.get("is_ongoing")
        ended_at = cleaned_data.get("ended_at")
 
        if not is_ongoing and not ended_at:
            self.add_error(
                "ended_at",
                "Isi tanggal selesai, atau centang 'Masih Berjalan' jika proyek belum selesai.",
            )
        return cleaned_data

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()