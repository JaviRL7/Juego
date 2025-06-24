# level.py
from pgzero.actor import Actor

TILE_SIZE = 64
blocks = []
coins = []
lava_zones = []
_flag = None

level_data = [
    "                                                        ",
    "                                                        ",
    "      1      1      1      1      1      1              ",
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "         1                                              ",
    "                                                        ",
    "     LMMR       1         LMMR                          ",
    "                                                        ",
    "                     LMMR                               ",
    "         1                                              ",
    "            LMMR    1         LMMR     1   LMMMMMR      ",
    "                                                        ",
    "XXXXXXXXXXXXXXXXXXXXXlllXXXXXXXXXXXXXXXXXXXXXXXXXXXXXFXX",
    "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
    "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
    "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
    "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
    "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
]

def build_level():
    global _flag
    blocks.clear()
    coins.clear()
    lava_zones.clear()

    for y, row in enumerate(level_data):
        for x, tile in enumerate(row):
            world_x = x * TILE_SIZE
            world_y = y * TILE_SIZE

            if tile == "X":
                block = Actor("terrain_grass_block_top")
                block.topleft = (world_x, world_y)
                blocks.append(block)

            elif tile == "C":
                block = Actor("terrain_grass_block_center")
                block.topleft = (world_x, world_y)
                blocks.append(block)

            elif tile == "L":
                block = Actor("terrain_grass_horizontal_overhang_left")
                block.topleft = (world_x, world_y)
                blocks.append(block)

            elif tile == "M":
                block = Actor("terrain_grass_horizontal_middle")
                block.topleft = (world_x, world_y)
                blocks.append(block)

            elif tile == "R":
                block = Actor("terrain_grass_horizontal_overhang_right")
                block.topleft = (world_x, world_y)
                blocks.append(block)

            elif tile == "F":
                base = Actor("terrain_grass_block_top")
                base.topleft = (world_x, world_y)
                blocks.append(base)
                flag_actor = Actor("flag_blue_a")
                flag_actor.midbottom = (base.x + TILE_SIZE // 2, base.top)
                _flag = flag_actor

            elif tile == "1":
                coin = Actor("coin_gold")
                coin.topleft = (world_x, world_y)
                coins.append(coin)

            elif tile == "V" or tile == "l":  # "l" para lava también
                lava = Actor("lava_top")
                lava.topleft = (world_x, world_y)
                lava_zones.append(lava)

def draw_level(screen, camera_x, coin_frame):
    for block in blocks:
        screen.blit(block.image, (block.x - camera_x, block.y))

    for coin in coins:
        coin.image = ["coin_gold", "coin_gold_side"][coin_frame]
        screen.blit(coin.image, (coin.x - camera_x, coin.y))

    for lava in lava_zones:
        screen.blit(lava.image, (lava.x - camera_x, lava.y))

    if _flag:
        screen.blit(_flag.image, (_flag.x - camera_x, _flag.y))

def get_flag():
    return _flag
