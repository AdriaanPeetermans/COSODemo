import DemoEngine
import RandScreen
import RandScreenButtons
import LiveData
import Graph
import BoundButton
import Lock
import RS
import Light
import pygame
import os

class DemoScreen(DemoEngine.SceneBase):

    def __init__(self, FPGAReader):
        DemoEngine.SceneBase.__init__(self, 800, 480)
        #Lock colors:
        lockScreen = pygame.Surface(self.LockSize)
        self.lock = Lock.Lock(lockScreen, self)
        #Random bits:
        rand = pygame.Surface(self.RandomBitsSize)
        self.randScreen = RandScreen.RandScreen(rand, FPGAReader, self)
        randT = pygame.Surface(self.RandomTitleSize)
        self.randTitle = RandScreenButtons.RandScreenButtons(randT, self.randScreen, self, self.RandomTitlePos)
        #Live data:
        liveScreen = pygame.Surface(self.LiveSize)
        self.liveData = LiveData.LiveData(liveScreen, FPGAReader, self)
        #Graph:
        graphScreen = pygame.Surface(self.GraphSize)
        self.graph = Graph.Graph(graphScreen, FPGAReader, self, self.GraphPos)
        #Bounds button:
        boundScreen = pygame.Surface(self.BoundButSize)
        self.boundButton = BoundButton.BoundButton(boundScreen, FPGAReader, self)
        #ROSel:
        RSScreen = pygame.Surface(self.RSSize)
        self.RS = RS.RS(RSScreen, FPGAReader, self)
        #Lock light:
        lockLightScreen = pygame.Surface(self.LockLightSize)
        self.lockLight = Light.Light(lockLightScreen, 'Lock', FPGAReader.getLock, self)
        #Not found light:
        nfLightScreen = pygame.Surface(self.NFLightSize)
        f = lambda: not(FPGAReader.getFound())
        self.nfLight = Light.Light(nfLightScreen, 'Found', f, self)
        #FPGA reader:
        self.FPGAReader = FPGAReader
    
    #Colors:
    KulBlue = (38, 141, 174)
    KulDarkBlue = (0, 64, 122)
    KulWhite = (255, 255, 255)

    #Positions and sizes:
    KulLogoPos = (20, 20)
    KulLogoHeight = 40
    CosicLogoPos = (700, 0)
    CosicLogoHeight = 100
    KulTopBandWidth = 40
    TitleSize = 30
    RandomTitlePos = (20, 105)
    RandomTitleSize = (200, 50)
    RandomBitsPos = (20,165)
    RandomBitsSize = (200,250)
    LivePos = (650, 165)
    LiveSize = (130, 250)
    GraphPos = (260, 105)
    GraphSize = (350, 310)
    BoundButPos = (260, 432)
    BoundButSize = (100, 30)
    LockPos = (20, 432)
    LockSize = (200, 30)
    RSPos = (580, 432)
    RSSize = (200, 30)
    LockLightPos = (380, 432)
    LockLightSize = (80, 30)
    NFLightPos = (480, 432)
    NFLightSize = (80, 30)

    #Fonts:
    preferedFonts = ['Arial']

    def ProcessInput(self, events, pressed_keys):
        self.randTitle.ProcessInput(events, pressed_keys)
        self.graph.ProcessInput(events, pressed_keys)
        self.boundButton.ProcessInput(events, pressed_keys)
        self.lock.ProcessInput(events, pressed_keys)

    def Update(self):
        pass

    def Render(self, screen):
        screen.fill(self.KulBlue)
        pygame.draw.rect(screen, self.KulWhite, pygame.Rect(0, 0, screen.get_width(), self.KulTopBandWidth))
        #Draw KUL and COSIC logos:
        screen.blit(self.setImageHeight(self.getImage('Images/KulLogo.png'), self.KulLogoHeight), self.KulLogoPos)
        screen.blit(self.setImageHeight(self.getImage('Images/CosicLogo.png'), self.CosicLogoHeight), self.CosicLogoPos)
        #Title:
        titleText = self.createText('COSO TRNG Demo', self.preferedFonts, self.TitleSize, self.KulDarkBlue)
        screen.blit(titleText, (screen.get_width()/2-titleText.get_width()/2, self.KulTopBandWidth/2-titleText.get_height()/2))
        #Random bits:
        pygame.draw.rect(screen, self.KulWhite, pygame.Rect(self.RandomTitlePos[0], self.RandomTitlePos[1], self.RandomTitleSize[0], self.RandomTitleSize[1])) 
        pygame.draw.rect(screen, self.KulWhite, pygame.Rect(self.RandomBitsPos[0], self.RandomBitsPos[1], self.RandomBitsSize[0], self.RandomBitsSize[1]))
        self.randScreen.Render()
        self.randTitle.Render()
        screen.blit(self.randScreen.screen, self.RandomBitsPos)
        screen.blit(self.randTitle.screen, self.RandomTitlePos)
        #LiveData:
        self.liveData.Render()
        screen.blit(self.liveData.screen, self.LivePos)
        #Graph:
        self.graph.Render()
        screen.blit(self.graph.screen, self.GraphPos)
        #Bound button:
        self.boundButton.Render()
        screen.blit(self.boundButton.screen, self.BoundButPos)
        #Lock colors:
        self.lock.Render()
        screen.blit(self.lock.screen, self.LockPos)
        #ROSel:
        self.RS.Render()
        screen.blit(self.RS.screen, self.RSPos)
        #Lights:
        self.lockLight.Render()
        screen.blit(self.lockLight.screen, self.LockLightPos)
        self.nfLight.Render()
        screen.blit(self.nfLight.screen, self.NFLightPos)
        
    #Helpers:
    __imageLibrary = {}

    def getImage(self, path):
        image = self.__imageLibrary.get(path)
        if (image == None):
                canonicalizedPath = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalizedPath)
                self.__imageLibrary[path] = image
        return image

    @staticmethod
    def setImageHeight(image, height):
        rect = image.get_rect()
        ratio = rect.width/rect.height
        image = pygame.transform.scale(image, (int(height*ratio+0.5), height))
        return image

    @staticmethod
    def __makeFont(fonts, size):
        available = pygame.font.get_fonts()
        choices = map(lambda x:x.lower().replace(' ', ''), fonts)
        for choice in choices:
            if choice in available:
                return pygame.font.SysFont(choice, size)
        return pygame.font.Font(None, size)
    
    __cachedFonts = {}
    
    def __getFont(self, fontPreferences, size):
        key = str(fontPreferences) + '|' + str(size)
        font = self.__cachedFonts.get(key, None)
        if font == None:
            font = self.__makeFont(fontPreferences, size)
            self.__cachedFonts[key] = font
        return font

    __cachedText = {}
    
    def createText(self, text, fonts, size, color):
        key = '|'.join(map(str, (fonts, size, color, text)))
        image = self.__cachedText.get(key, None)
        if image == None:
            font = self.__getFont(fonts, size)
            image = font.render(text, True, color)
            self.__cachedText[key] = image
        return image
