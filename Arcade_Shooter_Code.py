import pygame
from sys import exit
import random
from random import randint
from pygame import MOUSEBUTTONDOWN, K_SPACE

# Initialise pygame
pygame.init()

# Set icon and title
pygame.display.set_caption("Placeholder")
icon_image = pygame.image.load("Placeholder")

pixel = pygame.font.Font("Placeholder")

# Set window size
screen = pygame.display.set_mode((800, 400))

# Set clock to cap framerate
clock = pygame.time.Clock()

gunfire_sfx = pygame.mixer.Sound("Placeholder")
empty_sfx = pygame.mixer.Sound("Placeholder")


start_time = pygame.time.get_ticks()
#classes
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()  


        # Load images and audio
        self.player_stationary = pygame.image.load("Placeholder").convert_alpha()
        self.player_walk_1 = pygame.image.load("Placeholder").convert_alpha()
        player_walk_2 = pygame.image.load("Placeholder").convert_alpha()
        player_walk_3 = pygame.image.load("Placeholder").convert_alpha()
        player_walk_4 = pygame.image.load("Placeholder").convert_alpha()

        self.gunfire_sfx = pygame.mixer.Sound("Placeholder")
        self.gunsight_surface = pygame.image.load("Placeholder")
        self.gunfire_surface = pygame.image.load("Placeholder")

        self.shield_full = pygame.image.load("Placeholder")
        self.shield_empty = pygame.image.load("Placeholder")
        shield_1 = pygame.image.load("Placeholder")
        shield_2 = pygame.image.load("Placeholder")
        shield_3 = pygame.image.load("Placeholder")
        shield_4 = pygame.image.load("Placeholder")
        shield_5 = pygame.image.load("Placeholder")
        shield_6 = pygame.image.load("Placeholder")
        shield_7 = pygame.image.load("Placeholder")
        shield_8 = pygame.image.load("Placeholder")
        shield_9 = pygame.image.load("Placeholder")
        shield_10 = pygame.image.load("Placeholder")
        shield_11 = pygame.image.load("Placeholder")
        shield_12 = pygame.image.load("Placeholder")
        self.shield_frames = [shield_1, shield_2, shield_3, shield_4, shield_5, shield_6, shield_7, shield_8, shield_9,
                              shield_10, shield_11, shield_12, self.shield_full]

        self.health_full = pygame.image.load("Placeholder")
        self.health_half = pygame.image.load("Placeholder")
        self.health_low = pygame.image.load("Placeholder")

        self.shield_full_rect = self.shield_full.get_rect(topright=(780, 10))
        self.shield_empty_rect = self.shield_empty.get_rect(topright=(780, 10))

        self.empty = pygame.mixer.Sound("Placeholder")
        self.full = pygame.mixer.Sound("Placeholder")

        self.channel_1 = pygame.mixer.Channel(1)
        self.channel_2 = pygame.mixer.Channel(2)

        self.player_walk = [self.player_walk_1, player_walk_2, player_walk_3, player_walk_4]
        self.player_walk_backward = [player_walk_4, player_walk_3, player_walk_2, self.player_walk_1]
        self.player_index = 0

        # Initial settings
        self.image = self.player_stationary  # Start with the stationary image
        self.rect = self.image.get_rect(bottomleft=(100, 354))
        self.gravity = 0
        self.shield_active = True

        self.cooldown_timer = 0

    def player_input(self): # Player input and movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.left += 5
        if keys[pygame.K_a]:
            self.rect.right -= 5
        if keys[pygame.K_SPACE] and self.rect.bottom >= 354:
            self.gravity = -20

    def player_animation(self): # Player Animation
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        
        if mouse_pos[0] > self.rect.centerx:  # Check if mouse is right of the player
            if self.rect.bottom < 354:
                self.image = self.player_walk_1  # Default to stationary when airborne
            else:
                if keys[pygame.K_d]: # Amimation when moving right
                    self.player_index += 0.15
                    if self.player_index >= len(self.player_walk):
                        self.player_index = 0
                    self.image = self.player_walk[int(self.player_index)]
                elif keys[pygame.K_a]: # Amimation when moving left
                    self.player_index += 0.15
                    if self.player_index >= len(self.player_walk_backward):
                        self.player_index = 0
                    self.image = self.player_walk_backward[int(self.player_index)]
                else:
                    self.image = self.player_stationary # Stationary animation
        else:
            if self.rect.bottom < 354:
                self.image = pygame.transform.flip(self.player_walk_1, 1, 0)
            else:
                if keys[pygame.K_d]: # Amimation when moving right (flipped)
                    self.player_index += 0.15
                    if self.player_index >= len(self.player_walk_backward):
                        self.player_index = 0
                    self.image = pygame.transform.flip(self.player_walk_backward[int(self.player_index)], 1, 0)
                elif keys[pygame.K_a]: # Amimation when moving left (flipped)
                    self.player_index += 0.15
                    if self.player_index >= len(self.player_walk):
                        self.player_index = 0
                    self.image = pygame.transform.flip(self.player_walk[int(self.player_index)], 1, 0)
                else:
                    self.image = pygame.transform.flip(self.player_stationary, 1, 0) # Stationary (flipped)

    def apply_gravity(self): # Implement gravity
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 354:
            self.rect.bottom = 354

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation()
        self.muzzle_flash()
        self.player_bounds()
        self.gunsight_init()
        self.check_collision()
        self.shield()
        self.health()

    def check_collision(self): # Checking collisions to trigger shield recharge timer
        if pygame.sprite.spritecollide(self, grunt_group, False) or pygame.sprite.spritecollide(self, elite_group, False) or pygame.sprite.spritecollide(self, zealot_group, False):
            self.shield_active = False
            if self.cooldown_timer == 0:
                self.cooldown_timer = 50

    def player_bounds(self): # Limit player bounds
        if self.rect.x < -30:
            self.rect.x = -30
        if self.rect.x > 750:
            self.rect.x = 750

    def muzzle_flash(self): # Add muzzle flash animations
        if event.type == MOUSEBUTTONDOWN:
            self.flipped_gunfire_surface = pygame.transform.flip(self.gunfire_surface, 1, 0)
            if mouse_pos > self.rect.center:
                screen.blit(self.gunfire_surface, (self.rect.x + 83, self.rect.y + 16))
            else:
                screen.blit(self.flipped_gunfire_surface, (self.rect.x - 13, self.rect.y + 16))

    def gunsight_init(self): # Have gunsight follow mouse
        self.gunsight_rect = self.gunsight_surface.get_rect(topleft=(0, 0))
        self.gunsight_rect.center = mouse_pos
        screen.blit(self.gunsight_surface, self.gunsight_rect)

    def shield(self):
        # Check if the shield is active
        if self.shield_active:
            # Display the full shield
            screen.blit(self.shield_full, self.shield_full_rect)
        else:
            if not hasattr(self, 'shield_time_1'):
                self.shield_time_1 = pygame.time.get_ticks()

            elapsed_time = pygame.time.get_ticks() - self.shield_time_1

            if elapsed_time < 4000: # Shield audio
                screen.blit(self.shield_empty, self.shield_empty_rect)
                if elapsed_time == 0:
                    self.channel_1.play(self.empty)
                if elapsed_time >= 2500 and elapsed_time <= 3000:
                    self.channel_1.play(self.full)



            elif 4000 <= elapsed_time < 6000:
                if not hasattr(self, 'shield_index'):
                    self.shield_index = 0


                self.shield_index += 0.3
                if self.shield_index >= len(self.shield_frames):
                    self.shield_index = len(self.shield_frames) - 1

                screen.blit(self.shield_frames[int(self.shield_index)], self.shield_full_rect)
            
            else: # After 8 seconds reactivate the shield and reset variables
                self.shield_active = True
                delattr(self, 'shield_time_1')
                if hasattr(self, 'shield_index'):
                    delattr(self, 'shield_index')

    def health(self): # Implement 3 bar health system
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1
        if pygame.sprite.spritecollide(self, grunt_group, False) or pygame.sprite.spritecollide(self, elite_group, False) or pygame.sprite.spritecollide(self, zealot_group, False):
            if self.cooldown_timer == 0:
                player_health.remove(1)
                print(len(player_health))
                self.cooldown_timer = 50
        if len(player_health) == 3:
            screen.blit(self.health_full, self.shield_full_rect)
        if len(player_health) == 2:
            screen.blit(self.health_half, self.shield_full_rect)
        if len(player_health) == 1:
            screen.blit(self.health_low, self.shield_full_rect)

