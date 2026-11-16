import unittest
from build import count_changed, next_log, filing_dates


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


class FilingDates(unittest.TestCase):
    def test_only_monthly_and_year_end_sorted_no_repeats(self):
        rows = [
            {"report_type": "YE", "report_type_full": "YEAR-END", "due_date": "2027-01-31"},
            {"report_type": "30GR", "due_date": "2026-12-31"},
            {"report_type": "12G", "report_type_full": "PRE-GENERAL", "due_date": "2026-10-22"},
            {"report_type": "M12", "report_type_full": "DECEMBER MONTHLY", "due_date": "2026-12-20"},
            {"report_type": "M12", "report_type_full": "DECEMBER MONTHLY", "due_date": "2026-12-20"},
        ]
        self.assertEqual(filing_dates(rows), [{"due": "2026-12-20", "name": "December Monthly"},
                                              {"due": "2027-01-31", "name": "Year-End"}])


if __name__ == "__main__":
    unittest.main()
