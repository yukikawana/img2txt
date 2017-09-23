#!/usr/bin/python

from PIL import Image
import pdb
import os
blockwidth = 30
respb = 16

def main():
    im = Image.open('yad2k/images/horses.jpg')
    width, height = im.size
    ratio = float(blockwidth) / float(width)
    blockheight = int(ratio * height)

    print ratio
    print im.size
    imr = im.resize((blockwidth * respb, blockheight * respb), Image.ANTIALIAS)
    print imr.size
    part = imr.crop((50,50,50+16,50+16))
    print part.size
    part.save('original.bmp')
    part.quantize(2).save('bicolor.bmp')


if __name__ == '__main__':
    main()
