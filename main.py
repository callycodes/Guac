# Simple pygame program

# Import and initialize the pygame library
import pygame
import glob

pygame.init()

moving_speed = 3;

height = 480
width = 1440
# Set up the drawing window
screen = pygame.display.set_mode([width, height])

# background = pygame.image.load("assets/background/background.png")
logo = pygame.image.load("assets/logo.png")
fire_frames = glob.glob("assets/guaca/fire/*.png")

font = pygame.font.Font("assets/fonts/.ttf", 26)

clock = pygame.time.Clock()

dialogue_event = pygame.USEREVENT + 1

# Run until the user asks to quit
running = True


class Layer:
    def __init__(self, speed, image, x, y):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(image)

    def setX(self, x):
        self.x = x


class Dialogue:
    def __init__(self):
        self.message = ""
        self.layer = None
        self.showing = False

    def say(self, message):
        self.message = message
        self.layer = Layer(0, "assets/dialogue/sprite_0.png", (width - 400), (height - 310))
        self.showing = True
        print("dialogue created")
        pygame.time.set_timer(dialogue_event, 5000)

    def display(self):
        if self.showing:
            screen.blit(self.layer.image, (self.layer.x, self.layer.y))

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
        self.back = Layer(moving_speed, "assets/background/background.png", 0, 0)
        self.back2 = Layer(moving_speed, "assets/background/background.png", width, 0)

        # self.mid = Layer(2, "", 0)
        # self.mid2 = Layer(2, "", width)

        # self.front = Layer(3, "", 0)
        # self.front2 = Layer(3, "", width)

    def update(self):
        if (self.back.x + width) == 0:
            self.back.x = width

        if (self.back2.x + width) == 0:
            self.back2.x = width

        self.back.x -= self.back.speed
        self.back2.x -= self.back2.speed

        screen.blit(self.back.image, (self.back.x, self.back.y))
        screen.blit(self.back2.image, (self.back2.x, self.back2.y))



class Guaca(pygame.sprite.Sprite):
    def __init__(self):
        self.action = "idle"
        self.velocity = 0
        self.frames = glob.glob("assets/guaca/idle/*.png")
        self.frame_pos = 0
        self.frame_max = len(self.frames) - 1
        self.img = pygame.image.load(self.frames[self.frame_pos])
        self.x = 0
        self.y = 380
        self.fire_pos = 0;

    def flame(self):
        image = pygame.image.load(fire_frames[self.fire_pos])
        if self.fire_pos == len(fire_frames) - 1:
            self.fire_pos = 0
        else:
            self.fire_pos += 1

        screen.blit(image, (self.x - 30, self.y + 3))

    def update(self):

        self.img = pygame.image.load(self.frames[self.frame_pos])
        if self.frame_pos == self.frame_max:
            self.frame_pos = 0
        else:
            self.frame_pos += 1

        self.x -= moving_speed
        self.x += self.velocity

        if self.x <= 0:
            self.x = 0

        if self.action == "run":
            self.flame()

        screen.blit(self.img, (self.x, self.y))

    def state(self, state):
        if self.action != state:
            self.frames = glob.glob("assets/guaca/" + state + "/*.png")
            self.frame_pos = 0
            self.frame_max = len(self.frames) - 1
            self.img = pygame.image.load(self.frames[self.frame_pos])
            self.action = state

    def move(self, speed):
        self.velocity = speed


player = Guaca()
background = Background()
logo = Logo()
dialogue = Dialogue()

while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.state("walk")
                player.move(3)
            if event.key == pygame.K_RIGHT:
                player.state("run")
                player.move(6)
            if event.key == pygame.K_UP:
                dialogue.say("test")

        if event.type == pygame.KEYUP:
            player.move(0)
            player.state("idle")

        if event.type == dialogue_event:
            dialogue.destroy()

    # Fill the background with white
    # screen.blit(background, (0, 0))
    background.update()

    if logo.remove_check(player.x):
        logo.move()
    else:
        logo.draw()

    player.update()

    dialogue.display()

    pygame.display.update()

    clock.tick(72);