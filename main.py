import pygame
from asteroid import Asteroid
from constants import *
from player import Player
from asteroidfield import AsteroidField
from shot import Shot

def main():
    _ = pygame.init()
    pygame.font.init()
    print("Starting asteroids!")
    print("Screen width:", SCREEN_WIDTH)
    print("Screen height:", SCREEN_HEIGHT)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    black = pygame.Color(0, 0, 0)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots,updatable, drawable)

    clock = pygame.time.Clock()
    dt = 0
    time_window = 0
    score = 0

    font = pygame.font.Font(None, 36)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    field = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
     
        for sprite in updatable:
            sprite.update(dt)

        for asteroid in asteroids:
            # see if this asteroid was destroyed by a bullet
            for shot in shots:
                if asteroid.collision(shot):
                    # 10 points for a shot
                    score += 10
                    asteroid.kill()
                    shot.kill()
                    break

            if asteroid.collision(player):
                print("Game over!")
                return

        # check if the player has been alive for 10 seconds to get another point 
        if time_window > 10:
            score += 1
            time_window = 0

        # render
        screen.fill(black)

        for sprite in drawable:
            sprite.draw(screen)

        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        dt = clock.tick(60) / 1000
        time_window += dt

if __name__ == "__main__":
    main()
