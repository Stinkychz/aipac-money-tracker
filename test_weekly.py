import unittest

import weekly

DAY = 24 * 3600 * 1000


def cand(cid, pac=0.0, support=0.0, oppose=0.0, n=True):
    c = {"id": cid, "name": "DOE, JANE", "party": "DEM", "office": "H", "state": "CA", "district": "14",
         "pac": pac, "support": support, "oppose": oppose}
    if n:
        c.update(nPac=int(pac > 0), nSupport=int(support > 0), nOppose=int(oppose > 0))
    return c


class Weekly(unittest.TestCase):
    def test_baseline_is_newest_a_week_old(self):
        snaps = [{"at": 20 * DAY}, {"at": 12 * DAY}, {"at": 9 * DAY}, None, {"at": 2 * DAY}]
        self.assertEqual(weekly.pick_baseline(snaps, 20 * DAY)["at"], 12 * DAY)
        self.assertIsNone(weekly.pick_baseline([{"at": 15 * DAY}], 20 * DAY))

    def test_moves_added_dropped_records(self):
        old = {"at": 0, "candidates": [cand("A", pac=1000), cand("B", support=500), cand("C", pac=5)]}
        new = {"at": 8 * DAY, "candidates": [cand("A", pac=3000), cand("B", support=500, oppose=9000),
                                              cand("D", pac=100)]}
        d = weekly.diff(old, new)
        self.assertEqual([m["c"]["id"] for m in d["moves"]], ["B", "A"])
        self.assertEqual(d["moves"][0]["by"], {"pac": 0, "support": 0, "oppose": 9000})
        self.assertEqual([c["id"] for c in d["added"]], ["D"])
        self.assertEqual([c["id"] for c in d["dropped"]], ["C"])
        self.assertEqual(d["records"], {"pac": 0, "support": 0, "oppose": 1})
        page = weekly.render(d)
        self.assertIn("Biggest moves", page)
        self.assertIn("+$9,000", page)
        self.assertIn("Nothing has been emailed", page)

    def test_old_snapshot_without_record_counts(self):
        old = {"at": 0, "candidates": [cand("A", pac=1000, n=False)]}
        new = {"at": 8 * DAY, "candidates": [cand("A", pac=1000)]}
        d = weekly.diff(old, new)
        self.assertIsNone(d["records"])
        self.assertIn("No new filings changed the figures", weekly.render(d))

    def test_quiet_period(self):
        snap = {"at": 0, "candidates": [cand("A", pac=1000)]}
        d = weekly.diff(snap, {**snap, "at": 8 * DAY})
        page = weekly.render(d)
        self.assertIn("No new filings changed the figures", page)
        self.assertNotIn("Biggest moves", page)

    def test_names_are_escaped(self):
        c = cand("A", pac=10)
        c["name"] = "<b>X</b>"
        self.assertNotIn("<b>X", weekly.who(c))

    def test_refunds_keep_their_minus_sign(self):
        self.assertEqual(weekly.money(-32301), "-$32,301")
        self.assertEqual(weekly.money(500, True), "+$500")
        self.assertEqual(weekly.money(500), "$500")
        self.assertIn("net refund", weekly.held(-6))
        self.assertEqual(weekly.held(6), "$6")


if __name__ == "__main__":
    unittest.main()
