import unittest
from app import app

class ProductBlueprintTests(unittest.TestCase):

    def setUp(self):

        app.config['TESTING'] = True
        self.client = app.test_client()


    def test_products_list_page_loads(self):

        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"list of products", response.data)

    def test_product_details_page_shows_id(self):

        response = self.client.get("/products/777")


        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Product ID: 777", response.data)