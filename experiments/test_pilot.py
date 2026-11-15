import unittest
from run_pilot import tasks, clean, analyst, check_independently, equal, evaluate, VARIANTS

class TestPilot(unittest.TestCase):
    def test_split(self):
        self.assertEqual((len(tasks()),sum(t["split"]=="test" for t in tasks())),(20,15))
    def test_full_clean_matches_checker(self):
        for task in tasks():
            rows,_ = clean(task["rows"],True,True)
            self.assertTrue(equal(analyst(task,rows),check_independently(task,task["rows"])))
    def test_checker_has_no_reference_access(self):
        task = tasks()[7]
        before = check_independently(task,task["rows"])
        task["expected"] = -9999
        self.assertEqual(before,check_independently(task,task["rows"]))
    def test_repair(self):
        for task in tasks():
            self.assertTrue(evaluate(task,VARIANTS[6])["accepted_correct"])

if __name__ == "__main__":
    unittest.main()
