import unittest
from unittest.mock import patch, MagicMock
import sys
from client import BestBuy, ProductAPI

class TestBestBuyAPI(unittest.TestCase):

    def setUp(self):
        self.best_buy = BestBuy()

    @patch('client._request')
    def test_search_with_keyword(self, mock_request):
        mock_request.return_value = {'products': [{'sku': '1234567890', 'name': 'Test Product', 'description': 'This is a test product', 'regularPrice': 99.99}]}
        products = self.best_buy.ProductAPI.search(keyword='test')
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].sku, '1234567890')
        self.assertEqual(products[0].name, 'Test Product')
        self.assertEqual(products[0].description, 'This is a test product')
        self.assertEqual(products[0].regularPrice, 99.99)

    @patch('client._request')
    def test_search_with_keyword_and_attributes(self, mock_request):
        mock_request.return_value = {'products': [{'sku': '1234567890', 'name': 'Test Product', 'description': 'This is a test product', 'regularPrice': 99.99}]}
        products = self.best_buy.ProductAPI.search(keyword='test', customerReviewAverage=4.5)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].sku, '1234567890')
        self.assertEqual(products[0].name, 'Test Product')
        self.assertEqual(products[0].description, 'This is a test product')
        self.assertEqual(products[0].regularPrice, 99.99)

    @patch('client._request')
    def test_search_sku(self, mock_request):
        mock_request.return_value = {'products': [{'sku': '5721600', 'name': 'MacBook Air 13.3" Laptop - Apple M1 chip - 8GB Memory - 256GB SSD - Space Gray', 'description': '', 'regularPrice': 999.99}]}
        product = self.best_buy.ProductAPI.search_sku('1234567890')
        self.assertIsNotNone(product)
        self.assertEqual(product.sku, '5721600')
        self.assertEqual(product.name, 'MacBook Air 13.3" Laptop - Apple M1 chip - 8GB Memory - 256GB SSD - Space Gray')
        self.assertEqual(product.description, '')
        self.assertEqual(product.regularPrice, 999.99)

    @patch('client._request')
    def test_search_upc(self, mock_request):
        mock_request.return_value = {'products': [{'sku': '1234567890', 'name': 'Test Product', 'description': 'This is a test product', 'regularPrice': 99.99}]}
        product = self.best_buy.ProductAPI.search_upc('1234567890')
        self.assertIsNotNone(product)
        self.assertEqual(product.sku, '1234567890')
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.description, 'This is a test product')
        self.assertEqual(product.regularPrice, 99.99)

    @patch('client._request')
    def test_search_description(self, mock_request):
        mock_request.return_value = {'products': [{'sku': '1234567890', 'name': 'Test Product', 'description': 'This is a test product', 'regularPrice': 99.99}]}
        products = self.best_buy.ProductAPI.search_description('test')
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].sku, '1234567890')
        self.assertEqual(products[0].name, 'Test Product')
        self.assertEqual(products[0].description, 'This is a test product')


