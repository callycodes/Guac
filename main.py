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
logo = pygame.transform.scale(pygame.image.load("assets/logo.png").convert_alpha(), (265, 150))
fire_frames = glob.glob("assets/guaca/fire/*.png")

text = pygame.font.Font("assets/fonts/pixelated.ttf", 18)
title = pygame.font.Font("assets/fonts/pixelated.ttf", 24)
menu = pygame.font.Font("assets/fonts/pixelated.ttf", 12)

play_button = pygame.transform.scale(pygame.image.load("assets/buttons/sprite_1.png").convert_alpha(), (48, 48))
pause_button = pygame.transform.scale(pygame.image.load("assets/buttons/sprite_0.png").convert_alpha(), (48, 48))

clock = pygame.time.Clock()

dialogue_event = pygame.USEREVENT + 1
speedup_event = pygame.USEREVENT + 2

pygame.time.set_timer(speedup_event, 5000)


class Layer:
    def __init__(self, speed, image, x, y):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(image).convert_alpha()

    def setX(self, x):
        self.x = x

    def set_speed(self):
        self.speed = options.speed


RUNNING, PAUSED, QUIT, MAIN_MENU, INTRO = 0, 1, 2, 3, 4


class GameOptions:
    def __init__(self):
        self.score = 0
        self.speed = 0
        self.state = INTRO

    def draw(self):
        score = menu.render("SCORE: " + str(self.score), False, (255, 255, 255))
        screen.blit(score, (player.x, player.y - 100))
        # screen.blit(score, ((width // 2 - score.get_width() // 2), 10))

    def speedup(self):
        if self.speed < 11:
            self.speed += 1
            player.set_velocity()


options = GameOptions()


