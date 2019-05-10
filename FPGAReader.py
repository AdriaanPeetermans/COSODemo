import serial
import _thread
import time
import random
import numpy

class FPGAReader:

    def __init__(self, serialPort, baud, bufferSize):
        self.serialPort = serialPort
        self.baud = baud
        self.bufferSize = bufferSize
        self.initBuffers()
        self.mustStop = False
        self.overFlow = False
        self.averageRange = 100
        self.clkFreq = 100      #100 MHz FPGA clock frequency

    @classmethod
    def init(cls, pi):
        baud = 9600
        bSize = 2**10
        if (pi):
            return cls('/dev/ttyACM0', baud, bSize)
        else:
            return cls('/dev/cu.usbmodem141101', baud, bSize)

    def initBuffers(self):
        self.CSC = [0]*self.bufferSize
        self.RO0 = [0]*self.bufferSize
        self.RO1 = [0]*self.bufferSize
        self.CLK = [0]*self.bufferSize
        self.RO0Sel = [0]*self.bufferSize
        self.RO1Sel = [0]*self.bufferSize
        self.CTR = [0]*self.bufferSize
        self.RAND = [0]*(self.bufferSize*8)
        self.bufferIndex = 0

    def __run(self):
        while (True):
            self.__findNextSync()
            b = self.ser.read(4)
            self.CSC[self.bufferIndex] = b[0]*(2**24)+b[1]*(2**16)+b[2]*(2**8)+b[3]
            b = self.ser.read(4)
            self.RO0[self.bufferIndex] = b[0]*(2**24)+b[1]*(2**16)+b[2]*(2**8)+b[3]
            b = self.ser.read(4)
            self.RO1[self.bufferIndex] = b[0]*(2**24)+b[1]*(2**16)+b[2]*(2**8)+b[3]
            b = self.ser.read(4)
            self.CLK[self.bufferIndex] = b[0]*(2**24)+b[1]*(2**16)+b[2]*(2**8)+b[3]
            b = self.ser.read(2)
            self.RO0Sel[self.bufferIndex] = b[0]
            self.RO1Sel[self.bufferIndex] = b[1]
            b = self.ser.read(1)
            self.CTR[self.bufferIndex] = ord(b)
            b = self.ser.read(8)
            for i in range(8):
                self.RAND[self.bufferIndex*8+i] = b[i]
            self.bufferIndex += 1
            if (self.bufferIndex >= self.bufferSize):
                self.bufferIndex = 0
                self.overFlow = True
            if (self.mustStop):
                self.ser.close()
                return

    def __findNextSync(self):
        while (True):
            b = ord(self.ser.read(1))
            while (b == 170):
                b = ord(self.ser.read(1))
                if (b == 85):
                    return

    @staticmethod
    def __giveBytes(value, number):
        result = [0]*number
        if (value >= 256**number):
            value = value%(256**number)
        for i in range(number):
            if (value >= 256**(number-i-1)):
                result[i] = int(value/(256**(number-i-1)))
                value -= result[i]*(256**(number-i-1))
        return result

    @staticmethod
    def __byteToBits(b):
        result = [0]*8
        for i in range(8):
            if (b >= 2**(7-i)):
                result[i] = 1
                b -= 2**(7-i)
        return result           

    def start(self):
        self.mustStop = False
        self.ser = serial.Serial(self.serialPort, self.baud)
        _thread.start_new_thread(self.__run, ())

    def sendBounds(self, high, low):
        message = [170, 85] + self.__giveBytes(high, 4) + self.__giveBytes(low, 4)
        self.ser.write(message)

    def stop(self):
        self.mustStop = True

    #Returns the most recent 'size' bits
    def popRands(self, size):
##        result = []
##        for i in range(size):
##            result += [random.randint(0,1)]
##        return result
##        while ((size > self.bufferIndex) & (self.overFlow == False)):
##            pass
        numberBytes = int(size/8)+1
        result = []
        readPos = self.bufferIndex - 1
        for i in range(numberBytes):
            if (readPos < 0):
                readPos = self.bufferSize*8-1
            result += self.__byteToBits(self.RAND[readPos])
            readPos -= 1
        result = result[0:size]
        return result

    def popBytes(self, size):
##        result = []
##        for i in range(size):
##            result += [random.randint(0,255)]
##        return result
##        while ((size > self.bufferIndex) & (self.overFlow == False)):
##            pass
        result = []
        readPos = self.bufferIndex - 1
        for i in range(size):
            if (readPos < 0):
                readPos = self.bufferSize*8-1
            result += [self.RAND[readPos]]
            readPos -= 1
        return result

    def getLiveData(self):
##        return (random.randint(70,90), random.randint(40,60), random.randint(250,350), random.randint(250,350), random.randint(3,4))
        ro0 = self.__getValues(self.RO0, self.averageRange)
        ro1 = self.__getValues(self.RO1, self.averageRange)
        clk = self.__getValues(self.CLK, self.averageRange)
        ro0Diff = [0]*(self.averageRange-1)
        ro1Diff = [0]*(self.averageRange-1)
        clkDiff = [0]*(self.averageRange-1)
        for i in range(self.averageRange-1):
            ro0Diff[i] = ro0[i+1]-ro0[i]
            if (ro0Diff[i] < 0):
                ro0Diff[i] += 256**4
            ro1Diff[i] = ro1[i+1]-ro1[i]
            if (ro1Diff[i] < 0):
                ro1Diff[i] += 256**4
            clkDiff[i] = clk[i+1]-clk[i]
            if (clkDiff[i] < 0):
                clkDiff[i] += 256**4
        ro0A = numpy.median(ro0Diff)
        ro1A = numpy.median(ro1Diff)
        clkA = numpy.median(clkDiff)
        f0 = ro0A/clkA*100
        f1 = ro1A/clkA*100
        csc = self.__getValues(self.CSC, self.averageRange)
        cscA = int(numpy.median(csc))
        return (cscA, abs(1/f0-1/f1)*1000000, f0, f1, f1/cscA)

    def getROSel(self):
##        return (random.randint(0,63), random.randint(0,63))
        RS0 = self.__getValues(self.RO0Sel, self.averageRange)
        RS1 = self.__getValues(self.RO1Sel, self.averageRange)
        RS0A = numpy.median(RS0)
        RS1A = numpy.median(RS1)
        return (RS0A, RS1A)

    def __getValues(self, lst, size):
##        while ((self.bufferIndex < size) & (self.overFlow == False)):
##            pass
        result = [0]*size
        readPos = self.bufferIndex-1
        for i in range(size):
            if (readPos < 0):
                readPos += self.bufferSize
            result[i] = lst[readPos]
            readPos -= 1
        return result[::-1]

    def getLock(self):
        ctrs = self.__getValues(self.CTR, self.averageRange)
        ctr = int(numpy.median(ctrs))
        return numpy.sign(ctr&128)

    def getFound(self):
        ctrs = self.__getValues(self.CTR, self.averageRange)
        ctr = int(numpy.median(ctrs))
        return numpy.sign(ctr&64)
            
