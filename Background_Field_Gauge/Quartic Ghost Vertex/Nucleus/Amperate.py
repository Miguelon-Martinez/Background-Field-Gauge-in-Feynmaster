# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - -
# This is Amperate.py, a Python routine that converts the QGRAF output into a file with the amplitudes.
#
# Created by: António Lacerda
# Developed by: Duarte Fontes
# Email: duartefontes@tecnico.ulisboa.pt
# Last Update: 09.09.2020
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import os,sys,re

import FRExtract
(nscl,cscl,ancscl,fel,anfel,ngal,cgal,ancgal,ghl,anghl,glul,beal,anbeal,LAnscl,LAcscl,LAancscl,LAfel,LAanfel,LAngal,LAcgal,LAancgal,LAghl,LAanghl,LAglul,LAbeal,LAanbeal) = FRExtract.FRlists()
(intname,extname,FCsimp,FCeqs,PrMassFL,GFreno,FRrestr,mygluon,gaugegslist,gslist,mycomplex) = FRExtract.FRextra()

import General
(Qlist,Qanlist,LAlist,LAanlist,csclT,felT,cgalT,ghlT,scl,gal,bealT) = General.somelists()
import Drawing

import ControlExtract
(Seq,Loo,ParS,Fac,Opt) = ControlExtract.processes()
(FRinterLogic,Draw,Comp,FinLogic,DivLogic,RenoLogic,SumLogic,MoCoLogic,LoSpi) = ControlExtract.selection()

# rmbar removes the 'bar', that is, turns anti-particles into particles
def rmbar(stri):
	aux = stri[:-3] if stri[-3:] == 'bar' else stri
	return aux

# chbar checks whether the string at stake ends in 'bar', that is, checks if it is an anti-particle
def chbar(stri):
	aux = True if stri[-3:] == 'bar' else False
	return aux

# We start by adding the auxiliary beaks for the fermion fields to the total fermion list
for i in range(len(bealT)):
	if len(bealT[i])<4:
		felT.append(bealT[i])

# We take care of the colour factor
Nclist='Nclist.m'
if os.path.isfile(Nclist):
	f1 = open(Nclist, 'r');
	f2 = f1.read()
	MyNcpre = f2[1:-1].split(', ')
	MyNc=[]
	for i in range(len(MyNcpre)):
		MyNc.append(MyNcpre[i])
		# MyNc.append(MyNcpre[i].upper())
	f1.close()	

# LAargs will be used to write the subtitles of the set of the Feynman diagrams 
LAargs = []
for k1 in range(len(Seq)):
	LAargs.append([])
	for k2 in range(len(Seq[k1])):
		LAargs[k1].append([])
		LAargs[k1][k2] = ''
for i in range(len(Seq)):
	for j in range(len(Seq[i])):
		for k in range(len(Seq[i][j])):
			if any(Seq[i][j][k] == x for x in Qlist):
				for m in range(len(Qlist)):
					if Seq[i][j][k] == Qlist[m]:
						LAargs[i][j] += LAlist[m] + ','
			elif any(Seq[i][j][k] == x for x in Qanlist):
				for m in range(len(Qanlist)):
					if Seq[i][j][k] == Qanlist[m]:
						LAargs[i][j] += LAanlist[m] + ','
for i in range(len(LAargs)):
	for j in range(len(LAargs[i])):
		LAargs[i][j] = LAargs[i][j][:-1]

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

def buildJArray(arg):
	jArray = []
	for b1 in arg:
		for j in b1[1]:
			if j[0] == 'J':
				jArray.append(j)
	return jArray

def handleFirst(arg):
	num = re.findall(r"[(](.*)[)]", arg)[0]
	sign = arg[0]
	if sign == '+' and num == '1':
		built = ''
	elif sign == '+':
		built = '(' + num + ')'
	else:
		built = '(' + sign + num + ')'
	return built

def handleProp(arg,opt):	
	type = 'prop'
	b = splitter(arg, type)
	myp=b[0][0]
	if opt == 'ugauge' and any(b[0][0] == x for x in gaugegslist):
		myp+='UG'
	built = type+myp+'[m'+b[0][0]+','+b[0][1][1]+','+b[0][1][0]+','+b[1][1][0]+']'
	return (buildJArray(b), built)

