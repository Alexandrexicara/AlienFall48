class Recipe:


    def __init__(self, name, materials, result):

        self.name = name

        self.materials = materials

        self.result = result



class CraftingSystem:


    def __init__(self):

        self.recipes = []


        self.create_recipes()



    def create_recipes(self):


        self.recipes.append(

            Recipe(

                "Pistola Laser",

                {
                    "Peça de Metal": 5,
                    "Cristal Alienígena": 2,
                    "Chip Alien": 1
                },

                "Pistola Laser"

            )

        )


        self.recipes.append(

            Recipe(

                "Kit Médico Avançado",

                {
                    "Peça de Metal": 2,
                    "Cristal Alienígena": 1
                },

                "Kit Médico Avançado"

            )

        )


        self.recipes.append(

            Recipe(

                "Munição Energética",

                {
                    "Cristal Alienígena": 1,
                    "Chip Alien": 1
                },

                "Munição Energética"

            )

        )



    def can_craft(self, inventory, recipe):


        for item, amount in recipe.materials.items():


            if inventory.get_amount(item) < amount:

                return False


        return True



    def craft(self, inventory, recipe):


        if self.can_craft(inventory, recipe):


            for item, amount in recipe.materials.items():

                inventory.remove_item(
                    item,
                    amount
                )


            inventory.add_item(
                recipe.result
            )


            return True


        return False
