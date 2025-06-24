from pgzero.actor import Actor
from pgzero.keyboard import keys

GRAVITY = 1.0
JUMP_STRENGTH = 18
MOVE_SPEED = 5

class Player:
    def __init__(self, pos):
        self.actor = Actor("zombie_idle", topleft=pos)
        self.vy = 0
        self.on_ground = False
        self.walk_images = ["zombie_action1", "zombie_action2"]
        self.jump_image = "zombie_jump"
        self.idle_image = "zombie_idle"
        self.walk_timer = 0
        self.frame = 0
        self.facing_left = False

    def update(self, blocks, keyboard):
        moving = False

        if keyboard[keys.LEFT]:
            self.actor.x -= MOVE_SPEED
            self.facing_left = True
            moving = True

        if keyboard[keys.RIGHT]:
            self.actor.x += MOVE_SPEED
            self.facing_left = False
            moving = True

        if keyboard[keys.SPACE] and self.on_ground:
            self.vy = -JUMP_STRENGTH
            self.on_ground = False

        self.vy += GRAVITY
        self.actor.y += self.vy

        self.on_ground = False
        for block in blocks:
            if self.actor.colliderect(block) and self.vy >= 0:
                self.actor.bottom = block.top
                self.vy = 0
                self.on_ground = True

        # Animación
        if not self.on_ground:
            self.actor.image = self.jump_image
        elif moving:
            self.walk_timer += 1
            if self.walk_timer % 10 == 0:
                self.frame = (self.frame + 1) % len(self.walk_images)
            self.actor.image = self.walk_images[self.frame]
        else:
            self.actor.image = self.idle_image
            self.walk_timer = 0

        # Mirar hacia la izquierda
        self.actor.flip_x = self.facing_left

    def draw(self, camera_x):
        original_x = self.actor.x
        self.actor.x -= camera_x
        self.actor.draw()
        self.actor.x = original_x
