from pgzero.actor import Actor

TILE_SIZE = 64
blocks = []
coins = []
lava_zones = []
decorations = []
_flag = None
current_level = 1

flag_frames = ["flag_blue_a", "flag_blue_b"]

# Nivel 1
level_data = [
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "       1                                                ",
    "     LMMR       1         LMMR                          ",
    "                                                        ",
    "                     LMMR                               ",
    "            1                   K                       ",
    "            LMMR              LMMR     1   LMMMMMR      ",
    "      K                        K                        ",
    "XXXXXXXXXXXXXXXXXXXXXlllXXXXXXXXXXXXXXlllXXXXXXXXXXXXFXX",
    "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
    "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
    "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
    "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
    "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
]

# Nivel 2
level_data_2 = [
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "       1                                                ",
    "     DDD                     DDD                        ",
    "                                                        ",
    "                                      1                 ",
    "             1             DDD                          ",
    "     1      DDD     1              1    DDD             ",
    "           B                        B                   ",
    "XXXXXXXXXXXXXXXXXXXXlllXXXX  XXXXXXXXXXXXXXXXXXXXXXXFXXX",
    "CCCCCCCCCCCCCCCCCCCCCCCCCCC  CCCCCCCCCCCCCCCCCCCCCCCCCCC",
    "CCCCCCCCCCCCCCCCCCCCCCCCCCC  CCCCCCCCCCCCCCCCCCCCCCCCCCC",
    "CCCCCCCCCCCCCCCCCCCCCCCCCCC  CCCCCCCCCCCCCCCCCCCCCCCCCCC",
    "CCCCCCCCCCCCCCCCCCCCCCCCCCC  CCCCCCCCCCCCCCCCCCCCCCCCCCC",
    "CCCCCCCCCCCCCCCCCCCCCCCCCCC  CCCCCCCCCCCCCCCCCCCCCCCCCCC",
]

def draw_level(screen, camera_x, coin_frame):
    for block in blocks:
        screen.blit(block.image, (block.x - camera_x, block.y))

    for coin in coins:
        coin.image = ["coin_gold", "coin_gold_side"][coin_frame]
        screen.blit(coin.image, (coin.x - camera_x, coin.y))

    for lava in lava_zones:
        screen.blit(lava.image, (lava.x - camera_x, lava.y))

    if _flag:
        animated_flag = get_animated_flag_image()
        screen.blit(animated_flag, (_flag.x - camera_x, _flag.y))

    for deco in decorations:
        screen.blit(deco.image, (deco.x - camera_x, deco.y))

def get_flag():
    return _flag

def get_level_number():
    return current_level

def get_animated_flag_image():
    from time import time
    index = int(time() * 0.5) % len(flag_frames)  # cambia cada ~2 segundos
    return flag_frames[index]

def load_level(number=1):
    global current_level
    current_level = number
    if number == 2:
        data = level_data_2
    else:
        data = level_data
    build_level_from_data(data)

def build_level_from_data(data):
    global _flag
    blocks.clear()
    coins.clear()
    lava_zones.clear()
    decorations.clear()

    for y, row in enumerate(data):
        x = 0
        while x < len(row):
            tile = row[x]
            world_x = x * TILE_SIZE
            world_y = y * TILE_SIZE

            if tile == "X":
                blocks.append(Actor("terrain_grass_block_top", (world_x, world_y)))
            elif tile == "C":
                blocks.append(Actor("terrain_grass_block_center", (world_x, world_y)))
            elif tile == "L":
                blocks.append(Actor("terrain_grass_horizontal_overhang_left", (world_x, world_y)))
            elif tile == "M":
                blocks.append(Actor("terrain_grass_horizontal_middle", (world_x, world_y)))
            elif tile == "R":
                blocks.append(Actor("terrain_grass_horizontal_overhang_right", (world_x, world_y)))
            elif tile == "F":
                base = Actor("terrain_grass_block_top", (world_x, world_y))
                blocks.append(base)
                _flag = Actor("flag_blue_a")
                _flag.midbottom = (base.x + TILE_SIZE // 2, base.top)
            elif tile == "1":
                coins.append(Actor("coin_gold", (world_x, world_y)))
            elif tile == "V" or tile == "l":
                lava_zones.append(Actor("lava_top", (world_x, world_y)))
            elif tile == "K" and current_level == 1:
                decorations.append(Actor("cactus", (world_x, world_y)))
            elif tile == "B" and current_level == 2:
                decorations.append(Actor("bush", (world_x, world_y)))
            elif tile == "D" and current_level == 2:
                # Detectar longitud de plataforma de tierra
                start = x
                while x < len(row) and row[x] == "D":
                    x += 1
                end = x - 1

                for i in range(start, x):
                    tile_x = i * TILE_SIZE
                    if i == start:
                        img = "terrain_dirt_horizontal_left"
                    elif i == end:
                        img = "terrain_dirt_horizontal_right"
                    else:
                        img = "terrain_dirt_horizontal_middle"
                    blocks.append(Actor(img, (tile_x, world_y)))
                continue  # evitar x += 1 extra
            x += 1