def handleVrtx(arg):
	type = 'vrtx'
	b = splitter(arg, type)
	preStr = ''
	argStr = ''
	for s in b:
		preStr = preStr + s[0]
		argStr = argStr + ',' + ','.join(s[1])
	argStr = argStr[1:]
	built = type+preStr+'['+argStr+']'
	return (buildJArray(b), built)


def buildFinalStr(sid,all):
	b = []
	for i in range(len(sid)):
		if 'prop' in sid[i]:
			b.append(splitter(sid[i],'prop'))
		elif 'vrtx' in sid[i]:
			b.append(splitter(sid[i],'vrtx'))   

	im = ['p1','p2','p3','p4']
	om = ['-q1','-q2','-q3','-q4']
	em = []
	for i in range(len(im)):
		em.append(im[i])
	for i in range(len(om)):
		em.append(om[i])

	prefac=all[0][1]
	all.pop(0)
	aux = all[:]
	comp = ''

	ordpurset = ['']          # ordpurset will have to do with those fermionic lines which have only internal lines (i.e., are not connected with external fermionic lines)
	ordpurcount = 0				# ordpurcount counts the number of closed loops of fermions
	ordpurint = ''				# ordpurint is an auxiliary for # ordpurset
	ordpurext = ''         # ordpurext will have to do with those fermionic lines which have only external lines (i.e., are not connected with internal fermionic lines)
	ordco = ''                  # ordco will have to do with those fermionic lines which have both external and internal sections
	resto = ''                   # resto concerns vertices and propagators which do not involve fermionic particles	
	final = ''                    # final is the final string, which joins ordpurset, ordpurext, ordco and resto
	totfvertin = 0			# totfvertin and glufvertin have to do with SUN trace
	glufvertin = 0
	Ncflag=1					# Ncflag has to do with the colour factor for quarks


	 # The first thing to do is ascertain whether there are diagrams with external (in or out) fermions connected with internal fermionic propagators;
	 # if there are, we must assure that we start in the end of the line.

	for h in range(len(sid)):
		# So first, we ascertain whether there are fermionic lines whose order is relevant and which have out particles flowing from left to right
		if comp == '':
			for i in range(len(aux)):
				if len(b[i]) >= 3:
					for j in range(len(b[i])):
						if any(b[i][j][0] == x for x in felT) and '-' in b[i][j][1][0] and chbar(b[i][j][0]): # if the vertex i has an outgoing fermion flowing from left to right
							for k in range(len(b[i])):
								if b[i][j][1][0] != b[i][k][1][0] and any(b[i][k][0] == x for x in felT) and '-' not in b[i][k][1][0]: #if there is an internal fermionic propagator in vertex i
									comp = b[i][k][1][0]
									spinaux1 = ''
									if LoSpi == True:
										spinaux1 = 'SpinorUBarD[(-1)*(' + b[i][j][1][1] + '), m' + rmbar(b[i][j][0]) + '] . '
									ordco +=  spinaux1 + aux[i][1] + ' . '
									aux.pop(i)
									b.pop(i)
									break
								else:
									continue
								break       # close the k cycle 
						else:
							continue
						break      # close the j cycle
					else:
						continue
					break          # close the i cycle
		# Now, we ascertain whether there are fermionic lines whose order is relevant but do not have out particles flowing from left to right
		if comp == '':
			for i in range(len(aux)):
				if len(b[i]) >= 3:
					for j in range(len(b[i])):
						if any(b[i][j][0] == x for x in felT) and any(b[i][j][1][1] == x for x in im) and chbar(b[i][j][0]): # if the vertex i has an incoming fermion flowing from right to left
							for k in range(len(b[i])):
								if b[i][j][1][0] != b[i][k][1][0] and any(b[i][k][0] == x for x in felT) and '-' not in b[i][k][1][0]: #if there is an internal fermionic propagator in vertex i
									comp = b[i][k][1][0]
									spinaux2 = ''
									if LoSpi == True:
										spinaux2 = 'SpinorVBarD[' + b[i][j][1][1] + ', m' + rmbar(b[i][j][0]) + '] . '
									ordco += spinaux2 + aux[i][1] + ' . '
									aux.pop(i)
									b.pop(i)
									break
								else:
									continue
								break       # close the k cycle 
						else:
							continue
						break      # close the j cycle
					else:
						continue
					break          # close the i cycle
		# Finally, we cover the cases with external fermions which are not connected with internal fermionic lines
		if comp == '':
			for i in range(len(aux)):
				if len(b[i]) >= 3:
					for j in range(len(b[i])):
						if any(b[i][j][0] == x for x in felT) and any(b[i][j][1][1] == x for x in em): # if the vertex i has an external (in or out) fermion j
							for k in range(len(b[i])):
								if any(b[i][k][0] == x for x in felT) and any(b[i][k][1][1] == x for x in em) and b[i][j][1][0] != b[i][k][1][0]: # if, besides j, the vertex i has another external fermion, k
									if any(b[i][j][1][1] == x for x in om) and chbar(b[i][j][0]): #if the j fermion is an outgoing fermion flowing from left to right
										if any(b[i][k][1][1] == x for x in im) and not chbar(b[i][k][0]): #if the k fermion is an incoming fermion flowing from left to right
											spinaux3 = ''
											spinaux4 = ' '                                   
											if LoSpi == True:
												spinaux3 = 'SpinorUBarD[(-1)*(' + b[i][j][1][1] + '), m' + rmbar(b[i][j][0]) + '] . '
												spinaux4 = ' . SpinorUD[' + b[i][k][1][1] + ', m' + rmbar(b[i][k][0]) + '] '
											ordpurext += spinaux3 + aux[i][1] + spinaux4
											aux.pop(i)
											b.pop(i)
											break      # close the k cycle
										elif any(b[i][k][1][1] == x for x in om) and not chbar(b[i][k][0]): #if the k fermion is an outgoing fermion flowing from right to left
											spinaux3 = ''
											spinaux4 = ' '                                   
											if LoSpi == True:
												spinaux3 = 'SpinorUBarD[(-1)*(' + b[i][j][1][1] + '), m' + rmbar(b[i][j][0]) + '] . '
												spinaux4 = ' . SpinorVD[(-1)*(' + b[i][k][1][1] + '), m' + rmbar(b[i][k][0]) + '] '
											ordpurext += spinaux3 + aux[i][1] + spinaux4
											aux.pop(i)
											b.pop(i)
											break      # close the k cycle
									elif any(b[i][j][1][1] == x for x in im) and chbar(b[i][j][0]): #if the j fermion is an incoming fermion flowing from right to left
										if any(b[i][k][1][1] == x for x in om) and not chbar(b[i][k][0]): #if the k fermion is an outgoing fermion flowing from right to left
											spinaux3 = ''
											spinaux4 = ' '                                   
											if LoSpi == True:
												spinaux3 = 'SpinorVBarD[' + b[i][j][1][1] + ', m' + rmbar(b[i][j][0]) + '] . '
												spinaux4 = ' . SpinorVD[(-1)*(' + b[i][k][1][1] + '), m' + rmbar(b[i][k][0]) + '] '
											ordpurext += spinaux3 + aux[i][1] + spinaux4
											aux.pop(i)
											b.pop(i)
											break      # close the k cycle
										elif any(b[i][k][1][1] == x for x in im) and not chbar(b[i][k][0]): #if the k fermion is an incoming fermion flowing from left to right
											spinaux3 = ''
											spinaux4 = ' '                                   
											if LoSpi == True:
												spinaux3 = 'SpinorVBarD[' + b[i][j][1][1] + ', m' + rmbar(b[i][j][0]) + '] . '
												spinaux4 = ' . SpinorUD[' + b[i][k][1][1] + ', m' + rmbar(b[i][k][0]) + '] '
											ordpurext += spinaux3 + aux[i][1] + spinaux4
											aux.pop(i)
											b.pop(i)
											break      # close the k cycle
								else:
									continue
								break      # close the k cycle (if it was not closed in the meantime)
						else:
							continue
						break      # close the j cycle
					else:
						continue
					break          # close the i cycle                                  
		for i in range(len(aux)):
			if len(b[i]) >= 3:            #  VERTICES
				if comp == '': # if comparator is null
					feind = 0
					gaind = 0
					for j in range(len(b[i])):
						if any(b[i][j][0] == x for x in felT):   # count the nº of fermions
							feind += 1
						if any(b[i][j][0] == x for x in gal):  # count the nº of gauge bosons
							gaind += 1
					if feind == 0:    # if there are no fermions in the vertex
						resto += aux[i][1] + ' '
						aux.pop(i)
						b.pop(i)
						break         # OK: closes the i cycle
					else:              # if there are fermions in the vertex
						for j in range(len(b[i])):
							if any(b[i][j][0] == x for x in felT):   # if j is a fermion
								comp = b[i][j][1][0]
								myinicomp=comp
								for k in range(len(b[i])):
									if comp != b[i][k][1][0] and any(b[i][k][0] == x for x in felT):
										comp = b[i][k][1][0]
										totfvertin += 1
										for k2 in range(len(b[i])):
											if any(b[i][k2][0] == x for x in glul):   # if k2 is a gluon
												glufvertin += 1
										ordpurint += aux[i][1] + ' . '
										if any(b[i][j][0] == x for x in MyNc) or any(b[i][k][0] == x for x in MyNc):   # if the fermion is a quark, we include a colour factor
											Ncflag = 3
										aux.pop(i)
										b.pop(i)
										break              # closes the k cycle
								else:
									continue
								break                      # closes the j cycle
						else:
							continue
						break                              # closes the i cycle
				else: # if comp non-null
					feind = 0
					gaind = 0
					for j in range(len(b[i])):
						if any(b[i][j][0] == x for x in felT):   # count the nº of fermions
							feind += 1
						if any(b[i][j][0] == x for x in gal):  # count the nº of gauge bosons
							gaind += 1                         
					if feind == 0:    # if there are no fermions in the vertex
						resto += aux[i][1] + ' '
						aux.pop(i)
						b.pop(i)
						break         # closes the i cycle
					else:              # if there are fermions in the vertex
						for j in range(len(b[i])):
							if comp != b[i][j][1][0]: #if the fermion at stake is not the relevant one
								continue
							elif comp == b[i][j][1][0]:
								for k in range(len(b[i])):
									if comp != b[i][k][1][0] and any(b[i][k][0] == x for x in felT):
										if '-' in b[i][k][1][0]: #if the fermion is an external fermion
											comp = ''
											spinaux11 = ' . '
											spinaux12 = ' . '
											spinaux13 = ' . '
											spinaux14 = ' . '
											if LoSpi == True:
												spinaux11 = ' . SpinorVBarD[' + b[i][k][1][1] + ', m' + rmbar(b[i][k][0]) + ']   '
												spinaux12 = ' . SpinorUD[' + b[i][k][1][1] + ', m' + rmbar(b[i][k][0]) + ']   '
												spinaux13 = ' . SpinorUBarD[(-1)*(' + b[i][k][1][1] + '), m' + rmbar(b[i][k][0]) + ']   '
												spinaux14 = ' . SpinorVD[(-1)*(' + b[i][k][1][1] + '), m' + rmbar(b[i][k][0]) + ']   '                                             
											if '-' not in b[i][k][1][1] and chbar(b[i][k][0]):
												ordco += aux[i][1] + spinaux11
											elif '-' not in b[i][k][1][1] and not chbar(b[i][k][0]):
												ordco += aux[i][1] + spinaux12
											elif '-' in b[i][k][1][1] and chbar(b[i][k][0]):
												ordco += aux[i][1] + spinaux13
											elif '-' in b[i][k][1][1] and not chbar(b[i][k][0]):
												ordco += aux[i][1] + spinaux14
										else:  #if the fermion is not an external fermion
											compaux1 = '[' + comp
											compaux2 = ',' + comp + ','
											compaux3 = ',' + comp + ']'										
											comp = b[i][k][1][0]
											if compaux1 in ordco or compaux2 in ordco or compaux3 in ordco:
												ordco += aux[i][1] + ' . '
											elif compaux1 in ordpurint or compaux2 in ordpurint or compaux3 in ordpurint:
												totfvertin += 1
												for k2 in range(len(b[i])):
													if any(b[i][k2][0] == x for x in glul):   # if k2 is a gluon
														glufvertin += 1
												ordpurint += aux[i][1] + ' . '
												if any(b[i][j][0] == x for x in MyNc) or any(b[i][k][0] == x for x in MyNc):   # if the fermion is a quark, we include a colour factor
													Ncflag = 3
										aux.pop(i)
										b.pop(i)
										break # closes the k cycle                           
								else:
									continue
								break # closes the j cycle
						else:
							continue
						break          # closes the i cycle                             
			else:                         #  PROPAGATORS
				feind = 0
				for j in range(len(b[i])):
					if any(b[i][j][0] == x for x in felT):   # count the nº of fermions
						feind += 1                
				if feind == 0:          # if the prop has no fermions
					resto += aux[i][1] + ' '
					aux.pop(i)
					b.pop(i)
					break # closes the i cycle
				elif comp == '':   # if prop has fermions, but if it is the first prop, jump
					continue
				else:    # if prop has fermions, and it is not the first prop
					for j in range(len(b[i])):
						if comp != b[i][j][1][0]: #if the fermion at stake is not the relevant one
							continue
						else:
							for k in range(len(b[i])):
								if comp != b[i][k][1][0]:
									compaux1 = '[' + comp
									compaux2 = ',' + comp + ','
									compaux3 = ',' + comp + ']'
									comp = b[i][k][1][0]
									compaux4 = '[' + comp
									compaux5 = ',' + comp + ','
									compaux6 = ',' + comp + ']'									
									if compaux1 in ordco or compaux2 in ordco or compaux3 in ordco:
										if compaux4 in ordco or compaux5 in ordco or compaux6 in ordco:
											comp = ''
										ordco += aux[i][1] + ' . '
									elif compaux1 in ordpurint or compaux2 in ordpurint or compaux3 in ordpurint:
										ordpurint += aux[i][1] + ' . '
										if comp==myinicomp:
											comp=''
											ordpurset.append('')
											ordpurcount += 1
											ordpurset[ordpurcount-1]=ordpurint
											ordpurint = ''
										if any(b[i][j][0] == x for x in MyNc) or any(b[i][k][0] == x for x in MyNc):   # if the fermion is a quark, we include a colour factor
											Ncflag = 3
									aux.pop(i)
									b.pop(i)
									break  # closes the k cycle
							else:
								continue
							break  # closes the j cycle                     
					else:
						continue
					break  # closes the i cycle                      

	for i in range(len(ordpurset)-1):
		ordpurset[i] = ordpurset[i][:-3]
	ordco = ordco [:-2]
	resto = resto [:-1]

	if ordpurint != ['']:
		mytraux=''
		if totfvertin == glufvertin:
			for i in range(len(ordpurset)-1):
				mytraux+='SUNTrace[TrG5['+ordpurset[i]+']] '
			if Ncflag != 1:
				ordpurint = '('+str(Ncflag)+') ' + mytraux
			else:
				ordpurint = mytraux
		else:
			for i in range(len(ordpurset)-1):
				mytraux+='TrG5['+ordpurset[i]+'] '			
			if Ncflag != 1:
				ordpurint = '('+str(Ncflag)+') ' + mytraux
			else:
				ordpurint = mytraux

	final = ordpurext + ordco + ordpurint + resto

	p=[]
	for t in range(len(gal)):
		p.append('prop' + gal[t] + '[')
	if any(x in final for x in p):
		final = 'Contract[' + final + ']'

	col=[]
	for t in range(len(felT)):
		col.append('prop' + felT[t] + '[')
	if prefac != '':
		final = prefac + ' ' + final

	return final

