# > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
# This is the Drawing.py file, a Python routine where we draw the Feynman diagrams. 
# 
# Created by: Duarte Fontes
# Email: duartefontes@tecnico.ulisboa.pt
# Last Update: 01.10.2021
# > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >

import os,sys,re

import General
(Qlist,Qanlist,LAlist,LAanlist,csclT,felT,cgalT,ghlT,scl,gal,bealT) = General.somelists()

import FRExtract
(nscl,cscl,ancscl,fel,anfel,ngal,cgal,ancgal,ghl,anghl,glul,beal,anbeal,LAnscl,LAcscl,LAancscl,LAfel,LAanfel,LAngal,LAcgal,LAancgal,LAghl,LAanghl,LAglul,LAbeal,LAanbeal) = FRExtract.FRlists()

import ControlExtract
(Seq,Loo,ParS,Fac,Opt) = ControlExtract.processes()

SeqInd = 0
if len(sys.argv) == 2:
	inputFile = sys.argv[1]
elif len(sys.argv) == 3:
	inputFile = sys.argv[1]
	SeqInd = sys.argv[2]

# create lists of particles which obey a certain order
ordcomb = felT + ghlT
ordalt = csclT
ordext = csclT + cgalT
ordbig = felT + csclT + ghlT + cgalT

# basic function to read the QGRAF output
def splitter(arg, type):
	fun = re.findall(r"(?<="+type+r"\()(.*)(?=\))", arg)[0]
	pre = re.findall(r"(\w+)(?=\()", fun)
	args = re.findall(r"(?<=\()(.*?)(?=\))", fun)

	b = []
	for i in range(len(pre)):
		a1 = []
		for a in args[i].split(','):
			if a[0] == '-':
				if a[1:].isdigit():
					a1.append('-J' + a[1:])
				else:
					a1.append(a[:])
			else:
				if a.isdigit():
					a1.append('J' + a[:])
				else:
					a1.append(a[:])
		b.append((pre[i], a1))
	return b

