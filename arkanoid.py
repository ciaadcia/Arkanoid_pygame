import pygame
pygame.init()

back = (72, 61, 139)
mw = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Breakout Game")

jam = pygame.time.Clock()

dx = 3
dy = 3

platform_x = 200
platform_y = 330

move_right = False
move_left = False

running = True
game_over = False
result_text = ""

class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color

    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)

class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self):
        self.fill()
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        super().__init__(x, y, width, height)
        self.image = pygame.image.load(filename)

    def draw(self):
        mw.blit(self.image, self.rect)

ball = Picture('grimreaper.png', 160, 200, 50, 50)
platform = Picture('platform.png', platform_x, platform_y, 100, 30)

start_x = 5
start_y = 5
banyak = 9
monsters = []

for j in range(3):
    y = start_y + (55 * j)
    x = start_x + (27.5 * j)
    for i in range(banyak):
        monsters.append(Picture('enemyghost.png', x, y, 50, 50))
        x += 55
    banyak -= 1

while running:
    mw.fill(back)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False

    if not game_over:
        if move_right:
            platform.rect.x += 3
        if move_left:
            platform.rect.x -= 3

        ball.rect.x += dx
        ball.rect.y += dy

        if ball.rect.y < 0 or ball.rect.x < 0 or ball.rect.x > 450:
            dx *= -1
            dy *= -1

        if ball.rect.colliderect(platform.rect):
            dy *= -1

        for m in monsters[:]:
            if m.rect.colliderect(ball.rect):
                monsters.remove(m)
                dy *= -1

        if ball.rect.y > 350:
            game_over = True
            result_text = "YOU LOSE"

        if len(monsters) == 0:
            game_over = True
            result_text = "YOU WIN"

    for m in monsters:
        m.draw()

    platform.draw()
    ball.draw()

    if game_over:
        text = Label(120, 200, 260, 80, back)
        color = (255, 0, 0) if result_text == "YOU LOSE" else (0, 200, 0)
        text.set_text(result_text, 60, color)
        text.draw()

    pygame.display.update()
    jam.tick(40)

pygame.quit()
