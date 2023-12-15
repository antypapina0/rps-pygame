import pygame
import sys

class PaperRockScissorsGame:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 800, 600
        self.FPS = 60

        self.WHITE = (255, 255, 255)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Papier, Kamień, Nożyce")

        self.rock_img = pygame.image.load("rock.png")
        self.paper_img = pygame.image.load("paper.png")
        self.scissors_img = pygame.image.load("scissors.png")

    def draw_choices(self, player1_choice, player2_choice):
        self.screen.blit(player1_choice, (200, 400))
        self.screen.blit(player2_choice, (500, 400))

    def play_round(self, player1_choice, player2_choice):
        self.draw_choices(player1_choice, player2_choice)

        if player1_choice is not None and player2_choice is not None:
            if player1_choice == player2_choice:
                result = "Remis!"
            elif (
                (player1_choice == self.rock_img and player2_choice == self.scissors_img)
                or (player1_choice == self.paper_img and player2_choice == self.rock_img)
                or (player1_choice == self.scissors_img and player2_choice == self.paper_img)
            ):
                result = "Gracz 1 wygrał!"
            else:
                result = "Gracz 2 wygrał!"

            font = pygame.font.Font(None, 36)
            text = font.render(result, True, self.WHITE)
            self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2, 50))
            pygame.display.flip()
            pygame.time.wait(2000)  # Czekaj 2 sekundy przed wyczyszczeniem wyniku
            self.screen.fill((0, 0, 0))  # Wyczyść ekran

    def run(self):
        clock = pygame.time.Clock()
        running = True

        player1_choice = None
        player2_choice = None

        while running:
            clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key in [pygame.K_r, pygame.K_p, pygame.K_s]:
                        if player1_choice is None:
                            if event.key == pygame.K_r:
                                player1_choice = self.rock_img
                            elif event.key == pygame.K_p:
                                player1_choice = self.paper_img
                            elif event.key == pygame.K_s:
                                player1_choice = self.scissors_img
                        elif player2_choice is None:
                            if event.key == pygame.K_r:
                                player2_choice = self.rock_img
                            elif event.key == pygame.K_p:
                                player2_choice = self.paper_img
                            elif event.key == pygame.K_s:
                                player2_choice = self.scissors_img

                            self.play_round(player1_choice, player2_choice)
                            player1_choice = None
                            player2_choice = None

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = PaperRockScissorsGame()
    game.run()