def drawing(inargs,outargs,index,sid,all,d):
	b = []
	aux = all[:]

	for i in range(len(sid)):
		if 'prop' in sid[i]:
			b.append(splitter(sid[i],'prop'))
		elif 'vrtx' in sid[i]:
			b.append(splitter(sid[i],'vrtx'))   

	#basic in&out definitions
	im = ['p1','p2','p3','p4']
	inaux1=[]       #  - - - - - QGRAF indices
	inaux2=[]       #  - - - - - particle names
	for i in range(len(aux)):
		for j in range(len(b[i])):
			if any(b[i][j][1][1] == x for x in im) and '-' in b[i][j][1][0]:
				inaux1.append(b[i][j][1][0])
				inaux2.append(b[i][j][0])
	inp=''      #  - - - - - all the QGRAF indices of the in particles
	numin=len(inaux1)     #  - - - - - number of the in particles
	om = ['-q1','-q2','-q3','-q4']
	outaux1=[]      #  - - - - - QGRAF indices
	outaux2=[]      #  - - - - - particle names
	for i in range(len(aux)):
		for j in range(len(b[i])):
			if any(b[i][j][1][1] == x for x in om) and '-' in b[i][j][1][0]:
				outaux1.append(b[i][j][1][0])
				outaux2.append(b[i][j][0])                
	out=''      #  - - - - - all the QGRAF indices of the out particles
	numout=len(outaux1)     #  - - - - - number of the out particles

	# ascertain the number of (internal) propagators
	pnum = 0    
	for i in range(len(aux)):
		if len(b[i]) == 2:
			pnum += 1      

	# if there is a propagator with zero momentum (tadpole)
	tadpre = 0
	for i in range(len(b)):
		for j in range(len(b[i])):
			if b[i][j][1][1] == 'J0':       #  - - - - - although it's a momentum, and not a normal J index, it has a J, since all isolated numbers gain a precedent J 
				tadpre += 1

	# if the diagram is reducible but does not have tadpoles
	redecnotad = 0
	if tadpre == 0 and Loo[int(SeqInd)]!='0':
		for i in range(len(b)):
			if len(b[i]) == 2:
				for j in range(len(b[i])):
					if 'k' not in b[i][j][1][1]:
						redecnotad += 1

	# if the diagram is reducible and does have tadpoles
	tadp1 = 0; tadq1 = 0; tadq2 = 0; 
	redecwitad = 0
	if tadpre != 0:
		for i in range(len(b)):
			if len(b[i]) == 2:
				for j in range(len(b[i])):
					if 'k' not in b[i][j][1][1]:
						redecwitad += 1
						if 'p1' in b[i][j][1][1]:
							tadp1 = 1                             #  - - - - - tadp1 != 0 is when, in a two-body decay, the tadpole sprouts from the incoming particle
						elif 'q1' in b[i][j][1][1]:
							tadq1 = 1                             #  - - - - - tadq1 != 0 is when, in a two-body decay, the tadpole sprouts from the down outer particle
						elif 'q2' in b[i][j][1][1]:
							tadq2 = 1                             #  - - - - - tadq2 != 0 is when, in a two-body decay, the tadpole sprouts from the up outer particle

	# if a diagram is reducible with quartic vertex and a tadpole
	tadqua = 1 if (redecwitad != 0 and pnum==2) else 0
	# if a diagram is a self-energy with a tadpole
	tadinsel = 1 if (numin == 1 and numout == 1 and redecwitad != 0) else 0
	d.write('% \n')
	d.write('\\begin{subfigure}{2.5cm} \n')
	d.write('\\begin{fmffile}{' + str(index+1) + '} \n')
	# size of the Feynman graph
	if tadinsel != 0:
		d.write('\\begin{fmfgraph*}(90,150) \n')
	elif pnum == 1:
		d.write('\\begin{fmfgraph*}(100,70) \n')        
	elif pnum == 2 and redecwitad == 0:
		d.write('\\begin{fmfgraph*}(100,56) \n')
	elif pnum == 3:
		d.write('\\begin{fmfgraph*}(100,100) \n')
	elif pnum == 4:
		d.write('\\begin{fmfgraph*}(120,90) \n')
	else:
	   d.write('\\begin{fmfgraph*}(100,100) \n')
	d.write('\\fmfset{arrow_len}{3mm} \n')      #  - - - - - change the aspect of the arrow
	d.write('\\fmfset{arrow_ang}{20} \n')

	vert=[]
	for i in range(len(aux)):
		if len(b[i]) >= 3:
			vertaux=''
			for j in range(len(b[i])):
				vertaux+=b[i][j][1][0]
			vert.append(vertaux)

	# more in definitions
	if numin == 2:
		inaux4 = int(re.findall(r'\d+', inaux1[0])[0])        #  - - - - - to get the number in the QGRAF index
		inaux5 = int(re.findall(r'\d+', inaux1[1])[0])
		if inaux4 > inaux5:
			inp = inaux1[1] + ',' + inaux1[0] + ','
		else:
			inp = inaux1[0] + ',' + inaux1[1] + ','
	else:
		for i in range(len(inaux1)):
			inp += inaux1[i] + ','
	inp = inp [:-1]
	d.write('\\fmfleft{' + inp.replace('-','n') + '} \n')
	for i in range(len(inaux1)):
		if not any(inaux2[i] == x for x in ordcomb):        #  - - - - - labels for the non-fermionic particles
			if any(inaux2[i] == x for x in Qlist):
				for j in range(len(Qlist)):
					if inaux2[i]==Qlist[j]:
						pname = LAlist[j]
			elif any(inaux2[i] == x for x in Qanlist):
				for j in range(len(Qanlist)):
					if inaux2[i]==Qanlist[j]:
						pname = LAanlist[j]     
			d.write('\\fmflabel{$' + pname + '$}{' + inaux1[i].replace('-','n') + '} \n')

	# more out definitions
	cross=0     #  - - - - - cross != 0 is when the out particle which usually goes up (down) is going down (up); we will force it to go up (down)
	if numout == 2:
		outaux4 = int(re.findall(r'\d+', outaux1[0])[0])        #  - - - - - to get the number in the QGRAF index
		outaux5 = int(re.findall(r'\d+', outaux1[1])[0])
		if outaux4 > outaux5:
			out = outaux1[1] + ',' + outaux1[0] + ','
		else:
			out = outaux1[0] + ',' + outaux1[1] + ','
		if numin == 2:
			if Loo[int(SeqInd)]=='0':
				if (inaux4 < inaux5 and outaux4 > outaux5 and pnum != 0):
					cross = 1
			else:
				if (inaux4 > inaux5 and outaux4 < outaux5) or (inaux4 < inaux5 and outaux4 > outaux5):
					cross = 1
	else:
		for i in range(len(outaux1)):
			out += outaux1[i] + ','
	out = out [:-1]

	# if a digram is simply a tadpole, with nothing else
	justad = 1 if pnum == 1 and out == '' else 0

	if justad != 0:       #  - - - - - when the diagram is simply a tadpole
		d.write('\\fmfright{o1} \n')
	else:
		d.write('\\fmfright{' + out.replace('-','n') + '} \n')
		for i in range(len(outaux1)):
			if not any(outaux2[i] == x for x in ordcomb):       #  - - - - - labels for the fermionic particles
				if any(outaux2[i] == x for x in Qlist):
					for j in range(len(Qlist)):
						if outaux2[i]==Qlist[j]:
							pname = LAanlist[j]
				elif any(outaux2[i] == x for x in Qanlist):
					for j in range(len(Qanlist)):
						if outaux2[i]==Qanlist[j]:
							pname = LAlist[j]     
				d.write('\\fmflabel{$' + pname + '$}{' + outaux1[i].replace('-','n') + '} \n')

	# define the tensions (i.e., the sizes of the legs)
	if tadinsel != 0:
		tens = 50
	elif pnum == 1:
		tens = 1        
	elif pnum == 3:
		tens = 4
	else:
		tens = 3

	# define some topologies
	mark = 0        #  - - - - - mark != 0 is for the topology with 2 props and a vertex with one in and one out particle
	for i in range(len(outaux1)):
		for j in range(len(vert)):
			if outaux1[i] in vert[j]:
				if '-J1' in vert[j]:
					mark += 1
	indicA = 0        #  - - - - - indicA != 0 is for the topology with 3 props and a vertex with -3 and -4
	for i in range(len(vert)):
		if pnum == 3 and '-J3' in vert[i] and '-J4' in vert[i] and redecnotad == 0 and redecwitad == 0:
			indicA = 1
	indicB = 0        #  - - - - - indicB != 0 is for the topology with 3 props and a vertex with -1 and -2
	for i in range(len(vert)):
		if pnum == 3 and '-J1' in vert[i] and '-J2' in vert[i]  and redecnotad == 0 and redecwitad == 0:
			indicB = 1
	indicC = 0        #  - - - - - indicC != 0 is for the topology with 3 props and a vertex with -3 and -2
	for i in range(len(vert)):
		if cross != 0 and pnum == 3 and '-J3' in vert[i] and '-J2' in vert[i]  and redecnotad == 0 and redecwitad == 0:
			indicC = 1
	indicD = 0        #  - - - - - indicD != 0 is for the topology with 3 props and a vertex with -1 and -4
	for i in range(len(vert)):
		if cross != 0 and pnum == 3 and '-J1' in vert[i] and '-J4' in vert[i] and redecnotad == 0 and redecwitad == 0:
			indicD = 1

	#IN INTERACTIONS:
	tipo=''
	for i in range(len(inaux1)):
		for j in range(len(vert)):
			if inaux1[i] in vert[j]:
				needarrow=0        #  - - - - - needarrow is to give an arrow to the charged gauge boson propagators
				if any(inaux2[i] == x for x in nscl):
					tipo='dashes'                
				elif any(inaux2[i] == x for x in csclT):
					tipo='scalar'            
				elif any(inaux2[i] == x for x in felT):
					tipo='fermion'
				elif any(inaux2[i] == x for x in gal):
					tipo='photon'
					if any(inaux2[i] == x for x in cgalT):
						needarrow=1
				elif any(inaux2[i] == x for x in ghlT):
					tipo='ghost'
				elif any(inaux2[i] == x for x in glul):
					tipo='curly'
					d.write('\\fmfset{curly_len}{1.7mm} \n')        #  - - - - - change the aspect of the gluon propagator
				elif any(inaux2[i] == x for x in bealT):
					tipo='phantom'

				if cross == 1 and pnum == 2 and numin == 2 and numout == 2:
					tens = 2
				elif cross == 1 and pnum == 2 and mark != 0:
					tens = 40
				elif cross == 1 and pnum == 2 and mark == 0:
					tens = 3
				elif indicA == 1:
					if inaux1[i] == '-J1':
						tens = 3
					else:
						tens = 2
				elif indicB == 1:
					if inaux1[i] == '-J3':
						tens = 3
					else:
						tens = 2
				elif indicC == 1:
					if inaux1[i] == '-J1':
						tens = 2.5
					else:
						tens = 0.6
				elif indicD == 1:
					if inaux1[i] == '-J3':
						tens = 2.5
					else:
						tens = 0.6
				elif redecnotad != 0:
					if '-J2' in vert[j]:
						tens = 2
					elif '-J1-J4J1' in vert[j]:
						tens = 2
					elif '-J4' in vert[j]:
						tens = 5.5
					else:
						tens = 3
				elif redecwitad != 0:
					if tadp1 != 0:
						tens = 2
					elif tadq1 != 0 or tadq2 != 0:
						tens = 0.7
					elif '-J2' in vert[j] or '-J4' in vert[j]:
						tens = 2						
				if any(inaux2[i] == x for x in ordcomb):     #  - - - - - fermionic case
					if any(inaux2[i] == x for x in Qlist):
						for k in range(len(Qlist)):
							if inaux2[i]==Qlist[k]:
								pname = LAlist[k]
								d.write('\\fmf{' + tipo + ',label=$' + pname + '$,tension=' + str(tens) + '}{' + inaux1[i].replace('-','n') + ',' + vert[j].replace('-','n') + '} \n')
					elif any(inaux2[i] == x for x in Qanlist):
						for k in range(len(Qanlist)):
							if inaux2[i]==Qanlist[k]:
								pname = LAanlist[k]
								d.write('\\fmf{' + tipo + ',label=$' + pname + '$,tension=' + str(tens) + '}{' + vert[j].replace('-','n') + ',' + inaux1[i].replace('-','n') + '} \n')
				else:     #  - - - - - non fermionic case
					d.write('\\fmf{' + tipo + ',tension=' + str(tens) + '}{' + inaux1[i].replace('-','n') + ',' + vert[j].replace('-','n') + '} \n')
					if needarrow==1:
						needten=1 if inaux1[i] == vert[j] else 0
						d.write('\\fmf{phantom_arrow,tension=' + str(needten) + '}{' + inaux1[i].replace('-','n') + ',' + vert[j].replace('-','n') + '} \n')

	#OUT INTERACTIONS:
	tipo=''
	for i in range(len(outaux1)):
		for j in range(len(vert)):
			if outaux1[i] in vert[j]:
				needarrow=0
				if any(outaux2[i] == x for x in nscl):
					tipo='dashes'                
				elif any(outaux2[i] == x for x in csclT):
					tipo='scalar'
				elif any(outaux2[i] == x for x in felT):
					tipo='fermion'
				elif any(outaux2[i] == x for x in gal):
					tipo='photon'
					if any(outaux2[i] == x for x in cgalT):
						needarrow=1					
				elif any(outaux2[i] == x for x in ghlT):
					tipo='ghost'
				elif any(outaux2[i] == x for x in glul):
					tipo='curly'
					d.write('\\fmfset{curly_len}{1.7mm} \n')
				elif any(outaux2[i] == x for x in bealT):
					tipo='phantom'

				auxside = 'right'
				if numout == 3 and numin == 1 and Loo[int(SeqInd)]=='0':
					if '-J1' in vert[j]:
						tens = 0.35
					else:
						tens = 0.6
				elif redecnotad != 0 and pnum == 3:
					if '-J2' in vert[j] and '-J4' in vert[j]:
						tens = 1
					elif '-J1' in vert[j] and '-J2' in vert[j]:
						tens = 0.58
					elif '-J1' in vert[j] and '-J4' in vert[j]:
						tens = 0.7
					else:
						tens = 2	
				if redecwitad != 0 and pnum == 3:
					if tadp1 != 0:
						auxside = 'left'
						tens = 0.7
					elif tadq1 != 0:
						if '-J4' in vert[j]:
							tens = 0.7
						else:	
							tens = 2
					elif tadq2 != 0:
						if '-J2' in vert[j]:
							tens = 0.7
						else:	
							tens = 2					
					elif '-J1' in vert[j] and '-J2' in vert[j]:
						tens = 0.35
					elif '-J1' in vert[j] and '-J4' in vert[j]:
						tens = 0.5								
					elif '-J4' in vert[j]:
						tens = 0.7
					else:
						tens = 1

				if any(outaux2[i] == x for x in ordcomb):       #  - - - - - fermionic particles
					if numout == 2 and outaux1[i] == '-J4' and '-J1' in vert[j] and redecnotad == 0 and redecwitad == 0 and pnum >0:
						if any(outaux2[i] == x for x in Qanlist):
							for k in range(len(outaux1)):
								if outaux1[k] != outaux1[i]:
									for m in range(len(Qanlist)):
										if outaux2[i]==Qanlist[m]:
											pname = LAlist[m]
											d.write('\\fmf{phantom}{' + vert[j].replace('-','n') + ',' + outaux1[k].replace('-','n') + '} \n')
											d.write('\\fmf{' + tipo + ',label=$' + pname + '$,tension=0}{' + vert[j].replace('-','n') + ',' + outaux1[i].replace('-','n') + '} \n')
						elif any(outaux2[i] == x for x in Qlist):
							for k in range(len(outaux1)):
								if outaux1[k] != outaux1[i]:
									for m in range(len(Qlist)):
										if outaux2[i]==Qlist[m]:
											pname = LAanlist[m]
											d.write('\\fmf{phantom}{' + outaux1[k].replace('-','n') + ',' + vert[j].replace('-','n') + '} \n')
											d.write('\\fmf{' + tipo + ',label=$' + pname + '$,tension=0}{' + outaux1[i].replace('-','n') + ',' + vert[j].replace('-','n') + '} \n')
					elif numout == 2 and outaux1[i] == '-J2' and '-J3' in vert[j] and redecnotad == 0 and pnum >0:
						if any(outaux2[i] == x for x in Qanlist):
							for k in range(len(outaux1)):
								if outaux1[k] != outaux1[i]:
									for m in range(len(Qanlist)):
										if outaux2[i]==Qanlist[m]:
											pname = LAlist[m]
											d.write('\\fmf{phantom}{' + vert[j].replace('-','n') + ',' + outaux1[k].replace('-','n') + '} \n')
											d.write('\\fmf{' + tipo + ',label=$' + pname + '$,tension=0}{' + vert[j].replace('-','n') + ',' + outaux1[i].replace('-','n') + '} \n')
						else:
							for k in range(len(outaux1)):
								if outaux1[k] != outaux1[i]:
									for m in range(len(Qlist)):
										if outaux2[i]==Qlist[m]:
											pname = LAanlist[m]                                    
											d.write('\\fmf{phantom}{' + outaux1[k].replace('-','n') + ',' + vert[j].replace('-','n') + '} \n')
											d.write('\\fmf{' + tipo + ',label=$' + pname + '$,tension=0}{' + outaux1[i].replace('-','n') + ',' + vert[j].replace('-','n') + '} \n')
					elif numout == 2 and cross == 1 and redecnotad == 0 and pnum >0:
						if any(outaux2[i] == x for x in Qlist):
							for i2 in range(len(outaux1)):
								if i2 != i:
									d.write('\\fmf{phantom}{' + outaux1[i2].replace('-','n') + ',' + vert[j].replace('-','n') + '} \n')
							for m in range(len(Qlist)):
								if outaux2[i]==Qlist[m]:
									pname = LAanlist[m]                                             
							d.write('\\fmf{' + tipo + ',label=$' + pname + '$,tension=0}{' + outaux1[i].replace('-','n') + ',' + vert[j].replace('-','n') + '} \n')
						else:
							for i2 in range(len(outaux1)):
								if i2 != i:
									d.write('\\fmf{phantom}{' + vert[j].replace('-','n') + ',' + outaux1[i2].replace('-','n') + '} \n')
							for m in range(len(Qanlist)):
								if outaux2[i]==Qanlist[m]:
									pname = LAlist[m]
							d.write('\\fmf{' + tipo + ',label=$' + pname + '$,tension=0}{' + vert[j].replace('-','n') + ',' + outaux1[i].replace('-','n') + '} \n')             
					else:
						if any(outaux2[i] == x for x in Qanlist):
							for m in range(len(Qanlist)):
								if outaux2[i]==Qanlist[m]:
									pname = LAlist[m]
							d.write('\\fmf{' + tipo + ',label=$' + pname + '$,label.side=' + auxside + ',tension=' + str(tens) + '}{' + vert[j].replace('-','n') + ',' + outaux1[i].replace('-','n') + '} \n')
						else:
							for m in range(len(Qlist)):
								if outaux2[i]==Qlist[m]:
									pname = LAanlist[m]                          
							d.write('\\fmf{' + tipo + ',label=$' + pname + '$,label.side=' + auxside + ',tension=' + str(tens) + '}{' + outaux1[i].replace('-','n') + ',' + vert[j].replace('-','n') + '} \n')
				else:       #  - - - - - non-fermionic particles
					if cross == 1:
						for i2 in range(len(outaux1)):
							if i2 != i:
								if numin == 2 and numout == 2 and pnum == 2:
									d.write('\\fmf{phantom}{' + outaux1[i2].replace('-','n') + ',' + vert[j].replace('-','n') + '} \n')
								elif pnum == 2 and i == 0:
									if mark == 0:
										tens = 1
									else:
										tens = 2
									d.write('\\fmf{phantom,tension=' + str(tens) + '}{' + outaux1[i2].replace('-','n') + ',' + vert[j].replace('-','n') + '} \n')
								elif pnum == 2:
									if mark == 0:
										tens = 1
									else:
										tens = 10
									d.write('\\fmf{phantom,tension=' + str(tens) + '}{' + outaux1[i2].replace('-','n') + ',' + vert[j].replace('-','n') + '} \n')
								else:
									d.write('\\fmf{phantom}{' + outaux1[i2].replace('-','n') + ',' + vert[j].replace('-','n') + '} \n')
						if numin == 2 and numout == 2 and pnum == 2:
							tens = 0
						elif pnum == 2 and i == 0:
							if mark == 0:
								tens = 1
							else:
								tens = 10
						elif pnum == 2:
							if mark == 0:
								tens = 1
							else:
								tens = 70                           
						else:
							if indicC == 1:
								if outaux1[i] == '-J4':
									tens = 0.05
								else:
									tens = 0
							elif indicD == 1:
								if outaux1[i] == '-J2':
									tens = 0.05
							else:
									tens = 0                                
						d.write('\\fmf{' + tipo +',tension=' + str(tens) + '}{' + outaux1[i].replace('-','n') + ',' + vert[j].replace('-','n') + '} \n')
						if needarrow==1:
							needten=1 if outaux1[i] == vert[j] else 0
							d.write('\\fmf{phantom_arrow,tension=' + str(needten) +'}{' + vert[j].replace('-','n') + ',' + outaux1[i].replace('-','n') + '} \n')
					else:        #  - - - - - no cross
						if indicA == 1:
							if outaux1[i] == '-J2':
								tens = 3
							else:
								tens = 2
						elif indicB == 1:
							if outaux1[i] == '-J4':
								tens = 3
							else:
								tens = 2
						elif redecnotad != 0:
							if vert[j] == '-J1-J2J1' or vert[j] == '-J1-J4J1':
								tens = 0.7
							else:
								tens = 3
						if any(outaux2[i] == x for x in ordalt):
							d.write('\\fmf{' + tipo +',tension=' + str(tens) + '}{' + vert[j].replace('-','n') + ',' + outaux1[i].replace('-','n') + '} \n')
						else:
							d.write('\\fmf{' + tipo +',tension=' + str(tens) + '}{' + outaux1[i].replace('-','n') + ',' + vert[j].replace('-','n') + '} \n')
							if needarrow==1:
								needten=1 if outaux1[i] == vert[j] else 0
								d.write('\\fmf{phantom_arrow,tension=' + str(needten) +'}{' + vert[j].replace('-','n') + ',' + outaux1[i].replace('-','n') + '} \n')

	# PROPAGATORS:
	auxtad = []
	countaux = 0
	propcount = 0
	vertaju = []
	ajucount = 0
	propcumul = []
	sideaux1 = 'right'

	if pnum == 2 and tadinsel == 0:        #  - - - - - to define the circulation (left or right) of propagation when there are only 2 propagators
		for i in range(len(aux)):
			if len(b[i]) == 2:
				countaux +=1
				if countaux == 1:
					X1 = b[i][0][0] + b[i][0][1][0]
				elif countaux == 2:
					X2 = b[i][0][0] + b[i][0][1][0] 
		for i in range(len(aux)):
			if len(b[i]) > 2:
				for j in range(len(b[i])):
					Y = b[i][j][0] + b[i][j][1][0]
					vertaju.append(Y)
				break
			else:
				continue
		for k in range(len(vertaju)):
			if X1 == vertaju[k]:
				ajucount += 1
			if X2 == vertaju[k]:
				ajucount += 1
		sideaux1 = 'right'
		if (ajucount == 0 or ajucount == 2):
			sideaux2 = 'left'
		else:
			sideaux2 = 'right'  

	for i in range(len(aux)):
		if len(b[i]) == 2:
			propcount += 1
			paux1=[]
			paux2=[]
			paux3=[]
			tipo=''
			for k in range(len(vert)):
				if b[i][1][1][0] in vert[k]:
					tem = vert[k].split(b[i][1][1][0])
					for m in range(len(tem)-1):
						if (tem[m][-1:] == '' and not tem[m+1][:1].isdigit()) or (tem[m][-1:].isdigit() and tem[m+1][:1] == '') or (tem[m][-1:].isdigit() and not tem[m+1][:1].isdigit()):
							paux1.append(vert[k])
							paux2.append(b[i][1][0])
							paux3.append(b[i][1][1][1])
							break			
					else:
						continue
					break   #  - - - - - close the k cycle 
			for k in range(len(vert)):
				if b[i][0][1][0] in vert[k]:
					tem = vert[k].split(b[i][0][1][0])
					for m in range(len(tem)-1):
						if (tem[m][-1:] == '' and not tem[m+1][:1].isdigit()) or (tem[m][-1:].isdigit() and tem[m+1][:1] == '') or (tem[m][-1:].isdigit() and not tem[m+1][:1].isdigit()):
							paux1.append(vert[k])
							paux2.append(b[i][0][0])
							paux3.append(b[i][0][1][1])
							break		
					else:
						continue
					break   #  - - - - - close the k cycle
			needarrow=0 
			if any(paux2[1] == x for x in nscl):
				tipo='dashes'
			elif any(paux2[1] == x for x in csclT):
				tipo='scalar'
			elif any(paux2[1] == x for x in felT):
				tipo='fermion'
			elif any(paux2[1] == x for x in gal):
				tipo='photon'
				if any(paux2[1] == x for x in cgalT):
					needarrow=1				
			elif any(paux2[1] == x for x in ghlT):
				tipo='ghost'
			elif any(paux2[1] == x for x in glul):
				tipo='curly'
				d.write('\\fmfset{curly_len}{1.7mm} \n')
			prop=''

			for j in range(len(paux1)):
				prop += paux1[j] + ','
			prop = prop [:-1]
			propcumul.append(prop)

			if any(paux2[1] == x for x in Qlist):
				for j in range(len(Qlist)):
					if paux2[1]==Qlist[j]:
						pname = LAlist[j]
			elif any(paux2[1] == x for x in Qanlist):
				for j in range(len(Qanlist)):
					if paux2[1]==Qanlist[j]:
						pname = LAanlist[j]
			if paux3[0] == 'J0':                    #  - - - - - for the cases with tadpoles
				if redecwitad != 0 and tadp1 == 0 and tadinsel == 0 and tadqua == 0:
					d.write('\\fmfright{tad} \n')
				else:
					d.write('\\fmftop{tad} \n')	
			if paux1[0] == paux1[1] and redecwitad != 0:
					if tadinsel==0:
						d.write('\\fmf{' + tipo + ',label=$' + pname + '$,tension=0.05,right=1}{' + paux1[0].replace('-','n') + ',' + 'tad' + ',' + paux1[1].replace('-','n') + '} \n')
						if needarrow==1:
							d.write('\\fmf{phantom_arrow,tension=0,right=1}{' + paux1[0].replace('-','n') + ',' + 'tad' + ',' + paux1[1].replace('-','n') + '} \n')
					else:
						d.write('\\fmf{' + tipo + ',label=$' + pname + '$,right=1}{' + paux1[0].replace('-','n') + ',' + 'tad' + ',' + paux1[1].replace('-','n') + '} \n')
						if needarrow==1:
							d.write('\\fmf{phantom_arrow,tension=0,right=1}{' + paux1[0].replace('-','n') + ',' + 'tad' + ',' + paux1[1].replace('-','n') + '} \n')
			else:              									#  - - - - - for all the other cases 
				if justad != 0:                        #  - - - - - when the diagram is but a tadpole
					d.write('\\fmf{' + tipo + ',label=$' + pname + '$,right=1}{' + paux1[0].replace('-','n') + ',' + 'o1' + ',' + paux1[1].replace('-','n') + '} \n')
					if needarrow==1:
						d.write('\\fmf{phantom_arrow,tension=0,right=1}{' + paux1[0].replace('-','n') + ',' + 'o1' + ',' + paux1[1].replace('-','n') + '} \n')
				elif pnum == 2 and paux3[0] != 'J0':      #  - - - - - when there are only two propagators and no tadpole
					if propcount == 1:
						if numin == 2 and numout == 2 and cross != 0:
							d.write('\\fmf{' + tipo + ',label=$' + pname + '$,' + sideaux1 + '=1,tension=0.3}{' + prop.replace('-','n') + '} \n')
							if needarrow==1:
								needten=1 if prop.split(',')[0] == prop.split(',')[1] else 0
								d.write('\\fmf{phantom_arrow,tension=' + str(needten) + ',' + sideaux1 + '=1}{' + prop.replace('-','n') + '} \n')
						else:
							rotesp = str(1) if redecnotad == 0 else str(0.3)
							d.write('\\fmf{' + tipo + ',label=$' + pname + '$,' + sideaux1 + '=' + rotesp + '}{' + prop.replace('-','n') + '} \n')
							if needarrow==1:
								needten=1 if prop.split(',')[0] == prop.split(',')[1] else 0
								d.write('\\fmf{phantom_arrow,tension=' + str(needten) + ',' + sideaux1 + '=' + rotesp + '}{' + prop.replace('-','n') + '} \n')
					elif propcount == 2:
						if numin == 2 and numout == 2 and cross != 0:
							d.write('\\fmf{' + tipo + ',label=$' + pname + '$,label.dist=1thick,tension=0}{' + prop.replace('-','n') + '} \n')
							if needarrow==1:
								needten=1 if prop.split(',')[0] == prop.split(',')[1] else 0
								d.write('\\fmf{phantom_arrow,tension=' + str(needten) + '}{' + prop.replace('-','n') + '} \n')
						else:
							d.write('\\fmf{' + tipo + ',label=$' + pname + '$,' + sideaux2 + '=1}{' + prop.replace('-','n') + '} \n')
							if needarrow==1:
								needten=1 if prop.split(',')[0] == prop.split(',')[1] else 0
								d.write('\\fmf{phantom_arrow,tension=' + str(needten) + ',' + sideaux2 + '=1}{' + prop.replace('-','n') + '} \n')
				elif pnum == 3 and redecnotad != 0:      #  - - - - - when there are exactly three propagators and the diagram is reducible but without tadpoles
					if propcount == 1:
						if 'p' in paux3[0] and 'k' not in paux3[0]:
							tens=2.5
						elif 'q' in paux3[0] and 'k' not in paux3[0]:
							tens=2
						d.write('\\fmf{' + tipo + ',label=$' + pname + '$,tension=' + str(tens) + '}{' + prop.replace('-','n') + '} \n')
						if needarrow==1:
							needten=1 if prop.split(',')[0] == prop.split(',')[1] else 0
							d.write('\\fmf{phantom_arrow,tension=' + str(needten) + '}{' + prop.replace('-','n') + '} \n')
					else:
						if len(propcumul)>1 and propcumul[propcount-1]==propcumul[propcount-2]: sideaux1 = 'left'
						d.write('\\fmf{' + tipo + ',label=$' + pname + '$,label.side=' + sideaux1 + ',' + sideaux1 + '=1,tension=0.8}{' + prop.replace('-','n') + '} \n')
						if needarrow==1:
							needten=1 if prop.split(',')[0] == prop.split(',')[1] else 0
							d.write('\\fmf{phantom_arrow,' + sideaux1 + '=1,tension=' + str(needten) + '}{' + prop.replace('-','n') + '} \n')
				else:
					tens = 1
					indside = 'left'
					inddist = '3thick'
					addtext = 0
					if tadinsel != 0:
						tens = 1.5
					elif numout == 3 and numin == 1 and Loo[int(SeqInd)]=='0':
						indside = 'right'
					elif redecwitad != 0 and ('J6J5J4' in paux1[0] or 'J4J5J6' in paux1[0] or 'J5J6J4' in paux1[0]):
						tens = 0.1
						indside = 'right' if (tadp1 != 0 or tadq2 != 0)  else 'left'
					elif tadqua != 0:
						tens = 0.1
					elif tadp1 != 0 and 'J3-J1J2' in paux1[0]:
						tens = 0.5
					elif '-' not in paux1[0] and '-' not in paux1[1]:
						tens = 0
					elif '-J1' in paux1[0] and '-J2' in paux1[1]:
						if indicA == 1:
							tens = 0.1
						elif indicC == 1:
							tens = 0.66                         
						elif indicD == 1:
							indside = 'left'
							tens = 0.18
						elif cross != 0 and pnum == 3:
							indside = 'left'
						else:
							indside = 'right'
						if cross == 1 and pnum == 1:
							indside = 'left'
					elif '-J1' in paux1[0] and '-J3' in paux1[1]:
						indside = 'left'
						if indicD == 1:
							tens = 0.66
					elif '-J1' in paux1[0] and '-J4' in paux1[1]:
						if indicC == 1:
							tens = 0.2
							indside = 'right'   
						elif cross == 1:
							tens = 0.6
							indside = 'right'
						elif pnum == 4:
							addtext = 1
							paux2[1] = '\\hspace{13mm}' + pname + '\\hspace{13mm}'
							inddist = '-13thick'                            
						elif '-J2' not in paux1[0]:
							indside = 'left'                        
						else:
							indside = 'right'
					elif '-J2' in paux1[0] and '-J1' in paux1[1]:
						if '-J3' not in paux1[0]:
							indside = 'left'
						else:
							indside = 'right'
						if indicA == 1:
							tens = 0.1
						elif indicC == 1:
							tens = 0.66
						elif indicD == 1:
							tens = 0.18
							indside = 'right'
					elif '-J2' in paux1[0] and '-J3' in paux1[1]:
						indside = 'right'
						if indicD == 1:
							tens = 0.2
						elif cross == 1:
							tens = 0.6
						elif pnum == 4:
							addtext = 1
							paux2[1] = '\\hspace{13mm}' + pname + '\\hspace{13mm}'
							inddist = '-13thick'
					elif '-J2' in paux1[0] and '-J4' in paux1[1]:
						indside = 'right'
						if indicC == 1:
							tens = 0.18
						elif cross == 1:
							tens = 0.34
					elif '-J3' in paux1[0] and '-J1' in paux1[1]:
						indside = 'right'
						if indicD == 1:
							tens = 0.66
					elif '-J3' in paux1[0] and '-J2' in paux1[1]:
						indside = 'left'
						if indicD == 1:
							tens = 0.2
						elif cross == 1:
							tens = 0.6
						elif pnum == 4:
							addtext = 1
							paux2[1] = '\\hspace{13mm}' + pname + '\\hspace{13mm}'
							inddist = '-13thick'
					elif '-J3' in paux1[0] and '-J4' in paux1[1]:
						indside = 'left'
						if indicB == 1:
							tens = 0.1
					elif '-J4' in paux1[0] and '-J1' in paux1[1]:
						indside = 'right'
						if indicC == 1:
							tens = 0.2
							indside = 'left'
						elif cross == 1:
							tens = 0.6
							indside = 'left'
						elif pnum == 4:
							addtext = 1
							paux2[1] = '\\hspace{13mm}' + pname + '\\hspace{13mm}'
							inddist = '-13thick'
					elif '-J4' in paux1[0] and '-J2' in paux1[1]:
						indside = 'left'
						if indicC == 1:
							tens = 0.18
						elif cross == 1:
							tens = 0.34
					elif '-J4' in paux1[0] and '-J3' in paux1[1]:
						indside = 'right'
						if indicB == 1:
							tens = 0.1                      
					if addtext == 0:
						d.write('\\fmf{' + tipo + ',label=$' + pname + '$,label.side=' + indside + ',tension=' + str(tens) + ',label.dist=' + inddist + '}{' + prop.replace('-','n') + '} \n')
						if needarrow==1:
							needten=1 if prop.split(',')[0] == prop.split(',')[1] else 0
							d.write('\\fmf{phantom_arrow,tension=' + str(needten) + '}{' + prop.replace('-','n') + '} \n')
					else:
						d.write('\\fmf{' + tipo + ',label=$' + paux2[1] + '$,label.side=' + indside + ',tension=' + str(tens) + ',label.dist=' + inddist + '}{' + prop.replace('-','n') + '} \n')
						if needarrow==1:
							needten=1 if prop.split(',')[0] == prop.split(',')[1] else 0
							d.write('\\fmf{phantom_arrow,tension=' + str(needten) + '}{' + prop.replace('-','n') + '} \n')

	d.write('\\end{fmfgraph*} \n')
	d.write('\\end{fmffile} \n')
	if tadinsel != 0:
		d.write('\\vspace{-2.5cm} \n')
	d.write('\\begin{center} \n')
	d.write('\\hspace{8mm} \n')
	d.write('\\textcolor{mycolor}{$' + str(index+1)+ '$} \n')
	d.write('\\end{center} \n')    
	d.write('\\end{subfigure} \n')
	d.write('% \n')
	ancila = index+1
	if ancila % 12 == 0:
		d.write('\\end{figure} \n')
		d.write('% \n')
		d.write('% \n')
		d.write('\\begin{figure}[htp] \\ContinuedFloat \n')
	elif ancila % 3 == 0:
		d.write('% \n')
		if pnum == 3:
			d.write('\\\\[5mm] \n') 
		else:
			d.write('\\\\[10mm] \n') 
		d.write('% \n')
	else:
		d.write('\\hspace{2.8cm} \n')

	return ()