class Grunt(pygame.sprite.Sprite): # Grunt class
    def __init__(self):
        super().__init__()
        # Load assets
        self.grunt_walk_1 = pygame.image.load("Placeholder").convert_alpha()
        grunt_walk_2 = pygame.image.load("Placeholder").convert_alpha()
        grunt_death_1 = pygame.image.load("Placeholder").convert_alpha()
        grunt_death_2 = pygame.image.load("Placeholder").convert_alpha()

        grunt_sfx_1 = pygame.mixer.Sound("Placeholder")
        grunt_sfx_2 = pygame.mixer.Sound("Placeholder")
        grunt_sfx_3 = pygame.mixer.Sound("Placeholder")
        grunt_sfx_4 = pygame.mixer.Sound("Placeholder")
        grunt_sfx_5 = pygame.mixer.Sound("Placeholder")
        grunt_sfx_6 = pygame.mixer.Sound("Placeholder")
        grunt_sfx_7 = pygame.mixer.Sound("Placeholder")
        grunt_sfx_8 = pygame.mixer.Sound("Placeholder")
        grunt_sfx_9 = pygame.mixer.Sound("Placeholder")

        self.frame_index = 0
        self.death_frame_index = 0
        self.walk_frames = [self.grunt_walk_1, grunt_walk_2]
        self.death_frames = [grunt_death_1, grunt_death_2]
        self.dead_grunt_list = []
        self.grunt_sfx_list = [grunt_sfx_1,grunt_sfx_2,grunt_sfx_3,grunt_sfx_4,grunt_sfx_5,grunt_sfx_6,grunt_sfx_7,grunt_sfx_8,grunt_sfx_9]
        self.gravity = 0
        self.speed = random.uniform(1.4, 1.9)
        self.die = False

        self.direction_set()

    def direction_set(self): # Pick random side for grunt to spawn
        self.image = self.grunt_walk_1
        self.direction = random.choice(['left', 'right'])
        if self.direction == 'left':
            self.rect = self.image.get_rect(bottomleft=(randint(1000, 1300), 355))
        else:
            self.rect = self.image.get_rect(bottomright=(randint(-300, -100), 355))

    def animation(self):
        if not self.die:  # If the grunt is alive
            self.frame_index += 0.12 # Simple walking animation
            if self.frame_index >= len(self.walk_frames):
                self.frame_index = 0
            if self.direction == 'right':
                self.image = pygame.transform.flip(self.walk_frames[int(self.frame_index)], 1, 0)
                self.rect.x += self.speed
            else:
                self.image = self.walk_frames[int(self.frame_index)]
                self.rect.x -= self.speed
        else:  # If the grunt is dead
            self.death_frame_index += 0.12 # Death animation
            if self.death_frame_index >= len(self.death_frames):
                self.death_frame_index = 0
            if self.direction == 'right':
                self.image = pygame.transform.flip(self.death_frames[int(self.death_frame_index)], 1, 0)
                self.rect.x += 1.5
                self.gravity += 0.5
            else:
                self.image = self.death_frames[int(self.death_frame_index)]
                self.rect.x -= 1.5
                self.gravity += 0.5
            self.rect.y += self.gravity



    def death(self): # Triggers enemy death once clicked
        self.mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(self.mouse_pos):  # Left click
            if not self.die:  # Only trigger once
                self.die = True
                noise = random.choice(self.grunt_sfx_list)
                noise.play()
                dead_grunt_list.append(self.rect)

    def execute(self): # Drop enemy off screen
        if self.rect.x >= 1600 or self.rect.x <= -500 or self.rect.y >= 600:
            self.kill()
        if game_active == False:
            self.kill()


    def update(self):
        self.animation()
        self.execute()
        self.death()

