import os
import unittest
from bank_sql import *


class testBank(unittest.TestCase):

    def setUp(self):
        self.bank = Bank("test.db")
        self.bank.run()

    def tearDown(self):
        self.bank.exit()
        os.remove("test.db")

    def test_deposit_new_account(self):
        self.bank.deposit("xd1", 0)
        value = self.bank.getBalance("xd1")
        self.assertEqual(value, 0)

        self.bank.deposit("xd1", 100)
        value = self.bank.getBalance("xd1")
        self.assertEqual(value, 100)

        self.bank.deposit("xd1", 100)
        value = self.bank.getBalance("xd1")
        self.assertEqual(value, 200)

        self.bank.deposit("xd1", 55)
        value = self.bank.getBalance("xd1")
        self.assertEqual(value, 255)

    def test_withdrawal(self):
        self.bank.deposit("xd1", 100)
        result = self.bank.withdrawal("xd1", 100)
        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], 100)
        value = self.bank.getBalance("xd1")
        self.assertEqual(value, 0)

        result = self.bank.withdrawal("xd1", 0)
        self.assertEqual(result, None)

    def test_withdrawal_err(self):
        result = self.bank.withdrawal("xd1", 100)
        self.assertEqual(result, None)

    def test_transfer(self):
        self.bank.deposit("xd1", 100)
        self.bank.deposit("xd2", 100)
        result = self.bank.transfer("xd1", "xd2", 100)
        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], 100)

        value = self.bank.getBalance("xd2")
        self.assertEqual(value, 200)
        value = self.bank.getBalance("xd1")
        self.assertEqual(value, 0)

        self.bank.transfer("xd2", "xd1", 100)
        value = self.bank.getBalance("xd2")
        self.assertEqual(value, 100)
        value = self.bank.getBalance("xd1")
        self.assertEqual(value, 100)

        self.bank.transfer("xd2", "xd1", 100)
        value = self.bank.getBalance("xd2")
        self.assertEqual(value, 0)
        value = self.bank.getBalance("xd1")
        self.assertEqual(value, 200)

        self.bank.transfer("xd1", "xd2", 0)
        value = self.bank.getBalance("xd2")
        self.assertEqual(value, 0)
        value = self.bank.getBalance("xd1")
        self.assertEqual(value, 200)

        self.bank.transfer("xd1", "xd2", 50)
        value = self.bank.getBalance("xd2")
        self.assertEqual(value, 50)
        value = self.bank.getBalance("xd1")
        self.assertEqual(value, 150)

    def test_transfer_err(self):
        self.bank.deposit("xd1", 100)
        self.bank.deposit("xd2", 100)
        result = self.bank.transfer("xd1", "xd2", 200)
        self.assertEqual(result, None)

        result = self.bank.transfer("xd1", "xd2", 0)
        self.assertEqual(result, None)

    def test_getrecord(self):
        self.bank.deposit("xd1", 100)
        self.bank.deposit("xd2", 100)
        result = self.bank.transfer("xd1", "xd2", 10)
        result = self.bank.sql.getRecord("xd1")
        print(result)
        result = self.bank.sql.getRecord("xd2")
        print(result)
        result = self.bank.sql.getRecordIndex()
        print(result)
        self.assertEqual(None, None)



if __name__ == '__main__':
    suite = unittest.TestSuite()
    tests = [testBank("test_deposit_new_account"),
             testBank("test_withdrawal"),
             testBank("test_withdrawal_err"),
             testBank("test_transfer"),
             testBank("test_transfer_err"),
             ]

    suite.addTests(tests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
