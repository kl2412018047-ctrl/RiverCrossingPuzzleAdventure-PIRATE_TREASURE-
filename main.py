import pygame
import sys

pygame.init()
pygame.font.init()
pygame.mixer.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("River Crossing Puzzle Adventure")

# Background
try:
    background = pygame.image.load("assets/background.png")
    background2 = pygame.image.load("assets/background2.png")
except Exception:
    try:
        background = pygame.image.load("background.png")
        background2 = background  
    except Exception as e:
        print("Background Error: Use blue instead.", e)
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill((30, 144, 255)) 
        background2 = background

background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
background2 = pygame.transform.scale(background2, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Text color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 30, 30)
GREEN = (30, 200, 30)

# Font
FONT_LARGE = pygame.font.SysFont("Georgia", 40, bold=True)
FONT_MED = pygame.font.SysFont("Arial", 22, bold=True)
FONT_SMALL = pygame.font.SysFont("Arial", 16)

# MUSIC (Wrapped in try/except in case assets are missing)
try:
    pygame.mixer.music.load("music/background_sound.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except Exception:
    print("Music files missing, continuing without background music.")

# SOUND EFFECTS 
try:
    click_sound = pygame.mixer.Sound("music/click_sound.mp3")
    sailing_sound = pygame.mixer.Sound("music/sailing.mp3")
    victory_sound = pygame.mixer.Sound("music/victory_sound.mp3")
    gameover_sound = pygame.mixer.Sound("music/game_over.mp3")
    water_sound = pygame.mixer.Sound("music/water_splash.mp3")

    click_sound.set_volume(0.7)
    sailing_sound.set_volume(0.7)
    victory_sound.set_volume(0.8)
    gameover_sound.set_volume(0.8)
except Exception:
    print("Sound effects missing, running in silent mode.")
    # Fallback dummy objects so code doesn't crash on .play()
    class DummySound:
        def play(self): pass
    click_sound = sailing_sound = victory_sound = gameover_sound = water_sound = DummySound()


class Entity:
    def __init__(self, name, image_path, fallback_color, initial_side="LEFT"):
        self.name = name
        self.side = initial_side  
        self.on_boat = False
        self.fallback_color = fallback_color
        self.rect = pygame.Rect(0, 0, 60, 60) 

        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (60, 60))
            self.has_image = True
        except Exception as e:
            self.has_image = False
            print(f"Image Error untuk {name}: {e}")

    def draw(self, screen, x, y):
        self.rect.topleft = (x, y) 
        if self.has_image:
            screen.blit(self.image, (x, y))
        else:
            pygame.draw.rect(screen, self.fallback_color, self.rect)
            text = FONT_SMALL.render(self.name, True, BLACK)
            screen.blit(text, (x + 5, y + 25))


pirate = Entity("Pirate", "assets/pirate.png", (255, 0, 0))
treasure = Entity("Treasure", "assets/treasure_chest.png", (255, 215, 0))
map_item = Entity("Map", "assets/map.png", (0, 255, 0))
cannon = Entity("Cannon", "assets/cannon.png", (100, 100, 100))
key = Entity("Key", "assets/key.png", (255, 255, 0))

entities = [map_item, treasure, cannon, pirate]

def reset_game():
    global boat_side, game_message, game_over, score, level, entities
    boat_side = "LEFT"
    game_over = False
    score = 0
    level = 1
    game_message = "Click entities to board. Press SPACE to cross!"
    entities = [map_item, treasure, cannon, pirate]
    for e in entities:
        e.side = "LEFT"
        e.on_boat = False

def load_level_2():
    global level, game_message, entities, boat_side
    level = 2
    boat_side = "LEFT"
    game_message = "LEVEL 2 STARTED!"
    entities = [map_item, treasure, cannon, pirate, key]
    for e in entities:
        e.side = "LEFT"
        e.on_boat = False

boat_side = "LEFT"
boat_rect = pygame.Rect(0, 0, 180, 110) 

try:
    boat_image = pygame.image.load("assets/boat.png")
    boat_image = pygame.transform.scale(boat_image, (180, 110))
    has_boat_image = True
except Exception as e:
    print("Boat Image Error: Using fallback brown block instead.", e)
    has_boat_image = False

LEFT_BANK_X = 40
RIGHT_BANK_X = 780

LEFT_POSITIONS = {
    "Pirate": (100, 320),
    "Treasure": (180, 320),
    "Map": (100, 390),
    "Cannon": (150, 350),
    "Key": (250, 350)
}

RIGHT_POSITIONS = {
    "Pirate": (650, 340),
    "Treasure": (730, 340),
    "Map": (650, 400),
    "Cannon": (730, 400),
    "Key": (800, 350)
}

BOAT_X_LEFT = 220
BOAT_X_RIGHT = 430
BOAT_Y = 380

game_message = "Click entities to board. Press SPACE to cross!"
game_over = False
level = 1
score = 0

restart_button = pygame.Rect(700, 15, 160, 40)
start_button = pygame.Rect(350, 220, 200, 60)
instruction_button = pygame.Rect(350, 310, 200, 60)
exit_button = pygame.Rect(350, 400, 200, 60)

print("Game Started")

running = True
clock = pygame.time.Clock()
game_state = "MENU"  # Set default state to MENU

