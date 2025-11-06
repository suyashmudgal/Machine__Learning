
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email



class Customer(User):
    def __init__(self, name, email):
        super().__init__(name, email)

    def place_order(self, item):
        print(f"{self.name} placed an order for {item.name}.")
        return item



class Chef(User):
    def __init__(self, name, email):
        super().__init__(name, email)

    def prepare_order(self, item):
        print(f"Chef {self.name} is preparing {item.name}...")
        item.prepare()
        print(f"Bill Amount: ₹{item.price}\n")



class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def prepare(self):
        raise NotImplementedError("Subclass must implement prepare()")



class Pizza(MenuItem):
    def __init__(self, size, price):
        super().__init__("Pizza", price)
        self.size = size

    def prepare(self):
        print(f"Preparing a {self.size} {self.name} with cheese & toppings.")



class Burger(MenuItem):
    def __init__(self, burger_type, price):
        super().__init__("Burger", price)
        self.burger_type = burger_type

    def prepare(self):
        print(f"Preparing a {self.burger_type} {self.name} with sauces & fillings.")



if __name__ == "__main__":
   
    customer = Customer("Rahul", "rahul@example.com")
    chef = Chef("Amit", "amit@restaurant.com")

   
    pizza = Pizza("Large", 350)
    order1 = customer.place_order(pizza)
    chef.prepare_order(order1)

 
    burger = Burger("Veg", 150)
    order2 = customer.place_order(burger)
    chef.prepare_order(order2)
