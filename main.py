# Simple pygame program

# Import and initialize the pygame library
import pygame
import glob
import random

pygame.init()

height = 480
width = 1440
# Set up the drawing window
screen = pygame.display.set_mode([width, height])

# background = pygame.image.load("assets/background/background.png")
logo = pygame.image.load("assets/logo.png")
fire_frames = glob.glob("assets/guaca/fire/*.png")

text = pygame.font.Font("assets/fonts/pixelated.ttf", 18)
title = pygame.font.Font("assets/fonts/pixelated.ttf", 24)
menu = pygame.font.Font("assets/fonts/pixelated.ttf", 12)

play_button = pygame.image.load("assets/buttons/sprite_1.png")
pause_button = pygame.image.load("assets/buttons/sprite_0.png")

clock = pygame.time.Clock()

dialogue_event = pygame.USEREVENT + 1


class Layer:
    def __init__(self, speed, image, x, y):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(image)

    def setX(self, x):
        self.x = x


RUNNING, PAUSED, QUIT, MAIN_MENU = 0, 1, 2, 3


class GameOptions:
    def __init__(self):
        self.score = 0
        self.speed = 3
        self.state = RUNNING

    def draw(self):
        score = menu.render("SCORE: 60", False, (255, 255, 255))
        screen.blit(score, (player.x, player.y - 100))
        # screen.blit(score, ((width // 2 - score.get_width() // 2), 10))


options = GameOptions()


class Button():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 48
        self.h = 48

    def draw(self):
        if options.state == RUNNING:
            screen.blit(pygame.transform.scale(pause_button, (self.w, self.h)), (self.x, self.y))
        else:
            screen.blit(pygame.transform.scale(play_button, (self.w, self.h)), (self.x, self.y))

    def collided(self, x, y):
        if self.x + self.w > x > self.x and self.y + self.h > y > self.y:
            return True
        else:
            return False

    def change(self):
        if options.state == RUNNING:
            options.state = PAUSED
        elif options.state == PAUSED:
            options.state = RUNNING


class Dialogue:
    def __init__(self):
        self.message = ""
        self.layer = None
        self.showing = False

    def crocodile_string(self):
        phrases = ["Run! Run! Run! I'll still catch you!",
                   "Slow down! I might not eat you.",
                   "Turtle legs taste delicious!"]
        return random.choice(phrases)

    def say(self):
        self.message = self.crocodile_string()
        self.layer = Layer(0, "assets/dialogue/sprite_0.png", (width - 400), (height - 310))
        self.showing = True
        print("dialogue created")
        pygame.time.set_timer(dialogue_event, 5000)

    def display(self):
        if self.showing:
            screen.blit(self.layer.image, (self.layer.x, self.layer.y))
            screen.blit(title.render("Fang", False, (0, 0, 0)), ((width - 350), (height - 98)))
            screen.blit(text.render(self.message, False, (0, 0, 0)), ((width - 350), (height - 63)))

    def destroy(self):
        print("dialogue deleted")
        self.showing = False
        self.message = ""
        self.layer = None
        pygame.time.set_timer(dialogue_event, 0)


class Logo:
    def __init__(self):
        self.layer = Layer(5, "assets/logo.png", (width - 900) / 2, 15)
        self.showing = True
        self.moving = False

    def draw(self):
        screen.blit(self.layer.image, (self.layer.x, self.layer.y))

    def remove_check(self, player_x):
        if self.moving:
            return True

        if self.showing:
            if player_x >= 50:
                return True

    def move(self):

        if not self.showing:
            return None

        self.moving = True
        self.layer.y -= self.layer.speed
        self.draw()

        if self.layer.y + 500 <= 0:
            showing = False
            moving = False