class Elite(pygame.sprite.Sprite):  # Elite class
    def __init__(self):
        super().__init__()

        # Load assets
        self.elite_stationary = pygame.image.load("Placeholder").convert_alpha()
        elite_walk_1 = pygame.image.load("Placeholder").convert_alpha()
        elite_walk_2 = pygame.image.load("Placeholder").convert_alpha()
        elite_walk_3 = pygame.image.load("Placeholder").convert_alpha()
        elite_walk_4 = pygame.image.load("Placeholder").convert_alpha()
        elite_death_1 = pygame.image.load("Placeholder").convert_alpha()
        elite_death_2 = pygame.image.load("Placeholder").convert_alpha()

        elite_scream_sfx = pygame.mixer.Sound("Placeholder")
        elite_sfx_1 = pygame.mixer.Sound("Placeholder")
        elite_sfx_2 = pygame.mixer.Sound("Placeholder")
        elite_sfx_3 = pygame.mixer.Sound("Placeholder")

        # Animation setup
        self.frame_index = 0
        self.death_frame_index = 0
        self.walk_frames = [elite_walk_1, elite_walk_2, elite_walk_3, elite_walk_4]
        self.death_frames = [elite_death_1, elite_walk_2, elite_death_2, elite_walk_2]
        self.elite_sfx_list = [elite_scream_sfx, elite_sfx_1, elite_sfx_2, elite_sfx_3]
        self.gravity = 0
        self.speed = random.uniform(2.8, 3.3)
        self.die = False

        self.direction_set()

    def direction_set(self):  # Pick random side for enemy to spawn
        self.image = self.elite_stationary
        self.direction = random.choice(['left', 'right'])
        if self.direction == 'left':
            self.rect = self.image.get_rect(bottomleft=(randint(1000, 1300), 375))
        else:
            self.rect = self.image.get_rect(bottomright=(randint(-300, -100), 375))

    def animation(self):  # Animation and movement 
        if not self.die:  # If the elite is alive
            self.frame_index += 0.12
            if self.frame_index >= len(self.walk_frames):
                self.frame_index = 0
            if self.direction == 'right':  # Move and animate to the right
                self.image = pygame.transform.flip(self.walk_frames[int(self.frame_index)], 1, 0)
                self.rect.x += self.speed
            else:  # Move and animate to the left
                self.image = self.walk_frames[int(self.frame_index)]
                self.rect.x -= self.speed
        else:  # If the enemy is dead
            self.death_frame_index += 0.15  # Death animation
            if self.death_frame_index >= len(self.death_frames):
                self.death_frame_index = 0
            if self.direction == 'right':  # Death movement (right)
                self.image = pygame.transform.flip(self.death_frames[int(self.death_frame_index)], 1, 0)
                self.rect.x += 2.5
                self.gravity += 0.5
            else:  # Death movement (left)
                self.image = self.death_frames[int(self.death_frame_index)]
                self.rect.x -= 2.5
                self.gravity += 0.5
            self.rect.y += self.gravity

    def death(self):  # Triggers enemy death when clicked
        self.mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(self.mouse_pos):  # Left click
            if not self.die:  # Only trigger once
                self.die = True
                noise = random.choice(self.elite_sfx_list)
                noise.play()
                dead_elite_list.append(self.rect)

    def execute(self):  # Remove elite off screen or after game ends
        if self.rect.x >= 1600 or self.rect.x <= -500 or self.rect.y >= 600:
            self.kill()
        if game_active == False:
            self.kill()

    def update(self):
        self.animation()
        self.execute()
        self.death()

