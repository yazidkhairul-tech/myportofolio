from django.forms import (
    ModelForm,
    TextInput,
    Textarea,
    DateTimeInput,
    NumberInput,
)

from main.models import Education

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