class Background(pygame.sprite.Sprite):
    def __init__(self):
        self.back = Layer(1, "assets/background/l1_sprite_1.png", 0, 0)
        self.back2 = Layer(1, "assets/background/l1_sprite_1.png", width, 0)

        self.mid = Layer(options.speed, "assets/background/l2_sprite_1.png", 0, 0)
        self.mid2 = Layer(options.speed, "assets/background/l2_sprite_1.png", width, 0)

        # self.front = Layer(3, "", 0)
        # self.front2 = Layer(3, "", width)

    def update(self):
        if (self.back.x + width) <= 0:
            self.back.x = width

        if (self.back2.x + width) <= 0:
            self.back2.x = width

        if (self.mid.x + width) <= 0:
            self.mid.x = width

        if (self.mid2.x + width) <= 0:
            self.mid2.x = width

        self.back.x -= options.speed - 1
        self.back2.x -= options.speed - 1

        self.mid.x -= options.speed
        self.mid2.x -= options.speed

        screen.blit(self.back.image, (self.back.x, self.back.y))
        screen.blit(self.back2.image, (self.back2.x, self.back2.y))
        screen.blit(self.mid.image, (self.mid.x, self.mid.y))
        screen.blit(self.mid2.image, (self.mid2.x, self.mid2.y))


class SpriteAnimation:
    def __init__(self, name, w=32, h=32):
        self.frames = glob.glob("assets/text/" + name + "/*.png")
        self.frame_pos = random.randint(0, len(self.frames) - 1)
        self.frame_max = len(self.frames) - 1
        self.img = pygame.image.load(self.frames[self.frame_pos]).convert_alpha()
        self.opacity = 255
        self.w = w
        self.h = h

    def is_collided_with(self, sprite_rect):
        return self.get_rect().colliderect(sprite_rect)

    def out_of_view(self):
        if self.opacity < 0:
            return True
        else:
            return False

    def blit_alpha(self, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((screen.get_width(), screen.get_height())).convert()
        temp.blit(screen, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        screen.blit(temp, location)

    def draw(self, x, y):
        self.img = pygame.image.load(self.frames[self.frame_pos]).convert_alpha().convert_alpha()
        if self.frame_pos == self.frame_max:
            self.frame_pos = 0
        else:
            self.frame_pos += 1

        self.blit_alpha(self.img, (x, y), self.opacity)
        self.opacity -= 5


class Guaca(pygame.sprite.Sprite):
    def __init__(self):
        self.action = "idle"
        self.velocity = 0
        self.frames = glob.glob("assets/guaca/idle/*.png")
        self.frame_pos = 0
        self.frame_max = len(self.frames) - 1
        self.img = pygame.image.load(self.frames[self.frame_pos]).convert_alpha()
        self.x = 0
        self.y = 380
        self.fire_pos = 0;
        self.sprite_animations = []

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 32, 32)

    def add_point(self):
        self.sprite_animations.append(SpriteAnimation("+1"))

    def flame(self):
        image = pygame.image.load(fire_frames[self.fire_pos])
        if self.fire_pos == len(fire_frames) - 1:
            self.fire_pos = 0
        else:
            self.fire_pos += 1

        screen.blit(image, (self.x - 30, self.y + 3))

    def update(self):

        self.img = pygame.image.load(self.frames[self.frame_pos]).convert_alpha()
        if self.frame_pos == self.frame_max:
            self.frame_pos = 0
        else:
            self.frame_pos += 1

        self.x -= options.speed
        self.x += self.velocity

        if self.x <= 0:
            self.x = 0

        if self.action == "run":
            self.flame()

        for sprite in self.sprite_animations:
            if sprite.opacity < 0:
                self.sprite_animations.remove(sprite)

            sprite.draw(self.x, self.y - 10)

        screen.blit(self.img, (self.x, self.y))

    def state(self, state):
        if self.action != state:
            self.frames = glob.glob("assets/guaca/" + state + "/*.png")
            self.frame_pos = 0
            self.frame_max = len(self.frames) - 1
            self.img = pygame.image.load(self.frames[self.frame_pos]).convert_alpha()
            self.action = state

    def move(self, speed):
        self.velocity = speed


class Components:
    def __init__(self, name, x, y, w = 64, h = 64):
        self.frames = glob.glob("assets/components/" + name + "/*.png")
        self.frame_pos = random.randint(0, len(self.frames)-1)
        self.frame_max = len(self.frames) - 1
        self.images = []

        for frame in self.frames:
            self.images.append(pygame.image.load(frame).convert_alpha())

        self.img = self.images[0]
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self):

        self.img = self.images[self.frame_pos]
        if self.frame_pos == self.frame_max:
            self.frame_pos = 0
        else:
            self.frame_pos += 1

        screen.blit(pygame.transform.scale(self.img, (self.w, self.h)), (self.x, self.y))


