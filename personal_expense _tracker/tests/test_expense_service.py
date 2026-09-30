import unittest
import os
from database.db_manager import init_database
from services.expense_service import add_expense, get_all_expenses, save_category_budget
from models.expense import make_expense

class TestExpenseService(unittest.TestCase):
    """Unit tests for expense service logic using a temporary test database."""

    def setUp(self):
        self.test_db = os.path.join("data", "unittest_tracker.db")
        init_database(db_path=self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_add_expense(self):
        exp = make_expense("Test Lunch", 15.50, "Food & Dining", "2026-03-01")
        res = add_expense(exp, db_path=self.test_db)
        self.assertTrue(res["success"])
        self.assertIsNotNone(res["id"])

    def test_get_all_expenses(self):
        exp = make_expense("Coffee", 4.00, "Food & Dining", "2026-03-01")
        add_expense(exp, db_path=self.test_db)
        records = get_all_expenses(db_path=self.test_db)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["title"], "Coffee")

    def test_budget_alert(self):
        save_category_budget("Food & Dining", 50.0, db_path=self.test_db)
        exp = make_expense("Dinner", 45.0, "Food & Dining", "2026-03-01")
        res = add_expense(exp, db_path=self.test_db)
        self.assertIsNotNone(res["warning"])
        self.assertIn("WARNING", res["warning"])

if _name_ == "_main_":
    unittest.main()