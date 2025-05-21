#-------IMPORTS-------

import unittest
from typing import List
from checkout import CheckOut, PricingRule, StoreItem

#-------TESTING SUITE-------

class TestCheckout(unittest.TestCase):

    def setUp(self):
        self.A = StoreItem("A", 50.0)
        self.B = StoreItem("B", 30.0)
        self.C = StoreItem("C", 20.0)
        self.D = StoreItem("D", 15.0)
        
        self.pricing_rules = [
            PricingRule(3, "A", "A", 30, False),  # 3 for 130 instead of 150
            PricingRule(2, "B", "B", 15, False)   # 2 for 45 instead of 60
        ]
    
    def price(self, goods: str) -> float:
        #Helper function to test price combos
        co = CheckOut(self.pricing_rules)
        for item_name in goods:
            if item_name == "A":
                co.scan(self.A)
            elif item_name == "B":
                co.scan(self.B)
            elif item_name == "C":
                co.scan(self.C)
            elif item_name == "D":
                co.scan(self.D)
        return co.get_total_cost()
    
    def test_totals(self):
        #test that total are being added correctly, regardless of combination
        self.assertEqual(0, self.price(""))
        self.assertEqual(50, self.price("A"))
        self.assertEqual(80, self.price("AB"))
        self.assertEqual(115, self.price("CDBA"))
        self.assertEqual(100, self.price("AA"))
        self.assertEqual(130, self.price("AAA"))
        self.assertEqual(180, self.price("AAAA"))
        self.assertEqual(230, self.price("AAAAA"))
        self.assertEqual(260, self.price("AAAAAA"))
        self.assertEqual(160, self.price("AAAB"))
        self.assertEqual(175, self.price("AAABB"))
        self.assertEqual(190, self.price("AAABBD"))
        self.assertEqual(190, self.price("DABABA"))
        self.assertEqual(190, self.price("DBBAAA"))
    
    def test_incremental(self):
        #test that totals are valid at each scan
        co = CheckOut(self.pricing_rules)
        self.assertEqual(0, co.get_total_cost())
        
        co.scan(self.A)
        self.assertEqual(50, co.get_total_cost())
        
        co.scan(self.B)
        self.assertEqual(80, co.get_total_cost())
        
        co.scan(self.A)
        self.assertEqual(130, co.get_total_cost())
        
        co.scan(self.A)
        self.assertEqual(160, co.get_total_cost())
        
        co.scan(self.B)
        self.assertEqual(175, co.get_total_cost())
    
    def test_unscan(self):
        #test that items can be unscanned
        co = CheckOut(self.pricing_rules)
        
        co.scan(self.A)
        self.assertEqual(50, co.get_total_cost())
        co.unscan(self.A)
        self.assertEqual(0, co.get_total_cost())
        
        co.scan(self.A)
        co.scan(self.B)
        co.scan(self.A)
        co.unscan(self.A)
        self.assertEqual(80, co.get_total_cost())  # Should be A + B = 80
    
    def test_unscan_error(self):
        #Test error on unscanning items
        co = CheckOut(self.pricing_rules)

        with self.assertRaises(ValueError):
            co.unscan(self.C)
    
    def test_discount_limits(self):
        #test discounts with limits to ensure that they're only being applied a valid number of times
        limited_rules = [
            PricingRule(3, "A", "A", 30, 1),  # Limit to one set of 3
            PricingRule(2, "B", "B", 15, 2)   # Limit to two sets of 2
        ]
        
        co = CheckOut(limited_rules)
        
        for _ in range(6):
            co.scan(self.A)
        self.assertEqual(280, co.get_total_cost())
        
        for _ in range(6):
            co.scan(self.B)
        self.assertEqual(430, co.get_total_cost())


if __name__ == "__main__":
    unittest.main()

# def test_checkout_output():
#         pricing_rules = [
#             PricingRule(3, "A", "A", 30.0, False), 
#             PricingRule(2, "B", "B", 15.0, False),  
#             PricingRule(1, "C", "C", 17.0, False)
#         ]

#         A = StoreItem("A", 50.0)
#         B = StoreItem("B", 30.0)
#         C = StoreItem("C", 20.0)
#         D = StoreItem("D", 15.0)

#         co = CheckOut(pricing_rules)
#         co.scan(A)
#         co.scan(A)
#         co.scan(B)
#         co.scan(A)
#         co.scan(B)
#         co.scan(C)
#         co.scan(C)
#         co.scan(D)
#         co.scan(A)

#         co.get_item_summary()

#test_checkout_output()