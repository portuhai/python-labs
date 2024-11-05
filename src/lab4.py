class Product:
    def __init__(self, manufacturer="Some", height=0, price=0, material="some", details="Some", distance=0):
        self.__tree_manufacturer = manufacturer
        self.__tree_height = height
        self.__tree_price = price
        self.__tree_material = material
        self.tree_details = details
        self.tree_distance = distance

    def get_manufacturer(self):
        return self.__tree_manufacturer

    def set_manufacturer(self, manufacturer):
        self.__tree_manufacturer = manufacturer

    def get_height(self):
        return self.__tree_height

    def set_height(self, height):
        self.__tree_height = height

    def get_price(self):
        return self.__tree_price

    def set_price(self, price):
        self.__tree_price = price

    def get_material(self):
        return self.__tree_material

    def set_material(self, material):
        self.__tree_material = material

    def __str__(self):
        return f"Fake christmas tree: manufacturer={self.__tree_manufacturer},\
height={self.__tree_height}, price={self.__tree_price}, material={self.__tree_material},{self.tree_details}, distance to seller={self.tree_distance}m"

    def __repr__(self):
        return f"Fake christmas tree: manufacturer='{self.__tree_manufacturer}',\
height={self.__tree_height}, price={self.__tree_price}, material={self.__tree_material},{self.tree_details}, distance to seller={self.tree_distance}m"

    def __del__(self):
        print("Tree deleted")

def main():
    christmas_tree_0 = Product()
    christmas_tree_1 = Product("Yalinka", 170, 1700, "plastic","soft", 1500)
    christmas_tree_2 = Product("Yalinka", 250, 2500, "plastic", "fluffy", 1530)
    christmas_tree_3 = Product("Yalinka", 270, 3000, "plastic", "not suitable for flat", 13000)
    print(christmas_tree_0)
    print(christmas_tree_1)
    print(christmas_tree_2)
    print(repr(christmas_tree_3))

main()
