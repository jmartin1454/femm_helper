#!/usr/bin/python

# FEMM Helper by Jeff Martin

import numpy
import math
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--selfshielded",
                  action="store_true", dest="ss", default=False,
                  help="included self-shielding coil")
(options, args) = parser.parse_args()

print
print
print "FEMM Helper"
print
ri=input('Input the inner radius of the magnetic shield (m):  ')
ro=input('Input the outer radius of the magnetic shield (m):  ')

print
print
print "Make the following points in FEMM"
print "Format:  (r-coord,z-coord)"
print
print "For the magnetic shield inner radius"
print ('({0:.6f},{1:.6f}) ({2:.6f},{3:.6f})'.format(0,-ri,0,ri))
print "Join these using Operate on Arc Segments, with 180 degree angle"
print
print "For the magnetic shield outer radius"
print ('({0:.6f},{1:.6f}) ({2:.6f},{3:.6f})'.format(0,-ro,0,ro))
print "Join these using Operate on Arc Segments, with 180 degree angle"
print

rc=input('Input the coil radius (m):  ')
nc=input('Input the number of coils:  ')
sc=input('Input the side length for each coil profile (m):  ')

zpositions=numpy.arange(-(nc-1)*rc/nc,+(nc-1)*rc/nc+2*rc/nc,2*rc/nc)
# z-positions of coils, based on Nouri and Plaster equation (5) and
# surrounding text, and based on how numpy.arange works.
rpositions=(rc**2-zpositions**2)**.5
rpositions_left=rpositions-sc/2
rpositions_right=rpositions+sc/2
zpositions_top=zpositions+sc/2
zpositions_bottom=zpositions-sc/2

for i in range(len(zpositions)):
    coilnumber=i+1
    print "For coil number ",coilnumber
    print ('({0:.6f},{1:.6f}) ({2:.6f},{3:.6f}) ({4:.6f},{5:.6f}) ({6:.6f},{7:.6f})'.format(rpositions_left[i],zpositions_bottom[i],rpositions_left[i],zpositions_top[i],rpositions_right[i],zpositions_top[i],rpositions_right[i],zpositions_bottom[i]))
    print "Join these using Operate on (Line) Segments"
    print


if options.ss:
    rc_ss=input('Input the radius of the self-shielding coil (m):  ')
    zpositions_ss=numpy.arange(-(nc-1)*rc_ss/nc,+(nc-1)*rc_ss/nc+2*rc_ss/nc,2*rc_ss/nc)
    rpositions_ss=(rc_ss**2-zpositions_ss**2)**.5
    rpositions_left_ss=rpositions_ss-sc/2
    rpositions_right_ss=rpositions_ss+sc/2
    zpositions_top_ss=zpositions_ss+sc/2
    zpositions_bottom_ss=zpositions_ss-sc/2
    for i in range(len(zpositions_ss)):
        coilnumber=i+1
        print "For coil number ",coilnumber
        print ('({0:.6f},{1:.6f}) ({2:.6f},{3:.6f}) ({4:.6f},{5:.6f}) ({6:.6f},{7:.6f})'.format(rpositions_left_ss[i],zpositions_bottom_ss[i],rpositions_left_ss[i],zpositions_top_ss[i],rpositions_right_ss[i],zpositions_top_ss[i],rpositions_right_ss[i],zpositions_bottom_ss[i]))
        print "Join these using Operate on (Line) Segments"
        print


b=input('Input the desired central field (uT):  ')

# http://hyperphysics.phy-astr.gsu.edu/hbase/magnetic/curloo.html

mu0o4pi=1.0e-7 # T*m/A
bzsum=sum(mu0o4pi*2*math.pi*rpositions**2/rc**3) # geometry factor
ic=b*1.0e-6/bzsum
print
print 'For free space, put a current of {0:.6e} A in the coil'.format(ic)
print

if options.ss:
    bzsum_ss=sum(mu0o4pi*2*math.pi*rpositions_ss**2/rc_ss**3) # same
                                                              # geometry
                                                              # factor
                                                              # as
                                                              # above
    bzsum_ss_sscurrent_correction=-bzsum_ss*rc**2/rc_ss**2 # correct
                                                           # factor
                                                           # for
                                                           # current
                                                           # in shield
                                                           # coil
    ic_ss=b*1.0e-6/(bzsum+bzsum_ss_sscurrent_correction)
    print
    print 'For self-shielded configuration, put a current of'
    print '{0:.6e} A in the inner coil, and'.format(ic_ss)
    print '{0:.6e} A on the outer coil.'.format(-ic_ss*rc**2/rc_ss**2)
    print
    print