while running:
    clock.tick(FPS)
    
    if level == 1:
        current_boat_x = BOAT_X_LEFT if boat_side == "LEFT" else BOAT_X_RIGHT
        current_boat_y = BOAT_Y
    else:  # LEVEL 2
        current_boat_x = 320 if boat_side == "LEFT" else 500
        current_boat_y = 420

    boat_rect.topleft = (current_boat_x, current_boat_y)
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = "MENU"
                
            elif event.key == pygame.K_SPACE and game_state == "GAME" and not game_over:
                if pirate.on_boat:
                    sailing_sound.play()
                    water_sound.play()

                    boat_side = "RIGHT" if boat_side == "LEFT" else "LEFT"
                    score += 20
                    game_message = "Sailing across the river..."

                    for e in entities:
                        if e.on_boat:
                            e.side = boat_side
                    
                    left_side = [e.name for e in entities if e.side == "LEFT" and not e.on_boat]
                    right_side = [e.name for e in entities if e.side == "RIGHT" and not e.on_boat]

                    for side_items in [left_side, right_side]:
                        if "Pirate" not in side_items:

                            #1. cannon + map (lose)
                            if "Cannon" in side_items and "Map" in side_items:
                                gameover_sound.play()
                                game_message = "GAME OVER! Cannon destroyed the Map!"
                                game_over = True
                                break

                            #2. cannon + treasure (lose)
                            elif level == 2 and "Treasure" in side_items and "Map" in side_items:
                                gameover_sound.play()
                                game_message = "GAME OVER! Rats from Treasure ate the Map!"
                                game_over = True
                                break

                else:
                    game_message = "The boat needs the Pirate to sail!"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if game_state == "MENU":
                if start_button.collidepoint(mouse_pos):
                    reset_game()
                    game_state = "GAME"
                elif instruction_button.collidepoint(mouse_pos):
                    game_state = "INSTRUCTION"
                elif exit_button.collidepoint(mouse_pos):
                    running = False

            elif game_state == "GAME":
                if restart_button.collidepoint(mouse_pos):
                    reset_game()
                    continue

                if not game_over:
                    for e in entities:
                        if e.rect.collidepoint(mouse_pos):
                            if e.on_boat:
                                e.on_boat = False
                                e.side = boat_side
                                click_sound.play()
                                game_message = f"{e.name} stepped off the boat."
                            else:
                                if e.side != boat_side:
                                    game_message = f"Too far! Boat is on the {boat_side} side."
                                    continue
                                
                                passenger_count = sum(1 for item in entities if item.on_boat)
                                if passenger_count >= 2:
                                    game_message = "The boat is full!"
                                    continue

                                e.on_boat = True
                                click_sound.play()
                                score += 10
                                game_message = f"{e.name} boarded the boat."
                            break

    # Win Checking Logic (Only while playing)
    if game_state == "GAME" and not game_over:
        if all(e.side == "RIGHT" and not e.on_boat for e in entities):
            if level == 1:
                victory_sound.play()
                load_level_2()
            elif level == 2:
                victory_sound.play()
                game_message = "CONGRATULATIONS! YOU WIN!"
                game_over = True


    if game_state == "GAME":
        if level == 1:
            screen.blit(background, (0, 0))
        else:
            screen.blit(background2, (0, 0))

        if has_boat_image:
            screen.blit(boat_image, (boat_rect.x, boat_rect.y))
        else:
            pygame.draw.rect(screen, (139, 69, 19), boat_rect)
        
        boat_slots = [
            (boat_rect.x + 40, boat_rect.y + 10),  
            (boat_rect.x + 90, boat_rect.y + 10)     
        ]
        slot_index = 0

        for e in entities:
            if e.on_boat:
                x, y = boat_slots[slot_index]
                slot_index += 1
            elif e.side == "LEFT":
                x, y = LEFT_POSITIONS[e.name]
            else:
                x, y = RIGHT_POSITIONS[e.name]

            e.draw(screen, x, y)

        msg_color = RED if "GAME OVER" in game_message else (GREEN if "CONGRATULATIONS" in game_message else BLACK)
        if level == 2 and not game_over:
            ui_text = FONT_MED.render(game_message, True, WHITE)
        else:
            ui_text = FONT_MED.render(game_message, True, msg_color)
        
        screen.blit(ui_text, (20, 20))
        
        level_text = FONT_MED.render(f"Level: {level}", True, WHITE)
        screen.blit(level_text, (20, 60))

        score_text = FONT_MED.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (20, 90))

        pygame.draw.rect(screen, (50, 150, 255), restart_button, border_radius=8)
        restart_text = FONT_MED.render("Restart", True, WHITE)
        text_rect = restart_text.get_rect(center=restart_button.center)
        screen.blit(restart_text, text_rect) 

    elif game_state == "MENU":
        screen.blit(background, (0, 0))
        title = FONT_LARGE.render("River Crossing Puzzle", True, WHITE)
        screen.blit(title, (220, 100))

        pygame.draw.rect(screen, (0, 180, 0), start_button)
        pygame.draw.rect(screen, (0, 100, 255), instruction_button)
        pygame.draw.rect(screen, (180, 0, 0), exit_button)

        screen.blit(FONT_MED.render("START", True, WHITE), (410, 235))
        screen.blit(FONT_MED.render("INSTRUCTIONS", True, WHITE), (370, 325))
        screen.blit(FONT_MED.render("EXIT", True, WHITE), (425, 415))

    elif game_state == "INSTRUCTION":
        screen.blit(background, (0, 0))
        title = FONT_LARGE.render("Instructions", True, WHITE)
        line1 = FONT_MED.render("1. Click items to board boat", True, WHITE)
        line2 = FONT_MED.render("2. Pirate must be on boat to navigate", True, WHITE)
        line3 = FONT_MED.render("3. Press SPACE to cross", True, WHITE)
        line4 = FONT_MED.render("Press ESC to return to Menu", True, WHITE)

        screen.blit(title, (300, 100))
        screen.blit(line1, (180, 200))
        screen.blit(line2, (180, 250))
        screen.blit(line3, (180, 300))
        screen.blit(line4, (180, 400))

    pygame.display.flip()  # Correctly inside the main while loop now!

pygame.quit()
sys.exit()