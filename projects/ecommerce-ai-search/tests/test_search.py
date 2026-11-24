import unittest
from search import search_products


class TestProductSearch(unittest.TestCase):

    def test_smartphone_search(self):
        results = search_products("smartphone")
        self.assertGreater(len(results), 0)

    def test_laptop_search(self):
        results = search_products("laptop")
        self.assertGreater(len(results), 0)

    def test_unknown_product(self):
        results = search_products("spaceship")
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()