def writeResult(inArgs, outArgs, allStrs, fname):
	f = open(fname, 'w')
	for i in range(len(allStrs)):
		f.write('amp'+str(i+1)+':= '+allStrs[i]+'\n')
	f.close()

def readInput(fname = 'Output-QGRAF'):
	f = open(fname, 'r')
	allLines = f.read().splitlines()
	f.close()

	formulas = []
	formula = ''

	for l in allLines:
		# If no info on that line, it has no interest
		if len(l) == 0: continue

		# Remove the leading space since it has no interest
		l = l.lstrip(' ')

		if l[0] == '#':
			# Comment lines -> search for input and output arguments
			if 'in= ' in l:
				if 'in= ;' in l or 'in=;' in l:
					inArgs = ''
				else:
					inArgs = ''.join(re.findall(r"(?<=\=\s)(.+)(?=;)", l)[0].split(','))
			elif 'out= ' in l:
				if 'out= ;' in l or 'out=;' in l:
					outArgs = ''    
				else:
					outArgs = ''.join(re.findall(r"(?<=\=\s)(.+)(?=;)", l)[0].split(','))

		elif l[0] in ['+', '-', ';']:
			# new formula
			if formula != '':
				formulas.append(formula)
			formula = l
		
		elif formula != '':
			formula += l

	return (inArgs, outArgs, formulas)

