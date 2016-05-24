#!/usr/bin/python

# FEMM Helper by Jeff Martin

import numpy
import math
from optparse import OptionParser


parser = OptionParser()

parser.add_option("-s", "--selfshielded",
                  action="store_true", dest="ss", default=False,
                  help="included self-shielding coil")

parser.add_option("-c", "--cylindrical",
                  action="store_true", dest="cyl", default=False,
                  help="cylindrical geometry")

parser.add_option("-r", "--read-file", action="store_true",
                  dest="yesread", default=False, help="read geometry from files")

parser.add_option("-i", "--inner", dest="innerfile",
                  default="Cylinder_inner_0.2mA.txt", help="read inner coils from FILE", metavar="FILE")

parser.add_option("-o", "--outer", dest="outerfile",
                  default="Cylinder_outer_0.2mA.txt", help="read outer coils from FILE", metavar="FILE")

parser.add_option("-f", "--file", dest="filename", default="femm_helper.fem",
                  help="write to FILE", metavar="FILE")

(options, args) = parser.parse_args()


points = []      # format:  r,z
segs = []        # format:  pt1,pt2
arcsegs = []     # format:  pt1,pt2
blocklabels = [] # format:  r,z,material,circuit

print
print
print "FEMM Helper"
print
ri=float(input('Input the inner radius of the magnetic shield (m):  '))
ro=float(input('Input the outer radius of the magnetic shield (m):  '))

if options.cyl:
    hi=float(input('Input the inner height of the magnetic shield (m):  '))
    ho=float(input('Input the outer height of the magnetic shield (m):  '))

print
print
print "Make the following points in FEMM"
print "Format:  (r-coord,z-coord)"
print
if not options.cyl:
    print "For the magnetic shield inner radius"
    print ('({0:.6f},{1:.6f}) ({2:.6f},{3:.6f})'.format(0,-ri,0,ri))
    print "Join these using Operate on Arc Segments, with 180 degree angle"
    print
    print "For the magnetic shield outer radius"
    print ('({0:.6f},{1:.6f}) ({2:.6f},{3:.6f})'.format(0,-ro,0,ro))
    print "Join these using Operate on Arc Segments, with 180 degree angle"
    points.append([0,-ri]) # 0
    points.append([0,ri])  # 1
    points.append([0,-ro]) # 2
    points.append([0,ro])  # 3
    arcsegs.append([0,1])
    arcsegs.append([2,3])
    segs.append([0,2])
    segs.append([1,3])
    r=(ri+ro)/2/2**.5
    z=r
    blocklabels.append([r,z,1,0])
else:
    print ('({0:.6f},{1:.6f}) ({2:.6f},{3:.6f})'.format(0,-hi/2,0,-ho/2))
    print ('({0:.6f},{1:.6f}) ({2:.6f},{3:.6f})'.format(0,hi/2,0,ho/2))
    print ('({0:.6f},{1:.6f}) ({2:.6f},{3:.6f})'.format(ri,-hi/2,ro,-ho/2))
    print ('({0:.6f},{1:.6f}) ({2:.6f},{3:.6f})'.format(ri,hi/2,ro,ho/2))
    print "Join these using Operate on (Line) Segments"
    points.append([0,-hi/2]) # 0
    points.append([0,-ho/2]) # 1
    points.append([0,hi/2])  # 2
    points.append([0,ho/2])  # 3
    points.append([ri,-hi/2])# 4
    points.append([ro,-ho/2])# 5
    points.append([ri,hi/2]) # 6
    points.append([ro,ho/2]) # 7
    segs.append([0,1])
    segs.append([1,5])
    segs.append([5,7])
    segs.append([7,3])
    segs.append([3,2])
    segs.append([2,6])
    segs.append([6,4])
    segs.append([4,0])
    r=(ri+ro)/2
    z=(hi+ho)/2/4
    blocklabels.append([r,z,1,0])
print