class Decoration:
    def __init__(self, name, obj_type, x, y, speed = 0, w = 32, h = 32):
        self.frames = glob.glob("assets/environment/" + obj_type + "/" + name + "/*.png")
        self.frame_pos = random.randint(0, len(self.frames)-1)
        self.frame_max = len(self.frames) - 1
        self.img = pygame.image.load(self.frames[self.frame_pos]).convert_alpha()
        self.x = x
        self.y = y
        self.speed = speed
        self.w = w
        self.h = h

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def is_collided_with(self, sprite_rect):
        return self.get_rect().colliderect(sprite_rect)

    def draw(self):

        self.img = pygame.image.load(self.frames[self.frame_pos]).convert_alpha()
        if self.frame_pos == self.frame_max:
            self.frame_pos = 0
        else:
            self.frame_pos += 1

        self.x -= options.speed
        self.x -= self.speed

        screen.blit(pygame.transform.scale(self.img, (self.w, self.h)), (self.x, self.y))


bug_names = ["bee"]
animal_names = ["llama"]
plant_names = []

object_type = ["bugs", "animals", "consumables"]


class Environment:
    def __init__(self):
        self.plants = []
        self.bugs = []
        self.animals = []
        self.grass = []
        self.coins = []

    def create(self, name, obj_type):
        if obj_type == "bugs":
            return Decoration(name, obj_type, width + random.randint(0, 2000), 380, 0, 64, 64)
        elif obj_type == "animals":
            speed = 0
            if name == "llama":
                speed = 4
            return Decoration(name, obj_type, width + random.randint(0, 2000), 370, speed, 80, 80)
        elif obj_type == "consumables":
            return Decoration(name, obj_type, width + random.randint(0, 2000), 400, 0, 64, 64)

    def invisible(self):
        for bug in self.bugs:
            if bug.x < -50:
                self.bugs.remove(bug)

        for animal in self.animals:
            if animal.x < -50:
                self.animals.remove(animal)

        for coin in self.coins:
            if coin.x < -50:
                self.coins.remove(coin)

    def loop(self):

        self.invisible()

        for coin in self.coins:
            if coin.is_collided_with(player.get_rect()):
                player.add_point()
                options.score += 1
                self.coins.remove(coin)

        if len(self.bugs) < 3:
            self.bugs.append(self.create(random.choice(bug_names), "bugs"))

        if len(self.animals) < 1 and random.randint(0, 5) < 2:
            self.animals.append(self.create(random.choice(animal_names), "animals"))

        if len(self.coins) < 1 and random.randint(0, 5) < 1:
            self.coins.append(self.create("coin", "consumables"))

        for bug in self.bugs:
            bug.draw()

        for animal in self.animals:
            animal.draw()

        for coin in self.coins:
            coin.draw()



player = Guaca()
environment = Environment()
background = Background()
logo = Logo()
dialogue = Dialogue()
state_button = Button(10, 10)
timer = Components("timer", width - 200, 20, 40, 45)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            options.state = QUIT

        if event.type == pygame.MOUSEBUTTONDOWN:
            # 1 is the left mouse button, 2 is middle, 3 is right.
            if event.button == 1:
                # `event.pos` is the mouse position.
                x, y = event.pos
                if state_button.collided(x, y):
                    state_button.change()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.state("walk")
                player.move(3)
            if event.key == pygame.K_RIGHT:
                player.state("run")
                player.move(6)
            if event.key == pygame.K_DOWN:
                player.state("spin")
                player.move(10)
            if event.key == pygame.K_UP:
                dialogue.say()
            if event.key == pygame.K_1:
                options.speed += 1
            if event.key == pygame.K_2:
                options.state = PAUSED
            if event.key == pygame.K_3:
                options.state = RUNNING

        if event.type == pygame.KEYUP:
            player.move(0)
            player.state("idle")

        if event.type == dialogue_event:
            dialogue.destroy()

    # Fill the background with white
    # screen.blit(background, (0, 0))
    if options.state == RUNNING:
        background.update()

        if logo.remove_check(player.x):
            logo.move()
        else:
            logo.draw()

        environment.loop()

        player.update()

        dialogue.display()

        options.draw()

    state_button.draw()
    timer.draw()

    pygame.display.update()

    clock.tick(60)
