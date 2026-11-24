
import unittest

from hybrid_search import hybrid_search


class TestHybridSearch(unittest.TestCase):

    def test_hybrid_returns_results(self):
        results = hybrid_search("smartphone")

        self.assertGreater(len(results), 0)

    def test_hybrid_result_structure(self):
        results = hybrid_search("laptop")

        self.assertIn("product", results[0])
        self.assertIn("rrf_score", results[0])

    def test_hybrid_respects_top_k(self):
        results = hybrid_search("computer", top_k=2)

        self.assertLessEqual(len(results), 2)


if __name__ == "__main__":
    unittest.main()