if options.yesread:
    rposition_list = []
    zposition_list = []
    with open(options.innerfile) as innerstream:
        for i in range(8):
            innerstream.readline();
        oldu=0
        for line in innerstream:
            x,y,z,u=map(float,line.split())
            if (oldu!=u):
                r=(x**2+y**2)**.5
                deltau=abs(oldu-u)
                rposition_list.append(r)
                zposition_list.append(z)
                oldu=u
        ic_inner=deltau
    rpositions=numpy.array(rposition_list)
    zpositions=numpy.array(zposition_list)
    rposition_list_ss = []
    zposition_list_ss = []
    with open(options.outerfile) as outerstream:
        for i in range(8):
            outerstream.readline();
        oldu=0
        for line in outerstream:
            x,y,z,u=map(float,line.split())
            if (oldu!=u):
                r=(x**2+y**2)**.5
                deltau=abs(oldu-u)
                rposition_list_ss.append(r)
                zposition_list_ss.append(z)
                oldu=u
        ic_outer=-deltau
    rpositions_ss=numpy.array(rposition_list_ss)
    zpositions_ss=numpy.array(zposition_list_ss)
    
    sc=input('Input the side length for each coil profile (m):  ')
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
        points.append([rpositions_left[i],zpositions_bottom[i]])
        points.append([rpositions_left[i],zpositions_top[i]])
        points.append([rpositions_right[i],zpositions_top[i]])
        points.append([rpositions_right[i],zpositions_bottom[i]])
        segs.append([len(points)-4,len(points)-3])
        segs.append([len(points)-3,len(points)-2])
        segs.append([len(points)-2,len(points)-1])
        segs.append([len(points)-1,len(points)-4])
        blocklabels.append([rpositions[i],zpositions[i],3,1])
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
        points.append([rpositions_left_ss[i],zpositions_bottom_ss[i]])
        points.append([rpositions_left_ss[i],zpositions_top_ss[i]])
        points.append([rpositions_right_ss[i],zpositions_top_ss[i]])
        points.append([rpositions_right_ss[i],zpositions_bottom_ss[i]])
        segs.append([len(points)-4,len(points)-3])
        segs.append([len(points)-3,len(points)-2])
        segs.append([len(points)-2,len(points)-1])
        segs.append([len(points)-1,len(points)-4])
        blocklabels.append([rpositions_ss[i],zpositions_ss[i],3,2])

    r=(ri+ro)/2
    blocklabels.append([r/2,0,2,0]) # Air label


else:
    rc=input('Input the coil radius (m):  ')
    nc=input('Input the number of coils:  ')
    sc=input('Input the side length for each coil profile (m):  ')

    if not options.cyl:
        zpositions=numpy.arange(-(nc-1)*rc/nc,+(nc-1)*rc/nc+2*rc/nc,2*rc/nc)
        # z-positions of coils, based on Nouri and Plaster equation (5) and
        # surrounding text, and based on how numpy.arange works.
        rpositions=(rc**2-zpositions**2)**.5
    else:
        zpositions=numpy.arange(-hi/2+hi/nc/2,hi/2+hi/nc/2,hi/nc)
        rpositions=zpositions*0+rc

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
        points.append([rpositions_left[i],zpositions_bottom[i]])
        points.append([rpositions_left[i],zpositions_top[i]])
        points.append([rpositions_right[i],zpositions_top[i]])
        points.append([rpositions_right[i],zpositions_bottom[i]])
        segs.append([len(points)-4,len(points)-3])
        segs.append([len(points)-3,len(points)-2])
        segs.append([len(points)-2,len(points)-1])
        segs.append([len(points)-1,len(points)-4])
        blocklabels.append([rpositions[i],zpositions[i],3,1])

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
            points.append([rpositions_left_ss[i],zpositions_bottom_ss[i]])
            points.append([rpositions_left_ss[i],zpositions_top_ss[i]])
            points.append([rpositions_right_ss[i],zpositions_top_ss[i]])
            points.append([rpositions_right_ss[i],zpositions_bottom_ss[i]])
            segs.append([len(points)-4,len(points)-3])
            segs.append([len(points)-3,len(points)-2])
            segs.append([len(points)-2,len(points)-1])
            segs.append([len(points)-1,len(points)-4])
            blocklabels.append([rpositions_ss[i],zpositions_ss[i],3,2])

    blocklabels.append([rc/2,0,2,0]) # Air label

    b=input('Input the desired central field (uT):  ')
    mu0o4pi=1.0e-7 # T*m/A

    if not options.cyl:
        # http://hyperphysics.phy-astr.gsu.edu/hbase/magnetic/curloo.html
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

    else:
        ic=b*1.0e-6*hi/nc/(4*math.pi*mu0o4pi)
        print
        print 'For infinite cylinder, put a current of '
        print '{0:.6e} A in the coil'.format(ic)
        print

# Write out all the points, segments, and arc segments, in FEMM format

if not options.yesread:
    ic_inner=ic
    ic_outer=0


f=open(options.filename,'w')