inputFile = 'output-qgraf'
outputFile = 'Amplitudes.m'

SeqInd = 0
if len(sys.argv) == 2:
	inputFile = sys.argv[1]
elif len(sys.argv) == 3:
	inputFile = sys.argv[1]
	SeqInd = sys.argv[2]

(inArgs, outArgs, strs) = readInput(inputFile)

allStrs = []
fdraw = open('diagrams.tex', 'w')
fdraw.write('\\documentclass[a4paper,12pt,twoside]{report} \n \n')
fdraw.write('\\usepackage{subcaption} \n')
fdraw.write('\\usepackage{feynmp-auto} \n')
fdraw.write('\\usepackage{color} \n \n')
fdraw.write('\\makeatletter \n')
fdraw.write('\\setlength{\@fptop}{10pt} \n')
fdraw.write('\\makeatother \n \n')
fdraw.write('\\definecolor{mycolor}{RGB}{165,111,29}\n \n')
fdraw.write('\\begin{document} \n \n')
fdraw.write('\\begin{figure}[htp] \n')
fdraw.write('\\centering \n')

imax = 0
for inputStr in strs:
	allRes = []
	again=[]

	for res in re.findall(r"(.*?)(?=$|\*)", inputStr):
		if res == '':
			continue
		elif res[0] == '+' or res[0] == '-':
			retStr = handleFirst(res)
			allRes.append(([], retStr))
			jArray = ['0']
		elif 'prop' in res:
			(jArray, retStr) = handleProp(res,Opt[int(SeqInd)])
			allRes.append((jArray, retStr))
			again.append(res)           
		elif 'vrtx' in res:
			(jArray, retStr) = handleVrtx(res)
			allRes.append((jArray, retStr))
			again.append(res)

	allStrs.append(buildFinalStr(again,allRes))
	if Draw:
		Drawing.drawing(inArgs,outArgs,imax,again,allRes,fdraw)
	imax += 1

