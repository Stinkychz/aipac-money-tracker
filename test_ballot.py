import unittest
from ballot import side_totals, top_donors


def cover(fid, amend, filer): return {"FILING_ID": fid, "AMEND_ID": str(amend), "FILER_ID": filer}
def rcpt(fid, amend, name, amt, cmte="", form="A", rec="RCPT"):
    return {"FILING_ID": fid, "AMEND_ID": str(amend), "FORM_TYPE": form, "REC_TYPE": rec,
            "CTRIB_NAML": name, "AMOUNT": str(amt), "CMTE_ID": cmte}


CMTES = {"Y1": "yes", "Y2": "yes", "N1": "no"}


class Totals(unittest.TestCase):
    def test_both_sides_and_donor_on_both(self):
        s = side_totals([cover("1", 0, "Y1"), cover("2", 0, "N1")],
                        [rcpt("1", 0, "Acme", 100), rcpt("2", 0, "Acme", 40)], CMTES)
        self.assertEqual((s["yes"]["total"], s["no"]["total"]), (100, 40))

    def test_amendment_replaces_old_filing(self):
        s = side_totals([cover("1", 0, "Y1"), cover("1", 1, "Y1")],
                        [rcpt("1", 0, "Acme", 100), rcpt("1", 1, "Acme", 90)], CMTES)
        self.assertEqual(s["yes"]["total"], 90)

    def test_pass_through_not_counted_twice(self):
        s = side_totals([cover("1", 0, "Y1"), cover("2", 0, "Y2")],
                        [rcpt("1", 0, "Acme", 100), rcpt("2", 0, "Y1 cmte", 100, cmte="Y1")], CMTES)
        self.assertEqual(s["yes"]["total"], 100)
        self.assertEqual(s["yes"]["viaCommittee"], 100)

    def test_no_money_on_one_side(self):
        s = side_totals([cover("1", 0, "Y1")], [rcpt("1", 0, "Acme", 5)], CMTES)
        self.assertEqual(s["no"]["total"], 0)
        self.assertEqual(top_donors(s["no"]), [])

    def test_other_committees_and_other_schedules_ignored(self):
        s = side_totals([cover("1", 0, "ZZ"), cover("2", 0, "Y1")],
                        [rcpt("1", 0, "Acme", 9), rcpt("2", 0, "Acme", 7, form="C")], CMTES)
        self.assertEqual(s["yes"]["total"], 0)

    def test_top_donors_ranked(self):
        s = side_totals([cover("1", 0, "Y1")],
                        [rcpt("1", 0, "A", 5), rcpt("1", 0, "B", 9), rcpt("1", 0, "A", 6)], CMTES)
        self.assertEqual(top_donors(s["yes"], 2), [("A", 11.0), ("B", 9.0)])


if __name__ == "__main__":
    unittest.main()
