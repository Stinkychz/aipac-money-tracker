import unittest
from build import count_changed, next_log


class RefreshLog(unittest.TestCase):
    def test_count_changed(self):
        old = [{"id": "A", "pac": 1}, {"id": "B", "pac": 2}, {"id": "C", "pac": 3}]
        new = [{"id": "A", "pac": 1}, {"id": "B", "pac": 5}, {"id": "D", "pac": 1}]
        self.assertEqual(count_changed(old, new), 3)  # B changed, C gone, D new
        self.assertEqual(count_changed(None, new), 3)
        self.assertEqual(count_changed(new, new), 0)

    def test_log_keeps_ten_newest_first(self):
        log = []
        for i in range(12):
            log = next_log(log, i, i)
        self.assertEqual(len(log), 10)
        self.assertEqual(log[0], {"at": 11, "changed": 11})
        self.assertEqual(log[-1]["at"], 2)


if __name__ == "__main__":
    unittest.main()