auxopt = ''
auxopt2 = 's'
auxsel = 'Complete'
if Opt[int(SeqInd)]=='onepi':
	auxopt = '1PI'
if str(Loo[int(SeqInd)]) == "1":
	auxopt2 = ''
if (ParS!=[]):
	if (ParS[int(SeqInd)]!=[]):
		auxsel = 'Selected'
myto=' \\to ' + LAargs[int(SeqInd)][1] if LAargs[int(SeqInd)][1]!='' else ' \\, \\textrm{tadpole}'
if str(Loo[int(SeqInd)]) != "0":
	fdraw.write('\\caption{' + auxsel + ' set of ' + auxopt + ' Feynman diagrams contributing to the process $'+ LAargs[int(SeqInd)][0] + myto + '$ at $' + str(Loo[int(SeqInd)]) + '$ loop' + auxopt2 + ' in ' + extname + '} \n')
else:
	fdraw.write('\\caption{' + auxsel + ' set of ' + auxopt + ' Feynman diagrams contributing to the process $'+ LAargs[int(SeqInd)][0] + myto + '$ at tree-level in ' + extname + '} \n')
fdraw.write('\\vspace{1cm}\n')
fdraw.write('\\raggedright\n')
fdraw.write('FeynMaster,\\\\[1mm]\n')
fdraw.write('\\today \n')
fdraw.write('\\end{figure} \n\n')
fdraw.write('\\end{document} \n \n')
fdraw.close()
writeResult(inArgs, outArgs, allStrs,'Amplitudes.m')