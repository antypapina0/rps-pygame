import pygame
import sys

class ColorSelectionWindow:
    def __init__(self):
        pygame.init()
        self.width, self.height = 400, 300
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Color Selection Window")
        self.clock = pygame.time.Clock()

        self.colors = {"Red": (255, 0, 0), "Green": (0, 255, 0), "Blue": (0, 0, 255)}
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
        self.BLACK = (0,0,0)
        self.choices = {
            "Papier": ((100, 50, 200, 50), (200, 75) ,self.RED), 
            "Kamien": ((100, 150, 200, 50), (200, 175) ,self.GREEN), 
            "Nozyce": ((100, 250, 200, 50), (200, 275) ,self.BLUE)}
        self.selected_color = None

        self.player_1_color = None
        self.player_2_color = None

        self.font = pygame.font.Font(None, 36)

        self.playerOneChoice = None
        self.playerTwoChoice = None

        self.playerOneScore = 0
        self.playerTwoScore = 0

        self.roundResult = 0

        self.menu = True
        self.player_one_turn = False
        self.player_two_turn = False
        self.summary = False

        self.rects = {}
        self.try_again = {}

        self.end_round = False

        self.playerOneWin = False
        self.playerTwoWin = False
        self.tie = False

    def create_checkboxes_player_1(self):
        self.checkbox_rects_player_1 = {}
        checkbox_y = 50

        for color, rgb_value in self.colors.items():
            checkbox_rect = pygame.Rect(50, checkbox_y, 20, 20)
            pygame.draw.rect(self.screen, rgb_value, checkbox_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), checkbox_rect, 2)
            checkbox_y += 30
            self.checkbox_rects_player_1[color] = checkbox_rect

    def create_checkboxes_player_2(self):
        self.checkbox_rects_player_2 = {}
        checkbox_y = 50

        for color, rgb_value in self.colors.items():
            checkbox_rect = pygame.Rect(350, checkbox_y, 20, 20)
            pygame.draw.rect(self.screen, rgb_value, checkbox_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), checkbox_rect, 2)
            checkbox_y += 30
            self.checkbox_rects_player_2[color] = checkbox_rect

    def create_start_button(self):
        button_rect = pygame.Rect((150, 100, 100, 40))
        pygame.draw.rect(self.screen, (0, 255, 0), button_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)

        font = pygame.font.Font(None, 36)
        text = font.render("Start!", True, (0, 0, 0))
        text_rect = text.get_rect(center=button_rect.center)

        self.screen.blit(text, text_rect)

        self.start_button_rect = button_rect

    def playerMove(self, player: int):
        self.rects = {}
        for key, value in self.choices.items():
                choice_rect = pygame.Rect(value[0])
                pygame.draw.rect(self.screen, value[2], choice_rect)
                text = self.font.render(key, True, (255,255,255))
                text_rect = text.get_rect(center=value[1])
                self.screen.blit(text, text_rect)
                self.rects[key] = pygame.Rect(value[0])
        print(f"gracz_1: {self.playerOneScore} | gracz_2: {self.playerTwoScore}")

    def compareChoices(self):
        if self.end_round == True:
            if self.playerOneChoice == "Papier" and self.playerTwoChoice == "Kamien":
                self.updateScore(1)
            elif self.playerOneChoice == "Kamien" and self.playerTwoChoice == "Nozyce":
                self.updateScore(1)
            elif self.playerOneChoice == "Nozyce" and self.playerTwoChoice == "Papier":
                self.updateScore(1)
            elif self.playerOneChoice == "Papier" and self.playerTwoChoice == "Nozyce":
                self.updateScore(2)
            elif self.playerOneChoice == "Kamien" and self.playerTwoChoice == "Papier":
                self.updateScore(2)
            elif self.playerOneChoice == "Nozyce" and self.playerTwoChoice == "Kamien":
                self.updateScore(2)
            elif self.playerOneChoice == self.playerTwoChoice:
                self.updateScore(0)

        self.end_round = False
            

    def updateScore(self, winner: int):
        if winner == 1:
            # zwiekszenie wyniku gracza 1 o 1
            self.playerOneScore += 1
            self.playerOneWin = True
        elif winner == 2:
            # zwiekszenie wyniku gracza 2 o 1
            self.playerTwoScore += 1
            self.playerTwoWin = True
        elif winner == 0:
            self.playerOneScore += 1
            self.playerTwoScore += 1
            self.tie = True

        self.end_round = False

    def startGame(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_mouse_click(event.pos)

            self.draw()
            if self.menu == True:
                self.create_checkboxes_player_1()
                self.create_checkboxes_player_2()
                self.draw_text_player_1((0,0))
                self.draw_text_player_2((380,0))
                self.create_start_button()

            if self.player_one_turn == True:
                self.draw()
                self.draw_text_player_1((0,0))
                self.playerMove(1)
            if self.player_two_turn == True:
                self.draw()
                self.draw_text_player_2((380,0))
                self.playerMove(2)
            if self.summary == True:
                self.draw()
                self.displayRoundResult()

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()


    def displayRoundResult(self):
        print(f"{self.playerOneChoice} | {self.playerTwoChoice}")
        if self.playerOneChoice and self.playerTwoChoice:
            self.compareChoices()

            if self.tie == True:
                self.draw_summary("Remis", self.BLACK)
            elif self.playerOneWin == True:
                self.draw_summary("Wygrał gracz 1", self.player_1_color)
            elif self.playerTwoWin == True:
                self.draw_summary("Wygrał gracz 2", self.player_2_color)

    def draw_summary(self, text, color):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center = (200, 100))
        self.screen.blit(text_surface, text_rect)

        again_rect = pygame.Rect(100,250,200,50)
        pygame.draw.rect(self.screen, self.GREEN, again_rect)
        text = self.font.render("Zagraj ponownie", True, (255,255,255))
        text_rect = text.get_rect(center=(200, 275))
        self.try_again[self.GREEN] = again_rect
        self.screen.blit(text, text_rect)

    def draw_text_player_1(self, position):
        if self.player_1_color:
            text_surface = self.font.render("Gracz 1", True, self.player_1_color)  # Utwórz powierzchnię z tekstem
            text_rect = text_surface.get_rect(topleft=position)  # Ustaw pozycję tekstu
            self.screen.blit(text_surface, text_rect)  # Narysuj tekst na ekranie

    def draw_text_player_2(self, position):
        if self.player_2_color:
            text_surface = self.font.render("Gracz 2", True, self.player_2_color)  # Utwórz powierzchnię z tekstem
            text_rect = text_surface.get_rect(topright=position)  # Ustaw pozycję tekstu
            self.screen.blit(text_surface, text_rect)  # Narysuj tekst na ekranie
    

    def handle_mouse_click(self, pos):
        if self.start_button_rect.collidepoint(pos):
            if self.player_1_color and self.player_2_color:
                self.manu = False
                self.player_one_turn = True 
        else:
            for color, rect in self.checkbox_rects_player_1.items():
                if rect.collidepoint(pos):
                    self.selected_color = color
                    self.player_1_color = color

            for color, rect in self.checkbox_rects_player_2.items():
                if rect.collidepoint(pos):
                    self.selected_color = color
                    self.player_2_color = color

        if self.player_one_turn == True:
            for choice, rect in self.rects.items():
                if rect.collidepoint(pos):
                    self.playerOneChoice = choice
                    self.player_two_turn = True
                    self.player_one_turn = False
        
        elif self.player_two_turn == True:
            for choice, rect in self.rects.items():
                if rect.collidepoint(pos):
                    self.playerTwoChoice = choice
                    self.summary = True
                    self.player_two_turn = False
                    self.end_round = True

        if self.playerOneWin or self.playerTwoWin or self.tie:
            for key, value in self.try_again.items():
                if value.collidepoint(pos):
                    self.tie = False
                    self.playerOneWin = False
                    self.playerTwoWin = False
                    self.player_one_turn = True
                    self.summary = False


    def draw(self):
        self.screen.fill((255, 255, 255))

if __name__ == "__main__":
    color_selection_window = ColorSelectionWindow()
    color_selection_window.startGame()