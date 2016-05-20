import csv #used to parse through csv file
import mimetypes #used to get the filetype of the given file
import sys

def _distance(rgb1, rgb2):
    return sum((a-b)**2 for a,b in zip(rgb1, rgb2))

def energy(row, col, height, width):
    result = 0
    pixel = get_pixel(row, col)
    for c in (col-1, col+1):
        if 0 <= c < width:
            result += _distance(pixel, get_pixel(row, c))
    for r in (row-1, row+1):
        if 0 <= r < height:
            result += _distance(pixel, get_pixel(r, col))
    if col in (0, width):
        result *= 2
    return result

class SeamCarver:

    #These are our class variables
    #file_path
    #file_type
    #pixel_map
    #energy_map
    #length
    #width

    def __init__(self, path):

        # capture the location of the image/txt file
        self.file_path = path
        self.pixel_map = []
        self.energy_map = []

        #This tells me what type of file we are using
        file_type =  mimetypes.guess_type(path)
        # make the decison to what type of file we are ding
        if file_type[0] == 'image/png':
            self.file_type = "image/png"
            print "image/png"
        elif (file_type[0] == 'text/plain'):
            self.file_type = 'text/plain'
            print "text/plain"
        else:
            self.file_type = None
            print file_type[0]

    def getPixelMap(self):
        if (self.file_type == 'image/png'):
            print "use image processing library"

        elif(self.file_type == 'text/plain'):
            with open(self.file_path, "rb") as f:
                reader = csv.reader(f, delimiter=",")

                for i, line in enumerate(reader):
                    temp_line = []
                    for weight in line:
                        temp_line.append(float(weight))
                    self.pixel_map.append(temp_line)
            self.length = len(self.pixel_map)
            self.width = len(self.pixel_map[0])
            print "length" , self.length
            print "width" , self.width
        else:
            print self.file_type, "this file type not supported yet"

        #return the pixel map
        #self.printPixels()
        #print '\n'
        return self.pixel_map

    #once our pixel map is generated we do this shiz!!
    def getEnergyMap(self):

        #initialize the energy map with first row of pixel map
        self.energy_map.append(map(float, self.pixel_map[0]))

        # iterate through every pixel in every row
        for length in range(1, self.length):
            nrg_arr = []
            for width in range(self.width):
                curr_pixel = self.pixel_map[length][width]

                #if leftmost
                if width == 0:
                    #print "first index"
                    pixel_above = self.energy_map[length - 1][width]
                    pixel_above_right = self.energy_map[length - 1][width + 1]
                    nrg_arr.append(float(curr_pixel) + float(min(pixel_above, pixel_above_right)))
                #if rightmost
                elif width == self.width-1:
                    #print "last index"
                    pixel_above = self.energy_map[length - 1][width]
                    pixel_above_left = self.energy_map[length - 1][width - 1]
                    nrg_arr.append(float(curr_pixel) + float(min(pixel_above, pixel_above_left)))

                #if anywhere in the middle
                else:
                    #print "middle index"
                    pixel_above_left = self.energy_map[length - 1][width - 1]
                    pixel_above = self.energy_map[length - 1][width]
                    pixel_above_right = self.energy_map[length - 1][width + 1]
                    nrg_arr.append(float(curr_pixel) + float(min(pixel_above, pixel_above_right, pixel_above_left)))

            self.energy_map.append(nrg_arr)
            #self.printEnergy()
            #print "\n"
        return self.energy_map

    def getTraceback(self):

        minpix = min(self.energy_map[self.length - 1 ])
        minpix_index = self.energy_map[self.length - 1].index(minpix)
        min_seam = self.pixel_map[self.length - 1][minpix_index]
        #print min_seam
        #print minpix
        #print minpix_index

        traceback_arr = []

        first = True
        for length in range(self.length-1, -1, -1):
            #if is leftmost index
            width = 0
            if minpix_index == 0:
                #print "leftmost"
                pixel_above = self.energy_map[length - 1][minpix_index]
                pixel_above_right = self.energy_map[length - 1][minpix_index + 1]
                width = self.energy_map[length].index((min(pixel_above, pixel_above_right)))

            #if is rightmost index
            elif minpix_index == self.length - 1:
                #print "rightmost"
                pixel_above = self.energy_map[length - 1][minpix_index]
                pixel_above_left = self.energy_map[length - 1][minpix_index - 1]
                width = self.energy_map[length - 1].index((min(pixel_above, pixel_above_left)))


            #if is in the middle
            else:
                #print "middle"
                #print "length ", length
                #print minpix_index
                pixel_above_left = self.energy_map[length - 1][minpix_index - 1]
                pixel_above = self.energy_map[length - 1][minpix_index]
                pixel_above_right = self.energy_map[length - 1][minpix_index + 1]
                width = self.energy_map[length - 1].index((min(pixel_above, pixel_above_left, pixel_above_right)))

            arr = []
            arr.append(length)
            arr.append(minpix_index)
            arr.append(self.pixel_map[length][minpix_index])
            traceback_arr.append(arr)

            #print '[', length, ',', minpix_index, ',', self.pixel_map[length][minpix_index] , ']'
            if first:
                first = False
            else:
                min_seam = min_seam + self.pixel_map[length][minpix_index]

            minpix_index = width


        # This redirects the output to a file
        orig_stdout = sys.stdout
        outfile = self.file_path.replace('.txt','_trace.txt')
        f = file( outfile , 'w')
        sys.stdout = f

        print "Min Seam: ", min_seam
        for i in range(0, self.length):
            print  "[", traceback_arr[i][0], ',', traceback_arr[i][1], ',', traceback_arr[i][2], "]"

        sys.stdout = orig_stdout
        f.close()
        # this indicates we are done
        print "Done. Check " + outfile + " for more details"

    def printEnergy(self):
        for i in range(0, len(self.energy_map)):
            print self.energy_map[i]

    def printPixels(self):
        for i in range(0, self.length):
            print self.pixel_map[i]

    def printTraceback(self):
        #since the traceback functions already prints no need to reinvent the wheel
        self.getTraceback()

    def consolelog(self, *content):

        print len(content)
        if content == 'pixelmap':
            self.printPixels()
        elif content == 'energymap':
            self.printEnergy()
        elif content == 'traceback':
            print self.traceback

        elif len(content) == 0:
            print 'PIXEL MAP =========================================================================================='
            self.printPixels()
            print 'ENERGY MAP ========================================================================================='
            self.printEnergy()
            print 'TRACEBACK =========================================================================================='
            self.getTraceback()

    def create_seam(self):
        self.getPixelMap()
        self.getEnergyMap()
        self.getTraceback()
        #self.consolelog()
