import sys, pygame
from pygame.locals import *
from PIL import Image
import torchvision.transforms as T
import matplotlib.pyplot as plt
import torch
import Tools


class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    # X property
    def getx(self): return self.__x

    def setx(self, x): self.__x = x

    x = property(getx, setx)

    # Y property
    def gety(self): return self.__y

    def sety(self, y): self.__y = y

    y = property(gety, sety)


def print_text(x, y, text, color=(255, 255, 255)):
    font = pygame.font.Font(None, 25)
    imgText = font.render(text, True, color)
    screen = pygame.display.get_surface()
    screen.blit(imgText, (x, y))


def close_win():
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]: sys.exit()


class Rect_Model():
    def __init__(self, name, color, position):
        self.name = name
        self.moving = True
        self.color = color
        self.score = 0
        self.count_cash = 0
        self.size = Point(30, 30)
        self.position = position
        self.model = Rect(self.position.x, self.position.y, self.size.x, self.size.y)

    def update(self):
        if self.model.x <= 0:
            self.model.x = 0
        elif self.model.x >= (W - self.size.x):
            self.model.x = W - self.size.x
        if self.model.y <= 0:
            self.model.y = 0
        elif self.model.y >= (H - self.size.y):
            self.model.y = H - self.size.y

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.model, 0)

    def move(self):
        if self.moving:
            keys = pygame.key.get_pressed()
            if keys[K_w]:
                self.model.y -= 20
            if keys[K_s]:
                self.model.y += 20
            if keys[K_d]:
                self.model.x += 20
            if keys[K_a]:
                self.model.x -= 20

    def move_(self, action):
        if self.moving:
            if action == 0:
                self.model.y -= 10
            if action == 1:
                self.model.y += 10
            if action == 2:
                self.model.x += 10
            if action == 3:
                self.model.x -= 10


def game_init():
    global screen, backbuffer, timer, farmer, cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, H, W, count_cash, sizev, c, c1, c2, c3, c4, c5, c6, c7, c8

    c = []
    c1 = []
    c2 = []
    c3 = []
    c4 = []
    c5 = []
    c6 = []
    c7 = []
    c8 = []

    H = 300
    W = 300
    size = 15
    pygame.init()
    screen = pygame.display.set_mode((H, W + 100))
    backbuffer = pygame.Surface((H, W))
    count_cash = 0
    pygame.display.set_caption("Color")
    timer = pygame.time.Clock()

    farmer_pos = Point(W / 2 - size, H / 2 - size)
    farmer = Rect_Model('farmer', (0, 0, 0), farmer_pos)

    cell1_pos = Point(0, 0)
    cell1 = Rect_Model('cell1', (100, 100, 100), cell1_pos)
    cell2_pos = Point(W / 2 - size, 0)
    cell2 = Rect_Model('cell2', (0, 255, 0), cell2_pos)
    cell3_pos = Point(W, 0)
    cell3 = Rect_Model('cell3', (50, 50, 50), cell3_pos)
    cell4_pos = Point(0, H / 2 - size)
    cell4 = Rect_Model('cell4', (0, 0, 255), cell4_pos)
    cell5_pos = Point(W, H / 2 - size)
    cell5 = Rect_Model('cell5', (255, 0, 0), cell5_pos)
    cell6_pos = Point(0, H)
    cell6 = Rect_Model('cell6', (150, 150, 150), cell6_pos)
    cell7_pos = Point(W / 2 - size, H)
    cell7 = Rect_Model('cell7', (250, 250, 250), cell7_pos)
    cell8_pos = Point(W, H)
    cell8 = Rect_Model('cell8', (200, 200, 200), cell8_pos)