class Zealot(pygame.sprite.Sprite):  # Zealot class
    def __init__(self):
        super().__init__()

        # Load assets
        self.zealot_walk_1 = pygame.image.load("Placeholder").convert_alpha()
        zealot_walk_2 = pygame.image.load("Placeholder").convert_alpha()
        zealot_walk_3 = pygame.image.load("Placeholder").convert_alpha()
        zealot_walk_4 = pygame.image.load("Placeholder").convert_alpha()
        zealot_death_1 = pygame.image.load("Placeholder").convert_alpha()
        zealot_death_2 = pygame.image.load("Placeholder").convert_alpha()
        zealot_death_3 = pygame.image.load("Placeholder").convert_alpha()

        elite_scream_sfx = pygame.mixer.Sound("Placeholder")
        elite_sfx_1 = pygame.mixer.Sound("Placeholder")
        elite_sfx_2 = pygame.mixer.Sound("Placeholder")
        elite_sfx_3 = pygame.mixer.Sound("Placeholder")

        # Animation setup
        self.frame_index = 0
        self.death_frame_index = 0
        self.walk_frames = [self.zealot_walk_1, zealot_walk_2, zealot_walk_3, zealot_walk_4]
        self.death_frames = [zealot_death_1, zealot_death_3, zealot_death_2, zealot_death_3]
        self.elite_sfx_list = [elite_scream_sfx, elite_sfx_1, elite_sfx_2, elite_sfx_3]
        self.gravity = 0
        self.speed = random.uniform(3.3, 3.8)
        self.die = False

        self.direction_set()

    def direction_set(self):  # Pick random side for enemy to spawn
        self.image = self.zealot_walk_1
        self.direction = random.choice(['left', 'right'])
        if self.direction == 'left':
            self.rect = self.image.get_rect(bottomleft=(randint(1000, 1300), 355))
        else:
            self.rect = self.image.get_rect(bottomright=(randint(-300, -100), 355))

    def animation(self):  # Animation and movement
        if not self.die:  # If the enemy is alive
            self.frame_index += 0.12
            if self.frame_index >= len(self.walk_frames):
                self.frame_index = 0
            if self.direction == 'right':  # Move and animate to the right
                self.image = pygame.transform.flip(self.walk_frames[int(self.frame_index)], 1, 0)
                self.rect.x += self.speed
            else:  # Move and animate to the left
                self.image = self.walk_frames[int(self.frame_index)]
                self.rect.x -= self.speed
        else:  # If the zealot is dead
            self.death_frame_index += 0.15  # Death animation
            if self.death_frame_index >= len(self.death_frames):
                self.death_frame_index = 0
            if self.direction == 'right':  # Death movement (right)
                self.image = pygame.transform.flip(self.death_frames[int(self.death_frame_index)], 1, 0)
                self.rect.x += 2.5
                self.gravity += 0.5
            else:  # Death movement (left)
                self.image = self.death_frames[int(self.death_frame_index)]
                self.rect.x -= 2.5
                self.gravity += 0.5
            self.rect.y += self.gravity

    def death(self):  # Triggers enemy death when clicked
        self.mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(self.mouse_pos):  # Left click
            if not self.die:  # Only trigger once
                self.die = True
                noise = random.choice(self.elite_sfx_list)
                noise.play()
                dead_zealot_list.append(self.rect)

    def execute(self):  # Remove enemy off screen or after game ends
        if self.rect.x >= 1600 or self.rect.x <= -500 or self.rect.y >= 600:
            self.kill()
        if game_active == False:
            self.kill()

    def update(self):
        self.animation()
        self.execute()
        self.death()



