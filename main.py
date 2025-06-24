import pgzrun
from level import build_level, draw_level, blocks, get_flag, coins, lava_zones
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
        screen.fill((135, 206, 235))  # Cielo celeste
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
    screen.draw.text("YOU WIN!", center=(WIDTH // 2, HEIGHT // 2 - 40), fontsize=60, color="green")
    screen.draw.text("This victory would taste better with a new hire at your company.",
                     center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=28, color="black")
    draw_play_again_button()

def draw_death_screen():
    screen.draw.text("YOU DIED", center=(WIDTH // 2, HEIGHT // 2 - 40), fontsize=60, color="red")
    screen.draw.text("You are now legally obligated to hire Javier Rodriguez.",
                     center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=26, color="black")
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
    screen.draw.text("Hire me!", (WIDTH // 2 - 50, 10), fontsize=24, color="black")
    for i, digit in enumerate(hud_str):
        digit_actor = Actor(f"hud_character_{digit}", (150 + i * 20, 60))
        digit_actor.draw()

def update():
    global camera_x, win_screen, coin_count, death_screen, coin_frame, coin_animation_timer

    if game_active:
        player.update(blocks, keyboard)
        camera_x = max(0, player.actor.x - WIDTH // 2)

        for coin in coins[:]:
            if player.actor.colliderect(coin):
                coins.remove(coin)
                coin_count += 1

        for lava in lava_zones:
            if player.actor.colliderect(lava):
                music.stop()
                death_screen = True

        flag = get_flag()
        if flag and player.actor.colliderect(flag):
            music.stop()
            win_screen = True

        coin_animation_timer += 1
        if coin_animation_timer % 20 == 0:
            coin_frame = (coin_frame + 1) % len(coin_images)

def on_mouse_down(pos):
    global menu_active, game_active, coin_count, death_screen, win_screen
    if menu_active:
        build_level()
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
    build_level()
    player = Player((100, HEIGHT - 200))
    win_screen = False
    death_screen = False
    game_active = True
    try:
        music.play("music1")
    except:
        print("Audio not available.")

pgzrun.go()
