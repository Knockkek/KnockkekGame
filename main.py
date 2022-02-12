import arcade
import sys
import enum
import random
import pygame as pg
from pygame import mixer
from pygame import *


class Button:
    def __init__(self, width, height: float, centerX: float, centerY: float, text: str, onButtonClick,
                 activeCondition, textSize=20,
                 buttonColor=arcade.color.WHITE, textColor=arcade.color.BLACK):
        self.width = width
        self.height = height
        self.centerX = centerX
        self.centerY = centerY
        self.text = text
        self.textColor = textColor
        self.onButtonClick = onButtonClick
        self.buttonColor = buttonColor
        self.activeCondition = activeCondition
        self.textSize = textSize


class GameState(enum.Enum):
    MainMenu = 0
    InGame = 1
    EndScreen = 2
    Terminating = 3


defaultX = 1920
defaultY = 1080


class GameWindow(arcade.Window):
    scaleMultiplierX = 0
    scaleMultiplierY = 0

    highScorePath = "highscore.score"
    currentGameState = GameState.MainMenu

    mousePosX = 0
    mousePosY = 0

    pg.init()

    mixer.music.load("music.mp3")
    mixer.music.play(-1)

    def StartGame(self):
        self.set_mouse_visible(False)
        self.currentGameState = GameState.InGame
        self.score = 0

    def StopGame(self):
        self.set_mouse_visible(True)
        self.currentGameState = GameState.EndScreen
        self.raumschiff.center_x = -100
        self.raumschiff.center_y = -100
        for gegner in self.gegnergruppe:
            gegner.center_x = -100
            gegner.center_y = random.randint(int((self.displaysize[1] / 5) * 2),
                                             int((self.displaysize[1] / 5) * 5))
        for bullet in self.gegnerbullets:
            bullet.center_x = -100
            bullet.center_y = -100

        self.gegnergruppemove = arcade.SpriteList()

    def Exit(self):
        self.currentGameState = GameState.Terminating

    def __init__(self, width, height):
        super().__init__(width, height)
        self.set_fullscreen(True)
        self.set_mouse_visible(True)

        self.displaysize = arcade.get_display_size()
        self.scaleMultiplierX = self.displaysize[0] / defaultX
        self.scaleMultiplierY = self.displaysize[1] / defaultY

        self.background = arcade.load_texture("ESA_root_pillars.jpg")
        self.raumschiff = arcade.Sprite("1B.png", 0.5)
        self.raumschiff.height *= self.scaleMultiplierY
        self.raumschiff.width *= self.scaleMultiplierX
        self.raumschiff.center_x = -100
        self.raumschiff.center_y = -100
        self.bullets = arcade.SpriteList()
        self.gegnerbullets = arcade.SpriteList()
        self.gegnergruppe = arcade.SpriteList()
        self.gegnergruppemove = arcade.SpriteList()

        self.timer = 0
        self.timer2 = 0
        self.x = 0
        self.score = 0
        self.clock = pg.time.Clock()

        self.highScoreFile = open(self.highScorePath, 'r')
        self.highScore = self.highScoreFile.readline()
        if self.highScore == '':
            self.highScore = 0
        else:
            tmp = self.highScore.split('\n')
            self.highScore = int(tmp[0])
        self.highScoreFile.close()

        self.buttons = [Button(self.displaysize[0] / 10, self.displaysize[1] / 10,
                               self.displaysize[0] // 2 - self.displaysize[0] / 12.5, self.displaysize[1] // 2.5,
                               "Start",
                               self.StartGame, lambda: True if self.currentGameState is not GameState.InGame else False,
                               30),
                        Button(self.displaysize[0] / 10, self.displaysize[1] / 10,
                               self.displaysize[0] // 2 + self.displaysize[0] / 12.5, self.displaysize[1] // 2.5,
                               "Exit",
                               self.Exit, lambda: True if self.currentGameState is not GameState.InGame else False, 30)]

        for x in range(50):
            laser = arcade.Sprite("laserBullet.png", 0.3)
            laser.height *= self.scaleMultiplierY
            laser.width *= self.scaleMultiplierX
            laser.center_x = -100
            laser.center_y = -100
            self.bullets.append(laser)

        for x in range(150):
            self.gegnerlaser = arcade.Sprite("Fireball1.png", 1.8)
            self.gegnerlaser.height *= self.scaleMultiplierY
            self.gegnerlaser.width *= self.scaleMultiplierX
            self.gegnerlaser.center_x = -49
            self.gegnerlaser.center_y = -49
            self.gegnerbullets.append(self.gegnerlaser)

        for x in range(21):
            self.gegner = arcade.Sprite("4.png", 0.5)
            self.gegner.height *= self.scaleMultiplierY
            self.gegner.width *= self.scaleMultiplierX
            self.gegner.center_x = - 100
            self.gegner.center_y = random.randint(int((self.displaysize[1] / 5) * 2),
                                                  int((self.displaysize[1] / 5) * 5))
            self.gegnergruppe.append(self.gegner)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(self.displaysize[0] // 2, self.displaysize[1] // 2, self.displaysize[0],
                                      self.displaysize[1], self.background)

        for current in self.buttons:
            if current.activeCondition():
                arcade.draw_rectangle_filled(current.centerX, current.centerY, current.width, current.height,
                                             current.buttonColor)
                arcade.draw_text(current.text, current.centerX, current.centerY, current.textColor, current.textSize,
                                 width=0, align="center", anchor_x="center", anchor_y="center")

        if self.currentGameState is GameState.MainMenu:
            arcade.draw_text("geiles Game", self.displaysize[0] // 2,
                             self.displaysize[1] // 2,
                             arcade.color.WHITE, 30,
                             width=0, align="center", anchor_x="center", anchor_y="center")

        if self.currentGameState is GameState.EndScreen:
            arcade.draw_text("You dead!\nScore: " + (str(self.score)) + "\nHighscore: " + (str(self.highScore)),
                             self.displaysize[0] // 2, self.displaysize[1] // 1.75, arcade.color.WHITE, 40,
                             width=0, align="center", anchor_x="center", anchor_y="center",
                             font_name=('calibri', 'arial'), bold=True)

        if self.currentGameState is GameState.InGame:
            self.gegner.draw()
            self.bullets.draw()
            self.gegnerbullets.draw()
            self.raumschiff.draw()
            self.gegnergruppe.draw()
            self.gegnerlaser.draw()
            arcade.draw_text("Your Score: " + (str(self.score)), 10, int(self.displaysize[1] - 25), arcade.color.WHITE,
                             15)

    def update(self, delta_time):
        if self.currentGameState is GameState.Terminating:
            sys.exit()

        if self.currentGameState is GameState.MainMenu:
            return

        for self.gegner in self.gegnergruppemove:
            collidedSprites = arcade.check_for_collision_with_list(self.gegner, self.bullets)
            if collidedSprites:
                self.gegnergruppemove.remove(self.gegner)
                self.gegner.center_x = -100
                self.score = self.score + 1
                collidedSprites[0].center_x = -100

        if arcade.check_for_collision_with_list(self.raumschiff,
                                                self.gegnergruppemove) or arcade.check_for_collision_with_list(self.raumschiff, self.gegnerbullets):
            if self.score > self.highScore:
                self.highScoreFile = open(self.highScorePath, 'w')
                self.highScoreFile.write(str(self.score))
                self.highScore = self.score
                self.highScoreFile.close()
                self.StopGame()
            else:
                self.StopGame()

        if self.timer >= random.randint(25, 40):
            for gegner in self.gegnergruppemove:
                for gegnerlaser in self.gegnerbullets:
                    if gegnerlaser.center_y < -10:
                        gegnerlaser.center_x = gegner.center_x + 15 * self.scaleMultiplierX
                        gegnerlaser.center_y = gegner.center_y - 25 * self.scaleMultiplierY
                        break

            self.timer = 0

        for gegnerlaser in self.gegnerbullets:
            gegnerlaser.center_y = gegnerlaser.center_y - 12

        if self.timer2 >= random.randint(40, 60):
            self.gegnergruppemove.append(self.gegnergruppe[self.x])
            if self.x == 20:
                self.x = 0
            else:
                self.x = self.x + 1
            self.timer2 = 0

        for gegner in self.gegnergruppemove:
            if gegner.center_x >= self.displaysize[0] * 1.1:
                gegner.center_x = -100
                self.gegnergruppemove.remove(gegner)

        for self.gegner in self.gegnergruppemove:
            self.gegner.center_x = self.gegner.center_x + 5 * self.scaleMultiplierX

        self.gegnergruppe.update()

        for laser in self.bullets:
            if laser.center_x >= 0:
                laser.change_y = 20 * self.scaleMultiplierY

            if laser.center_y > 2000:
                laser.center_x = -100
                laser.center_y = -100
                laser.change_y = 0

        for laser in self.bullets:
            laser.update()

        self.timer = self.timer + 1
        self.timer2 = self.timer2 + 1

        self.gegnerbullets.update()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.mousePosX = x
        self.mousePosY = y
        self.raumschiff.center_x = x
        self.raumschiff.center_y = y

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):

        for button in self.buttons:
            if button.centerX - button.width // 2 < x < button.centerX + button.width // 2 \
                    and button.centerY - button.height // 2 < y < button.centerY + button.height // 2 \
                    and button.activeCondition():
                button.onButtonClick()

        if self.currentGameState is GameState.InGame:
            for laser in self.bullets:
                if laser.center_x <= 0:
                    laser.center_x = x
                    laser.center_y = y + self.raumschiff.height // 2 + laser.height // 2
                    break


window = GameWindow(defaultX, defaultY)
arcade.run()
