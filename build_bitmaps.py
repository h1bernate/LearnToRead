#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Build Bitmaps for each character.
"""

import freetype
import numpy as np
import matplotlib.pyplot as plt

class Bitmapper:
    """Given a font file, render utf-8 characters onto a bitmap canvas and 
    return the result as a numpy array.
    """
    face = freetype.Face("NotoSansMonoCJKtc-Regular.otf")
    max_rows = 48
    max_width = 48
    # TODO(nwan): This seems to work better than 48*48, must be pertinent to
    # the widest glyph in the font, but this seems to get us close to a 48*48
    # for the small number of chinese characters I've tried.
    face.set_char_size( max_rows*64 )

    def render(this, c):
        # render only utf-8 characters
        assert type(c) == unicode
        # render only one utf-8 character
        assert len(c) == 1
        
        # create np array from bitmap buffer
        this.face.load_char(c)
        bitmap = this.face.glyph.bitmap
        buffer = np.array(bitmap.buffer).reshape([bitmap.rows,-1])
        
        # reshape np array into (max_rows x max_height) by padding right and
        # bottom
        assert buffer.shape[0] < this.max_rows
        assert buffer.shape[1] < this.max_width

        buffer = np.pad(buffer,
                        ((0,this.max_rows - bitmap.rows),
                            (0,this.max_width - bitmap.width)),
                        mode='constant')
        return buffer


bm = Bitmapper()
# plot the bitmap with pyplot as a sanity check
def plot(c):
    b = bm.render(c)
    plt.matshow(b, cmap='Greys')
    plt.show()

plot(u'我')
plot(u'麵')
plot(u'泼')
plot(u'S')


class BitmapVocab:
    """Vocabulary object to prepare bitmap data.
    """
    bm = Bitmapper()
    memo = {}

    def _encodeChar(this, c):
        # render only utf-8 characters
        assert type(c) == unicode
        # render only one utf-8 character
        assert len(c) == 1

        if not this.memo.has_key(c):
            this.memo[c] = this.bm.render(c)

        return this.memo[c]
        

    def encode(this, s):
        """Returns a (n, 48, 48) np.array of character bitmaps
        """
        # render only utf-8 characters
        assert type(s) == unicode

        bitmaps = []
        for c in s:
            x = this._encodeChar(c)
            bitmaps.append(x.reshape((1, x.shape[0], x.shape[1])))

        return np.vstack(bitmaps)

bv = BitmapVocab()
d = bv.encode(u'我麵泼S')
print d.shape  # (4, 48, 48)
d = bv.encode(u'我我我我我我我我我我我我我我我')
print d.shape  # (15, 48, 48)
