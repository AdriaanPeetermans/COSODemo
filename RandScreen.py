import pygame
import time
import numpy

class RandScreen:

    def __init__(self, screen, FPGAReader, demoScreen):
        self.mode = 0
        self.counter = 0
        self.screen = screen
        self.FPGAReader = FPGAReader
        self.demoScreen = demoScreen
        self.__initRandomBitstreamArray()
        self.__initHist()
        self.__initBias()
        self.__initCor()
        self.alpha = 0
        self.lockHist = [None]*len(self.demoScreen.lock.LockColors)
        self.lockBias = [None]*len(self.demoScreen.lock.LockColors)
        self.lockCor = [None]*len(self.demoScreen.lock.LockColors)

    numberModes = 4

    #Colors:
    BorderColor = (0, 64, 122)
    white = (255, 255, 255)
    black = (0, 0, 0)
    orange = (229, 177, 102)

    #Positions and sizes:
    BorderWidth = 3

    #Mode 0 (Random bitstreaam):
    numberPixelsLine = 25 #     Number of pixels in each line, should be a devider of screen height
    pixelSpeed = 20 #           Frames per pixel

    #Mode 1 (Histogram):
    blockSize = 100 #           Number of new samples to use when a new histogram is drawn
    redrawSpeed = 5 #           Number of frames before a new histogram is drawn
    boundThick = 6 #            Thickness of ideal hist value bound
    averageCells = 8 #          Number of histogram cells that are averaged togehter in the visualisation

    #Mode 2 (Bias):
    biasBlockSize = 100 #       Number of bytes used per bias prediction
    biasRedrawSpeed = 5 #       Number of frames before a new block is added
    biasBins = 100 #            Number of bins for bias histogram

    #Mode 3 (Correlation):
    corBlockSize = 100 #        Number of bytes used per correlation prediction
    corRedrawSpeed = 5 #        Number of frames before a new block is added
    corBins = 100 #             Number of bins for correlation histogram

    def Render(self):
        if (self.mode == 0):
            #Random bitstream
            self.__renderRandomBitstreamArray()
        elif (self.mode == 1):
            #Histogram
            self.__renderHist()
        elif (self.mode == 2):
            #Bias
            self.__renderBias()
        else:
            #Corelation
            self.__renderCor()
        self.counter += 1
        self.__drawBorders()

    def __drawBorders(self):
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,self.screen.get_height()-self.BorderWidth,self.screen.get_width(),self.BorderWidth))
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(self.screen.get_width()-self.BorderWidth,0,self.BorderWidth,self.screen.get_height()-self.BorderWidth))
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,0,self.BorderWidth,self.screen.get_height()-self.BorderWidth))
        pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(self.BorderWidth,0,self.screen.get_width()-2*self.BorderWidth,self.BorderWidth))

    def __renderRandomBitstreamArray(self):
        shift = -self.randomBitstreamPixelSize + int(self.randomBitstreamPixelSize*self.counter/self.pixelSpeed+0.5)
        if (self.counter == 0):
            self.helperScreen = pygame.Surface((self.randomBitstreamPixelSize*self.randomBitstreamArrayWidth, self.screen.get_height()))
            posX = 0
            posY = 0
            for i in range(self.randomBitstreamArrayWidth):
                for j in range(self.numberPixelsLine):
                    self.__drawRandomPixel(posX, posY, self.randomBitstreamArray[i][j])
                    posY += self.randomBitstreamPixelSize
                posX += self.randomBitstreamPixelSize
                posY = 0
        self.screen.blit(self.helperScreen, (shift,0))
        if (self.counter == self.pixelSpeed-1):
            self.counter = -1
            self.randomBitstreamArray = [self.FPGAReader.popRands(self.numberPixelsLine)] + self.randomBitstreamArray[0:-1]

    def __renderHist(self):
        if (self.counter == 0):
            self.__addToHist()
            self.__drawHist(self.screen, self.black, self.hist, True, True)
            for i in range(len(self.demoScreen.lock.LockColors)):
                if (self.lockHist[i] != None):
                    screen = pygame.Surface((self.screen.get_width(),self.screen.get_height()))
                    screen.set_alpha(self.alpha)
                    self.__drawHist(screen, self.demoScreen.lock.LockColors[i], self.lockHist[i], False, True)
                    self.screen.blit(screen, (0,0))
        elif (self.counter == self.redrawSpeed-1):
            self.counter = -1

    def __renderBias(self):
        if (self.counter == 0):
            self.__addBias()
            self.__drawBias(self.screen, self.black, self.biasHist, True, True)
            for i in range(len(self.demoScreen.lock.LockColors)):
                if (self.lockBias[i] != None):
                    screen = pygame.Surface((self.screen.get_width(),self.screen.get_height()))
                    screen.set_alpha(self.alpha)
                    self.__drawBias(screen, self.demoScreen.lock.LockColors[i], self.lockBias[i], False, True)
                    self.screen.blit(screen, (0,0))
        elif (self.counter == self.biasRedrawSpeed-1):
            self.counter = -1

    def __renderCor(self):
        if (self.counter == 0):
            self.__addCor()
            self.__drawCor(self.screen, self.black, self.corHist, True, True)
            for i in range(len(self.demoScreen.lock.LockColors)):
                if (self.lockCor[i] != None):
                    screen = pygame.Surface((self.screen.get_width(),self.screen.get_height()))
                    screen.set_alpha(self.alpha)
                    self.__drawBias(screen, self.demoScreen.lock.LockColors[i], self.lockCor[i], False, True)
                    self.screen.blit(screen, (0,0))
        elif (self.counter == self.corRedrawSpeed-1):
            self.counter = -1

    #Helpers:
    def __initRandomBitstreamArray(self):
        self.randomBitstreamPixelSize = int(self.screen.get_height()/self.numberPixelsLine)
        self.randomBitstreamArrayWidth = int(self.screen.get_width()/self.randomBitstreamPixelSize)+1
        self.randomBitstreamArray = []
        #Wait for bits from FPGA (FPGA reader should do this).
        #time.sleep(1)
        bits = self.FPGAReader.popRands(self.numberPixelsLine*self.randomBitstreamArrayWidth)
        for i in range(self.randomBitstreamArrayWidth):
            self.randomBitstreamArray += [bits[self.numberPixelsLine*i:self.numberPixelsLine*(i+1)]]

    def __drawRandomPixel(self, posX, posY, bit):
        #print(posX)
        if (bit == 1):
            pygame.draw.rect(self.helperScreen, self.white, pygame.Rect(posX, posY, self.randomBitstreamPixelSize, self.randomBitstreamPixelSize))
        else:
            pygame.draw.rect(self.helperScreen, self.black, pygame.Rect(posX, posY, self.randomBitstreamPixelSize, self.randomBitstreamPixelSize))

    def __initHist(self):
        self.hist = [0]*256
        self.numberHistBlocks = 1
        self.histBarWidth = self.screen.get_width()/256
        bs = self.FPGAReader.popBytes(self.blockSize)
        for i in range(self.blockSize):
            self.hist[bs[i]] += 1
        for i in range(256):
            self.hist[i] /= self.blockSize

    def __addToHist(self):
        scaledHist = self.hist
        for i in range(256):
            scaledHist[i] *= (self.numberHistBlocks*self.blockSize)
        bs = self.FPGAReader.popBytes(self.blockSize)
        for i in range(self.blockSize):
            scaledHist[bs[i]] += 1
        self.numberHistBlocks += 1
        for i in range (256):
            self.hist[i] = scaledHist[i] / (self.numberHistBlocks*self.blockSize)

    def __drawHist(self, screen, color, hist, drawBar, fill):
        if (fill):
            screen.fill(self.white)
        if (drawBar):
            pygame.draw.rect(screen, self.orange, pygame.Rect(0,int(screen.get_height()/2-self.boundThick/2+0.5),screen.get_width(),self.boundThick))
        for i in range(int(256/self.averageCells)):
            x1 = int(i*self.averageCells*self.histBarWidth+0.5)
            x2 = int((i+1)*self.averageCells*self.histBarWidth+0.5)
            h = int(numpy.mean(hist[i*self.averageCells:(i+1)*self.averageCells])*256/2*screen.get_height()+0.5)
            pygame.draw.rect(screen, color, pygame.Rect(x1,screen.get_height()-h,x2-x1,h))

    def __initBias(self):
        self.biasHist = [0]*self.biasBins
        self.numberBiasBlocks = 1
        self.biasBarWidth = self.screen.get_width()/self.biasBins
        bs = self.FPGAReader.popRands(self.biasBlockSize*8)
        e = sum(bs)/(self.biasBlockSize*8)
        self.biasHist[min(int(e*self.biasBins+0.5), self.biasBins-1)] += 1

    def __addBias(self):
        scaledHist = self.biasHist
        for i in range(self.biasBins):
            scaledHist[i] *= self.numberBiasBlocks
        bs = self.FPGAReader.popRands(self.biasBlockSize*8)
        e = sum(bs)/(self.biasBlockSize*8)
        scaledHist[min(int(e*self.biasBins+0.5), self.biasBins-1)] += 1
        self.numberBiasBlocks += 1
        for i in range (self.biasBins):
            self.biasHist[i] = scaledHist[i] / self.numberBiasBlocks

    def __drawBias(self, screen, color, hist, drawBar, fill):
        if (fill):
            screen.fill(self.white)
        if (drawBar):
            pygame.draw.rect(screen, self.orange, pygame.Rect(int(screen.get_width()/2-self.boundThick/2+0.5),0,self.boundThick,screen.get_height()))
        for i in range(self.biasBins):
            x1 = int(i*self.biasBarWidth+0.5)
            x2 = int((i+1)*self.biasBarWidth+0.5)
            h = int(hist[i]*screen.get_height()*5+0.5)
            pygame.draw.rect(screen, color, pygame.Rect(x1,screen.get_height()-h,x2-x1,h))

    def __initCor(self):
        self.corHist = [0]*self.corBins
        self.numberCorBlocks = 1
        self.corBarWidth = self.screen.get_width()/self.corBins
        bs = self.FPGAReader.popRands(self.corBlockSize*8)
        e = 0
        for i in range(self.corBlockSize):
            e += self.__getCor(bs[i*8:i*8+8])
        e /= self.corBlockSize
        self.corHist[min(int(e*self.corBins+0.5), self.corBins-1)] += 1

    def __addCor(self):
        scaledHist = self.corHist
        for i in range(self.corBins):
            scaledHist[i] *= self.numberCorBlocks
        bs = self.FPGAReader.popRands(self.corBlockSize*8)
        e = 0
        for i in range(self.corBlockSize):
            e += self.__getCor(bs[i*8:i*8+8])
        e /= self.corBlockSize
        scaledHist[min(int(e*self.corBins+0.5), self.corBins-1)] += 1
        self.numberCorBlocks += 1
        for i in range (self.corBins):
            self.corHist[i] = scaledHist[i] / self.numberCorBlocks

    def __drawCor(self, screen, color, hist, drawBar, fill):
        if (fill):
            screen.fill(self.white)
        if (drawBar):
            pygame.draw.rect(screen, self.orange, pygame.Rect(int(screen.get_width()/2-self.boundThick/2+0.5),0,self.boundThick,screen.get_height()))
        for i in range(self.corBins):
            x1 = int(i*self.corBarWidth+0.5)
            x2 = int((i+1)*self.corBarWidth+0.5)
            h = int(hist[i]*screen.get_height()*5+0.5)
            pygame.draw.rect(screen, color, pygame.Rect(x1,screen.get_height()-h,x2-x1,h))

    @staticmethod
    def __getCor(bits):
        s = 0
        for i in range(7):
            if (bits[i] != bits[i+1]):
                s += 1
        s /= 7
        return s

    def reset(self):
        self.counter = 0
        self.__initRandomBitstreamArray()
        self.__initHist()
        self.__initBias()
        self.__initCor()

    def lock(self, lockPos):
        if (self.lockHist[lockPos] == None):
            self.lockHist[lockPos] = self.hist.copy()
            self.lockBias[lockPos] = self.biasHist.copy()
            self.lockCor[lockPos] = self.corHist.copy()
        else:
            self.lockHist[lockPos] = None
            self.lockBias[lockPos] = None
            self.lockCor[lockPos] = None
        cnt = 0
        for i in range(len(self.lockHist)):
            if (self.lockHist[i] != None):
                cnt += 1
        self.alpha = int(256/(cnt+1)+0.5)
