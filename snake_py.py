
"""
Enhanced Graphical Snake Game
Features:
- Glow effect snake + eyes
- animation yellow feed
- Gradient background + grid
- Start, Pause, Game Over screens
- score and highest score
- WASD + arrow key control
"""

import pygame
import random
import math
import sys

# ------------------- Config -------------------
CELL = 24
GRID_W = 28
GRID_H = 20
SCREEN_W = GRID_W * CELL
SCREEN_H = GRID_H * CELL
FPS = 60

FONT_NAME = None  # default font
HIGHSCORE_FILE = "highscore.txt"

# Colors
BG_TOP = (30,30,30)
BG_BOTTOM = (50,50,50)
SNAKE_COLOR = (50,200,50)
SNAKE_HEAD = (120,255,120)
APPLE_COLOR = (255,220,60)
TEXT_COLOR = (230,230,230)
ACCENT = (200,200,255)

# Directions
UP, RIGHT, DOWN, LEFT = 0,1,2,3

# ------------------- Utils -------------------

def load_highscore():
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read().strip() or 0)
    except:
        return 0

def save_highscore(score):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))
    except:
        pass

# ------------------- Game -------------------

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Snake - Graphic Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(FONT_NAME, 20)
        self.bigfont = pygame.font.SysFont(FONT_NAME, 48)
        self.reset()
        self.highscore = load_highscore()

    def reset(self):
        self.snake = [(GRID_W//2, GRID_H//2)]
        self.direction = RIGHT
        self.spawn_apple()
        self.running = False
        self.paused = False
        self.game_over = False
        self.ticks_per_move = 8
        self.frame_counter = 0

    def spawn_apple(self):
        while True:
            a = (random.randint(0, GRID_W-1), random.randint(0, GRID_H-1))
            if a not in self.snake:
                self.apple = a
                self.apple_phase = 0.0
                return

    def handle_input(self, ev):
        if ev.type == pygame.KEYDOWN:
            if ev.key in (pygame.K_UP, pygame.K_w) and self.direction != DOWN:
                self.direction = UP
            elif ev.key in (pygame.K_DOWN, pygame.K_s) and self.direction != UP:
                self.direction = DOWN
            elif ev.key in (pygame.K_LEFT, pygame.K_a) and self.direction != RIGHT:
                self.direction = LEFT
            elif ev.key in (pygame.K_RIGHT, pygame.K_d) and self.direction != LEFT:
                self.direction = RIGHT
            elif ev.key == pygame.K_SPACE:
                if not self.running and not self.game_over:
                    self.running = True
                elif self.game_over:
                    self.reset()
                    self.running = True
                else:
                    self.paused = not self.paused

    def update(self):
        if not self.running or self.paused or self.game_over:
            return
        self.frame_counter += 1
        if self.frame_counter >= self.ticks_per_move:
            self.frame_counter = 0
            hx, hy = self.snake[0]
            nx, ny = hx, hy
            if self.direction == UP: ny -= 1
            elif self.direction == DOWN: ny += 1
            elif self.direction == LEFT: nx -= 1
            elif self.direction == RIGHT: nx += 1

            if nx <0 or nx>=GRID_W or ny<0 or ny>=GRID_H or (nx,ny) in self.snake:
                self.game_over = True
                score = len(self.snake)-1
                if score > self.highscore:
                    self.highscore = score
                    save_highscore(self.highscore)
                return

            self.snake.insert(0,(nx,ny))
            if (nx,ny) == self.apple:
                self.spawn_apple()
            else:
                self.snake.pop()

    def draw_gradient_bg(self):
        for y in range(SCREEN_H):
            color_ratio = y/SCREEN_H
            r = BG_TOP[0]*(1-color_ratio)+BG_BOTTOM[0]*color_ratio
            g = BG_TOP[1]*(1-color_ratio)+BG_BOTTOM[1]*color_ratio
            b = BG_TOP[2]*(1-color_ratio)+BG_BOTTOM[2]*color_ratio
            pygame.draw.line(self.screen,(int(r),int(g),int(b)),(0,y),(SCREEN_W,y))

    def draw_grid(self):
        for gx in range(GRID_W):
            for gy in range(GRID_H):
                rect = pygame.Rect(gx*CELL,gy*CELL,CELL,CELL)
                if (gx+gy)%2==0:
                    pygame.draw.rect(self.screen,(0,0,0,10),rect)

    def draw_snake(self):
        for i,(x,y) in enumerate(self.snake):
            px,py = x*CELL,y*CELL
            color = SNAKE_HEAD if i==0 else SNAKE_COLOR
            pygame.draw.rect(self.screen,color,(px,py,CELL,CELL),border_radius=4)
            # glow effect
            if i==0:
                for j in range(1,3):
                    s = CELL+j*2
                    a = max(0,255-90*j)
                    surf = pygame.Surface((s,s),pygame.SRCALPHA)
                    pygame.draw.rect(surf,(color[0],color[1],color[2],a),(0,0,s,s),border_radius=s//2)
                    self.screen.blit(surf,(px-(s-CELL)//2,py-(s-CELL)//2))
                # eyes
                eye_radius = CELL//6
                eye_y = py+CELL//3
                eye_x1 = px+CELL//3
                eye_x2 = px+CELL*2//3 - eye_radius
                pygame.draw.circle(self.screen,(255,255,255),(eye_x1,eye_y),eye_radius)
                pygame.draw.circle(self.screen,(255,255,255),(eye_x2,eye_y),eye_radius)
                pupil_radius = CELL//12
                pygame.draw.circle(self.screen,(0,0,0),(eye_x1,eye_y),pupil_radius)
                pygame.draw.circle(self.screen,(0,0,0),(eye_x2,eye_y),pupil_radius)

    def draw_apple(self):
        ax,ay = self.apple
        cx,cy = ax*CELL+CELL//2,ay*CELL+CELL//2
        self.apple_phase += 0.05
        r = int((CELL//2-2)+math.sin(self.apple_phase)*3)
        pygame.draw.circle(self.screen,APPLE_COLOR,(cx,cy),r)
        pygame.draw.circle(self.screen,(255,255,255),(cx-r//3,cy-r//3),max(1,r//6))

    def draw_ui(self):
        score = len(self.snake)-1
        txt = self.font.render(f"Score: {score}",True,TEXT_COLOR)
        self.screen.blit(txt,(8,8))
        hs = self.font.render(f"High: {self.highscore}",True,TEXT_COLOR)
        self.screen.blit(hs,(8,32))

    def draw_overlay(self,text=None):
        overlay = pygame.Surface((SCREEN_W,SCREEN_H),pygame.SRCALPHA)
        overlay.fill((0,0,0,160))
        self.screen.blit(overlay,(0,0))
        if text:
            t_surf = self.bigfont.render(text,True,ACCENT)
            self.screen.blit(t_surf,(SCREEN_W//2-t_surf.get_width()//2,SCREEN_H//2-24))

    def run(self):
        while True:
            dt = self.clock.tick(FPS)/1000.0
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    save_highscore(self.highscore)
                    pygame.quit()
                    sys.exit()
                self.handle_input(ev)

            self.update()
            self.draw_gradient_bg()
            self.draw_grid()
            self.draw_snake()
            self.draw_apple()
            self.draw_ui()

            if not self.running and not self.game_over:
                self.draw_overlay("Press SPACE to Start")
            if self.paused:
                self.draw_overlay("PAUSED")
            if self.game_over:
                self.draw_overlay("GAME OVER")

            pygame.display.flip()

if __name__=="__main__":
    game = SnakeGame()
    game.run()

#python3 snake_py.py



