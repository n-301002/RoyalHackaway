import pygame
import spriteSheet

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Sprites")

clock = pygame.time.Clock()
FPS = 60

sprite_sheet_image = pygame.image.load('Images/blueDino.png').convert_alpha()
sprite_sheet = spriteSheet.SpriteSheet(sprite_sheet_image)

clock = pygame.time.Clock()
FPS = 60

BG = (159, 226, 191) #seafoam
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Player():
    def __init__(self, x, y):
        self.image = sprite_sheet.get_image(0, 24, 24, 5, BLACK)
        self.width = 24 * 3
        self.height = 24 * 3
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x , y)
        self.flip = False
        
    def move(self):
        
        change_x = 0
        change_y = 0
        
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 10
            self.flip = True
        if key[pygame.K_RIGHT]:
            self.rect.x += 10
            self.flip = False
        if key[pygame.K_UP]:
            self.rect.y -= 10
            if self.flip:
                self.flip = True
            else:
                self.flip = False
        if key[pygame.K_DOWN]:
            self.rect.y += 10
            if self.flip:
                self.flip = True
            else:
                self.flip = False
        
        if self.rect.left + change_x < 0:
            change_x = -self.rect.left
        if self.rect.right + change_x > SCREEN_WIDTH:
            change_x = SCREEN_WIDTH - self.rect.right
        
        if self.rect.top + change_y < 0:
            change_y = -self.rect.top
        if self.rect.bottom + change_y > SCREEN_HEIGHT:
            change_y = SCREEN_HEIGHT - self.rect.bottom
        
        self.rect.x += change_x
        self.rect.y += change_y
        
    
    def draw(self):
        img = pygame.transform.flip(self.image, self.flip, False)
        img.set_colorkey(BLACK)
        screen.blit(img, (self.rect.x - 24, self.rect.y - 24))
        
        
dino = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

run = True
while run:
    screen.fill(BG)
    
    clock.tick(FPS)
    
    dino.move()
    dino.draw()


    
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False     
    
    pygame.display.update()

pygame.quit()