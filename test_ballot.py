import io
import os
import tempfile
import unittest
import zipfile
from ballot import side_totals, top_donors, top_share, read_rows, read_zip_table


def cover(fid, amend, filer): return {"FILING_ID": fid, "AMEND_ID": str(amend), "FILER_ID": filer}
def rcpt(fid, amend, name, amt, cmte="", form="A", rec="RCPT", st="CA"):
    return {"FILING_ID": fid, "AMEND_ID": str(amend), "FORM_TYPE": form, "REC_TYPE": rec,
            "CTRIB_NAML": name, "AMOUNT": str(amt), "CMTE_ID": cmte, "CTRIB_ST": st}


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


TSV = 'FILING_ID\tAMEND_ID\tCTRIB_NAML\tAMOUNT\n1\t0\t"Smith\tJr"\t5\n\n2\t1\tAcme\n'


class Reader(unittest.TestCase):
    def test_rows_quoted_tab_short_row_and_blank_line(self):
        rows = list(read_rows(io.StringIO(TSV)))
        self.assertEqual(rows[0]["CTRIB_NAML"], "Smith	Jr")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1]["AMOUNT"], "")  # short row padded, not crashed

    def test_wanted_columns_only(self):
        self.assertEqual(list(read_rows(io.StringIO(TSV), {"AMOUNT"}))[0], {"AMOUNT": "5"})

    def test_empty_file(self):
        self.assertEqual(list(read_rows(io.StringIO(""))), [])

    def test_reads_member_from_zip(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "b.zip")
            with zipfile.ZipFile(p, "w") as z:
                z.writestr("CalAccess/DATA/RCPT_CD.TSV", TSV)
            rows = list(read_zip_table(p, "CalAccess/DATA/RCPT_CD.TSV"))
        self.assertEqual(rows[0]["FILING_ID"], "1")

    def test_top3_share_and_out_of_state(self):
        rows = [rcpt("1", 0, "A", 60), rcpt("1", 0, "B", 20, st="NY"), rcpt("1", 0, "C", 10),
                rcpt("1", 0, "D", 10, st="TX")]
        s = side_totals([cover("1", 0, "Y1")], rows, CMTES)
        self.assertAlmostEqual(top_share(s["yes"], 3), 0.9)
        self.assertEqual(s["yes"]["outOfState"], 30)

    def test_top_share_empty_side(self):
        s = side_totals([], [], CMTES)
        self.assertEqual(top_share(s["no"]), 0.0)


if __name__ == "__main__":
    unittest.main()
