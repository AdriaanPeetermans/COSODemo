import pygame

class Lock:

    def __init__(self, screen, demoScreen):
        self.screen = screen
        self.demoScreen = demoScreen
        self.ColorWidth = self.screen.get_width()/len(self.LockColors)

    #Colors:
    BorderColor = (0, 64, 122)
    LockColors = [(175, 122, 197), (93, 173, 226), (88, 214, 141), (244, 208, 63), (235, 152, 78), (231, 76, 60)]

    #Positions and sizes:
    BorderWidth = 3
    InternalBorderWidth = 2

    def ProcessInput(self, events, keys):
        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (event.button == 1):
                    mousePos = pygame.mouse.get_pos()
                    self.__handleMouseDown(mousePos)
            if (event.type == pygame.MOUSEBUTTONUP):
                if (event.button == 1):
                    self.__handleMouseUp()

    def __handleMouseDown(self, pos):
        x = pos[0] - self.demoScreen.LockPos[0]
        y = pos[1] - self.demoScreen.LockPos[1]
        if ((x < 0) | (x > self.screen.get_width())):
            return
        if ((y < 0) | (y > self.screen.get_height())):
            return
        for i in range(len(self.LockColors)):
            x1 = i*self.ColorWidth
            x2 = x1 + self.ColorWidth
            if ((x1 <= x) & (x < x2)):
                self.demoScreen.randScreen.lock(i)
                return

    def __handleMouseUp(self):
        pass

    def Render(self):
        #Colors:
        for i in range(len(self.LockColors)):
            pygame.draw.rect(self.screen, self.LockColors[i], pygame.Rect(int(i*self.ColorWidth+0.5),0,int(self.ColorWidth+0.5),self.screen.get_height()))
        #Borders:
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,0,self.screen.get_width(),self.BorderWidth))
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,0,self.BorderWidth,self.screen.get_height()))
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(self.screen.get_width()-self.BorderWidth,0,self.BorderWidth,self.screen.get_height()))
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,self.screen.get_height()-self.BorderWidth,self.screen.get_width(),self.BorderWidth))
        #Internal borders:
        for i in range(len(self.LockColors)-1):
            pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(int((i+1)*self.ColorWidth-self.InternalBorderWidth/2+0.5),0,self.InternalBorderWidth,self.screen.get_height()))
