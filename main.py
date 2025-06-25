import pgzrun
from level import load_level, draw_level, blocks, get_flag, coins, lava_zones, get_level_number
from player import Player
import pygame

WIDTH = 800
HEIGHT = 600

menu_active = True
game_active = False
win_screen = False
death_screen = False

player = Player((100, HEIGHT - 200))
camera_x = 0
coin_count = 0

coin_images = ["coin_gold", "coin_gold_side"]
coin_frame = 0
coin_animation_timer = 0

def draw():
    screen.clear()
    if menu_active:
        draw_menu()
    elif win_screen:
        draw_win_screen()
    elif death_screen:
        draw_death_screen()
    elif game_active:
        if get_level_number() == 1:
            screen.fill((135, 206, 235))  # Cielo celeste
        else:
            screen.fill((252, 186, 3))  # Atardecer / anochecer
        draw_level(screen, camera_x, coin_frame)
        player.draw(camera_x)
        draw_hud()

def draw_menu():
    screen.draw.text("PLATFORMER GAME", center=(WIDTH // 2, 100), fontsize=50, color="white")
    start_button = Rect((300, 250), (200, 50))
    screen.draw.filled_rect(start_button, "dodgerblue")
    screen.draw.text("Start Game", center=start_button.center, color="white", fontsize=30)
    screen.draw.text("Game by Javier Rodriguez", center=(WIDTH // 2, 320), fontsize=30, color="white")
    screen.draw.text("Documentation: see my LinkedIn or attached file", center=(WIDTH // 2, 360), fontsize=24, color="white")
    screen.draw.text("LinkedIn: javier-rodriguez-lopez-4795a8180", center=(WIDTH // 2, 390), fontsize=20, color="white")

def draw_win_screen():
    screen.fill((200, 255, 200))
    screen.draw.text("YOU WIN!", center=(WIDTH // 2, HEIGHT // 2 - 40), fontsize=60, color="green")
    screen.draw.text("This victory would feel better with a new hire in your team.", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=28, color="black")
    screen.draw.text("Why not celebrate by hiring Javier Rodriguez?", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=28, color="black")
    draw_play_again_button()

def draw_death_screen():
    screen.fill((255, 200, 200))
    screen.draw.text("YOU DIED", center=(WIDTH // 2, HEIGHT // 2 - 40), fontsize=60, color="red")
    screen.draw.text("You're now forced to hire Javier Rodriguez.", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=28, color="black")
    draw_retry_button()

def draw_retry_button():
    retry_button = Rect((300, 400), (200, 50))
    screen.draw.filled_rect(retry_button, "darkred")
    screen.draw.text("Retry", center=retry_button.center, color="white", fontsize=30)

def draw_play_again_button():
    play_again_button = Rect((300, 400), (200, 50))
    screen.draw.filled_rect(play_again_button, "green")
    screen.draw.text("Play Again", center=play_again_button.center, color="white", fontsize=30)

def draw_hud():
    global coin_count
    hud_str = str(coin_count)
    screen.draw.text(f"LEVEL {get_level_number()}", (10, 10), fontsize=30, color="black")
    screen.draw.text("Hire me!", (WIDTH // 2 - 50, 10), fontsize=24, color="black")
    for i, digit in enumerate(hud_str):
        digit_actor = Actor(f"hud_character_{digit}", (150 + i * 20, 60))
        digit_actor.draw()

def update():
    global camera_x, win_screen, coin_count, death_screen, coin_frame, coin_animation_timer, player

    if game_active:
        player.update(blocks, keyboard)
        camera_x = max(0, player.actor.x - WIDTH // 2)

        for coin in coins[:]:
            if player.actor.colliderect(coin):
                coins.remove(coin)
                coin_count += 1

        for lava in lava_zones:
            if player.actor.colliderect(lava):
                try:
                    music.stop()
                except:
                    pass
                death_screen = True

        flag = get_flag()
        if flag and player.actor.colliderect(flag):
            try:
                music.stop()
            except:
                pass
            if get_level_number() == 1:
                load_level(2)
                player = Player((100, HEIGHT - 200))
            else:
                win_screen = True

        coin_animation_timer += 1
        if coin_animation_timer % 20 == 0:
            coin_frame = (coin_frame + 1) % len(coin_images)

def on_mouse_down(pos):
    global menu_active, game_active, coin_count, death_screen, win_screen, player
    if menu_active:
        load_level(1)
        menu_active = False
        game_active = True
        coin_count = 0
        death_screen = False
        win_screen = False
        try:
            music.play("music1")
        except:
            print("Audio not available.")
    elif death_screen or win_screen:
        reset_game()

def reset_game():
    global game_active, win_screen, death_screen, player
    load_level(1)
    player = Player((100, HEIGHT - 200))
    win_screen = False
    death_screen = False
    game_active = True
    try:
        music.play("music1")
    except:
        print("Audio not available.")

pgzrun.go()
