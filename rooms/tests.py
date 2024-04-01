from django.test import TestCase, client
from django.urls import reverse
from rooms.models import Review, Room
from accounts.models import Profile
class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(
            username='testuser', password='testpassword')
        self.room = Room.objects.create(
            name='testroom', capacity=10, is_active=True)
        self.review = Review.objects.create(
            room_id=1, user=self.user, content='Test Content', rating=5)

    def test_review_content(self):
        self.assertEqual(f'{self.review.room}', 'testroom')
        self.assertEqual(f'{self.review.user}', 'testuser')
        self.assertEqual(self.review.content, 'Test Content')
        self.assertEqual(self.review.rating, 5)


class ReviewViewTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(
            username='testuser', password='testpassword')

        self.room = Room.objects.create(
            name='testroom', capacity=10, is_active=True)

        self.client.login(
            username='testuser', password='testpassword')

        self.review = Review.objects.create(
            room_id=1, user=self.user, content='Test Content', rating=5)

    def test_review_list_view(self):
        response = self.client.get(reverse('rooms:reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rooms/review.html')

    def test_review_detail_view(self):
        response = self.client.get(
            reverse('rooms:review_detail', args=[self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Content')
        self.assertTemplateUsed(response, 'rooms/review_detail.html')

    def test_review_create_view(self):
        response = self.client.post(reverse('rooms:review_create'), {
            'room': 1,
            'content': 'New Test Content',
            'rating': 4
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(content='New Test Content').exists())

    def test_review_update_view(self):
        response = self.client.post(reverse('rooms:review_update', args=[self.review.id]), {
            'room': 1,
            'content': 'Updated Test Content',
            'rating': 3
        })
        self.assertEqual(response.status_code, 302)
        self.review.refresh_from_db()
        self.assertEqual(self.review.content, 'Updated Test Content')

    def test_review_delete_view(self):
        response = self.client.post(reverse('rooms:review_delete', args=[self.review.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(content='Test Content').exists())