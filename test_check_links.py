import unittest, urllib.error
from check_links import source_links, find_broken


class Links(unittest.TestCase):
    def test_links_cover_committees_and_real_candidate_ids_only(self):
        urls = source_links([{"id": "H0AL01055"}, {"id": "S6TX00001"}, {"id": "XYZ"}])
        self.assertEqual(len(urls), 4)
        self.assertIn("https://www.fec.gov/data/candidate/H0AL01055/", urls)
        self.assertIn("https://www.fec.gov/data/committee/C00799031/", urls)
        self.assertNotIn("https://www.fec.gov/data/candidate/XYZ/", urls)

    def test_broken_found_by_code_http_error_and_crash(self):
        def status(u):
            if u == "ok": return 200
            if u == "moved": return 301
            if u == "gone": return 404
            if u == "err": raise urllib.error.HTTPError(u, 503, "x", {}, None)
            raise TimeoutError()
        bad = find_broken(["ok", "moved", "gone", "err", "slow"], status)
        self.assertEqual(bad, [("gone", "HTTP 404"), ("err", "HTTP 503"), ("slow", "TimeoutError")])

    def test_no_links_no_problems(self):
        self.assertEqual(find_broken([], None), [])


if __name__ == "__main__":
    unittest.main()
