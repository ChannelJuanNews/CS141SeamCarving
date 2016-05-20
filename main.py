#Import our seam carver class which does all our magikkkkk
from seamcarver import SeamCarver
import sys

def main():

    #In order to carve a seam we need to feed our SeamCarver object a file. Only png or txt will work

    #image = SeamCarver('TestExamples/input0small.txt')
    #image.getPixelMap() # This returns the pixel map created from the above file
    #image.getEnergyMap() # This returns the energy map created from
    #image.getTraceback() # This returns the traceback along with the min seam value

    # This will print out the current state of the pixel map and engergy map
    # Acceptable parameters are 'pixelmap' 'energymap' or 'traceback'. If no params are given it prints all of them
    #image.consolelog()

    #Alternatively you can do the same thing above with only one line of code
    image = SeamCarver(sys.argv[1]).create_seam()

if __name__ == '__main__':
    main()
