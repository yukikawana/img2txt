#!/usr/bin/python

from PIL import Image, ImageDraw, ImageChops
import numpy as np
from numpy import linalg
import colortrans

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
    part = imr.crop((start+8,start,start+8+respb/2,start+respb))
    print part.size
    part.save('original.png')
    imgq = part.quantize(2, kmeans=True)
    imgq.save('bicolor.png')
    default_palette =  getPaletteInRgb(imgq)
    bg = hex(default_palette[0])[2:4]+hex(default_palette[1])[2:4]+hex(default_palette[2])[2:4]
    fg = hex(default_palette[3])[2:4]+hex(default_palette[4])[2:4]+hex(default_palette[5])[2:4]
    print default_palette
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
    print len(imgs)
    count2 = len(imgs)
    print count2
    #pdb.set_trace()
    diffs = np.zeros([1,25])
    for img in imgs:
        imgnp = np.asarray(img)
        imgqnp = np.asarray(imgq)
        diffs[0,count] = linalg.norm(imgnp-imgqnp)
        count+=1
    bgshort,rgb = colortrans.rgb2short(bg)
    fgshort,rgb = colortrans.rgb2short(fg)
    print '\033[38;5;{0};48;5;{1}m'.format(fgshort,bgshort)+unicodes[np.argmin(diffs)]+'\033[0;00m'





def create_temp_imgs(count,default_palette):
    tempimgs = []
    for w in xrange(0,respb/2):
        temp = Image.new('P', (respb/2,respb), 0)
        temp.putpalette(default_palette)
        d = ImageDraw.ImageDraw(temp)
        d.rectangle([0, 0, w, 15], fill=1)
        count+=1
        tempimgs.append(temp)
        temp.save('{}.png'.format(count))

    for h in xrange(1,respb/2):
        temp = Image.new('P', (respb/2,respb), 0)
        temp.putpalette(default_palette)
        d = ImageDraw.ImageDraw(temp)
        d.rectangle([0, 15-h*2+1, respb/2-1, 15], fill=1)
        count+=1
        tempimgs.append(temp)
        temp.save('{}.png'.format(count))

    #quarter blocks
    for qw in [0,respb/4]:
        for qh in [0,respb/2]:
            temp = Image.new('P', (respb/2,respb), 0)
            temp.putpalette(default_palette)
            d = ImageDraw.ImageDraw(temp)
            d.rectangle([qw, qh, qw+respb/4-1, respb/2-1+qh], fill=1)
            count+=1
            tempimgs.append(temp)
            temp.save('{}.png'.format(count))

    #quarter diagonal two blocks
    for qwqh in [ [[0,0],[respb/4,respb/2]], [[0,respb/2],[respb/4,0]]]:
        temp = Image.new('P', (respb/2,respb), 0)
        temp.putpalette(default_palette)
        d = ImageDraw.ImageDraw(temp)
        for qw, qh in qwqh:
            d.rectangle([qw, qh, qw+respb/4-1, respb/2-1+qh], fill=1)
        count+=1
        tempimgs.append(temp)
        temp.save('{}.png'.format(count))

    #three blocks
    for qwqh in [ [[0,0],[respb/4,respb/2],[respb/4,0]], [[0,0],[respb/4,respb/2],[0,respb/2]], [[0,respb/2],[respb/4,0],[0,0]],[[0,respb/2],[respb/4,0],[respb/4,respb/2]]]:
        temp = Image.new('P', (respb/2,respb), 0)
        temp.putpalette(default_palette)
        d = ImageDraw.ImageDraw(temp)
        for qw, qh in qwqh:
            d.rectangle([qw, qh, qw+respb/4-1, respb/2-1+qh], fill=1)
        count+=1
        tempimgs.append(temp)
        temp.save('{}.png'.format(count))

    return tempimgs




def getPaletteInRgb(img):
    assert img.mode == 'P', "image should be palette mode"
    pal = img.getpalette()
    color = pal[0:6]
    return color

if __name__ == '__main__':
    main()
