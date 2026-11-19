import unittest
from build import count_changed, next_log, filing_dates, race_key, top_raisers, small_big


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


def weball_row(cid, name, party, raised, state, district, through="09/30/2026"):
    f = [""] * 30
    f[0], f[1], f[4], f[5], f[18], f[19], f[27] = cid, name, party, raised, state, district, through
    return "|".join(f)


class TopRaisers(unittest.TestCase):
    # Real row from the FEC's weball26.zip (Nov 19, 2026), to pin the column positions.
    REAL = ("S6AK00276|PELTOLA, MARY|C|1|DEM|36887509.15|2732081.26|32785383.22|0|0|4102125.93|0|0|0|0|0|0|"
            "32756766.41|AK|00||||||845258.64|1500|10/14/2026|178769.36|0")

    def test_race_keys(self):
        self.assertEqual(race_key("H", "CA", "14"), "H-CA-14")
        self.assertEqual(race_key("S", "AK", "00"), "S-AK")
        self.assertEqual(race_key("P", "00", "00"), "P")

    def test_real_row_columns(self):
        self.assertEqual(top_raisers([self.REAL], {"S-AK"}), {"S-AK": [
            {"id": "S6AK00276", "name": "PELTOLA, MARY", "party": "DEM", "raised": 36887509.15,
             "through": "10/14/2026"}]})

    def test_top_two_per_tracked_race_only(self):
        lines = [weball_row("H1", "A", "DEM", "100", "CA", "14"),
                 weball_row("H2", "B", "REP", "300", "CA", "14"),
                 weball_row("H3", "C", "LIB", "200", "CA", "14"),
                 weball_row("H4", "D", "DEM", "0", "CA", "14"),
                 weball_row("H5", "E", "DEM", "999", "CA", "15"),   # race not tracked
                 weball_row("H6", "F", "REP", "", "NY", "01"),      # raised nothing
                 "short|row"]
        got = top_raisers(lines, {"H-CA-14", "H-NY-01"})
        self.assertEqual([c["id"] for c in got["H-CA-14"]], ["H2", "H3"])
        self.assertNotIn("H-CA-15", got)
        self.assertNotIn("H-NY-01", got)


class SmallBig(unittest.TestCase):
    def test_real_row_split_at_200(self):
        # Peltola's itemized total from the FEC totals API (Nov 19, 2026), same coverage end as the weball row.
        got = small_big([TopRaisers.REAL], {"S6AK00276": (20327338.39, "2026-10-14")})
        self.assertEqual(got, {"S6AK00276": {"small": 12429428.02, "big": 20327338.39, "through": "10/14/2026"}})

    def test_left_out_when_sources_disagree(self):
        row = TopRaisers.REAL
        self.assertEqual(small_big([row], {"S6AK00276": (1.0, "2026-09-30")}), {})        # other period
        self.assertEqual(small_big([row], {"S6AK00276": (9e9, "2026-10-14")}), {})        # more than total
        self.assertEqual(small_big([row, "short|row"], {"H1": (1.0, "2026-10-14")}), {})  # not tracked


if __name__ == "__main__":
    unittest.main()