player = pygame.sprite.GroupSingle()
player.add(Player())


grunt_group = pygame.sprite.Group()
elite_group = pygame.sprite.Group()
zealot_group = pygame.sprite.Group()

dead_grunt_list = []
dead_elite_list = []
dead_zealot_list = []
player_health = [1,1,1]


grunt_timer = pygame.USEREVENT + 1
elite_timer = pygame.USEREVENT + 2
zealot_timer = pygame.USEREVENT + 3
# Set flags
game_active = False
level_active = False
death_active = False
level_1 = False
level_2 = False

# Game music
channel_3 = pygame.mixer.Channel(3)
halo_theme_sfx = pygame.mixer.Sound("Placeholder")
zeta_halo_sfx = pygame.mixer.Sound("Placeholder")
through_the_trees_sfx = pygame.mixer.Sound("Placeholder")

# Set volumes
halo_theme_sfx.set_volume(1.0)
zeta_halo_sfx.set_volume(0.7)
through_the_trees_sfx.set_volume(1.0)

# Flags to track music state
is_playing_zeta_halo = False
is_playing_halo_theme = False
is_playing_through_the_trees = False


# Functions

def background_init(): # Backdrop setup (mostly scoring)

    # Score graphics    
    score_text = pygame.font.Font(None, 30)

    grunt_text = pygame.font.Font(None, 25)
    elite_text = pygame.font.Font(None, 25)
    zealot_text = pygame.font.Font(None, 25)
    score_surface = score_text.render(f'Score: {(int(len(dead_grunt_list))*10) + (int(len(dead_elite_list))*25) + (int(len(dead_zealot_list))*50)}', False, 'black')
    grunt_text_surface = grunt_text.render(f'Grunts: {int(len(dead_grunt_list))} x10', False, 'black')
    elite_text_surface = elite_text.render(f'Elites: {int(len(dead_elite_list))} x25', False, 'black')
    zealot_text_surface = zealot_text.render(f'Zealots: {int(len(dead_zealot_list))} x50', False, 'black')

     # More score graphics

    score_rect = score_surface.get_rect(topleft=(5, 5))
    grunt_rect = grunt_text_surface.get_rect(topleft=(5,30))
    elite_rect = elite_text_surface.get_rect(topleft=(5, 50))
    zealot_rect = zealot_text_surface.get_rect(topleft=(5, 70))



    pygame.draw.rect(screen, 'white', score_rect)
    pygame.draw.rect(screen, 'orange', grunt_rect)
    pygame.draw.rect(screen, (114,140,227), elite_rect)
    pygame.draw.rect(screen, (255, 194, 14), zealot_rect)

    screen.blit(score_surface, score_rect)
    screen.blit(grunt_text_surface, (5,30))
    screen.blit(elite_text_surface, (6, 50))
    screen.blit(zealot_text_surface, (6, 70))

