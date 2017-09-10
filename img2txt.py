#!/usr/bin/python

from PIL import Image, ImageDraw, ImageChops
import numpy as np
from numpy import linalg
from extra import colortrans
import sys

import pdb
import os
blockwidth = 30
respb = 16
unicodes = [
u'\u258f',
u'\u258e',
u'\u258d',
u'\u258c',
u'\u258b',
u'\u258a',
u'\u2589',
u'\u2588',
u'\u2581',
u'\u2582',
u'\u2583',
u'\u2584',
u'\u2585',
u'\u2586',
u'\u2587',
u'\u2598',
u'\u259d',
u'\u2596',
u'\u2597',
u'\u259a',
u'\u259e',
u'\u259c',
u'\u2599',
u'\u259b',
u'\u259f',
]




def main():
    im = Image.open('../re.jpg').quantize(256)
    width, height = im.size
    ratio = float(blockwidth) / float(width)
    blockheight = int(ratio * height)

    print ratio
    print im.size
    imr = im.resize((blockwidth * respb, blockheight * respb), Image.ANTIALIAS)
    print imr.size
    start = 50
    for hh in xrange(blockheight):
        for ww in xrange(blockwidth):
            part = imr.crop((ww*respb/2,hh*respb,(ww+1)*respb/2,(hh+1)*respb))
            imgq = part.quantize(2, kmeans=True)
            default_palette =  getPaletteInRgb(imgq)
            bg = hex(default_palette[0])[2:4].zfill(2)+hex(default_palette[1])[2:4].zfill(2)+hex(default_palette[2])[2:4].zfill(2)
            fg = hex(default_palette[3])[2:4].zfill(2)+hex(default_palette[4])[2:4].zfill(2)+hex(default_palette[5])[2:4].zfill(2)
            """
            default_palette = [
            255,0,0,
            0,0,255
            ]
            """
            count = 0
            imgs = create_temp_imgs(count, default_palette)
            new_palette = [
            0,0,255,
            255,0,0
            ]
            count2 = len(imgs)
            #pdb.set_trace()
            diffs = np.zeros([1,25])
            for img in imgs:
                imgnp = np.asarray(img)
                imgqnp = np.asarray(imgq)
                diffs[0,count] = linalg.norm(imgnp-imgqnp)
                count+=1
            bgshort,rgb = colortrans.rgb2short(bg)
            fgshort,rgb = colortrans.rgb2short(fg)
            
            sys.stdout.write('\033[38;5;{0};48;5;{1}m'.format(fgshort,bgshort)+unicodes[np.argmin(diffs)]+'\033[0;00m')
        sys.stdout.write('\n')





def create_temp_imgs(count,default_palette):
    tempimgs = []
    for w in xrange(0,respb/2):
        temp = Image.new('P', (respb/2,respb), 0)
        temp.putpalette(default_palette)
        d = ImageDraw.ImageDraw(temp)
        d.rectangle([0, 0, w, 15], fill=1)
        count+=1
        tempimgs.append(temp)

    for h in xrange(1,respb/2):
        temp = Image.new('P', (respb/2,respb), 0)
        temp.putpalette(default_palette)
        d = ImageDraw.ImageDraw(temp)
        d.rectangle([0, 15-h*2+1, respb/2-1, 15], fill=1)
        count+=1
        tempimgs.append(temp)

    #quarter blocks
    for qw in [0,respb/4]:
        for qh in [0,respb/2]:
            temp = Image.new('P', (respb/2,respb), 0)
            temp.putpalette(default_palette)
            d = ImageDraw.ImageDraw(temp)
            d.rectangle([qw, qh, qw+respb/4-1, respb/2-1+qh], fill=1)
            count+=1
            tempimgs.append(temp)

    #quarter diagonal two blocks
    for qwqh in [ [[0,0],[respb/4,respb/2]], [[0,respb/2],[respb/4,0]]]:
        temp = Image.new('P', (respb/2,respb), 0)
        temp.putpalette(default_palette)
        d = ImageDraw.ImageDraw(temp)
        for qw, qh in qwqh:
            d.rectangle([qw, qh, qw+respb/4-1, respb/2-1+qh], fill=1)
        count+=1
        tempimgs.append(temp)

    #three blocks
    for qwqh in [ [[0,0],[respb/4,respb/2],[respb/4,0]], [[0,0],[respb/4,respb/2],[0,respb/2]], [[0,respb/2],[respb/4,0],[0,0]],[[0,respb/2],[respb/4,0],[respb/4,respb/2]]]:
        temp = Image.new('P', (respb/2,respb), 0)
        temp.putpalette(default_palette)
        d = ImageDraw.ImageDraw(temp)
        for qw, qh in qwqh:
            d.rectangle([qw, qh, qw+respb/4-1, respb/2-1+qh], fill=1)
        count+=1
        tempimgs.append(temp)

    return tempimgs




def getPaletteInRgb(img):
    assert img.mode == 'P', "image should be palette mode"
    pal = img.getpalette()
    color = pal[0:6]
    return color

if __name__ == '__main__':
    main()