class Button():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 48
        self.h = 48

    def draw(self):
        if options.state == RUNNING:
            screen.blit(pause_button, (self.x, self.y))
        else:
            screen.blit(play_button, (self.x, self.y))

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

    def say_line(self, line):
        print("created")
        self.message = line
        self.layer = Layer(0, "assets/dialogue/sprite_0.png", (width - 400), (height - 310))
        self.showing = True
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
        self.layer = Layer(5, "assets/logo.png", (width - logo.get_width()) // 4, 20)
        self.showing = True
        self.moving = False

    def draw(self):
        screen.blit(self.layer.image, (self.layer.x, self.layer.y))

    def remove_check(self, player_x):
        if self.moving:
            return True

        if self.showing:
            if player_x >= 200:
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

        self.back = Layer(0, "assets/background/l0_sprite_1.png", 0, 0)
        self.back2 = Layer(0, "assets/background/l0_sprite_1.png", width, 0)

        self.mid = Layer(0, "assets/background/l1_sprite_1.png", 0, 0)
        self.mid2 = Layer(0, "assets/background/l1_sprite_1.png", width, 0)

        self.front = Layer(options.speed, "assets/background/l3_sprite_2.png", 0, 0)
        self.front2 = Layer(options.speed, "assets/background/l3_sprite_2.png", width, 0)

    def set_background_speeds(self):
        self.back.speed = 1
        self.back2.speed = 1
        self.mid.speed = 2
        self.mid2.speed = 2
        self.front.speed = options.speed
        self.front2.speed = options.speed

    def update(self):
        self.front.set_speed()

        self.back.x -= self.back.speed
        self.back2.x -= self.back.speed

        self.mid.x -= self.mid.speed
        self.mid2.x -= self.mid.speed

        self.front.x -= self.front.speed
        self.front2.x -= self.front.speed

        if self.back.x < width * -1:
            self.back.x = width - 2
        if self.back2.x < width * -1:
            self.back2.x = width - 2

        if self.mid.x < width * -1:
            self.mid.x = width - 2
        if self.mid2.x < width * -1:
            self.mid2.x = width - 2

        if self.front.x < width * -1:
            self.front.x = width - 2
        if self.front2.x < width * -1:
            self.front2.x = width - 2

        screen.blit(self.back.image, (self.back.x, self.back.y))
        screen.blit(self.back2.image, (self.back2.x, self.back2.y))
        screen.blit(self.mid.image, (self.mid.x, self.mid.y))
        screen.blit(self.mid2.image, (self.mid2.x, self.mid2.y))
        screen.blit(self.front.image, (self.front.x, self.front.y))
        screen.blit(self.front2.image, (self.front2.x, self.front2.y))


class SpriteAnimation:
    def __init__(self, name, w=32, h=32):
        self.frames = glob.glob("assets/text/" + name + "/*.png")
        self.frame_pos = random.randint(0, len(self.frames) - 1)
        self.frame_max = len(self.frames) - 1
        self.images = []

        for frame in self.frames:
            self.images.append(pygame.image.load(frame).convert_alpha())

        self.img = self.images[0]
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
        self.img = self.images[self.frame_pos]
        if self.frame_pos == self.frame_max:
            self.frame_pos = 0
        else:
            self.frame_pos += 1

        self.blit_alpha(self.img, (x, y), self.opacity)
        self.opacity -= 5


class Intro():
    def __init__(self):
        self.progress = 0

    def tutorial(self):
        # parachute in
        if self.progress == 0:
            player.parachute()
            # parachute in
            if player.y >= 385:
                player.state("idle")
                self.progress = 1

        elif self.progress == 1:
            if dialogue.showing == False:
                dialogue.say_line("Haha! You landed right in my trap!")

        elif self.progress == 2:
            if dialogue.showing == False:
                dialogue.say_line("Prepare to get eaten! This should be fun!")
        elif self.progress == 3:
            background.set_background_speeds()
            player.state("walk")
            options.state = RUNNING
            options.speed = 3
            player.set_velocity()


class Guaca(pygame.sprite.Sprite):
    def __init__(self):
        self.action = "idle"
        self.velocity = 0
        self.frames = glob.glob("assets/guaca/idle/*.png")
        self.frame_pos = 0
        self.frame_max = len(self.frames) - 1
        self.images = []

        for frame in self.frames:
            self.images.append(pygame.image.load(frame).convert_alpha())

        self.img = self.images[0]

        self.fire_frames = glob.glob("assets/guaca/fire/*.png")
        self.fire_images = []
        for frame in self.fire_frames:
            self.fire_images.append(pygame.image.load(frame).convert_alpha())

        self.x = 60
        self.y = -70
        self.fire_pos = 0;
        self.sprite_animations = []

        self.parachuting_sprite = pygame.image.load("assets/guaca/parachute/sprite_0.png").convert_alpha()
        self.parachute_sprite = pygame.image.load("assets/guaca/parachute/para_0.png").convert_alpha()

    def walk(self):
        self.state("walk")

    def run(self):
        self.state("run")

    def spin(self):
        self.state("spin")

    def idle(self):
        self.state("idle")

    def parachute(self):
        self.action = "parachute"

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 32, 32)

    def add_point(self):
        self.sprite_animations.append(SpriteAnimation("+1"))

    def flame(self):
        image = self.fire_images[self.fire_pos]
        if self.fire_pos == len(fire_frames) - 1:
            self.fire_pos = 0
        else:
            self.fire_pos += 1

        screen.blit(image, (self.x - 30, self.y + 3))

    def update(self):

        if options.state == RUNNING:
            self.img = self.images[self.frame_pos]
            if self.frame_pos == self.frame_max:
                self.frame_pos = 0
            else:
                self.frame_pos += 1

            self.x -= options.speed
            self.x += self.velocity

            if self.x <= 50:
                self.x = 50

            if self.action == "run":
                self.flame()

            for sprite in self.sprite_animations:
                if sprite.opacity < 0:
                    self.sprite_animations.remove(sprite)

                sprite.draw(self.x, self.y - 10)

        elif options.state == INTRO:
            if self.action == "parachute":
                self.x += 2
                self.y += 4
                screen.blit(self.parachute_sprite, (self.x - 10, self.y - 10))
                self.img = self.parachuting_sprite

        screen.blit(self.img, (self.x, self.y))

    def state(self, state):

        if self.action != state:

            self.frames = glob.glob("assets/guaca/" + state + "/*.png")
            self.frame_pos = 0
            self.frame_max = len(self.frames) - 1
            self.images = []

            for frame in self.frames:
                self.images.append(pygame.image.load(frame).convert_alpha())

            self.img = self.images[0]

            self.action = state
            self.set_velocity()

    def set_velocity(self):
        print("Velocity changed")
        if self.action == "idle":
            self.velocity = 0
        elif self.action == "walk":
            self.velocity = options.speed
        elif self.action == "run" or self.action == "spin":
            self.velocity = options.speed * 2


