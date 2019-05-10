import pygame

class BoundButton:

    def __init__(self, screen, FPGAReader, demoScreen):
        self.screen = screen
        self.FPGAReader = FPGAReader
        self.demoScreen = demoScreen
        self.active = False

    #Colors:
    white = (255, 255, 255)
    BorderColor = (0, 64, 122)
    ButtonBack = (83, 191, 238)
    LabelColor = (0, 64, 122)
    ActiveBack = (229, 177, 102)

    #Positions and sizes:
    BorderWidth = 3
    LabelSize = 17

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
        x = pos[0] - self.demoScreen.BoundButPos[0]
        y = pos[1] - self.demoScreen.BoundButPos[1]
        if ((x < 0) | (x > self.screen.get_width())):
            return
        if ((y < 0) | (y > self.screen.get_height())):
            return
        self.active = True
        self.__setBounds()

    def __handleMouseUp(self):
        self.active = False

    def __setBounds(self):
        L = self.demoScreen.graph.L
        H = self.demoScreen.graph.H
        self.FPGAReader.sendBounds(H,L)
        self.FPGAReader.initBuffers()
        self.demoScreen.randScreen.reset()

    def Render(self):
        if (not(self.active)):
            self.screen.fill(self.ButtonBack)
        else:
            self.screen.fill(self.ActiveBack)
        #Borders:
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,0,self.screen.get_width(),self.BorderWidth))
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,0,self.BorderWidth,self.screen.get_height()))
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(self.screen.get_width()-self.BorderWidth,0,self.BorderWidth,self.screen.get_height()))
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,self.screen.get_height()-self.BorderWidth,self.screen.get_width(),self.BorderWidth))
        #Text:
        labelText = self.demoScreen.createText('Set Bounds', self.demoScreen.preferedFonts, self.LabelSize, self.LabelColor)
        self.screen.blit(labelText, (int(self.screen.get_width()/2-labelText.get_width()/2+0.5),int(self.screen.get_height()/2-labelText.get_height()/2+0.5)))
        
