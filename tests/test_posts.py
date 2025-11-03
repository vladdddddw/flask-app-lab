import unittest
from app import create_app, db
from app.posts.models import Post, PostCategory


class PostCRUDTestCase(unittest.TestCase):
    """
    Клас для тестування CRUD-операцій з Постами.
    """

    def setUp(self):
        """
        Виконується перед кожним тестом.
        Створює додаток у 'тестовому' режимі та чисту БД у пам'яті.
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        """
        Виконується після кожного тесту.
        Видаляє сесію та всі таблиці з БД.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_us01_create_post(self):
        """Тест US01: Створення нового поста."""
        response = self.client.post('/post/create', data={
            'title': 'My Test Post',
            'content': 'This is the content of the test post.',
            'category': 'tech',
            'publish_date': '2025-11-03T14:30',
            'is_active': True
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post My Test Post has been created!", response.data)
        post = db.session.scalar(db.select(Post).where(Post.title == 'My Test Post'))
        self.assertIsNotNone(post)
        self.assertEqual(post.category, PostCategory.TECH)

    def test_us02_list_posts(self):
        """Тест US02: Перегляд списку всіх постів."""

        post1 = Post(title="Post 1", content="Content 1", category=PostCategory.NEWS)
        db.session.add(post1)
        db.session.commit()

        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post 1', response.data)

    def test_us03_view_post_detail(self):
        """Тест US03: Перегляд одного поста."""
        post1 = Post(title="Detail Test", content="Full Content", category=PostCategory.NEWS)
        db.session.add(post1)
        db.session.commit()

        response = self.client.get(f'/post/{post1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Full Content', response.data)
        self.assertIn(b'Edit Post', response.data)

    def test_us04_update_post(self):
        """Тест US04: Редагування поста."""
        post1 = Post(title="Original Title", content="Original", category=PostCategory.NEWS)
        db.session.add(post1)
        db.session.commit()

        response = self.client.post(f'/post/{post1.id}/update', data={
            'title': 'Updated Title',
            'content': 'Updated Content',
            'category': 'other',
            'publish_date': '2025-01-01T01:00'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post Updated Title has been updated!", response.data)
        updated_post = db.get_or_404(Post, post1.id)
        self.assertEqual(updated_post.title, 'Updated Title')

    def test_us05_delete_post(self):
        """Тест US05: Видалення поста."""
        post1 = Post(title="To Be Deleted", content="Delete me", category=PostCategory.NEWS)
        db.session.add(post1)
        db.session.commit()
        post_id = post1.id

        response = self.client.post(f'/post/{post_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post To Be Deleted has been deleted.", response.data)

        deleted_post = db.session.get(Post, post_id)
        self.assertIsNone(deleted_post)

    def test_us06_404_not_found(self):
        """Тест US06: 404 при відсутньому пості."""
        response = self.client.get('/post/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)