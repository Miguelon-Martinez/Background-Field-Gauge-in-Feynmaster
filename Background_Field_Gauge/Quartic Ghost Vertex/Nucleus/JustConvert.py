# > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
# This is JustConvert.py, a Python routine that supports the conversion functions available
# in the Notebooks.
#
# Created by: Duarte Fontes
# Email: duartefontes@tecnico.ulisboa.pt
# Last Update: 12.05.2021
# > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >

import os,sys,re,os.path
from datetime import date
import Converter
import zipfile

import FRExtract
(intname,extname,FCsimp,FCeqs,PrMassFL,GFreno,FRrestr,mygluon,gaugegslist,gslist,mycomplex) = FRExtract.FRextra()

def Addd0(arg):
	auxdot = re.findall(r'(?<![a-zA-Z0-9])(\d+\.?(?<![a-z])\d*)', arg)
	auxdot2=[];
	for i in range(len(auxdot)):
		if auxdot[i] not in auxdot2:
			auxdot2.append(auxdot[i])
	for i in range(len(auxdot2)):
		arg = re.sub(r'(?<![a-zA-Z0-9])'+auxdot2[i]+r'(?![a-zA-Z0-9])',auxdot2[i]+'d0',arg)
	alist=list(arg)
	for i in range(len(alist)):
		if i != (len(alist)-1) and i!=0:
			if alist[i] == 'I' and not alist[i-1].isalnum() and not alist[i+1].isalnum():
				alist[i]='(0d0,1d0)'
		elif i!=0:
			if alist[i] == 'I' and not alist[i-1].isalnum():
				alist[i]='(0d0,1d0)'
		elif i!=(len(alist)-1):
			if alist[i] == 'I' and not alist[i+1].isalnum():
				alist[i]='(0d0,1d0)'					
	arg="".join(alist)
	return arg

dataFR='dataFR.m'
if os.path.isfile(dataFR):
	f1 = open(dataFR, 'r');
	conv = open('MyTeXForm-last-output.tex', 'w')
	f2 = f1.read()
	scribendum=Converter.FCtoTEX(Converter.FRtoFC(f2),'express')
	conv.write(scribendum)
	conv.close()

dataFC='dataFC.m'
if os.path.isfile(dataFC):
	f1 = open(dataFC, 'r');
	conv = open('MyTeXForm-last-output.tex', 'w')
	f2 = f1.read()
	scribendum=Converter.FCtoTEX(f2,'express')
	conv.write(scribendum)
	conv.close()

