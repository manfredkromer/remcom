#/usr/bin/python
#
# remcom: remove commercials
#
# comp.py: compare hashes from movie images to hashes from commercials

import sys
from dhash import *
from PIL import Image

from remcomlib import *





if __name__ == '__main__':

    if len(sys.argv) != 3:
        print 'comp.py path-to-movie-images filename'
        exit(1)

    hashlist = readFromPickle(sys.argv[2])

    images = getFilesFromDir(sys.argv[1])
    for f in images:
        image = Image.open(f)
        row, col = dhash_row_col(image)
        hash = format_hex(row, col)

        for item in hashlist:
            diff = get_num_bits_different(int(item[1], 16), int(hash, 16))
            if diff <=2:
                print item[0] + ', diff: ' + str(diff)
                print f + ':  hash found: ' + item[0]