def update_score():
    if pygame.Rect.colliderect(farmer.model, cell1.model):
        farmer.score += 1
        farmer.model.x = W / 2
        farmer.model.y = H / 2
        cell1.count_cash += 1
    if pygame.Rect.colliderect(farmer.model, cell2.model):
        farmer.score += 1
        farmer.model.x = W / 2
        farmer.model.y = H / 2
        cell2.count_cash += 1
    if pygame.Rect.colliderect(farmer.model, cell3.model):
        farmer.score += 1
        farmer.model.x = W / 2
        farmer.model.y = H / 2
        cell3.count_cash += 1
    if pygame.Rect.colliderect(farmer.model, cell4.model):
        farmer.score += 1
        farmer.model.x = W / 2
        farmer.model.y = H / 2
        cell4.count_cash += 1
    if pygame.Rect.colliderect(farmer.model, cell5.model):
        farmer.score += 1
        farmer.model.x = W / 2
        farmer.model.y = H / 2
        cell5.count_cash += 1
    if pygame.Rect.colliderect(farmer.model, cell6.model):
        farmer.score += 1
        farmer.model.x = W / 2
        farmer.model.y = H / 2
        cell6.count_cash += 1
    if pygame.Rect.colliderect(farmer.model, cell7.model):
        farmer.score += 1
        farmer.model.x = W / 2
        farmer.model.y = H / 2
        cell7.count_cash += 1
    if pygame.Rect.colliderect(farmer.model, cell8.model):
        farmer.score += 1
        farmer.model.x = W / 2
        farmer.model.y = H / 2
        cell8.count_cash += 1


def reset_score():
    farmer.score = 0


def draw_and_update():
    backbuffer.fill((255, 255, 255))
    screen.fill((0, 0, 0))
    # timer.tick(64)

    farmer.draw(backbuffer)
    farmer.update()

    cell1.draw(backbuffer)
    cell1.update()
    cell2.draw(backbuffer)
    cell2.update()
    cell3.draw(backbuffer)
    cell3.update()
    cell4.draw(backbuffer)
    cell4.update()
    cell5.draw(backbuffer)
    cell5.update()
    cell6.draw(backbuffer)
    cell6.update()
    cell7.draw(backbuffer)
    cell7.update()
    cell8.draw(backbuffer)
    cell8.update()

    print_text(0, 300, "count: " + str(farmer.score))
    print_text(0, 320, "cell1: " + str(cell1.count_cash))
    print_text(0, 340, "cell2: " + str(cell2.count_cash))
    print_text(0, 360, "cell3: " + str(cell3.count_cash))
    print_text(0, 380, "cell4: " + str(cell4.count_cash))
    print_text(100, 300, "cell5: " + str(cell5.count_cash))
    print_text(100, 320, "cell6: " + str(cell6.count_cash))
    print_text(100, 340, "cell7: " + str(cell7.count_cash))
    print_text(100, 360, "cell8: " + str(cell8.count_cash))

    screen.blit(backbuffer, (0, 0))

    pygame.display.update()


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
resize = T.Compose([T.ToPILImage(),
                    T.Resize(200, interpolation=Image.CUBIC),
                    T.ToTensor()])


def get_image():
    image = pygame.surfarray.array3d(backbuffer)

    image = resize(image).unsqueeze(0).to(device)

    return image


def plt_img(img):
    plt.imshow(img.cpu().squeeze(0).permute(2, 1, 0).numpy(),
               interpolation='none')
    plt.title('Example extracted screen')
    plt.show()


def set_cash(count):
    c1.append(cell1.count_cash)
    c2.append(cell2.count_cash)
    c3.append(cell3.count_cash)
    c4.append(cell4.count_cash)
    c5.append(cell5.count_cash)
    c6.append(cell6.count_cash)
    c7.append(cell7.count_cash)
    c8.append(cell8.count_cash)
    c.append(count)

    cell1.count_cash = cell2.count_cash = cell3.count_cash = cell4.count_cash = cell5.count_cash = cell6.count_cash = cell7.count_cash = cell8.count_cash = 0


def plt_cash():
    Tools.plot(c, c1, c2, c3, c4, c5, c6, c7, c8)
    c1.clear()
    c2.clear()
    c3.clear()
    c4.clear()
    c5.clear()
    c6.clear()
    c7.clear()
    c8.clear()
    c.clear()