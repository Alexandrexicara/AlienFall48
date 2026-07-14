class Item:


    def __init__(self, name, item_type, value):

        self.name = name

        self.type = item_type

        self.value = value



    def info(self):

        return {
            "nome": self.name,
            "tipo": self.type,
            "valor": self.value
        }



# =========================
# ITENS DO ALIEN FALL 48
# =========================


class MedKit(Item):

    def __init__(self):

        super().__init__(
            "Kit Médico",
            "cura",
            50
        )



class Ammo(Item):

    def __init__(self):

        super().__init__(
            "Munição",
            "municao",
            30
        )



class EnergyCell(Item):

    def __init__(self):

        super().__init__(
            "Célula de Energia",
            "energia",
            40
        )



class AlienCrystal(Item):

    def __init__(self):

        super().__init__(
            "Cristal Alienígena",
            "recurso raro",
            100
        )



class MetalPart(Item):

    def __init__(self):

        super().__init__(
            "Peça de Metal",
            "construção",
            20
        )



class AlienChip(Item):

    def __init__(self):

        super().__init__(
            "Chip Alien",
            "tecnologia",
            200
        )
