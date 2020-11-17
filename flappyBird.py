import pygame
import sys
import random

# Variables
gravity = 0.23
bird_velocity = 0
game_state = False
score = 0
high_score = 0


class Bird:

    def __init__(self, bird_down, bird_mid, bird_up):
        self.bird_down = pygame.transform.scale2x(pygame.image.load(bird_down)).convert_alpha()
        self.bird_mid = pygame.transform.scale2x(pygame.image.load(bird_mid)).convert_alpha()
        self.bird_up = pygame.transform.scale2x(pygame.image.load(bird_up)).convert_alpha()
        self.bird_states = [self.bird_down, self.bird_mid, self.bird_up]
        self.index = 0
        self.bird_surface = self.bird_states[self.index]
        self.bird_col_rect = self.bird_surface.get_rect(center=(100, 512))

    def set_index(self, value):
        self.index = value

    def get_index(self):
        return self.index

    def get_bird_surface(self):
        return self.bird_surface

    def get_col_rect(self):
        return self.bird_col_rect

    def animate_bird(self):
        anim_bird = pygame.transform.rotozoom(self.bird_surface, -bird_velocity * 2.3, 1)
        return anim_bird

    def bird_animation(self):
        bird = self.bird_surface
        bird_rect = self.bird_col_rect
        return bird, bird_rect

    def set_center(self, x, y):
        self.bird_col_rect.center = (x, y)

    def add_centerY(self, value):
        self.bird_col_rect.centery += value


def spawn_pipe():
    pipe_pos = random.choice(pipe_y)
    pipe_top = pipe_surface.get_rect(midbottom=(700, pipe_pos - 280))
    pipe_bottom = pipe_surface.get_rect(midtop=(700, pipe_pos))
    return pipe_top, pipe_bottom


def pipe_move(pipe_list):
    for pipe in pipe_list:
        pipe.centerx -= 4
    return pipe_list


def draw_pipes(pipe_list):
    for pipe in pipe_list:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            pipe_flip = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(pipe_flip, pipe)


def floor_cycle(x):
    screen.blit(floor_surface, (x, 850))
    screen.blit(floor_surface, (x + 576, 850))


def display_score(game_st):
    if game_st:
        score_surface = font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_st is False:
        score_surface = font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 800))
        screen.blit(high_score_surface, high_score_rect)


def update_hs(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def collision_checker(pipe_list):
    if _bird.get_col_rect().top <= -100 or _bird.get_col_rect().bottom >= 850:
        die_sound.play()
        return False
    for pipe in pipe_list:
        if _bird.get_col_rect().colliderect(pipe):
            die_sound.play()
            return False
    return True

#
# def animate_bird(bird):
#     anim_bird = pygame.transform.rotozoom(bird, -bird_velocity*2.3, 1)
#     return anim_bird
# def bird_animation():
#     new_bird = bird_states[index]
#     new_bird_rect = new_bird.get_rect(center=(100, bird_col_rect.centery))
#     return new_bird, new_bird_rect


pygame.init()

font = pygame.font.Font('04B_19.ttf', 40)


screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()


# bird_down = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png')).convert_alpha()
# bird_mid = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png')).convert_alpha()
# bird_up = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png')).convert_alpha()
# bird_states = [bird_down, bird_mid, bird_up]
# bird_img = bird_states[index]
# bird_col_rect = bird_img.get_rect(center=(100, 512))

_bird = Bird('assets/bluebird-downflap.png', 'assets/bluebird-midflap.png', 'assets/bluebird-upflap.png')


background_surface = pygame.image.load('assets/background-day.png').convert()
background_surface = pygame.transform.scale2x(background_surface)


game_start_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_start_rect = game_start_surface.get_rect(center=(288, 512))
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x = 0

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipes = []
pipe_y = [450, 500, 600, 700, 750]




SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

BIRDANIM = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDANIM, 300)

# Sounds

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
die_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
point_sound = pygame.mixer.Sound('sound/sfx_point.wav')

point_sound_cd = 1000

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and game_state is True:
            if event.key == pygame.K_SPACE:
                bird_velocity = 0
                bird_velocity -= 9.5
                flap_sound.play()
        if event.type == pygame.KEYDOWN and game_state is False:
            game_state = True
            pipes.clear()
            _bird.set_center(100, 512)
            bird_velocity = 0
            score = 0
            point_sound_cd = 1000

        if event.type == SPAWNPIPE:
            pipes.extend(spawn_pipe())
        if event.type == BIRDANIM:
            if _bird.get_index() < 2:
                _bird.set_index(_bird.get_index() + 1)
            else:
                _bird.set_index(0)
            # bird_img, bird_col_rect = bird_animation()
    # Displaying Background Sky
    screen.blit(background_surface, (0, 0))
    if game_state:

        # Displaying Bird
        bird_velocity += gravity
        animated_bird = _bird.animate_bird()
        _bird.add_centerY(bird_velocity)
        screen.blit(_bird.animate_bird(), _bird.get_col_rect())
        game_state = collision_checker(pipes)

        # Displaying Pipes
        pipes = pipe_move(pipes)
        draw_pipes(pipes)
        score += 0.005
        display_score(game_state)
        point_sound_cd -= 5
        if point_sound_cd == 0 and score != 0:
            point_sound.play()
            point_sound_cd = 1000

    else:
        screen.blit(game_start_surface, game_start_rect)
        high_score = update_hs(score, high_score)
        display_score(game_state)
    # Displaying the Floor
    floor_x -= 1
    if floor_x <= -576:
        floor_x = 0
    floor_cycle(floor_x)

    pygame.display.update()
    clock.tick(120)

