import os, sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import lsst.afw.image as afwImage
import lsst.afw.detection as afwDetect
import lsst.afw.geom as afwGeom
from astropy.io import fits

import numpy as np

def makeBBList(mask, ccd) :

    # Create a bounding box corresponding to the useful part of the CCD (exclude overscan regions)
    bb = afwGeom.Box2I(afwGeom.Point2I(32, 0), afwGeom.Point2I(2079, 4611))
    # Read mask file provided by Elixir team
    im = afwImage.ImageF('%s.fits['%mask + str(ccd+1) + ']', bbox=bb, origin=afwImage.ImageOrigin.PARENT)
    # Pixel values in mask files are 1 for background and 0 for bad pixels - Need to inverse this
    im *= -1.
    im += 1.
    im *= 10.

    level = 2
    s = afwDetect.FootprintSet(im, afwDetect.Threshold(level, polarity=True))

    keys = ['x', 'y', 'w', 'h']
    defect = {k: [] for k in keys}
    defectE = {k: [] for k in keys}

    for f in s.getFootprints():
        fpl = afwDetect.footprintToBBoxList(f)
        for i in fpl:
            i.shift(afwGeom.Extent2I(-32,0))

            x0 = i.getBeginX()
            y0 = i.getBeginY()
            w0 = i.getWidth()
            h0 = i.getHeight()
            defect['x'].append(x0)
            defect['y'].append(y0)
            defect['w'].append(w0)
            defect['h'].append(h0)

            if (x0 % 2 == 0) :
                x1 = x0
                if (w0 % 2 == 0) :
                    w1 = w0
                else :
                    w1 = w0 + 1
            else :
                x1 = max(x0 - 1, 0)
                if (w0 % 2 == 0) :
                    w1 = min(w0 + 2, 2048)
                else :
                    w1 = min(w0 + 1, 2048)
            if (y0 % 2 == 0):
                y1 = y0
                if (h0 % 2 == 0) :
                    h1 = h0
                else :
                    h1 = min(h0 + 1, 4612)
            else :
                y1 = max(y0 - 1, 0)
                if (h0 % 2 == 0) :
                    h1 = min(h0 + 2, 4612)
                else :
                    h1 = min(h0 + 1, 4612)

            defectE['x'].append(x1)
            defectE['y'].append(y1)
            defectE['w'].append(w1)
            defectE['h'].append(h1)

    return defect, defectE

def writeFits(ccd, defect, fileOut) :

    ccdSerial = ['834175',  '835234',  '8352153', '8261144', '8341174', '8351205',
                '8351133', '835163',  '8261133', '917213',  '835244',  '8352155',
                '8351204', '8351173', '8434135', '8341173', '8351114', '7432193',
                '917243',  '8341165', '8352134', '8374175', '8351115', '835164',
                '8351185', '8352185', '835173',  '8261165', '743233',  '8351164',
                '8261195', '835183',  '8352104', '8352154', '826173',  '8261143',
                '917224',  '835264',  '835235',  '8261155']

    col1 = fits.Column(name="x0", format="I", array=np.asarray(defect['x']))
    col2 = fits.Column(name="y0", format="I", array=np.asarray(defect['y']))
    col3 = fits.Column(name="width", format="I", array=np.asarray(defect['w']))
    col4 = fits.Column(name="height", format="I", array=np.asarray(defect['h']))

    tbhdr = fits.Header()
    cols = fits.ColDefs([col1, col2, col3, col4])
    tbhdr['SERIAL'] = ccdSerial[ccd]
    tbhdu = fits.BinTableHDU.from_columns(cols, header=tbhdr)

    tbhdu.writeto(fileOut, overwrite=True)

    return

def main(argv=None) :

    description = """Transforms Elixir defect masks to LSST format"""
    prog = "genDefects.py"
    usage = """%s [options] config""" % prog

    parser = ArgumentParser(prog=prog, usage=usage, description=description,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--mask', help='Elixir mask name')
    parser.add_argument('--numccd', default=36, type=int, help='Number of CCD')
    args = parser.parse_args(argv)

    if args.numccd != 36 :
        print("Warning : LSST DM stack knows about 36 CCD only")

    dir1 = args.mask + ".nn"
    dir2 = args.mask + "_enlarged.nn"
    if not os.path.exists(dir1):
        os.makedirs(dir1)
    if not os.path.exists(dir2):
        os.makedirs(dir2)

    for ccd in range(args.numccd) :
        print("Computing masks for ccd %i"%ccd)
        defect, defectE = makeBBList(args.mask, ccd)
        writeFits(ccd, defect, os.path.join(dir1, 'ccd%02i'%ccd + '.fits'))
        writeFits(ccd, defectE, os.path.join(dir2, 'ccd%02i'%ccd + '.fits'))

if __name__ == "__main__":
    main()
