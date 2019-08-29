import pygame
import math

class Graph:

    def __init__(self, screen, FPGAReader, demoScreen, absolutePos):
        self.screen = screen
        self.FPGAReader = FPGAReader
        self.demoScreen = demoScreen
        self.absolutePos = absolutePos
        self.counter = 0
        self.CSC = 0
        self.L = 50
        self.H = 150
        self.LDrag = False
        self.HDrag = False
        self.prevPos = 0
        self.LFirst = True

    #Colors:
    BorderColor = (0, 64, 122)
    GraphColor = (38, 141, 174)
    white = (255, 255, 255)
    black = (0, 0, 0)
    orange = (229, 177, 102)
    LColor = (88, 214, 141)
    HColor = (236, 112, 99)
    LHTextColor = (255, 255, 255)

    #Positions and sizes:
    BorderWidth = 3
    GraphHeight = 100
    BotImageMarg = 25
    LeftImageMarg = 45
    TopBorder = 60
    GraphWidth = 290
    AxisThickness = 1
    TickLength = 5
    labelSize = 10
    labelSkew = 4
    HTPVerticalUnit = 23
    HVerticalUnit = 10
    CSCCursorWidth = 5
    LHThickness = 4
    LHWidth = 40
    LHHeight = 40
    LHTextSize = 20

    #Others:
    DeltaTicks = [600, 500, 400, 300, 200, 100, 90, 80, 70, 60, 50, 40, 30, 20]
    DeltaLabels = [200, 100, 60, 40, 20]
    CSCRefresh = 30
    LHMax = 200

    def Render(self):
        self.screen.fill(self.white)
        pygame.draw.rect(self.screen, self.GraphColor, pygame.Rect(0,0,self.screen.get_width(),self.TopBorder))
        #Draw borders:
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,self.screen.get_height()-self.BorderWidth,self.screen.get_width(),self.BorderWidth))
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(self.screen.get_width()-self.BorderWidth,self.TopBorder,self.BorderWidth,self.screen.get_height()-self.BorderWidth-self.TopBorder))
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,self.TopBorder,self.BorderWidth,self.screen.get_height()-self.BorderWidth-self.TopBorder))
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(self.BorderWidth,self.TopBorder,self.screen.get_width()-2*self.BorderWidth,self.BorderWidth))
        #Background graph:
        self.screen.blit(self.demoScreen.setImageHeight(self.demoScreen.getImage('Images/HTP.png'), self.GraphHeight), (self.LeftImageMarg,self.screen.get_height()-self.BotImageMarg-self.GraphHeight))
        self.screen.blit(self.demoScreen.setImageHeight(self.demoScreen.getImage('Images/H.png'), self.GraphHeight), (self.LeftImageMarg, self.BotImageMarg+self.TopBorder))
        #Graph axis:
        pygame.draw.rect(self.screen, self.black, pygame.Rect(self.LeftImageMarg,self.screen.get_height()-self.BotImageMarg,self.GraphWidth,self.AxisThickness))
        pygame.draw.rect(self.screen, self.black, pygame.Rect(self.LeftImageMarg,self.BotImageMarg+self.TopBorder,self.AxisThickness,self.screen.get_height()-self.BotImageMarg-(self.BotImageMarg+self.TopBorder)))
        pygame.draw.rect(self.screen, self.black, pygame.Rect(self.LeftImageMarg,self.BotImageMarg+self.TopBorder-1,self.GraphWidth,self.AxisThickness))
        pygame.draw.rect(self.screen, self.black, pygame.Rect(self.LeftImageMarg,self.screen.get_height()-self.BotImageMarg-self.GraphHeight,self.GraphWidth,self.AxisThickness))
        #Graph labels:
        for i in range(11):
            pygame.draw.rect(self.screen, self.black, pygame.Rect(int(self.LeftImageMarg+self.GraphWidth/10*i+0.5),self.BotImageMarg+self.TopBorder-1,self.AxisThickness, self.TickLength))
            labelText = self.demoScreen.createText(str(i*20), self.demoScreen.preferedFonts, self.labelSize, self.black)
            self.screen.blit(labelText, (int(self.LeftImageMarg+self.GraphWidth/10*i-labelText.get_width()/2+0.5),self.BotImageMarg+self.TopBorder-1-labelText.get_height()))
        CSCLabel = self.demoScreen.createText('CSCnt [-]', self.demoScreen.preferedFonts, self.labelSize, self.black)
        self.screen.blit(CSCLabel, (int(self.LeftImageMarg+self.GraphWidth/2+0.5),self.BotImageMarg+self.TopBorder-1-labelText.get_height()-CSCLabel.get_height()+self.labelSkew))
        for i in range(len(self.DeltaTicks)):
            x = int(self.LeftImageMarg + 3.79/self.DeltaTicks[i]*1000/200*290+0.5)
            y = self.screen.get_height()-self.BotImageMarg-self.TickLength
            pygame.draw.rect(self.screen, self.black, pygame.Rect(x,y,self.AxisThickness,self.TickLength))
            if (self.DeltaTicks[i] in self.DeltaLabels):
                labelText = self.demoScreen.createText(str(self.DeltaTicks[i]), self.demoScreen.preferedFonts, self.labelSize, self.black)
                self.screen.blit(labelText, (int(x-labelText.get_width()/2+0.5),y+self.TickLength))
        DeltaLabel = self.demoScreen.createText('Delta [ps]', self.demoScreen.preferedFonts, self.labelSize, self.black)
        self.screen.blit(DeltaLabel, (int(self.LeftImageMarg+self.GraphWidth/2+0.5),y+self.TickLength+labelText.get_height()-self.labelSkew))
        for i in range(5):
            x = self.LeftImageMarg
            y = self.screen.get_height()-self.BotImageMarg-self.HTPVerticalUnit*i
            pygame.draw.rect(self.screen, self.black, pygame.Rect(x,y,self.TickLength,self.AxisThickness))
            labelText = self.demoScreen.createText(str(i), self.demoScreen.preferedFonts, self.labelSize, self.black)
            self.screen.blit(labelText, (x-labelText.get_width(),int(y-labelText.get_height()/2+0.5)))
        HTPLabel = self.demoScreen.createText('HTP [Mbit/s]', self.demoScreen.preferedFonts, self.labelSize, self.black)
        self.screen.blit(pygame.transform.rotate(HTPLabel,90),(x-labelText.get_width()-HTPLabel.get_height(),int(self.screen.get_height()-self.BotImageMarg-self.GraphHeight/2-HTPLabel.get_width()/2+0.5)))
        for i in range(6):
            y = self.BotImageMarg+self.TopBorder+self.GraphHeight-self.HVerticalUnit*i*2
            pygame.draw.rect(self.screen, self.black, pygame.Rect(x,y,self.TickLength,self.AxisThickness))
            labelText = self.demoScreen.createText(str(i/5), self.demoScreen.preferedFonts, self.labelSize, self.black)
            self.screen.blit(labelText, (x-labelText.get_width(),int(y-labelText.get_height()/2+0.5)))
        HLabel = self.demoScreen.createText('Min-entropy [bit/bit]', self.demoScreen.preferedFonts, self.labelSize, self.black)
        self.screen.blit(pygame.transform.rotate(HLabel,90), (x-labelText.get_width()-HTPLabel.get_height(),int(self.BotImageMarg+self.TopBorder+self.GraphHeight/2-HLabel.get_width()/2+0.5)))
        #CSCnt cursor:
        if (self.counter == 0):
            data = self.FPGAReader.getLiveData()
            if (not(math.isnan(data[0]))):
                self.CSC = data[0]
        elif (self.counter == self.CSCRefresh-1):
            self.counter = -1
        self.counter += 1
        pygame.draw.rect(self.screen, self.orange, pygame.Rect(int(self.LeftImageMarg+self.CSC/200*self.GraphWidth-self.CSCCursorWidth/2+0.5),self.BotImageMarg+self.TopBorder,self.CSCCursorWidth,self.screen.get_height()-self.BotImageMarg-(self.BotImageMarg+self.TopBorder)))
        #LH:
        self.__drawLH()

    def ProcessInput(self, events, keys):
        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (event.button == 1):
                    mousePos = pygame.mouse.get_pos()
                    self.__handleMouseDown(mousePos)
            if (event.type == pygame.MOUSEBUTTONUP):
                if (event.button == 1):
                    self.__handleMouseUp()
            if (event.type == pygame.MOUSEMOTION):
                mousePos = pygame.mouse.get_pos()
                self.__handleMouseMotion(mousePos)

    def __handleMouseDown(self, pos):
        x = pos[0] - self.absolutePos[0]
        y = pos[1] - self.absolutePos[1]
        if ((x < 0) | (x > self.screen.get_width())):
            return
        if ((y < 0) | (y > self.screen.get_height())):
            return
        x1L = int(self.LeftImageMarg+self.L/200*self.GraphWidth-self.LHWidth/2+0.5)
        x2L = x1L + self.LHWidth
        x1H = int(self.LeftImageMarg+self.H/200*self.GraphWidth-self.LHWidth/2+0.5)
        x2H = x1H + self.LHWidth
        y1 = 0
        y2 = self.LHHeight
        if (not(self.LFirst)):
            if ((x >= x1L) & (x <= x2L) & (y >= y1) & (y <= y2)):
                self.LDrag = True
                self.prevPos = int(self.LeftImageMarg+self.L/200*self.GraphWidth+0.5)-x
                self.LFirst = False
                return
        if ((x >= x1H) & (x <= x2H) & (y >= y1) & (y <= y2)):
            self.HDrag = True
            self.prevPos = int(self.LeftImageMarg+self.H/200*self.GraphWidth+0.5)-x
            self.LFirst = True
            return
        if (self.LFirst):
            if ((x >= x1L) & (x <= x2L) & (y >= y1) & (y <= y2)):
                self.LDrag = True
                self.prevPos = int(self.LeftImageMarg+self.L/200*self.GraphWidth+0.5)-x
                self.LFirst = False
                return

    def __handleMouseUp(self):
        self.LDrag = False
        self.HDrag = False

    def __handleMouseMotion(self, pos):
        x = pos[0] - self.absolutePos[0]
        if (self.LDrag):
            newL = x + self.prevPos
            newL = int((newL-self.LeftImageMarg)*200/self.GraphWidth+0.5)
            if ((newL >= 0) & (newL <= self.LHMax) & (newL <= self.H)):
                self.L = newL
                return
        if (self.HDrag):
            newH = x + self.prevPos
            newH = int((newH-self.LeftImageMarg)*200/self.GraphWidth+0.5)
            if ((newH >= 0) & (newH <= self.LHMax) & (newH >= self.L)):
                self.H = newH

    def __drawLH(self):
        if (self.LFirst):
            pygame.draw.rect(self.screen, self.LColor, pygame.Rect(int(self.LeftImageMarg+self.L/200*self.GraphWidth-self.LHThickness/2+0.5),0,self.LHThickness,self.screen.get_height()-self.BotImageMarg))
            pygame.draw.rect(self.screen, self.LColor, pygame.Rect(int(self.LeftImageMarg+self.L/200*self.GraphWidth-self.LHWidth/2+0.5),0,self.LHWidth,self.LHHeight))
            LText = self.demoScreen.createText(str(self.L), self.demoScreen.preferedFonts, self.LHTextSize, self.LHTextColor)
            self.screen.blit(LText, (int(self.LeftImageMarg+self.L/200*self.GraphWidth-LText.get_width()/2+0.5),int(self.LHHeight/2-LText.get_height()/2+0.5)))
        pygame.draw.rect(self.screen, self.HColor, pygame.Rect(int(self.LeftImageMarg+self.H/200*self.GraphWidth-self.LHThickness/2+0.5),0,self.LHThickness,self.screen.get_height()-self.BotImageMarg))
        pygame.draw.rect(self.screen, self.HColor, pygame.Rect(int(self.LeftImageMarg+self.H/200*self.GraphWidth-self.LHWidth/2+0.5),0,self.LHWidth,self.LHHeight))
        HText = self.demoScreen.createText(str(self.H), self.demoScreen.preferedFonts, self.LHTextSize, self.LHTextColor)
        self.screen.blit(HText, (int(self.LeftImageMarg+self.H/200*self.GraphWidth-HText.get_width()/2+0.5),int(self.LHHeight/2-HText.get_height()/2+0.5)))
        if (not(self.LFirst)):
            pygame.draw.rect(self.screen, self.LColor, pygame.Rect(int(self.LeftImageMarg+self.L/200*self.GraphWidth-self.LHThickness/2+0.5),0,self.LHThickness,self.screen.get_height()-self.BotImageMarg))
            pygame.draw.rect(self.screen, self.LColor, pygame.Rect(int(self.LeftImageMarg+self.L/200*self.GraphWidth-self.LHWidth/2+0.5),0,self.LHWidth,self.LHHeight))
            LText = self.demoScreen.createText(str(self.L), self.demoScreen.preferedFonts, self.LHTextSize, self.LHTextColor)
            self.screen.blit(LText, (int(self.LeftImageMarg+self.L/200*self.GraphWidth-LText.get_width()/2+0.5),int(self.LHHeight/2-LText.get_height()/2+0.5)))

    def __drawHTP(self):
        height = int(self.GraphHeight/2+0.5)
        for i in range(self.screen.get_width()):
            x = i/self.screen.get_width()
            y = 490.1*x**9-2838.2*x**8+6886.2*x**7-9053.3*x**6+6947.7*x**5-3115.2*x**4+775.6*x**3-102.1*x**2+9.5*x
            y = self.screen.get_height()-y*height
            x = i
            pygame.draw.rect(self.screen, self.GraphColor, pygame.Rect(x,y,1,1))
