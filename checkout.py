#-------IMPORTS--------

from typing import List, Literal

#-------CLASSES--------

#pricing rule class - describes the discount rules in the store
#for every n of item y, item x costs b - costs a otherwise (y can be x) - can set limit on amount of offers
class PricingRule:

    def __init__(self, frequency: int, item1_name: str, item2_name: str, new_cost: float, limit: int | Literal[False]):
        self.frequency = frequency
        self.item1_name = item1_name
        self.item2_name = item2_name
        self.new_cost = new_cost
        self.limit = limit

#store item class - describes an item in the store getting scanned
class StoreItem:

    def __init__(self, name: str, base_cost: float):
        self.name = name
        self.base_cost = base_cost

    def __repr__(self):
        return f"StoreItem(name: '{self.name}', cost: {self.base_cost})"

#cart item class - wrapper for storing items in the checkout
class CartItem:

    def __init__(self, store_item: StoreItem, actual_cost: float = None):
        self.store_item = store_item
        self.actual_cost = actual_cost if actual_cost is not None else store_item.base_cost
        self.name = store_item.name  # For convenience
    
    def __repr__(self):
        if self.actual_cost != self.store_item.base_cost:
            return f"CartItem('{self.name}', base: {self.store_item.base_cost}, discounted: {self.actual_cost})"
        return f"CartItem('{self.name}', cost: {self.actual_cost})"
   
#checkout class, used to initiate and manage a checkout interaction
class CheckOut:
    
    def __init__(self, pricing_rules: List[PricingRule]):
        self.pricing_rules = pricing_rules
        self.items = []
        self.total_cost = 0

    #checks through list of pricing rules - finds the first applicable one and applies it, otherwise returns the regular cost
    #LIMITATION - more than one discount can't be applied at once, discount priority
    def check_pricing_rules(self, item: StoreItem, item_count: int):
        for rule in self.pricing_rules:
            if (rule.item1_name == item.name) and (item_count % rule.frequency == 0):
                if (rule.limit == False) or (item_count <= rule.limit * rule.frequency):
                    return rule.new_cost
        return item.base_cost

    def get_total_cost(self):
        return sum(item.actual_cost for item in self.items)

    def get_item_summary(self):
        total_cost = self.get_total_cost()
        for item in self.items:
            print(item)
        print(f"Total cost: {total_cost}")

    def scan(self, item: StoreItem):
        item_count = sum(1 for i in self.items if i.name == item.name) + 1
        current_cost = self.check_pricing_rules(item, item_count)
        cart_item = CartItem(item, current_cost)
        self.items.append(cart_item)

    #unscan method for returning items/missed item
    def unscan(self, item: StoreItem):
        for i in range(len(self.items) - 1, -1, -1):
            if self.items[i].name == item.name:
                self.items.pop(i)
                break
        else:
            raise ValueError(f"{item.name} not in checkout list.")
