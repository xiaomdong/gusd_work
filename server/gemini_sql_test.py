import os
import unittest
from gemini_sql import *


class testBank(unittest.TestCase):

    def setUp(self):
        self.gemini = gemini("test.db")
        self.gemini.run()

    def tearDown(self):
        self.gemini.exit()
        os.remove("test.db")


    def test_add_new_user(self):
        self.gemini.addUser("xd1_gemini","12345678","xd1@gmail.com","18033441000","xd1_withdraw_bank","xd1_withdraw_address","xd1_deposit_address")
        result= self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][0], 0)
        self.assertEqual(result[0][1], 0)

        result =self.gemini.sql.getUser("xd1_gemini")
        # print(result)

        self.assertNotEqual(result,None)
        self.assertEqual(result[0][0], "xd1_gemini")
        self.assertEqual(result[0][1], "12345678")
        self.assertEqual(result[0][2], "xd1@gmail.com")
        self.assertEqual(result[0][3], "18033441000")
        self.assertEqual(result[0][4], "xd1_withdraw_bank")
        self.assertEqual(result[0][5], "xd1_withdraw_address")
        self.assertEqual(result[0][6], "xd1_deposit_address")


        self.gemini.addUser("xd1_gemini","87654321","xd1@gmail.com","17033441000","xd1_withdraw_bank1","xd1_withdraw_address1","xd1_deposit_address1")
        result= self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][0], 0)
        self.assertEqual(result[0][1], 0)

        result =self.gemini.sql.getUser("xd1_gemini")
        # print(result)
        self.assertNotEqual(result,None)
        self.assertEqual(result[0][0], "xd1_gemini")
        self.assertEqual(result[0][1], "87654321")
        self.assertEqual(result[0][2], "xd1@gmail.com")
        self.assertEqual(result[0][3], "17033441000")
        self.assertEqual(result[0][4], "xd1_withdraw_bank1")
        self.assertEqual(result[0][5], "xd1_withdraw_address1")
        self.assertEqual(result[0][6], "xd1_deposit_address1")


    def test_depositUSD(self):
        self.gemini.addUser("xd1_gemini", "12345678", "xd1@gmail.com", "18033441000", "xd1_withdraw_bank",
                            "xd1_withdraw_address", "xd1_deposit_address")
        result = self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][0], 0)
        self.assertEqual(result[0][1], 0)

        self.gemini.depositUSD("xd1_gemini",100)
        result = self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][0], 100)
        self.assertEqual(result[0][1], 0)

        self.gemini.depositUSD("xd1_gemini",200)
        result = self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][0], 300)
        self.assertEqual(result[0][1], 0)

        self.gemini.depositUSD("xd1_gemini",55)
        result = self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][0], 355)
        self.assertEqual(result[0][1], 0)

        self.gemini.depositUSD("xd1_gemini",1000)
        result = self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][0], 1355)
        self.assertEqual(result[0][1], 0)


    def test_depositGUSD(self):
        self.gemini.addUser("xd1_gemini", "12345678", "xd1@gmail.com", "18033441000", "xd1_withdraw_bank",
                            "xd1_withdraw_address", "xd1_deposit_address")
        result = self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][0], 0)
        self.assertEqual(result[0][1], 0)


        self.gemini.addUser("xd2_gemini", "12345678", "xd2@gmail.com", "18033441001", "xd2_withdraw_bank",
                            "xd2_withdraw_address", "xd2_deposit_address")
        result = self.gemini.getBalance("xd2_gemini")
        self.assertEqual(result[0][0], 0)
        self.assertEqual(result[0][1], 0)

        self.gemini.depositGUSD("xd2_gemini",100)
        result = self.gemini.getBalance("xd2_gemini")
        self.assertEqual(result[0][1], 100)
        self.assertEqual(result[0][0], 0)


        self.gemini.depositGUSD("xd2_gemini",200)
        result = self.gemini.getBalance("xd2_gemini")
        self.assertEqual(result[0][1], 300)
        self.assertEqual(result[0][0], 0)

        self.gemini.depositGUSD("xd1_gemini",100)
        result = self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][1], 100)
        self.assertEqual(result[0][0], 0)


        self.gemini.depositGUSD("xd1_gemini",200)
        result = self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][1], 300)
        self.assertEqual(result[0][0], 0)

        self.gemini.depositGUSD("xd1_gemini",55)
        result = self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][1], 355)
        self.assertEqual(result[0][0], 0)

        self.gemini.depositGUSD("xd1_gemini",1000)
        result = self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][1], 1355)
        self.assertEqual(result[0][0], 0)

        self.gemini.depositGUSD("xd2_gemini",55)
        result = self.gemini.getBalance("xd2_gemini")
        self.assertEqual(result[0][1], 355)
        self.assertEqual(result[0][0], 0)

        self.gemini.depositGUSD("xd2_gemini",1000)
        result = self.gemini.getBalance("xd2_gemini")
        self.assertEqual(result[0][1], 1355)
        self.assertEqual(result[0][0], 0)

    def test_withdrawalUSD(self):
        self.gemini.addUser("xd1_gemini", "12345678", "xd1@gmail.com", "18033441000", "xd1_withdraw_bank",
                            "xd1_withdraw_address", "xd1_deposit_address")
        result = self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][0], 0)
        self.assertEqual(result[0][1], 0)

        self.gemini.addUser("xd2_gemini", "12345678", "xd2@gmail.com", "18033441001", "xd2_withdraw_bank",
                            "xd2_withdraw_address", "xd2_deposit_address")
        result = self.gemini.getBalance("xd2_gemini")
        self.assertEqual(result[0][0], 0)
        self.assertEqual(result[0][1], 0)

        self.gemini.depositUSD("xd1_gemini",100)
        result = self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][0], 100)
        self.assertEqual(result[0][1], 0)

        self.gemini.depositUSD("xd2_gemini",100)
        result = self.gemini.getBalance("xd2_gemini")
        self.assertEqual(result[0][0], 100)
        self.assertEqual(result[0][1], 0)


        self.gemini.withdrawalUSD("xd1_gemini",100)
        result = self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][0], 0)
        self.assertEqual(result[0][1], 0)

        self.gemini.withdrawalUSD("xd2_gemini",100)
        result = self.gemini.getBalance("xd2_gemini")
        self.assertEqual(result[0][0], 0)
        self.assertEqual(result[0][1], 0)



    def test_withdrawalUSD(self):
        self.gemini.addUser("xd1_gemini", "12345678", "xd1@gmail.com", "18033441000", "xd1_withdraw_bank",
                            "xd1_withdraw_address", "xd1_deposit_address")
        result = self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][0], 0)
        self.assertEqual(result[0][1], 0)

        self.gemini.addUser("xd2_gemini", "12345678", "xd2@gmail.com", "18033441000", "xd2_withdraw_bank",
                            "xd2_withdraw_address", "xd2_deposit_address")
        result = self.gemini.getBalance("xd2_gemini")
        self.assertEqual(result[0][0], 0)
        self.assertEqual(result[0][1], 0)

        self.gemini.depositGUSD("xd1_gemini",100)
        result = self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][1], 100)
        self.assertEqual(result[0][0], 0)

        self.gemini.depositGUSD("xd2_gemini",100)
        result = self.gemini.getBalance("xd2_gemini")
        self.assertEqual(result[0][1], 100)
        self.assertEqual(result[0][0], 0)


        self.gemini.withdrawalGUSD("xd1_gemini",100)
        result = self.gemini.getBalance("xd1_gemini")
        self.assertEqual(result[0][0], 0)
        self.assertEqual(result[0][1], 0)

        self.gemini.withdrawalGUSD("xd2_gemini",100)
        result = self.gemini.getBalance("xd2_gemini")
        self.assertEqual(result[0][0], 0)
        self.assertEqual(result[0][1], 0)






if __name__ == '__main__':
    suite = unittest.TestSuite()
    tests = [testBank("test_add_new_user"),
             testBank("test_depositUSD"),
             testBank("test_depositGUSD"),
             testBank("test_withdrawalUSD"),
             testBank("test_withdrawalUSD"),
             ]

    suite.addTests(tests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