print>>f,'[Format]      =  4.0'
print>>f,'[Frequency]   =  0'
print>>f,'[Precision]   =  1e-008'
print>>f,'[MinAngle]    =  30'
print>>f,'[Depth]       =  1'
print>>f,'[LengthUnits] =  meters'
print>>f,'[ProblemType] =  axisymmetric'
print>>f,'[Coordinates] =  cartesian'
print>>f,'[ACSolver]    =  0'
print>>f,'[Comment]     =  \"Add comments here.\"'
print>>f,'[PointProps]   = 0'
print>>f,'[BdryProps]   = 1'
print>>f,'[BlockProps]  = 3'
print>>f,'  <BeginBlock>'
print>>f,'    <BlockName> = \"mu\"'
print>>f,'    <Mu_x> = 20000'
print>>f,'    <Mu_y> = 20000'
print>>f,'    <H_c> = 0'
print>>f,'    <H_cAngle> = 0'
print>>f,'    <J_re> = 0'
print>>f,'    <J_im> = 0'
print>>f,'    <Sigma> = 0'
print>>f,'    <d_lam> = 0'
print>>f,'    <Phi_h> = 0'
print>>f,'    <Phi_hx> = 0'
print>>f,'    <Phi_hy> = 0'
print>>f,'    <LamType> = 0'
print>>f,'    <LamFill> = 1'
print>>f,'    <NStrands> = 0'
print>>f,'    <WireD> = 0'
print>>f,'    <BHPoints> = 0'
print>>f,'  <EndBlock>'
print>>f,'  <BeginBlock>'
print>>f,'    <BlockName> = \"Air\"'
print>>f,'    <Mu_x> = 1'
print>>f,'    <Mu_y> = 1'
print>>f,'    <H_c> = 0'
print>>f,'    <H_cAngle> = 0'
print>>f,'    <J_re> = 0'
print>>f,'    <J_im> = 0'
print>>f,'    <Sigma> = 0'
print>>f,'    <d_lam> = 0'
print>>f,'    <Phi_h> = 0'
print>>f,'    <Phi_hx> = 0'
print>>f,'    <Phi_hy> = 0'
print>>f,'    <LamType> = 0'
print>>f,'    <LamFill> = 1'
print>>f,'    <NStrands> = 0'
print>>f,'    <WireD> = 0'
print>>f,'    <BHPoints> = 0'
print>>f,'  <EndBlock>'
print>>f,'  <BeginBlock>'
print>>f,'    <BlockName> = \"Copper\"'
print>>f,'    <Mu_x> = 1'
print>>f,'    <Mu_y> = 1'
print>>f,'    <H_c> = 0'
print>>f,'    <H_cAngle> = 0'
print>>f,'    <J_re> = 0'
print>>f,'    <J_im> = 0'
print>>f,'    <Sigma> = 58'
print>>f,'    <d_lam> = 0'
print>>f,'    <Phi_h> = 0'
print>>f,'    <Phi_hx> = 0'
print>>f,'    <Phi_hy> = 0'
print>>f,'    <LamType> = 0'
print>>f,'    <LamFill> = 1'
print>>f,'    <NStrands> = 0'
print>>f,'    <WireD> = 0'
print>>f,'    <BHPoints> = 0'
print>>f,'  <EndBlock>'
print>>f,'[CircuitProps]  = 2'
print>>f,'  <BeginCircuit>'
print>>f,'    <CircuitName> = \"coil\"'
print>>f,'    <TotalAmps_re> = ',ic_inner
print>>f,'    <TotalAmps_im> = 0'
print>>f,'    <CircuitType> = 1'
print>>f,'  <EndCircuit>'
print>>f,'  <BeginCircuit>'
print>>f,'    <CircuitName> = \"coil2\"'
print>>f,'    <TotalAmps_re> = ',ic_outer
print>>f,'    <TotalAmps_im> = 0'
print>>f,'    <CircuitType> = 1'
print>>f,'  <EndCircuit>'

print>>f,"[NumPoints] = ",len(points)
for i in range(len(points)):
    r,z=points[i]
    print>>f,r,z,0,0

print>>f,"[NumSegments] = ",len(segs)
for i in range(len(segs)):
    p1,p2=segs[i]
    print>>f,p1,p2,-1,0,0,0

if len(arcsegs) > 0:
    print>>f,"[NumArcSegments] = ",len(arcsegs)
    for i in range(len(arcsegs)):
        p1,p2=arcsegs[i]
        print>>f,p1,p2,180,1,0,0,0

print>>f,"[NumHoles] = 0"

print>>f,"[NumBlockLabels] = ",len(blocklabels)
for i in range(len(blocklabels)):
    r,z,material,circuit=blocklabels[i]
    print>>f,r,z,material,-1,circuit,0,0,1,0


f.close()