dataFT='dataFT.m'
if os.path.isfile(dataFT):
	f1 = open(dataFT, 'r');
	f2pre = f1.read().splitlines()
	f2clean=list(filter(('').__ne__, f2pre))

	mycom=f2clean[0]
	tag=mycom.split(';')[0]
	myloops=0
	loopcheck=mycom.find('loop')
	if loopcheck != -1:
		myloops=mycom[loopcheck-2]

	auxn = re.findall(r'Process (.*?) at', mycom)[0]
	auxn0 = auxn.split('to')[0]
	auxnv = auxn0.find(',')
	myprocess = 'decay' if auxnv==-1 else 'scat'

	myretil = True if 'True' in f2clean[1] else False

	f2=f2clean[2]
	formfactors=[]
	newexpr=[]	
	for i in range(len(f2clean)-3):
		myaux=f2clean[i+3].split(' -> ', 1)
		formfactors.append(myaux[0].replace(' ',''))
		newexpr.append(myaux[1])

	faux='Matrixind.m'
	rowaux = [];
	if os.path.isfile(faux):
		f = open(faux, 'r');	allLines = f.read().splitlines();	f.close()
		for l in allLines:
			rowaux.append(l)
		rowaux2=[]
		for i in range(len(rowaux)):
			rowaux2.append(rowaux[i].split(', '))
		matnames=[]
		for i in range(len(rowaux2)):
			matnames.append(rowaux2[i][0])
		for h in range(len(matnames)):
			auxmat = re.findall(r''+matnames[h]+'\[(.*?), (.*?)\]', f2)
			for i in range(len(auxmat)):
				f2=f2.replace(matnames[h]+'[' + auxmat[i][0] + ', ' + auxmat[i][1] + ']',matnames[h]+auxmat[i][0]+auxmat[i][1])	
			for j in range(len(newexpr)):
				auxmat = re.findall(r''+matnames[h]+'\[(.*?), (.*?)\]', newexpr[j])
				for i in range(len(auxmat)):
					newexpr[j]=newexpr[j].replace(matnames[h]+'[' + auxmat[i][0] + ', ' + auxmat[i][1] + ']',matnames[h]+auxmat[i][0]+auxmat[i][1])

	(scribbasic,nmaxbasic,myvars)=Converter.FCtoFT(f2,myretil)

	scrib2=scribbasic[0][20:]
	newscrib=[]
	nmaxtot=[]
	for i in range(len(newexpr)):
		(prescribendum,nmax,myvars)=Converter.FCtoFT(newexpr[i],myretil)
		newscrib.append(prescribendum)
		nmaxtot.append(nmax)

	fvar = open('MyVariables.h', 'w')
	fvar.write('#if 0\n')
	fvar.write('#endif\n')
	rol=myvars.split(',')

	Goreal='real*8' # choose this for normal precision
	#Goreal='real*16' # choose this for quadrupole precision
	Gocomplex='complex*16' # choose this for normal precision
	#Gocomplex='complex*32' # choose this for quadrupole precision

	for h in range(len(rol)):
		if rol[h] not in mycomplex:
			fvar.write('      ' + Goreal + ' ' + rol[h] + '\n')
		else:
			fvar.write('      '+Gocomplex+' ' + rol[h] + '\n')
	fvar.close()

	# We start by making the general description for the main function
	conv = open('My'+tag+'.F', 'w')
	conv.write('\n')
	nt=53; thestr1='';
	thestr='      '+Gocomplex+' function My'+tag+'(' + myvars + ')\n'
	for t in range(0,len(thestr),nt):
		if (len(thestr)-t)>nt:
			thestr1=thestr1+thestr[t:t+nt]+'\n     & '
		else:
			thestr1=thestr1+thestr[t:t+nt]+'\n'
	rol=myvars.split(',')
	conv.write(thestr1)
	conv.write('      implicit none\n')
	conv.write('      '+Goreal+' Pi\n')
	conv.write('      integer i\n')
	for i in range(nmaxbasic):
		conv.write('      '+Gocomplex+' '+tag+'_'+str(i+1)+'_x\n')
	conv.write('      '+Gocomplex+' '+tag+'V(5000)\n\n')
	conv.write('#include "MyVariables.h"\n')
	if myloops == '1':
		conv.write('#include "looptools.h"\n\n')
	conv.write('      Pi=acos(-1.d0)\n')
	conv.write('      My'+tag+' = 0d0\n')
	thestr2='';
	for i in range(nmaxbasic):
		thestr='      '+tag+'V('+str(i+1)+')='+tag+'_'+str(i+1)+'_x(' + myvars + ')\n'
		for t in range(0,len(thestr),nt):
			if (len(thestr)-t)>nt:
				thestr2=thestr2+thestr[t:t+nt]+'\n     & '
			else:
				thestr2=thestr2+thestr[t:t+nt]+'\n'
	conv.write(thestr2)	
	conv.write('\n')
	conv.write('      do i=1,' + str(nmaxbasic) + '\n')
	conv.write('            My'+tag+'=My'+tag+'+'+tag+'V(i)\n')
	conv.write('      enddo\n\n')
	conv.write('      return\n')
	conv.write('      end\n\n\n\n')

	# We now write individually the parts of the main expression
	newcount=0
	for i0 in range(nmaxbasic):
		myinflim=10;
		mytrunc=10;
		if i0<myinflim:
			alt=conv
		else:
			if i0 % mytrunc == 0:
				newcount=newcount+1
				alt = open('MyAux_' + tag + '_' + str(newcount) + '.F', 'w')	
		nt=53; thestr2='';
		alt.write('* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *\n')
		thestr='      '+Gocomplex+' function '+tag+'_'+str(i0+1)+'_x(' + myvars + ')\n'
		for t in range(0,len(thestr),nt):
			if (len(thestr)-t)>nt:
				thestr2=thestr2+thestr[t:t+nt]+'\n     & '
			else:
				thestr2=thestr2+thestr[t:t+nt]+'\n'
		rol=myvars.split(',')
		alt.write(thestr2)
		alt.write('      implicit none\n')
		alt.write('      integer i\n')
		alt.write('      '+Goreal+' Pi\n\n')
		alt.write('#include "MyVariables.h"\n')
		if myloops == '1':
			alt.write('#include "looptools.h"\n\n')
		for i in range(len(formfactors)):
			alt.write('      '+Gocomplex+' '+ formfactors[i] +','+ formfactors[i] +'_x\n')
		alt.write('\n')
		alt.write('      Pi=acos(-1.d0)\n\n')

		thestr3=''; thestr4='';
		for i in range(len(formfactors)):
			thestr3='      '+formfactors[i]+'='+formfactors[i]+'_x(' + myvars + ')\n'
			for t in range(0,len(thestr3),nt):
				if (len(thestr3)-t)>nt:
					thestr4=thestr4+thestr3[t:t+nt]+'\n     & '
				else:
					thestr4=thestr4+thestr3[t:t+nt]+'\n'

		alt.write(thestr4)	
		alt.write('\n')		
		alt.write(scribbasic[i0].replace('Out('+str(i0+1)+')',tag+'_'+str(i0+1)+'_x'))
		alt.write('\n')
		alt.write('      return\n')
		alt.write('      end\n')
		alt.write('* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *')
		if i0 != nmaxbasic-1:
			alt.write('\n\n\n\n')
		alt.write('\n\n\n\n\n\n')
		if alt != conv:
			if ((i0+1) % mytrunc == 0) or (i0 == (nmaxbasic-1)):
				alt.close()

	# Now, we turn to the  main description of the form factors
	for h0 in range(len(nmaxtot)):
		conv.write('* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *\n')
		nt=53; thestr2=''
		thestr='      '+Gocomplex+' function '+formfactors[h0]+'_x(' + myvars + ')\n'
		for t in range(0,len(thestr),nt):
			if (len(thestr)-t)>nt:
				thestr2=thestr2+thestr[t:t+nt]+'\n     & '
			else:
				thestr2=thestr2+thestr[t:t+nt]+'\n'
		rol=myvars.split(',')
		conv.write(thestr2)
		conv.write('      implicit none\n')
		conv.write('      '+Goreal+' Pi\n')
		conv.write('      integer i\n')
		for i in range(nmaxtot[h0]):
			conv.write('      '+Gocomplex+' '+formfactors[h0]+'_x'+str(i+1)+'\n')
		conv.write('      '+Gocomplex+' '+formfactors[h0]+'_y(5000)\n\n')
		conv.write('#include "MyVariables.h"\n')
		if myloops == '1':
			conv.write('#include "looptools.h"\n\n')
		conv.write('      Pi=acos(-1.d0)\n')
		conv.write('      '+formfactors[h0]+'_x = 0d0\n')
		thestr2='';
		for i in range(nmaxtot[h0]):
			thestr='      '+formfactors[h0]+'_y('+str(i+1)+')='+formfactors[h0]+'_x'+str(i+1)+'(' + myvars + ')\n'
			for t in range(0,len(thestr),nt):
				if (len(thestr)-t)>nt:
					thestr2=thestr2+thestr[t:t+nt]+'\n     & '
				else:
					thestr2=thestr2+thestr[t:t+nt]+'\n'
		conv.write(thestr2)	
		conv.write('\n')
		conv.write('      do i=1,' + str(nmaxtot[h0]) + '\n')
		conv.write('            '+formfactors[h0]+'_x='+formfactors[h0]+'_x+'+formfactors[h0]+'_y(i)\n')
		conv.write('      enddo\n\n')
		conv.write('      return\n')
		conv.write('      end\n\n\n\n')

	# Finally, we write individually the parts of the form factors
		for i0 in range(nmaxtot[h0]):
			if i0<myinflim:
				alt=conv
			else:
				if i0 % mytrunc == 0:
					newcount=newcount+1
					alt = open('MyAux_' + tag + '_' + str(newcount) + '.F', 'w')
			nt=53; thestr2='';
			alt.write('* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *\n')
			thestr='      '+Gocomplex+' function '+formfactors[h0]+'_x'+str(i0+1)+'(' + myvars + ')\n'
			for t in range(0,len(thestr),nt):
				if (len(thestr)-t)>nt:
					thestr2=thestr2+thestr[t:t+nt]+'\n     & '
				else:
					thestr2=thestr2+thestr[t:t+nt]+'\n'
			rol=myvars.split(',')
			alt.write(thestr2)
			alt.write('      implicit none\n')
			alt.write('      integer i\n')
			alt.write('      '+Goreal+' Pi\n\n')
			alt.write('#include "MyVariables.h"\n')
			if myloops == '1':
				alt.write('#include "looptools.h"\n\n')
			alt.write('      Pi=acos(-1.d0)\n\n')
			alt.write(newscrib[h0][i0].replace('Out('+str(i0+1)+')',formfactors[h0]+'_x'+str(i0+1)))
			alt.write('\n')
			alt.write('      return\n')
			alt.write('      end\n\n')
			if ((i0+1) % mytrunc == 0) or (i0 == (nmaxtot[h0]-1)):
				alt.write('* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *\n\n')
				if alt!=conv:
					alt.close()
			else:
				alt.write('\n')
	conv.close()


	yolo = open('Makefile-template', 'w')
	yolo.write('FC         = ifort\n\n')
	if myloops == '1':
		yolo.write('LT         = /usr/local/lib/LoopTools\n\n')
		yolo.write('FFLAGS	   =   -c -O  -I$(LT)/include\n\n')
	else:
		yolo.write('LT         = \n\n')
		yolo.write('FFLAGS	   =   -c -O \n\n')
	yolo.write('LDFLAGS    =  \n\n')
	yolo.write('LINKER	   = $(FC)\n\n\n\n')
	if myloops == '1':
		yolo.write('LIB        = -L$(LT)/lib64\n')
		yolo.write('LIBS       = -looptools\n\n')
	else:
		yolo.write('LIB        = \n')
		yolo.write('LIBS       = \n\n')
	yolo.write('.F.o:\n')
	yolo.write('	$(FC) $(FFLAGS) $*.F\n')
	yolo.write('.f.o:\n')
	yolo.write('	$(FC) $(FFLAGS) $*.f\n\n\n\n')
	yolo.write('files	= MainFT.o My'+tag+'.o')
	for i7 in range(newcount):
		yolo.write(' MyAux_'+tag+'_'+str(i7+1)+'.o')
	if myprocess == 'scat':
		yolo.write(' IntGauss.o\n')
	else:
		yolo.write(' \n')
	yolo.write('all:	$(files) \n')
	yolo.write('	$(LINKER) $(LDFLAGS) -o MainFT $(files) $(LIB) $(LIBS)\n')
	yolo.close()


	# yolo = open('Makefile', 'w')
	# yolo.write('FC         = /usr/local/bin/gfortran\n\n')
	# yolo.write('LT	   = /Users/duarte/Physics/Programas/LoopTools/x86_64\n\n')
	# yolo.write('FFLAGS	   =  -c -O -I$(LT)/include\n\n')
	# yolo.write('LDFLAGS    =  \n\n')
	# yolo.write('LINKER	   = $(FC)\n\n\n\n')
	# yolo.write('LIB        = -L/Users/duarte/Physics/Programas/LoopTools/x86_64/lib\n')
	# yolo.write('LIBS       = -looptools\n\n')
	# yolo.write('.F.o:\n')
	# yolo.write('	$(FC) $(FFLAGS) $*.F\n')
	# yolo.write('.f.o:\n')
	# yolo.write('	$(FC) $(FFLAGS) $*.f\n\n\n\n')
	# yolo.write('files	= MainFT.o My'+tag+'.o\n')
	# yolo.write('all:	$(files) \n')
	# yolo.write('	$(LINKER) $(LDFLAGS) -o MyExe $(files) $(LIB) $(LIBS)\n')
	# yolo.close()


	fPV='ParamsValues.m'
	ecri = open('MyParameters.h', 'w')
	if os.path.isfile(fPV):
		f = open(fPV, 'r');	allLines = f.read().splitlines();	f.close()
		ecri.write('       Parameter(\n')
		totco=0
		for l in allLines:
			totco+=1
			mysplit1=l.split('=')
			if any(mysplit1[0] == x for x in matnames):
				mysplit2=mysplit1[1].split(',')
				for k in range(len(matnames)):
					if mysplit1[0]==matnames[k]:
						count=0
						for k1 in range(int(rowaux2[k][1])):
							if len(rowaux2[k])>2: 
								for k2 in range(int(rowaux2[k][2])):
									if totco == len(allLines) and (k1+1) == int(rowaux2[k][1]) and (k2+1) == int(rowaux2[k][2]):
										ecri.write('     &		'+mysplit1[0]+str(k1+1)+str(k2+1)+'='+Addd0(mysplit2[count])+'\n')
									else:
										ecri.write('     &		'+mysplit1[0]+str(k1+1)+str(k2+1)+'='+Addd0(mysplit2[count])+',\n')
									count+=1
							else:
								if totco == len(allLines) and (k1+1) == int(rowaux2[k][1]):
									ecri.write('     &		'+mysplit1[0]+str(k1+1)+'='+Addd0(mysplit2[count])+'\n')
								else:
									ecri.write('     &		'+mysplit1[0]+str(k1+1)+'='+Addd0(mysplit2[count])+',\n')
								count+=1								
			else:
				if totco == len(allLines):
					ecri.write('     &		'+Addd0(l)+'\n')
				else:
					ecri.write('     &		'+Addd0(l)+',\n')
		ecri.write('     &)\n')
		ecri.close()


	scri = open('MainFT.F', 'w')
	today = date.today()
	mydate = today.strftime("%B %d, %Y")
	scri.write('*-----------------------------------------------------------------------*\n')
	scri.write('* This program was automatically generated by FeynMaster \n')
	scri.write('* ' + mydate + '\n')
	scri.write('* ' + mycom + '\n')
	scri.write('*-----------------------------------------------------------------------*\n')
	scri.write('      program FCtoFT\n')
	scri.write('      implicit none\n')
	scri.write('      integer i\n')
	scri.write('      '+Goreal+' Pi\n\n')
	if myloops == '1':
		scri.write('      '+Goreal+' lbd2,mu2    ! For LoopTools\n')	
	if myprocess == 'scat':
		scri.write('      integer npoints\n')
		scri.write('      '+Goreal+' rs,fx,a,b,integral\n')
		scri.write('      external fx\n')
		scri.write('      common /MyData/S\n\n')
	else:
		scri.write('      '+Gocomplex+' My'+tag+'\n\n')
	if myloops == '1':
		scri.write('#include "looptools.h"\n')
	scri.write('#include "MyVariables.h"\n')
	scri.write('#include "MyParameters.h"\n\n')
	if myloops == '1':
		scri.write('      call ltini\n\n')
	scri.write('      open(50,file=\'FTout.dat\',status=\'unknown\')  \n\n')
	scri.write('      Pi=acos(-1.d0)\n\n')
	scri.write('* Write now the rest of the program\n')
	if myprocess == 'scat':
		scri.write('\n\n')
		scri.write('      npoints=8\n')
		if myloops == '1':
			scri.write('      rs=10d0 -0.5d0 + 1d-6\n')
		else:
			scri.write('      rs=10d0 -0.5d0\n')
		scri.write('      a=0d0\n')
		scri.write('      b=Pi\n')
		if myloops == '1':
			scri.write('      do i=1,981\n')
		else:
			scri.write('      do i=1,901\n')
		scri.write('         rs=rs+0.5d0\n')
		scri.write('         S=rs**2\n\n')
		scri.write('         call gauss1D(npoints, fx, a, b, integral)\n')
		scri.write('         write(50,98)rs,integral\n\n')
		scri.write('      enddo\n\n')
	else:
		scri.write('\n\n\n\n\n\n')
	scri.write('* Final declarations:\n')
	if myloops == '1':
		scri.write('      call ltexi\n\n')
	scri.write(' 98   format(6(e13.5,1x))\n\n')
	scri.write('      end\n')
	if myprocess == 'scat':
		scri.write('\n\n')
		scri.write('* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *\n')
		scri.write('      '+Goreal+' function fx(Theta)\n')
		scri.write('      implicit none\n')
		scri.write('#include "MyVariables.h"\n')
		scri.write('#include "MyParameters.h"\n')
		scri.write('      '+Goreal+' Pi\n')
		scri.write('      '+Goreal+' factor\n')
		scri.write('      '+Gocomplex+' My'+tag+',fxCmplx\n')
		scri.write('      common /MyData/S\n\n')
		scri.write('*\n')
		scri.write('***  1GeV^(-2)= 3.893795 10^(8) pb (Conversion factor)\n')
		scri.write('*\n\n')
		scri.write('      factor=3.893795d+08\n\n')
		scri.write('      Pi=acos(-1d0)\n\n')
		scri.write('      fxCmplx='+thestr1[26:])
		scri.write('      fx=real(fxCmplx) * factor * 2d0*Pi * sin(Theta)\n\n')
		scri.write('      return\n')
		scri.write('      end\n')
		scri.write('* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *\n')
	scri.close()

	mlist = ['My'+tag+'.F','MainFT.F','MyVariables.h','MyParameters.h','Makefile-template']
	for i5 in range(newcount):
		mlist.append('MyAux_' + tag + '_' + str(i5+1) + '.F')
	if myprocess == 'scat':
		mlist.append('IntGauss.f')
	with zipfile.ZipFile('movendum.zip', 'w') as zipMe:        
	    for file in mlist:
	        zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)
	if myprocess == 'scat':
		for i5 in range(len(mlist)-1):
			os.remove(mlist[i5])
	else:
		for i5 in range(len(mlist)):
			os.remove(mlist[i5])