def city(): # Map graphics (city)
    floor_surface = pygame.image.load("Placeholder").convert_alpha()
    backdrop_surface = pygame.image.load("Placeholder").convert_alpha()
    city_surface = pygame.image.load("Placeholder")

    screen.blit(backdrop_surface, (0, 0))
    screen.blit(city_surface, (0, -45))
    screen.blit(floor_surface, (0, 45))

def forest(): # Map graphics (forest)
    floor_surface = pygame.image.load("Placeholder").convert_alpha()
    backdrop_surface = pygame.image.load("Placeholder").convert_alpha()
    screen.blit(backdrop_surface, (0, 0))
    screen.blit(floor_surface, (0, 58))

def game(): # Menu code
    global game_active, level_active, death_active, level_1, level_2
    escape_text = pygame.font.Font(None, 25)
    escape_rect = escape_text.render('Press ESCAPE to Quit', False, 'white')

    if not game_active: # If gameplay is not running
        if not level_active and not death_active: # If not on death screen or level select
            # menu graphics
            menu_1 = pygame.image.load("Placeholder").convert_alpha() 
            
            screen.blit(menu_1, (0,0))
            screen.blit(escape_rect, (600,10))
            
            if pygame.key.get_pressed()[pygame.K_SPACE]: # Press space to move to level select
                level_active = True
        elif level_active and not death_active: # Level select
            # Load assets
            menu_2 = pygame.image.load("Placeholder").convert_alpha()
            gameplay_1 = pygame.image.load("Placeholder").convert_alpha()
            gameplay_2 = pygame.image.load("Placeholder").convert_alpha()
            # Graphics
            screen.blit(menu_2, (0,0))
            screen.blit(pygame.transform.scale_by(gameplay_1, (0.25,0.25)), (70,140))
            screen.blit(pygame.transform.scale_by(gameplay_2, (0.25, 0.25)), (70, 260))
            screen.blit(escape_rect, (600, 10))
            
            one_text = pygame.font.Font(None , 25)
            two_text = pygame.font.Font(None , 25)
            
            one_rect = one_text.render('1. Delta Halo Woodland', False, 'white')
            two_rect = two_text.render('2. New Alexandria', False, 'white')
            
            screen.blit(one_rect, (70,120))
            screen.blit(two_rect, (70, 240))
            # Clear previous scores
            dead_grunt_list.clear()
            dead_elite_list.clear()
            dead_zealot_list.clear()
            
            keys = pygame.key.get_pressed()

            if keys[pygame.K_1]: # Select level 1
                level_1 = True
                level_2 = False
                level_active = False
                game_active = True
                # Start spawn timers
                pygame.time.set_timer(grunt_timer, 1200) 
                pygame.time.set_timer(elite_timer, 3000)
                pygame.time.set_timer(zealot_timer, 6000)

            elif keys[pygame.K_2]: # Select level 2
                level_2 = True
                level_1 = False
                level_active = False
                game_active = True
                # Start spawn timers
                pygame.time.set_timer(grunt_timer, 1200)
                pygame.time.set_timer(elite_timer, 3000)
                pygame.time.set_timer(zealot_timer, 6000)

        elif death_active and not level_active: # Death screen
            # Graphics
            menu_3 = pygame.image.load("Placeholder").convert_alpha()
            screen.blit(menu_3, (0,0))
            score_text = pygame.font.Font(None, 70)
            grunt_text = pygame.font.Font(None, 40)
            elite_text = pygame.font.Font(None, 40)
            zealot_text = pygame.font.Font(None, 40)
            # Show scores
            score_surface = score_text.render(f'Score: {(int(len(dead_grunt_list)) * 10) + (int(len(dead_elite_list)) * 25) + (int(len(dead_zealot_list)) * 50)}',False, 'white')
            grunt_text_surface = grunt_text.render(f'Grunts: {int(len(dead_grunt_list))} x10', False, 'white')
            elite_text_surface = elite_text.render(f'Elites: {int(len(dead_elite_list))} x25', False, 'white')
            zealot_text_surface = zealot_text.render(f'Zealots: {int(len(dead_zealot_list))} x50', False, 'white')

            screen.blit(score_surface, (300,50))
            screen.blit(grunt_text_surface, (305, 100))
            screen.blit(elite_text_surface, (305, 130))
            screen.blit(zealot_text_surface, (305, 160))

            if pygame.key.get_pressed()[pygame.K_SPACE]: # Press space to level select
                level_active = True
                death_active = False



    if len(player_health) == 0: # Reset parameters
        game_active = False
        level_1 = False
        level_2 = False
        level_active = False
        death_active = True
        player_health.append(1)
        player_health.append(1)
        player_health.append(1)
        grunt_group.empty()
        elite_group.empty()
        zealot_group.empty()



