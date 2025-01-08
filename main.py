import pygame
import random

pygame.init()

width, height = 600, 400

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Sprint")

clock = pygame.time.Clock()
running = True

BLOCK_SIZE = 20

score_font = pygame.font.SysFont("times new roman", 35)
msg_font = pygame.font.SysFont("times new roman", 20)


class Snake:
    def __init__(self):
        self.x, self.y = width//2, height//2
        self.xdir, self.ydir = 1, 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = []
        self.dead = False

    def update(self):
        global food

        new_head = pygame.Rect(
            self.head.x + self.xdir * BLOCK_SIZE,
            self.head.y + self.ydir * BLOCK_SIZE,
            BLOCK_SIZE,
            BLOCK_SIZE,
        )

        if new_head.x < 0 or new_head.x >= width or new_head.y < 0 or new_head.y >= height:
            self.dead = True
        if new_head in self.body:
            self.dead = True

        self.body.insert(0, new_head)
        self.head = new_head

        if food.x == self.head.x and food.y == self.head.y:
            food = Food()
        else:
            self.body.pop()


class Food:
    def __init__(self):
        self.x = (random.randint(0, width-1)//BLOCK_SIZE)*BLOCK_SIZE
        self.y = (random.randint(0, height-1)//BLOCK_SIZE)*BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        pygame.draw.rect(screen, "red", self.rect)


def game_over():
    screen.fill("green")
    y_offset = height // 3

    score_text = score_font.render(f"Your Score: {len(snake.body)}", True, "blue")
    screen.blit(score_text, score_text.get_rect(center=(width // 2, y_offset)))
    y_offset += score_font.get_linesize()

    msg_text = msg_font.render("Press Q to Quit or C to Play Again", True, "red")
    screen.blit(msg_text, msg_text.get_rect(center=(width // 2, y_offset)))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_c:
                    return

snake = Snake()
food = Food()

while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            # print(event.key, "eeeeeee")
            if event.key == pygame.K_DOWN and snake.ydir != -1:
                snake.ydir = 1
                snake.xdir = 0
            elif event.key == pygame.K_UP and snake.ydir != 1:
                snake.ydir = -1
                snake.xdir = 0
            elif event.key == pygame.K_RIGHT and snake.xdir != -1:
                snake.ydir = 0
                snake.xdir = 1
            elif event.key == pygame.K_LEFT and snake.xdir != 1:
                snake.ydir = 0
                snake.xdir = -1

    snake.update()
    if snake.dead:
        game_over()
        snake = Snake()
        food = Food()
        continue

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("green")

    score_text = msg_font.render(f"Score: {len(snake.body)}", True, "black")
    screen.blit(score_text, score_text.get_rect(center=(40, 20)))

    pygame.draw.rect(screen, "purple", snake.head)

    for square in snake.body:
        pygame.draw.rect(screen, "purple", square)

    pygame.draw.rect(screen, "red", food.rect)

    if food.x == snake.head.x and food.y == snake.head.y:
        snake.body.append(pygame.Rect(snake.head.x, snake.head.y, BLOCK_SIZE, BLOCK_SIZE))
        food = Food()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(5)

# pygame.quit()
