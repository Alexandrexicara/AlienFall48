class Inventory:


    def __init__(self):

        self.items = {}



    def add_item(self, item, amount=1):

        if item in self.items:

            self.items[item] += amount

        else:

            self.items[item] = amount



    def remove_item(self, item, amount=1):

        if item in self.items:

            self.items[item] -= amount


            if self.items[item] <= 0:

                del self.items[item]



    def has_item(self, item):

        return item in self.items



    def get_amount(self, item):

        if item in self.items:

            return self.items[item]

        return 0



    def clear(self):

        self.items.clear()



    def get_all(self):

        return self.items



    def print_inventory(self):

        print("=== INVENTÁRIO ===")

        for item, amount in self.items.items():

            print(
                item,
                ":",
                amount
            )
