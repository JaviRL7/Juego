import pgzrun
from pygame import Rect  # Permitido por las reglas
from level import load_level, draw_level, blocks, get_flag, coins, lava_zones, get_level_number
from player import Player

WIDTH = 800
HEIGHT = 600

menu_active = True
game_active = False
win_screen = False
death_screen = False
sound_enabled = True

player = Player((100, HEIGHT - 200))
camera_x = 0
coin_count = 0

coin_images = ["coin_gold", "coin_gold_side"]
coin_frame = 0
coin_animation_timer = 0

buttons = {
    "start": Rect((300, 230), (200, 50)),
    "sound": Rect((300, 300), (200, 50)),
    "exit": Rect((300, 370), (200, 50))
}

def draw():
    screen.clear()
    if menu_active:
        draw_menu()
    elif win_screen:
        draw_win_screen()
    elif death_screen:
        draw_death_screen()
    elif game_active:
        if get_level_number() == 2:
            screen.fill((100, 80, 130))  # Dusk-like tone
        else:
            screen.fill((135, 206, 235))  # Sky blue
        draw_level(screen, camera_x, coin_frame)
        player.draw(camera_x)
        draw_hud()

def draw_menu():
    screen.draw.text("PLATFORMER GAME", center=(WIDTH // 2, 100), fontsize=50, color="white")
    for key, rect in buttons.items():
        color = "dodgerblue" if key == "start" else "green" if key == "sound" else "darkred"
        label = "Sound: ON" if key == "sound" and sound_enabled else "Sound: OFF" if key == "sound" else key.capitalize()
        screen.draw.filled_rect(rect, color)
        screen.draw.text(label, center=rect.center, color="white", fontsize=30)

def draw_win_screen():
    screen.fill((200, 255, 200))
    screen.draw.text("YOU WIN!", center=(WIDTH // 2, HEIGHT // 2 - 40), fontsize=60, color="green")
    screen.draw.text("This victory would feel better with a new hire in your team.", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=28, color="black")
    screen.draw.text("Why not celebrate by hiring Javier Rodríguez?", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=28, color="black")
    draw_play_again_button()

def draw_death_screen():
    screen.fill((255, 200, 200))
    screen.draw.text("YOU DIED", center=(WIDTH // 2, HEIGHT // 2 - 40), fontsize=60, color="red")
    screen.draw.text("You're now forced to hire Javier Rodríguez.", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=28, color="black")
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
                death_screen = True

        flag = get_flag()
        if flag and player.actor.colliderect(flag):
            if get_level_number() == 1:
                load_level(2)
                player.actor.topleft = (100, HEIGHT - 200)
                camera_x = 0
            else:
                win_screen = True

        coin_animation_timer += 1
        if coin_animation_timer % 20 == 0:
            coin_frame = (coin_frame + 1) % len(coin_images)

def on_mouse_down(pos):
    global menu_active, game_active, coin_count, death_screen, win_screen, sound_enabled
    if menu_active:
        if buttons["start"].collidepoint(pos):
            load_level(1)
            menu_active = False
            game_active = True
            coin_count = 0
            death_screen = False
            win_screen = False
        elif buttons["exit"].collidepoint(pos):
            exit()
        elif buttons["sound"].collidepoint(pos):
            sound_enabled = not sound_enabled

    elif death_screen or win_screen:
        reset_game()

def reset_game():
    global game_active, win_screen, death_screen, player
    load_level(1)
    player = Player((100, HEIGHT - 200))
    win_screen = False
    death_screen = False
    game_active = True

pgzrun.go()