def music(): # Music function
    global is_playing_zeta_halo, is_playing_halo_theme, is_playing_through_the_trees

    if not game_active: # If in menu
        if not is_playing_zeta_halo:
            channel_3.stop()  # Stop any currently playing sound
            channel_3.play(zeta_halo_sfx, loops=-1)
            is_playing_zeta_halo = True # Play menu music
            is_playing_halo_theme = False
            is_playing_through_the_trees = False
    else:
        if not level_1 and not is_playing_halo_theme:
            channel_3.stop() # Stop any currently playing sound
            channel_3.play(halo_theme_sfx, loops=-1)
            is_playing_zeta_halo = False
            is_playing_halo_theme = True # Play level 1 music
            is_playing_through_the_trees = False
        elif level_1 and not is_playing_through_the_trees:
            channel_3.stop() # Stop any currently playing sound
            channel_3.play(through_the_trees_sfx, loops=-1)
            is_playing_zeta_halo = False
            is_playing_halo_theme = False
            is_playing_through_the_trees = True # Play level 2 music


# Event loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]: # If escape is pressed
            pygame.quit() # Quit
            exit()
        if game_active == True: # Adding enemies to game
            if event.type == grunt_timer:
                grunt_group.add(Grunt())
            if event.type == elite_timer:
                elite_group.add(Elite())
            if event.type == zealot_timer:
                zealot_group.add(Zealot())
            if event.type == MOUSEBUTTONDOWN:
                gunfire_sfx.play()

    game()
    music()
    pygame.display.update()
    clock.tick(60)

    mouse_pos = pygame.mouse.get_pos()
    if game_active == True: # Level falg selection
        if level_1 == True:
            forest()
        if level_2 == True:
            city()

        background_init()



        grunt_group.draw(screen)
        grunt_group.update()

        elite_group.draw(screen)
        elite_group.update()

        zealot_group.draw(screen)
        zealot_group.update()

        player.draw(screen)
        player.update()


