import pygame


class NPC:


    def __init__(self, x, y, name):

        self.x = x
        self.y = y

        self.name = name

        self.width = 32
        self.height = 48

        self.dialogs = []

        self.rect = pygame.Rect(
            x,
            y,
            self.width,
            self.height
        )

        self.color = (200,200,50)



    def add_dialog(self, text):

        self.dialogs.append(
            text
        )



    def talk(self):

        if len(self.dialogs) > 0:

            return self.dialogs[0]

        return "..."



    def draw(self, screen, camera):

        pygame.draw.rect(

            screen,

            self.color,

            camera.apply(self)

        )



# ==========================
# NPCs DO ALIEN FALL 48
# ==========================


class Survivor(NPC):


    def __init__(self,x,y):

        super().__init__(
            x,
            y,
            "Sobrevivente"
        )

        self.add_dialog(
            "A nave caiu perto da antiga cidade..."
        )

        self.add_dialog(
            "Precisamos encontrar abrigo."
        )



class Scientist(NPC):


    def __init__(self,x,y):

        super().__init__(
            x,
            y,
            "Cientista"
        )

        self.add_dialog(
            "Os alienígenas usam uma tecnologia desconhecida."
        )

        self.add_dialog(
            "Preciso de cristais alienígenas para estudar."
        )



class Commander(NPC):


    def __init__(self,x,y):

        super().__init__(
            x,
            y,
            "Comandante"
        )

        self.add_dialog(
            "Precisamos formar uma resistência."
        )

        self.add_dialog(
            "A Terra depende de nós."
        )