class Components:
    def __init__(self, name, x, y, w=64, h=64):
        self.frames = glob.glob("assets/components/" + name + "/*.png")
        self.frame_pos = random.randint(0, len(self.frames) - 1)
        self.frame_max = len(self.frames) - 1

        self.w = w
        self.h = h

        self.images = []

        for frame in self.frames:
            self.images.append(pygame.transform.scale(pygame.image.load(frame).convert_alpha(), (self.w, self.h)))

        self.img = self.images[0]
        self.x = x
        self.y = y

    def draw(self):

        self.img = self.images[self.frame_pos]
        if self.frame_pos == self.frame_max:
            self.frame_pos = 0
        else:
            self.frame_pos += 1

        screen.blit(self.img, (self.x, self.y))


class Decoration:
    def __init__(self, name, obj_type, x, y, speed=0, w=32, h=32):
        self.frames = glob.glob("assets/environment/" + obj_type + "/" + name + "/*.png")
        self.frame_pos = random.randint(0, len(self.frames) - 1)
        self.frame_max = len(self.frames) - 1
        self.name = name
        self.w = w
        self.h = h

        self.images = []

        for frame in self.frames:
            self.images.append(pygame.transform.scale(pygame.image.load(frame).convert_alpha(), (self.w, self.h)))

        self.img = self.images[0]
        self.x = x
        self.y = y
        self.speed = speed
        self.eagle_up = False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def is_collided_with(self, sprite_rect):
        return self.get_rect().colliderect(sprite_rect)

    def draw(self):

        self.img = self.images[self.frame_pos]
        if self.frame_pos == self.frame_max:
            self.frame_pos = 0
        else:
            self.frame_pos += 1

        if self.name == "eagle":
            if self.eagle_up or self.y >= 350:
                self.x -= self.speed
                self.y -= self.speed // 2
                self.eagle_up = True
            else:
                self.x -= self.speed
                self.y += self.speed // 2

        else:
            self.x -= options.speed
            self.x -= self.speed

        screen.blit(self.img, (self.x, self.y))


bug_names = ["bee"]
animal_names = ["llama", "bunny", "meerkat", "eagle"]
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
            w, h = 80, 80
            y = 370
            speed = 0
            if name == "llama":
                speed = 4
            if name == "bunny":
                speed = 8
            if name == "meerkat":
                speed = 0
                w = 60
                h = 60
            if name == "eagle":
                print("eagled spawned")
                speed = 8
                w = 120
                h = 120
                return Decoration(name, obj_type, (width-500) + random.randint(0, 1000), -120, speed, w, h)
            return Decoration(name, obj_type, width + random.randint(0, 100), y, speed, w, h)
        elif obj_type == "consumables":
            return Decoration(name, obj_type, width + random.randint(0, 2000), 400, 0, 64, 64)


    def invisible(self):
        for bug in self.bugs:
            if bug.x < -50:
                self.bugs.remove(bug)

        for animal in self.animals:
            if animal.x < -120:
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

        if len(self.animals) < 3 and random.randint(0, 5) < 2:
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
introduction = Intro()

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
                player.idle()
            if event.key == pygame.K_RIGHT:
                player.run()
            if event.key == pygame.K_DOWN:
                player.spin()
            if event.key == pygame.K_UP:
                dialogue.say()
            if event.key == pygame.K_1:
                options.speed += 1
            if event.key == pygame.K_2:
                options.state = PAUSED
            if event.key == pygame.K_3:
                options.state = RUNNING

        if event.type == pygame.KEYUP:
            if options.state == RUNNING:
                player.walk()

        if event.type == dialogue_event:
            print("found dialogue")
            dialogue.destroy()
            if options.state == INTRO:
                print("is intro dialogue")
                introduction.progress += 1

        if event.type == speedup_event & options.state != INTRO:
            options.speedup()

    # Fill the background with white
    # screen.blit(background, (0, 0))

    if options.state == MAIN_MENU:
        if logo.remove_check(player.x):
            logo.move()
        else:
            logo.draw()

    if options.state == INTRO:
        # print("intro")
        background.update()

        introduction.tutorial()
        player.update()
        dialogue.display()

    elif options.state == RUNNING:
        background.update()

        environment.loop()

        player.update()

        dialogue.display()

        options.draw()
        state_button.draw()
        timer.draw()

    pygame.display.update()

    clock.tick(30)
