from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User
from main.models import Experience
from main.models import Education


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

class EducationTest(TestCase):
    def setUp(self):
        self.url = reverse("main:show_education")

    def test_url_is_accessible_and_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_data_appears_on_page_when_data_exists(self):
        Education.objects.create(
            institution_name="Universitas Indonesia",
            program="S1 Ilmu Komputer",
            description="Belajar dasar-dasar ilmu komputer.",
            started_at=timezone.now(),
        )

        response = self.client.get(self.url)

        self.assertContains(response, "Universitas Indonesia")
        self.assertContains(response, "S1 Ilmu Komputer")

    def test_page_shows_empty_state_message_when_no_data(self):
        self.assertEqual(Education.objects.count(), 0)

        response = self.client.get(self.url)

        self.assertContains(
            response, "Belum ada riwayat pendidikan yang ditambahkan."
        )


class EducationAjaxTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin",
            password="adminpassword123",
            email="admin@example.com",
        )
        self.regular_user = User.objects.create_user(
            username="regularuser",
            password="userpassword123",
        )
        self.education = Education.objects.create(
            institution_name="Universitas Indonesia",
            program="Ilmu Komputer",
            description="Kuliah pemrograman web",
            score=90.0,
            started_at=timezone.now(),
        )

    def test_get_education_json_anonymous(self):
        url = reverse("main:get_education_json")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["institution_name"], "Universitas Indonesia")
        self.assertEqual(data[0]["fields"]["star_count"], 0)
        self.assertFalse(data[0]["fields"]["is_starred"])

    def test_get_education_json_with_search_filter(self):
        Education.objects.create(
            institution_name="SMA Negeri 1",
            program="IPA",
            started_at=timezone.now(),
        )
        url = reverse("main:get_education_json")
        response = self.client.get(url, {"institution_name": "Indonesia"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["institution_name"], "Universitas Indonesia")

    def test_get_education_json_starred_status(self):
        self.education.starred_by.add(self.regular_user)
        url = reverse("main:get_education_json")
        
        # When logged in as regular_user
        self.client.login(username="regularuser", password="userpassword123")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(data[0]["fields"]["star_count"], 1)
        self.assertTrue(data[0]["fields"]["is_starred"])

    def test_create_education_ajax_requires_superuser(self):
        url = reverse("main:create_education_ajax")
        post_data = {
            "institution_name": "Institut Teknologi Bandung",
            "program": "Teknik Informatika",
            "started_at": "2024-08-01T08:00",
        }

        # Anonymous user -> 403
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 403)

        # Regular user -> 403
        self.client.login(username="regularuser", password="userpassword123")
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 403)

    def test_create_education_ajax_success_by_superuser(self):
        url = reverse("main:create_education_ajax")
        self.client.login(username="admin", password="adminpassword123")
        post_data = {
            "institution_name": "Institut Teknologi Bandung",
            "program": "Teknik Informatika",
            "started_at": "2024-08-01T08:00",
            "score": 85.5,
            "description": "Program pertukaran",
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("pk", data)
        self.assertTrue(Education.objects.filter(institution_name="Institut Teknologi Bandung").exists())

    def test_create_education_ajax_invalid_data(self):
        url = reverse("main:create_education_ajax")
        self.client.login(username="admin", password="adminpassword123")
        # Missing required started_at
        response = self.client.post(url, {"institution_name": "ITB"})
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("errors", data)

    def test_xss_protection_strips_html_tags(self):
        url = reverse("main:create_education_ajax")
        self.client.login(username="admin", password="adminpassword123")
        post_data = {
            "institution_name": '<img src="x" onerror="alert(\'XSS!\')">Universitas Indonesia',
            "program": '<b>Ilmu Komputer</b>',
            "started_at": "2024-08-01T08:00",
            "description": '<a href="javascript:alert(1)">Deskripsi</a>',
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()

        created_edu = Education.objects.get(pk=data["pk"])
        self.assertEqual(created_edu.institution_name, "Universitas Indonesia")
        self.assertEqual(created_edu.program, "Ilmu Komputer")
        self.assertEqual(created_edu.description, "Deskripsi")

    def test_toggle_star_education(self):
        url = reverse("main:toggle_star_education", kwargs={"education_id": self.education.pk})
        self.client.login(username="regularuser", password="userpassword123")

        # Toggle on
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.education.starred_by.filter(pk=self.regular_user.pk).exists())

        # Toggle off
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.education.starred_by.filter(pk=self.regular_user.pk).exists())


