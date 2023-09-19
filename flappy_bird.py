import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
BIRD_RADIUS = 20
BIRD_WIDTH = BIRD_RADIUS * 2  # Derived from the radius
BIRD_HEIGHT = BIRD_RADIUS * 2  # Derived from the radius
PIPE_WIDTH = 50
GAP_HEIGHT = 200
FLAP_POWER = -10
GRAVITY = 0.5
PIPE_SPACING = 250
PIPE_SPEED = 3
LIVES = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
font = pygame.font.Font(None, 36)

bird_image = pygame.image.load("birdpic.jpg")
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))  # Resize the image

class Bird:
    def __init__(self):
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity += FLAP_POWER

    def fall(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def move_down(self):
        self.y += 10

    def display(self):
        screen.blit(bird_image, (self.x - BIRD_RADIUS, self.y - BIRD_RADIUS))

    def check_collision(self, pipes):
        for pipe in pipes:
            if pipe.collides(self.x, self.y, BIRD_RADIUS):
                return True
        return self.y - BIRD_RADIUS <= 0 or self.y + BIRD_RADIUS >= HEIGHT

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.gap_start = random.randint(BIRD_RADIUS * 2, HEIGHT - GAP_HEIGHT - BIRD_RADIUS * 2)
        self.passed = False

    def move(self):
        self.x -= PIPE_SPEED

    def offscreen(self):
        return self.x + PIPE_WIDTH < 0

    def display(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.gap_start))
        pygame.draw.rect(screen, GREEN, (self.x, self.gap_start + GAP_HEIGHT, PIPE_WIDTH, HEIGHT))

    def collides(self, bird_x, bird_y, bird_radius):
        if bird_x + bird_radius > self.x and bird_x - bird_radius < self.x + PIPE_WIDTH:
            if bird_y - bird_radius < self.gap_start or bird_y + bird_radius > self.gap_start + GAP_HEIGHT:
                return True
        return False

def main():
    bird = Bird()
    pipes = []
    score = 0
    lives = LIVES
    clock = pygame.time.Clock()

    running = True
    while running and lives > 0:
        screen.fill(WHITE)
        bird.fall()
        bird.display()

        if len(pipes) == 0 or pipes[-1].x <= WIDTH - PIPE_SPACING:
            pipes.append(Pipe())

        for pipe in pipes:
            if pipe.offscreen():
                pipes.remove(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1
            pipe.move()
            pipe.display()

        pygame.draw.rect(screen, BROWN, (0, HEIGHT - 50, WIDTH, 50))
        score_display = font.render(f"Score: {score}", True, WHITE)
        lives_display = font.render(f"Lives: {lives}", True, RED)

        screen.blit(score_display, (10, 10))
        screen.blit(lives_display, (WIDTH - 150, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                lives = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bird.flap()
                if event.key == pygame.K_DOWN:
                    bird.move_down()

        if bird.check_collision(pipes):
            lives -= 1
            bird = Bird()  # Reset bird position
            pipes.clear()  # Clear pipes

        pygame.display.flip()
        clock.tick(60)

    print(f"Game Over! Score: {score}")

if __name__ == "__main__":
    main()
    pygame.quit()
