import pygame

class RandScreenButtons:

    def __init__(self, screen, randScreen, demoScreen, absolutePos):
        self.mode = 0
        self.screen = screen
        self.randScreen = randScreen
        self.demoScreen = demoScreen
        self.iconWidth = int((self.screen.get_width() - 2*self.BorderWidth - 3*self.InternalBorderWidth)/4)
        self.iconHeight = self.screen.get_height() - 2*self.BorderWidth
        self.absolutePos = absolutePos

    #Colors:
    BorderColor = (0, 64, 122)
    ActiveColor = (229, 177, 102)
    NoActiveColor = (255, 255, 255)

    #Positions and sizes:
    BorderWidth = 3
    InternalBorderWidth = 2

    def ProcessInput(self, events, keys):
        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (event.button == 1):
                    mousePos = pygame.mouse.get_pos()
                    newMode = self.__getModePos(mousePos)
                    if (newMode >= 0):
                        self.mode = newMode
                        self.randScreen.mode = newMode
                        self.randScreen.counter = 0
                    

    def Render(self):
        #Draw borders:
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,self.screen.get_height()-self.BorderWidth,self.screen.get_width(),self.BorderWidth))
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(self.screen.get_width()-self.BorderWidth,0,self.BorderWidth,self.screen.get_height()-self.BorderWidth))
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,0,self.BorderWidth,self.screen.get_height()-self.BorderWidth))
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(self.BorderWidth,0,self.screen.get_width()-2*self.BorderWidth,self.BorderWidth))
        for i in range(3):
            pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(self.BorderWidth+(i+1)*self.iconWidth+i*self.InternalBorderWidth,self.BorderWidth,self.InternalBorderWidth,self.iconHeight))
        #Draw backgrounds:
        for i in range(4):
            if (i == self.mode):
                color = self.ActiveColor
            else:
                color = self.NoActiveColor
            pygame.draw.rect(self.screen, color, pygame.Rect(self.BorderWidth+i*(self.iconWidth+self.InternalBorderWidth),self.BorderWidth,self.iconWidth,self.iconHeight))
        #Draw icons:
        for i in range(4):
            self.screen.blit(self.demoScreen.setImageHeight(self.demoScreen.getImage('Images/RandMode'+str(i)+'.png'), self.iconHeight), (self.BorderWidth+i*(self.iconWidth+self.InternalBorderWidth),self.BorderWidth))

    def __getModePos(self, pos):
        x = pos[0] - self.absolutePos[0]
        y = pos[1] - self.absolutePos[1]
        if ((x < 0) | (x > self.screen.get_width())):
            return -1
        if ((y < 0) | (y > self.screen.get_height())):
            return -1
        for i in range(4):
            if (x < self.BorderWidth+(i+1)*self.iconWidth+self.InternalBorderWidth/2):
                return i
        return i
