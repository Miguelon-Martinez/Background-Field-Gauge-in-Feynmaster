# > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
# This is the General.py file, a Python routine where we chain all the other programs.
# We create several auxiliary files: not only Mathematica files, which will serve as
# support for either the FeynRules environment or the FeynCalc environment, but also
# batch files, which allow Windows or Linux or Mac to run all the relevant programs
# in an automatic sequence.
#
# Created by: Duarte Fontes
# Email: duartefontes@tecnico.ulisboa.pt
# Last Update: 25.05.2021
# > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >

import os,sys,re,glob,time

starttime = time.time()

FMversion='2.0.2'
FMdate='September 28, 2021'

import FRExtract
(nscl,cscl,ancscl,fel,anfel,ngal,cgal,ancgal,ghl,anghl,glul,beal,anbeal,LAnscl,LAcscl,LAancscl,LAfel,LAanfel,LAngal,LAcgal,LAancgal,LAghl,LAanghl,LAglul,LAbeal,LAanbeal) = FRExtract.FRlists()
(CTtot,renoparams,CTelsparams,renconsnum,LArenconsnum,renconstens,LArenconstens,renconstensdims,renorrules) = FRExtract.FRreno()
(intname,extname,FCsimp,FCeqs,PrMassFL,GFreno,FRrestr,mygluon,gaugegslist,gslist,mycomplex) = FRExtract.FRextra()

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import ControlExtract
(Seq,Loo,ParS,Fac,Opt) = ControlExtract.processes()
(FRinterLogic,Draw,Comp,FinLogic,DivLogic,RenoLogic,SumLogic,MoCoLogic,LoSpinors) = ControlExtract.selection()
(dirFM,dirFR,dirFRmod,dirMain,dirQ,dirQmod,dirPro,dirFey,dirCT) = ControlExtract.directories()

# - - - - - - - - - - - - - - - - - What follows is only going to be run if General.py is not being imported by other routines
if __name__ == '__main__':
	#
	# Printing name of the program, authors, etc.
	print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	print('FeynMaster')
	print('created by Duarte Fontes and Jorge C. Romao')
	print('version ' + FMversion + ' (' + FMdate + ')')
	print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	#
	# OS definition and basic errors
	from sys import platform
	if platform == "linux" or platform == "linux2":
	    osswitch = 'Linux'
	elif platform == "darwin":
	    osswitch = 'Mac'
	elif platform == "win32":
		osswitch = 'Windows'
	#
	if osswitch == 'Windows':
		dirNuc = dirFM + 'Nucleus\\'
	elif osswitch == 'Linux' or osswitch == 'Mac':
		dirNuc = dirFM + 'Nucleus/'

	flatSeq = []
	for s in Seq:
	    for ss in s:
	    	for i in ss:
	        	flatSeq.append(i)
	testfel=0
	for i in range(len(flatSeq)):
		if any(flatSeq[i] == x for x in fel) or any(flatSeq[i] == x for x in anfel):
			testfel+=1

	if len(nscl)!= len(LAnscl) or len(cscl)!= len(LAcscl) or len(ancscl)!= len(LAancscl) or len(fel)!= len(LAfel) or len(anfel)!= len(LAanfel) or len(ngal)!= len(LAngal) or len(cgal)!= len(LAcgal) or len(ancgal)!= len(LAancgal) or len(ghl)!= len(LAghl) or len(anghl)!= len(LAanghl) or len(glul)!= len(LAglul) or len(beal)!= len(LAbeal) or len(anbeal)!= len(LAanbeal):
		sys.exit("Model error: inconsistent number of at least one of the particles types and its LaTeX names \n")
	# if Comp and RenoLogic and not MoCoLogic:
	# 	sys.exit("Control error: when Comp and RenoLogic are both True, MoCoLogic should also be True \n")
	if Comp and RenoLogic and LoSpinors and testfel!=0:
		sys.exit("Control error: when Comp and RenoLogic are both True with external fermions, LoSpinors should be False \n")
	if RenoLogic and renorrules == []:
		sys.exit("Control error: RenoLogic should be False when there are no renormalization rules \n")
	if (not FRinterLogic and RenoLogic and not os.path.isdir(dirCT)) or (not FRinterLogic and RenoLogic and not os.path.isfile(dirCT+'CTini.m')):
		sys.exit("Control error: RenoLogic should be False when the Feynman rules for the counterterms were not yet generated \n")

# - - - - - - - - - - - - - - - - - OK, we go back to normal. Now, we merge lists in a way which shall be useful for what comes next
def somelists():
	Qlist = []
	for i in range(len(nscl)):
		Qlist.append(nscl[i])
	for i in range(len(cscl)):
		Qlist.append(cscl[i])
	for i in range(len(fel)):
		Qlist.append(fel[i])
	for i in range(len(ngal)):
		Qlist.append(ngal[i])
	for i in range(len(cgal)):
		Qlist.append(cgal[i])
	for i in range(len(ghl)):
		Qlist.append(ghl[i])
	for i in range(len(glul)):
		Qlist.append(glul[i])
	for i in range(len(beal)):
		Qlist.append(beal[i])

	Qanlist = []
	for i in range(len(nscl)):
		Qanlist.append(nscl[i])
	for i in range(len(ancscl)):
		Qanlist.append(ancscl[i])
	for i in range(len(anfel)):
		Qanlist.append(anfel[i])
	for i in range(len(ngal)):
		Qanlist.append(ngal[i])
	for i in range(len(ancgal)):
		Qanlist.append(ancgal[i])
	for i in range(len(anghl)):
		Qanlist.append(anghl[i])
	for i in range(len(glul)):
		Qanlist.append(glul[i])
	for i in range(len(anbeal)):
		Qanlist.append(anbeal[i])       

	LAlist = []
	for i in range(len(LAnscl)):
		LAlist.append(LAnscl[i])
	for i in range(len(LAcscl)):
		LAlist.append(LAcscl[i])
	for i in range(len(LAfel)):
		LAlist.append(LAfel[i])
	for i in range(len(LAngal)):
		LAlist.append(LAngal[i])
	for i in range(len(LAcgal)):
		LAlist.append(LAcgal[i])
	for i in range(len(LAghl)):
		LAlist.append(LAghl[i])
	for i in range(len(LAglul)):
		LAlist.append(LAglul[i])
	for i in range(len(LAbeal)):
		LAlist.append(LAbeal[i])        

	LAanlist = []
	for i in range(len(LAnscl)):
		LAanlist.append(LAnscl[i])
	for i in range(len(LAancscl)):
		LAanlist.append(LAancscl[i])
	for i in range(len(LAanfel)):
		LAanlist.append(LAanfel[i])
	for i in range(len(LAngal)):
		LAanlist.append(LAngal[i])
	for i in range(len(LAancgal)):
		LAanlist.append(LAancgal[i])
	for i in range(len(LAanghl)):
		LAanlist.append(LAanghl[i])
	for i in range(len(LAglul)):
		LAanlist.append(LAglul[i])
	for i in range(len(LAanbeal)):
		LAanlist.append(LAanbeal[i])            

	csclT = []
	for i in range(len(cscl)):
		csclT.append(cscl[i])
	for i in range(len(ancscl)):
		csclT.append(ancscl[i])

	felT = []
	for i in range(len(fel)):
		felT.append(fel[i])
	for i in range(len(anfel)):
		felT.append(anfel[i])

	cgalT = []
	for i in range(len(cgal)):
		cgalT.append(cgal[i])
	for i in range(len(ancgal)):
		cgalT.append(ancgal[i])

	ghlT = []
	for i in range(len(ghl)):
		ghlT.append(ghl[i])
	for i in range(len(anghl)):
		ghlT.append(anghl[i])

	scl = []
	for i in range(len(nscl)):
		scl.append(nscl[i])
	for i in range(len(csclT)):
		scl.append(csclT[i])

	gal = []
	for i in range(len(ngal)):
		gal.append(ngal[i])
	for i in range(len(cgalT)):
		gal.append(cgalT[i])

	bealT = []
	for i in range(len(beal)):
		bealT.append(beal[i])
	for i in range(len(anbeal)):
		bealT.append(anbeal[i])     

	return (Qlist,Qanlist,LAlist,LAanlist,csclT,felT,cgalT,ghlT,scl,gal,bealT)

(Qlist,Qanlist,LAlist,LAanlist,csclT,felT,cgalT,ghlT,scl,gal,bealT) = somelists()
scltot = nscl + csclT
galtot = ngal + cgalT

if len(sys.argv) == 2:
	if sys.argv[1]=="help":
		print("\n")
		print("********* Variables for Control **********")
		print("Variable          Default          Example")
		print("- - - - - - - - - - - - - - - - - - - - -")
		print("inparticles      (empty)           e,ebar")
		print("outparticles     (empty)           H,Z")
		print("loops            0                 1")
		print("parsel           (empty)           {avoid,Z,1,3},{keep,e,1,1}")
		print("factor           1                 16 Pi^2/I")
		print("options          (empty)           onepi")
		print("\n")
		print("****************** Avaliable options *******************")
		print("Options      Description                 Converse option")
		print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")
		print("ugauge       unitary gauge               (none)")
		print("noPVauto     PaVeAutoReduce -> False     (none)")
		print("onepi        1PI diagrams only           onepr")
		print("onshell      no external self-energies   offshell")
		print("nosigma      no self-energies at all     sigma")
		print("nosnail      no snails                   snail")
		print("notadpole    no tadpoles                 tadpole")
		print("simple       at most one propagator      notsimple")
		print("             between different vertices ")
		sys.exit()
	else:
		print("Particles of the FeynMaster model " + intname + ":")
		sys.exit(Qlist)

# - - - - - - - - - - - - - - - - - Now we protect the program against any choice of particles that are not defined in the model:
# Just to make sure that void particles are allowed (to allow tadpoles)
Qlistv=[]; Qanlistv=[]
for i in range(len(Qlist)):
	Qlistv.append(Qlist[i])
	Qanlistv.append(Qanlist[i])
Qlistv.append(''); Qanlistv.append('')
for i in range(len(Seq)):
	for j in range(len(Seq[i])):
		for k in range(len(Seq[i][j])):
			if Seq[i][j][k] not in Qlistv and Seq[i][j][k] not in Qanlistv:
				sys.exit("Control error: at least one of the external particles selected is not defined in the model \n")
for i in range(len(ParS)):
	for j in range(len(ParS[i])):
		if ParS[i][j][1] not in Qlist and ParS[i][j][1] not in Qanlist:
			sys.exit("Control error: at least one of the particles selected in Parsel is not defined in the model \n")

# - - - - - - - - - - - - - - - - - Function types() creates a list of all the types (scalar, fermion, etc.) of the particles involved in the
# - - - - - - - - - - - - - - - - - processes chosen at Control.py
def types():
	Typ = []
	for i in range(len(Seq)):
		Typ.append([])
		for j in range(len(Seq[i])):
			Typ[i].append([])
			for k in range(len(Seq[i][j])):
				Typ[i][j].append([])
	for i in range(len(Seq)):
		for j in range(len(Seq[i])):
			for k in range(len(Seq[i][j])):
				if Seq[i][j][k] == '':
					Typ[i][j][k] = 'phantom'
				elif any(Seq[i][j][k]  == x for x in scltot):
					Typ[i][j][k] = 'scalar'
				elif any(Seq[i][j][k]  == x for x in felT) or any(Seq[i][j][k]  == x for x in ghlT):
					Typ[i][j][k] = 'fermion'
				elif any(Seq[i][j][k]  == x for x in galtot):
					Typ[i][j][k] = 'gauge'
				elif any(Seq[i][j][k]  == x for x in glul):
					Typ[i][j][k] = 'gluon'
				elif any(Seq[i][j][k]  == x for x in bealT):
					Typ[i][j][k] = 'phantom'
	return (Typ)
Typ=types()

# - - - - - - - - - - - - - - - - - We create other useful lists for renormalization:
renconstensexpa = ''
for i in range(len(renconstens)):
	if len(renconstensdims[i])==1:
		for j in range(int(renconstensdims[i][0])):
			renconstensexpa +=  renconstens[i] + '[' + str(j+1) + ']' + ','
			for m in range(len(CTtot)):
				if renconstens[i]==CTtot[m][0]:
					if FRExtract.getarrow1(CTtot[m][1],'ComplexParameter')=='True':
						renconstensexpa +=  'Conjugate[' + renconstens[i] + '[' + str(j+1) + ']]' + ','
	elif len(renconstensdims[i])==2:
		for j in range(int(renconstensdims[i][0])):
			for k in range(int(renconstensdims[i][1])):
				renconstensexpa +=  renconstens[i] + '[' + str(j+1) + ',' + str(k+1) + ']' + ','
				for m in range(len(CTtot)):
					if renconstens[i]==CTtot[m][0]:
						if FRExtract.getarrow1(CTtot[m][1],'ComplexParameter')=='True':
							renconstensexpa += 'Conjugate[' +  renconstens[i] + '[' + str(j+1) + ',' + str(k+1) + ']]' + ','
renconstensexpa = renconstensexpa [:-1]

renps = ''
CTcor = ''
if len(renoparams) != len(CTelsparams):
	print("Model error: number of counterterms does not match renormalization rules for the parameters:\n")
	print("Renormalization rules:\n")
	for i in range(len(renoparams)):
		print(renoparams[i])
	print('Total: '+str(len(renoparams))+'\n\n')
	print("Parameter counterterms:\n")
	for i in range(len(CTelsparams)):
		print(CTelsparams[i])
	sys.exit('Total: '+str(len(CTelsparams))+'\n\n')
for i in range(len(renoparams)):
	renps += renoparams[i] + ','
	CTcor += CTelsparams[i] + ','
renps=renps[:-1]
CTcor=CTcor[:-1]

renconsadd = ''
renconsaddlist = []
LArenconsadd = ''
renconscar = ''
for i in range(len(renconsnum)):
	renconsadd += renconsnum[i] + ','
	renconsaddlist.append(renconsnum[i])
	renconscar += renconsnum[i] + ','
	LArenconsadd += '\"' + LArenconsnum[i].replace('\\','\\\\') + '\"' + ','
for i in range(len(renconstens)):
	renconsadd += renconstens[i] + ','
	renconsaddlist.append(renconstens[i])
	LArenconsadd += '\"' + LArenconstens[i].replace('\\','\\\\') + '\"' + ','
renconsadd = renconsadd [:-1]
LArenconsadd = LArenconsadd [:-1]
renconscar = renconscar [:-1]
renconslist = ''
for i in range(len(renconsnum)):
	renconslist += renconsnum[i] + ','
if renconstensexpa == '':
	renconslist = renconslist [:-1]
renconslist += renconstensexpa
ancR = ''
for i in range(len(renorrules)):
	ancR += renorrules[i] + ','     
ancR = ancR [:-1]
def toexport():
	return (renconsaddlist)


# - - - - - - - - - - - - - - - - - What follows is only going to be run if General.py is not being imported by other routines
if __name__ == '__main__':
	# - - - - - - - - - - - - - - - - - We now define what to do in the case the user wants to use the FeynRules interface
	if FRinterLogic == True:
		# - - - - - - - - - - - - - - - - - First, a list to establish a connection between particles and their respective antiparticles
		antimap=''
		for i in range(len(ancscl)):
			if ancscl[i] != '':
				antimap += ancscl[i] + '->' + cscl[i] + ', '
		for i in range(len(anfel)):
			if anfel[i] != '':
				antimap += anfel[i] + '->' + fel[i] + ', '
		for i in range(len(ancgal)):
			if ancgal[i] != '':
				antimap += ancgal[i] + '->' + cgal[i] + ', '
		for i in range(len(anghl)):
			if anghl[i] != '':
				antimap += anghl[i] + '->' + ghl[i] + ', '
		if antimap!='':
			antimap = antimap[:-2]
		antimap = '{'+antimap+'}'

		# gaugegslist2: gauge bosons with Goldstones
		gaugegslist2='{'
		for i in range(len(gaugegslist)):
			gaugegslist2+=gaugegslist[i]+', '
		if gaugegslist2!='{':
			gaugegslist2=gaugegslist2[:-2]
		gaugegslist2=gaugegslist2+'}'

		# - - - - - - - - - - - - - - - - - Ok. Now we create the PreControl.m file. This is thus an automatically generated file,
		# - - - - - - - - - - - - - - - - - which contains some preliminary informations about the model for the FeynRules environment
		f = open(''+dirFRmod+'PreControl.m', 'w')
		f.write('FMversion = "' + FMversion + '"; \n \n')
		f.write('FMdate = "' + FMdate + '"; \n \n')
		f.write('osswitch = "' + osswitch + '"; \n \n')
		f.write('antimap = ' + antimap + '; \n \n')
		f.write('PrMassFL = ' + str(PrMassFL) + '; \n \n')
		f.write('GaugeWithGold = ' + gaugegslist2 + '; \n \n')
		f.write('renps = {' + renps + '}; \n \n')
		f.write('CTcor = {' + CTcor + '}; \n \n')
		f.write('renconscar = {' + renconscar + '}; \n \n')
		f.write('renconsadd = {' + renconsadd + '}; \n \n')
		f.write('LArenconsadd = {' + LArenconsadd + '}; \n \n')         
		f.write('renconslist = {' + renconslist + '}; \n \n')
		f.write('GFreno = ' + str(GFreno) + '; \n \n')
		f.write('RenoLogic = ' + str(RenoLogic) + '; \n \n')
		f.write('renorrules = {' + ancR + '}; \n \n')           
		f.close()

		f = open(''+dirFRmod+'Execute.m', 'w')
		f.write('$FeynRulesPath =  SetDirectory[ "' + dirFR.replace('\\','/') + '"];\n')
		f.write('dirNuc = "' + dirNuc.replace('\\','/') + '";\n\n')
		f.write('Off[PacletManager`Name::shdw];\n')
		f.write('Off[FeynRules`Name::shdw]; \n')
		f.write('Off[CloudFunction::argt]; \n')
		f.write('Off[Syntax::stresc]; \n\n')		
		f.write('<< FeynRules`\n')
		f.write('dirFRmod = "' + dirFRmod.replace('\\','/') + '";\n')
		f.write('SetDirectory[dirFRmod];\n')
		f.write('LoadModel["' + intname + '.fr"];\n\n')
		if FRrestr != '':
			f.write('LoadRestriction[' + FRrestr + '];\n\n')
		f.write('<< PreControl.m\n')
		f.write('Get["Preamble.m", Path->{dirNuc}]\n\n')
		f.write('Get["Addendum.m", Path->{dirNuc}]\n')
		f.write('If[RenoLogic,\n')
		f.write('Get["Renapp.m", Path -> {dirNuc}]]; \n')    
		f.close()

		# - - - - - - - - - - - - - - - - - Here we create the Notebook.m file, automatically generated as well, which is equivalent to Execute.m, only
		# - - - - - - - - - - - - - - - - - this is a real Mathematica Notebook. This is useful if the user wants to have control over the Mathematica/
		# - - - - - - - - - - - - - - - - - FeynRules results, in which case he or she should work (non automatically) with the Notebook here created
		lido=open(''+dirFRmod+'Execute.m', 'r')
		allLines = lido.read().splitlines()
		lido.close()
		auxwri='' if osswitch=='Mac' else '\\n'
		f = open(''+dirFRmod+'Notebook.nb', 'w')
		f.write('Notebook[{Cell[BoxData["')
		for i7, i8 in enumerate(allLines):
			if i7 != len(allLines)-1:
				f.write(i8.replace('"','\\"') + '\n' + auxwri)
			else:
				f.write(i8.replace('"','\\"'))
		f.write('"], "Input"]}')
		if osswitch == 'Mac':
			f.write(',\n')
			f.write('WindowSize->{720, 855},\n')
			f.write('WindowMargins->{{Automatic, 0}, {Automatic, 0}}\n')
		f.write(']')
		f.close()

		# - - - - - - - - - - - - - - - - - We now create at batch file to run FeynRules and move certain files to the FeynCalc environment
		if osswitch == 'Windows':
			f = open(''+dirNuc+'FRinter.bat', 'w')
			f.write('@echo off \n')
			f.write('cd ' + dirFRmod + ' \n')
			f.write('copy Execute.m Test.nb \n')
			f.write('wolframscript -file Execute.m \n')
			f.write('del Test.nb \n')
			f.write('del Execute.m \n')
			f.write('if not exist ' + dirQmod + ' (mkdir ' + dirQmod + ') \n')
			f.write('move built-model ' + dirQmod + ' \n')
			f.write('cd ' + dirQmod + ' \n')
			f.write('if exist ' + intname + ' del ' + intname + ' \n')
			f.write('rename built-model ' + intname + ' \n')
			f.write('cd ' + dirNuc + ' \n')
			# - - - - - - - - We delete possible old files that might have remained in dirNuc
			f.write('if exist PrePropagators.m del PrePropagators.m \n')
			f.write('if exist PreRulesv3Higgs.m del PreRulesv3Higgs.m \n')
			f.write('if exist PreRulesv4Higgs.m del PreRulesv4Higgs.m \n')
			f.write('if exist PreRulesv3Gauge.m del PreRulesv3Gauge.m \n')
			f.write('if exist PreRulesv4Gauge.m del PreRulesv4Gauge.m \n')
			f.write('if exist PreRulesv3Fermions.m del PreRulesv3Fermions.m \n')
			f.write('if exist PreRulesv3Yukawa.m del PreRulesv3Yukawa.m \n')
			f.write('if exist PreRulesv3Ghosts.m del PreRulesv3Ghosts.m \n')
			f.write('if exist PreRulesv4Ghosts.m del PreRulesv4Ghosts.m \n')
			f.write('if exist PreRulesv3Beaks.m del PreRulesv3Beaks.m \n')
			f.write('if exist PreRulesv4Beaks.m del PreRulesv4Beaks.m \n')
			f.write('if exist PrePrintPropagators.m del PrePrintPropagators.m \n')
			f.write('if exist PrePrintRulesv3Higgs.m del PrePrintRulesv3Higgs.m \n')
			f.write('if exist PrePrintRulesv4Higgs.m del PrePrintRulesv4Higgs.m \n')
			f.write('if exist PrePrintRulesv3Gauge.m del PrePrintRulesv3Gauge.m \n')
			f.write('if exist PrePrintRulesv4Gauge.m del PrePrintRulesv4Gauge.m \n')
			f.write('if exist PrePrintRulesv3Fermions.m del PrePrintRulesv3Fermions.m \n')
			f.write('if exist PrePrintRulesv3Yukawa.m del PrePrintRulesv3Yukawa.m \n')
			f.write('if exist PrePrintRulesv3Ghosts.m del PrePrintRulesv3Ghosts.m \n')
			f.write('if exist PrePrintRulesv4Ghosts.m del PrePrintRulesv4Ghosts.m \n')
			f.write('if exist PrePrintRulesv3Beaks.m del PrePrintRulesv3Beaks.m \n')
			f.write('if exist PrePrintRulesv4Beaks.m del PrePrintRulesv4Beaks.m \n')            
			f.write('if exist PrePrintCTRulesv1Tads.m del PrePrintCTRulesv1Tads.m \n')
			f.write('if exist PrePrintCTRulesv2Props.m del PrePrintCTRulesv2Props.m \n')            
			f.write('if exist PrePrintCTRulesv3Higgs.m del PrePrintCTRulesv3Higgs.m \n')
			f.write('if exist PrePrintCTRulesv4Higgs.m del PrePrintCTRulesv4Higgs.m \n')
			f.write('if exist PrePrintCTRulesv3Gauge.m del PrePrintCTRulesv3Gauge.m \n')
			f.write('if exist PrePrintCTRulesv4Gauge.m del PrePrintCTRulesv4Gauge.m \n')
			f.write('if exist PrePrintCTRulesv3Fermions.m del PrePrintCTRulesv3Fermions.m \n')
			f.write('if exist PrePrintCTRulesv3Yukawa.m del PrePrintCTRulesv3Yukawa.m \n')
			f.write('if exist PrePrintCTRulesv3Ghosts.m del PrePrintCTRulesv3Ghosts.m \n')
			f.write('if exist PrePrintCTRulesv4Ghosts.m del PrePrintCTRulesv4Ghosts.m \n')
			f.write('if exist IndicesList.m del IndicesList.m \n')
			f.write('if exist FRtoTeX.m del FRtoTeX.m \n')
			f.write('if exist Extras.m del Extras.m \n')
			f.write('if exist ParamsValues.m del ParamsValues.m \n')
			f.write('if exist Matrixind.m del Matrixind.m \n')
			f.write('if exist Nclist.m del Nclist.m \n')
			# - - - - - - - - Ok, now we go on
			f.write('if not exist ' + dirMain + ' (mkdir ' + dirMain + ') \n')
			f.write('if not exist ' + dirPro + ' (mkdir ' + dirPro + ') \n')
			f.write('if not exist ' + dirFey + ' (mkdir ' + dirFey + ') \n')
			f.write('if not exist ' + dirCT + ' (mkdir ' + dirCT + ') \n')					
			f.write('py FRExtract.py \n')
			f.write('move Extras.m ' + dirFey + ' \n')
			f.write('move ParamsValues.m ' + dirFey + ' \n')
			f.write('move Matrixind.m ' + dirFey + ' \n')
			f.write('move Nclist.m ' + dirFey + ' \n')
			f.write('cd ' + dirFRmod + ' \n')			
			f.write('move Feynman-Rules-Main.m ' + dirFey + ' \n')
			f.write('if exist PrePropagators.m move PrePropagators.m ' + dirNuc + ' \n')
			f.write('if exist PreRulesv3Higgs.m move PreRulesv3Higgs.m ' + dirNuc + ' \n')
			f.write('if exist PreRulesv4Higgs.m move PreRulesv4Higgs.m ' + dirNuc + ' \n')
			f.write('if exist PreRulesv3Gauge.m move PreRulesv3Gauge.m ' + dirNuc + ' \n')
			f.write('if exist PreRulesv4Gauge.m move PreRulesv4Gauge.m ' + dirNuc + ' \n')
			f.write('if exist PreRulesv3Fermions.m move PreRulesv3Fermions.m ' + dirNuc + ' \n')
			f.write('if exist PreRulesv3Yukawa.m move PreRulesv3Yukawa.m ' + dirNuc + ' \n')
			f.write('if exist PreRulesv3Ghosts.m move PreRulesv3Ghosts.m ' + dirNuc + ' \n')
			f.write('if exist PreRulesv4Ghosts.m move PreRulesv4Ghosts.m ' + dirNuc + ' \n')
			f.write('if exist PreRulesv3Beaks.m move PreRulesv3Beaks.m ' + dirNuc + ' \n')
			f.write('if exist PreRulesv4Beaks.m move PreRulesv4Beaks.m ' + dirNuc + ' \n')
			f.write('if exist PrePrintPropagators.m move PrePrintPropagators.m ' + dirNuc + ' \n')
			f.write('if exist PrePrintRulesv3Higgs.m move PrePrintRulesv3Higgs.m ' + dirNuc + ' \n')
			f.write('if exist PrePrintRulesv4Higgs.m move PrePrintRulesv4Higgs.m ' + dirNuc + ' \n')
			f.write('if exist PrePrintRulesv3Gauge.m move PrePrintRulesv3Gauge.m ' + dirNuc + ' \n')
			f.write('if exist PrePrintRulesv4Gauge.m move PrePrintRulesv4Gauge.m ' + dirNuc + ' \n')
			f.write('if exist PrePrintRulesv3Fermions.m move PrePrintRulesv3Fermions.m ' + dirNuc + ' \n')
			f.write('if exist PrePrintRulesv3Yukawa.m move PrePrintRulesv3Yukawa.m ' + dirNuc + ' \n')
			f.write('if exist PrePrintRulesv3Ghosts.m move PrePrintRulesv3Ghosts.m ' + dirNuc + ' \n')
			f.write('if exist PrePrintRulesv4Ghosts.m move PrePrintRulesv4Ghosts.m ' + dirNuc + ' \n')
			f.write('if exist PrePrintRulesv3Beaks.m move PrePrintRulesv3Beaks.m ' + dirNuc + ' \n')
			f.write('if exist PrePrintRulesv4Beaks.m move PrePrintRulesv4Beaks.m ' + dirNuc + ' \n')
			if RenoLogic == True:			
				f.write('move CTpre.m ' + dirNuc + ' \n')
				f.write('if exist PrePrintCTRulesv1Tads.m move PrePrintCTRulesv1Tads.m ' + dirNuc + ' \n')
				f.write('if exist PrePrintCTRulesv2Props.m move PrePrintCTRulesv2Props.m ' + dirNuc + ' \n')
				f.write('if exist PrePrintCTRulesv3Higgs.m move PrePrintCTRulesv3Higgs.m ' + dirNuc + ' \n')
				f.write('if exist PrePrintCTRulesv4Higgs.m move PrePrintCTRulesv4Higgs.m ' + dirNuc + ' \n')
				f.write('if exist PrePrintCTRulesv3Gauge.m move PrePrintCTRulesv3Gauge.m ' + dirNuc + ' \n')
				f.write('if exist PrePrintCTRulesv4Gauge.m move PrePrintCTRulesv4Gauge.m ' + dirNuc + ' \n')
				f.write('if exist PrePrintCTRulesv3Fermions.m move PrePrintCTRulesv3Fermions.m ' + dirNuc + ' \n')
				f.write('if exist PrePrintCTRulesv3Yukawa.m move PrePrintCTRulesv3Yukawa.m ' + dirNuc + ' \n')
				f.write('if exist PrePrintCTRulesv3Ghosts.m move PrePrintCTRulesv3Ghosts.m ' + dirNuc + ' \n')
				f.write('if exist PrePrintCTRulesv4Ghosts.m move PrePrintCTRulesv4Ghosts.m ' + dirNuc + ' \n')          
			f.write('cd ' + dirNuc + ' \n')
			f.write('py Converter.py \n')
			f.write('if exist Propagators.m move Propagators.m ' + dirFey + ' \n')
			f.write('if exist Rulesv3Higgs.m move Rulesv3Higgs.m ' + dirFey + ' \n')
			f.write('if exist Rulesv4Higgs.m move Rulesv4Higgs.m ' + dirFey + ' \n')
			f.write('if exist Rulesv3Gauge.m move Rulesv3Gauge.m ' + dirFey + ' \n')
			f.write('if exist Rulesv4Gauge.m move Rulesv4Gauge.m ' + dirFey + ' \n')
			f.write('if exist Rulesv3Fermions.m move Rulesv3Fermions.m ' + dirFey + ' \n')
			f.write('if exist Rulesv3Yukawa.m move Rulesv3Yukawa.m ' + dirFey + ' \n')
			f.write('if exist Rulesv3Ghosts.m move Rulesv3Ghosts.m ' + dirFey + ' \n')
			f.write('if exist Rulesv4Ghosts.m move Rulesv4Ghosts.m ' + dirFey + ' \n')
			f.write('if exist Rulesv3Beaks.m move Rulesv3Beaks.m ' + dirFey + ' \n')
			f.write('if exist Rulesv4Beaks.m move Rulesv4Beaks.m ' + dirFey + ' \n')
			f.write('if exist CTpre.m del CTpre.m \n')
			f.write('if exist CTini.m move CTini.m ' + dirCT + ' \n')
			f.write('py Printer.py \n')
			dirFeyDraw = dirFey + 'TeXs-drawing\\'
			f.write('if not exist ' + dirFeyDraw + ' (mkdir ' + dirFeyDraw + ') \n')
			f.write('move DrawRules.tex ' + dirFeyDraw + ' \n')
			dirCTDraw = dirCT + 'TeXs-drawing\\'
			f.write('if not exist ' + dirCTDraw + ' (mkdir ' + dirCTDraw + ') \n')          
			f.write('move DrawCTRules.tex ' + dirCTDraw + ' \n')
			f.write('cd ' + dirFeyDraw + ' \n')
			f.write('pdflatex -interaction=nonstopmode --shell-escape DrawRules.tex \n')
			f.write('pdflatex -interaction=nonstopmode --shell-escape DrawRules.tex \n')
			f.write('start DrawRules.pdf \n')
			if RenoLogic == True:			
				f.write('cd ' + dirCTDraw + ' \n')
				f.write('pdflatex -interaction=nonstopmode --shell-escape DrawCTRules.tex \n')
				f.write('pdflatex -interaction=nonstopmode --shell-escape DrawCTRules.tex \n')
				f.write('start DrawCTRules.pdf \n')         
			f.close()
		elif osswitch == 'Linux' or osswitch == 'Mac':
			f = open(''+dirNuc+'FRinter.sh', 'w')
			f.write('cd ' + dirFRmod + ' \n')
			if osswitch == 'Linux':
				f.write('math -noprompt -script Execute.m \n')
			elif osswitch == 'Mac':
				f.write('wolframscript -file Execute.m \n')
			f.write('rm -f Execute.m \n')
			f.write('mkdir -p ' + dirQmod + '\n')
			f.write('mv built-model ' + dirQmod + ' \n')
			f.write('cd ' + dirQmod + ' \n')
			f.write('rm -f ' + intname + ' \n')
			f.write('mv built-model ' + intname + ' \n')
			f.write('cd ' + dirNuc + ' \n')
			f.write('rm -f PrePropagators.m \n')
			f.write('rm -f PreRulesv3Higgs.m \n')
			f.write('rm -f PreRulesv4Higgs.m \n')
			f.write('rm -f PreRulesv3Gauge.m \n')
			f.write('rm -f PreRulesv4Gauge.m \n')
			f.write('rm -f PreRulesv3Fermions.m \n')
			f.write('rm -f PreRulesv3Yukawa.m \n')
			f.write('rm -f PreRulesv3Ghosts.m \n')
			f.write('rm -f PreRulesv4Ghosts.m \n')
			f.write('rm -f PreRulesv3Beaks.m \n')
			f.write('rm -f PreRulesv4Beaks.m \n')
			f.write('rm -f PrePrintPropagators.m \n')
			f.write('rm -f PrePrintRulesv3Higgs.m \n')
			f.write('rm -f PrePrintRulesv4Higgs.m \n')
			f.write('rm -f PrePrintRulesv3Gauge.m \n')
			f.write('rm -f PrePrintRulesv4Gauge.m \n')
			f.write('rm -f PrePrintRulesv3Fermions.m \n')
			f.write('rm -f PrePrintRulesv3Yukawa.m \n')
			f.write('rm -f PrePrintRulesv3Ghosts.m \n')
			f.write('rm -f PrePrintRulesv4Ghosts.m \n')
			f.write('rm -f PrePrintRulesv3Beaks.m \n')
			f.write('rm -f PrePrintRulesv4Beaks.m \n')
			f.write('rm -f PrePrintCTRulesv1Tads.m \n')
			f.write('rm -f PrePrintCTRulesv2Props.m \n')
			f.write('rm -f PrePrintCTRulesv3Higgs.m \n')
			f.write('rm -f PrePrintCTRulesv4Higgs.m \n')
			f.write('rm -f PrePrintCTRulesv3Gauge.m \n')
			f.write('rm -f PrePrintCTRulesv4Gauge.m \n')
			f.write('rm -f PrePrintCTRulesv3Fermions.m \n')
			f.write('rm -f PrePrintCTRulesv3Yukawa.m \n')
			f.write('rm -f PrePrintCTRulesv3Ghosts.m \n')
			f.write('rm -f PrePrintCTRulesv4Ghosts.m \n')
			f.write('rm -f IndicesList.m \n')
			f.write('rm -f FRtoTeX.m \n')
			f.write('rm -f Extras.m \n')
			f.write('rm -f ParamsValues.m \n')
			f.write('rm -f Matrixind.m \n')
			f.write('rm -f Nclist.m \n')
			f.write('mkdir -p ' + dirMain + '\n')
			f.write('mkdir -p ' + dirPro + '\n')
			f.write('mkdir -p ' + dirFey + '\n')
			f.write('mkdir -p ' + dirCT + '\n')
			f.write('python3 FRExtract.py \n')
			f.write('mv Extras.m ' + dirFey + ' \n')			
			f.write('mv ParamsValues.m ' + dirFey + ' \n')
			f.write('mv Matrixind.m ' + dirFey + ' \n')
			f.write('mv Nclist.m ' + dirFey + ' \n')			
			f.write('cd ' + dirFRmod + ' \n')     
			f.write('mv Feynman-Rules-Main.m ' + dirFey + ' \n')
			f.write('if [ -f ./PrePropagators.m ]; then mv PrePropagators.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PreRulesv3Higgs.m ]; then mv PreRulesv3Higgs.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PreRulesv4Higgs.m ]; then mv PreRulesv4Higgs.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PreRulesv3Gauge.m ]; then mv PreRulesv3Gauge.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PreRulesv4Gauge.m ]; then mv PreRulesv4Gauge.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PreRulesv3Fermions.m ]; then mv PreRulesv3Fermions.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PreRulesv3Yukawa.m ]; then mv PreRulesv3Yukawa.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PreRulesv3Ghosts.m ]; then mv PreRulesv3Ghosts.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PreRulesv4Ghosts.m ]; then mv PreRulesv4Ghosts.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PreRulesv3Beaks.m ]; then mv PreRulesv3Beaks.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PreRulesv4Beaks.m ]; then mv PreRulesv4Beaks.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PrePrintPropagators.m ]; then mv PrePrintPropagators.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PrePrintRulesv3Higgs.m ]; then mv PrePrintRulesv3Higgs.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PrePrintRulesv4Higgs.m ]; then mv PrePrintRulesv4Higgs.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PrePrintRulesv3Gauge.m ]; then mv PrePrintRulesv3Gauge.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PrePrintRulesv4Gauge.m ]; then mv PrePrintRulesv4Gauge.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PrePrintRulesv3Fermions.m ]; then mv PrePrintRulesv3Fermions.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PrePrintRulesv3Yukawa.m ]; then mv PrePrintRulesv3Yukawa.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PrePrintRulesv3Ghosts.m ]; then mv PrePrintRulesv3Ghosts.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PrePrintRulesv4Ghosts.m ]; then mv PrePrintRulesv4Ghosts.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PrePrintRulesv3Beaks.m ]; then mv PrePrintRulesv3Beaks.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PrePrintRulesv4Beaks.m ]; then mv PrePrintRulesv4Beaks.m ' + dirNuc + '; fi \n')
			if RenoLogic == True:			
				f.write('mv CTpre.m ' + dirNuc + ' \n')
				f.write('if [ -f ./PrePrintCTRulesv1Tads.m ]; then mv PrePrintCTRulesv1Tads.m ' + dirNuc + '; fi \n')
				f.write('if [ -f ./PrePrintCTRulesv2Props.m ]; then mv PrePrintCTRulesv2Props.m ' + dirNuc + '; fi \n')
				f.write('if [ -f ./PrePrintCTRulesv3Higgs.m ]; then mv PrePrintCTRulesv3Higgs.m ' + dirNuc + '; fi \n')
				f.write('if [ -f ./PrePrintCTRulesv4Higgs.m ]; then mv PrePrintCTRulesv4Higgs.m ' + dirNuc + '; fi \n')
				f.write('if [ -f ./PrePrintCTRulesv3Gauge.m ]; then mv PrePrintCTRulesv3Gauge.m ' + dirNuc + '; fi \n')
				f.write('if [ -f ./PrePrintCTRulesv4Gauge.m ]; then mv PrePrintCTRulesv4Gauge.m ' + dirNuc + '; fi \n')
				f.write('if [ -f ./PrePrintCTRulesv3Fermions.m ]; then mv PrePrintCTRulesv3Fermions.m ' + dirNuc + '; fi \n')
				f.write('if [ -f ./PrePrintCTRulesv3Yukawa.m ]; then mv PrePrintCTRulesv3Yukawa.m ' + dirNuc + '; fi \n')
				f.write('if [ -f ./PrePrintCTRulesv3Ghosts.m ]; then mv PrePrintCTRulesv3Ghosts.m ' + dirNuc + '; fi \n')
				f.write('if [ -f ./PrePrintCTRulesv4Ghosts.m ]; then mv PrePrintCTRulesv4Ghosts.m ' + dirNuc + '; fi \n')
			f.write('cd ' + dirNuc + ' \n')
			f.write('python3 Converter.py \n')
			f.write('if [ -f ./Propagators.m ]; then mv Propagators.m ' + dirFey + '; fi \n')
			f.write('if [ -f ./Rulesv3Higgs.m ]; then mv Rulesv3Higgs.m ' + dirFey + '; fi \n')
			f.write('if [ -f ./Rulesv4Higgs.m ]; then mv Rulesv4Higgs.m ' + dirFey + '; fi \n')
			f.write('if [ -f ./Rulesv3Gauge.m ]; then mv Rulesv3Gauge.m ' + dirFey + '; fi \n')
			f.write('if [ -f ./Rulesv4Gauge.m ]; then mv Rulesv4Gauge.m ' + dirFey + '; fi \n')
			f.write('if [ -f ./Rulesv3Fermions.m ]; then mv Rulesv3Fermions.m ' + dirFey + '; fi \n')
			f.write('if [ -f ./Rulesv3Yukawa.m ]; then mv Rulesv3Yukawa.m ' + dirFey + '; fi \n')
			f.write('if [ -f ./Rulesv3Ghosts.m ]; then mv Rulesv3Ghosts.m ' + dirFey + '; fi \n')
			f.write('if [ -f ./Rulesv4Ghosts.m ]; then mv Rulesv4Ghosts.m ' + dirFey + '; fi \n')
			f.write('if [ -f ./Rulesv3Beaks.m ]; then mv Rulesv3Beaks.m ' + dirFey + '; fi \n')
			f.write('if [ -f ./Rulesv4Beaks.m ]; then mv Rulesv4Beaks.m ' + dirFey + '; fi \n')
			f.write('rm -f CTpre.m \n')
			f.write('if [ -f ./CTini.m ]; then mv CTini.m ' + dirCT + '; fi \n')
			f.write('python3 Printer.py \n')
			dirFeyDraw = dirFey + 'TeXs-drawing/'
			f.write('mkdir -p ' + dirFeyDraw + ' \n')
			f.write('mv DrawRules.tex ' + dirFeyDraw + ' \n')
			dirCTDraw = dirCT + 'TeXs-drawing/'
			f.write('mkdir -p ' + dirCTDraw + ' \n')
			f.write('mv DrawCTRules.tex ' + dirCTDraw + ' \n')          
			f.write('cd ' + dirFeyDraw + ' \n')
			f.write('pdflatex -interaction=nonstopmode --shell-escape DrawRules.tex \n')
			f.write('pdflatex -interaction=nonstopmode --shell-escape DrawRules.tex \n')
			if osswitch == 'Linux':
				f.write('evince DrawRules.pdf & \n')
			elif osswitch == 'Mac':
				f.write('open DrawRules.pdf & \n')
			if RenoLogic == True:			
				f.write('cd ' + dirCTDraw + ' \n')
				f.write('pdflatex -interaction=nonstopmode --shell-escape DrawCTRules.tex \n')
				f.write('pdflatex -interaction=nonstopmode --shell-escape DrawCTRules.tex \n')
				if osswitch == 'Linux':
					f.write('evince DrawCTRules.pdf & \n')
				elif osswitch == 'Mac':
					f.write('open DrawCTRules.pdf & \n')
			f.close()       

		# - - - - - - - - - - - - - - - - - To run the just created batch file
		if osswitch == 'Windows':
			from subprocess import Popen
			p = Popen(''+dirNuc+"FRinter.bat", cwd=r''+dirNuc+'')   
			stdout, stderr = p.communicate()
		elif osswitch == 'Linux' or osswitch == 'Mac':
			import os
			os.chmod("FRinter.sh",0o764)
			import subprocess
			subprocess.call(''+dirNuc+"FRinter.sh", shell=True)     

	# - - - - - - - - - - - - - - - - - Here we create (if the user wants to do renormalization) the CTfin.m file. This is thus an automatically
	# - - - - - - - - - - - - - - - - - generated file, which, as the FeynCalc environment starts working, will contain the values of the counterterms.
	# - - - - - - - - - - - - - - - - - In this phase, it thus starts as simply an empty Mathematica list
	if RenoLogic == True:
		f = open(''+dirCT+'CTfin.m', 'w')
		f.write('CTfinlist = {}; \n')
		f.close()

	# - - - - - - - - - - - - - - - - - We now start the main part of General.py. For each process in the sequence of processes defined in Control.m,
	# - - - - - - - - - - - - - - - - - we do several operations
	for i in range(len(Seq)):
		# - - - - - - - - - - - - - - - - - We start by creating useful lists of the particles involved. The A lists are simply a sequence of the particles
		# - - - - - - - - - - - - - - - - - involved (therefore, they have no commas and are not Mathematicas list). The B lists are Mathematicas lists.
		# - - - - - - - - - - - - - - - - - The C lists (to appear later on) are strings with the particles separated by commas. The LA lists are equivalent
		# - - - - - - - - - - - - - - - - - to the C lists, but in LaTeX style
		inParTotA = ''
		outParTotA = ''
		inParTotB = ''
		outParTotB = ''
		inParTotB2 = ''
		outParTotB2 = ''
		inTypTotB = ''
		outTypTotB = ''
		inParTotLA = ''
		outParTotLA = ''
		UGLogic=False
		if Opt[i]=='ugauge':
			UGLogic=True
			Opt[i]=''
			for k in range(len(ghl)):
				parsaux=[]
				parsaux.append('avoid')
				parsaux.append(ghl[k])
				parsaux.append('1')
				parsaux.append('9')
				ParS[i].append(parsaux)
			for k in range(len(gslist)):
				parsaux=[]
				parsaux.append('avoid')
				parsaux.append(gslist[k])
				parsaux.append('1')
				parsaux.append('9')
				ParS[i].append(parsaux)
		for j in range(len(Seq[i])):
			for k in range(len(Seq[i][j])):
				if j == 0:
					inParTotA += Seq[i][j][k]
					inParTotB += Seq[i][j][k] + ','
					inTypTotB += Typ[i][j][k] + ','
					if any(Seq[i][j][k] == x for x in Qlist):
						for m in range(len(Qlist)):
							if Seq[i][j][k]==Qlist[m]:
								inParTotLA += LAlist[m] + ','
								inParTotB2 += Qlist[m] + ','
					elif any(Seq[i][j][k] == x for x in Qanlist):
						for m in range(len(Qanlist)):
							if Seq[i][j][k]==Qanlist[m]:
								inParTotLA += LAanlist[m] + ','
								inParTotB2 += Qlist[m] + ','
				elif j == 1:
					outParTotA += Seq[i][j][k]
					outParTotB += Seq[i][j][k] + ','
					outTypTotB += Typ[i][j][k] + ','
					if Seq[i][j][k] == '':
						outParTotLA += ','
						outParTotB2 += ','						
					elif any(Seq[i][j][k] == x for x in Qlist):
						for m in range(len(Qlist)):
							if Seq[i][j][k]==Qlist[m]:
								outParTotLA += LAlist[m] + ','
								outParTotB2 += Qlist[m] + ','
					elif any(Seq[i][j][k] == x for x in Qanlist):
						for m in range(len(Qanlist)):
							if Seq[i][j][k]==Qanlist[m]:
								outParTotLA += LAanlist[m] + ','
								outParTotB2 += Qlist[m] + ','
		inParTotB = inParTotB[:-1]
		outParTotB = outParTotB[:-1]
		inParTotB2 = inParTotB2[:-1]
		outParTotB2 = outParTotB2[:-1]
		inTypTotB = inTypTotB[:-1]
		outTypTotB = outTypTotB[:-1]
		inParTotLA = inParTotLA[:-1]
		outParTotLA = outParTotLA[:-1]  

		# - - - - - - We now define some useful directories (first in Windows, then in Linux)
		if osswitch == 'Windows':
			# - - - - - - Each specific process:
			dirSpe = dirPro + str(i+1) + '-' + inParTotA + outParTotA + '\\'
			# - - - - - - TeXs for Drawing:
			dirTeXDr = dirSpe + 'TeXs-drawing\\'
			# - - - - - - TeXs for final expressions:
			dirTeXWr = dirSpe + 'TeXs-expressions\\'
			# - - - - - - Eventual useful lists:
			dirLists = dirSpe + 'Lists\\'
		elif osswitch == 'Linux' or osswitch == 'Mac':
		# - - - - - - Each specific process:
			dirSpe = dirPro + str(i+1) + '-' + inParTotA + outParTotA + '/'
			# - - - - - - TeXs for Drawing:
			dirTeXDr = dirSpe + 'TeXs-drawing/'
			# - - - - - - TeXs for final expressions:
			dirTeXWr = dirSpe + 'TeXs-expressions/'
			# - - - - - - Eventual useful lists:
			dirLists = dirSpe + 'Lists/'
		# - - - - - - - - - - - - - - - - - Here we create the Helper.m file.  This is thus an automatically generated file, which contains some
		# - - - - - - - - - - - - - - - - - preliminary informations about the model for the FeynCalc environment
		f = open(''+dirNuc+'Helper.m', 'w')
		f.write('FMversion = "' + FMversion + '"; \n')
		f.write('FMdate = "' + FMdate + '"; \n')
		f.write('osswitch = "' + osswitch + '"; \n')
		f.write('<<Amplitudes.m \n')
		f.write('inparticlesA = ' + inParTotA + '; \n')
		if outParTotA != '':
			f.write('outparticlesA = ' + outParTotA + '; \n')   
		f.write('inparticlesB = {' + inParTotB + '}; \n')
		f.write('outparticlesB = {' + outParTotB + '}; \n')
		f.write('inparticlesB2 = {' + inParTotB2 + '}; \n')
		f.write('outparticlesB2 = {' + outParTotB2 + '}; \n')		
		f.write('inparticlesC = \"' + inParTotB + '\"; \n')
		f.write('outparticlesC = \"' + outParTotB + '\"; \n')
		f.write('inparticlesLA = \"' + inParTotLA.replace('\\', '\\\\') + '\"; \n')
		f.write('outparticlesLA = \"' + outParTotLA.replace('\\', '\\\\') + '\"; \n') 
		f.write('intypes = {' + inTypTotB + '}; \n')
		f.write('outtypes = {' + outTypTotB + '}; \n')
		f.write('factor = ' + Fac[i] + '; \n')  
		f.write('loops = ' + Loo[i] + '; \n')
		f.write('Qoptions = \"' + Opt[i] + '\"; \n')
		f.write('modelname = \"' + extname + '\"; \n')
		f.write('FinLogic = ' + str(FinLogic) + '; \n')
		f.write('DivLogic = ' + str(DivLogic) + '; \n')
		f.write('RenoLogic = ' + str(RenoLogic) + '; \n')
		f.write('SumLogic = ' + str(SumLogic) + '; \n')
		f.write('MoCoLogic = ' + str(MoCoLogic) + '; \n')
		f.write('LoSpinors = ' + str(LoSpinors) + '; \n')
		f.write('ParselLen = ' + str(len(ParS[i])) + '; \n')
		f.write('renconsadd = {' + renconsadd + '}; \n')
		f.write('renconslist = {' + renconslist + '}; \n')
		f.write('renorrules = {' + ancR + '}; \n')
		FCaux=''
		for j in range(len(FCeqs)):
			if not (len(FCeqs) == 1 and FCeqs[0]==''):
				FCanc=[];
				if ':=' in FCeqs[j]:
					FCanc=FCeqs[j].split(':=')
				elif '=' in FCeqs[j]:
					FCanc=FCeqs[j].split('=')
				FCaux=FCaux+'"'+FCanc[0]+'"->'+FCanc[1]+','
				f.write(FCeqs[j]+'; \n')            
		if FCaux!='':
			FCaux = FCaux[:-1]
			f.write('FCeqsaux = {'+FCaux+'}; \n')
		f.write('FCsimp = ' + FCsimp + '; \n')            
		f.close()

		# - - - - - - - - - - - - - - - - - Here is where we create the qgraf.dat file. This file is the input file for QGRAF. It is thus
		# - - - - - - - - - - - - - - - - - automatically generated, based on the choices made by the user on Control.m
		f = open(''+dirQ+'qgraf.dat', 'w')
		f.write('\n')
		f.write(' output= \'output-qgraf\' ; \n \n')
		if osswitch == 'Windows':
			if os.path.isdir(dirQ+"Styles\\"):
				f.write(' style= \'Styles/sum.sty\' ; \n\n')
			else:
				f.write(' style= \'sum.sty\' ; \n\n')
		elif 	osswitch == 'Linux' or osswitch == 'Mac':
			if os.path.isdir(dirQ+"Styles/"):
				f.write(' style= \'Styles/sum.sty\' ; \n\n')
			else:
				f.write(' style= \'sum.sty\' ; \n\n')				
		f.write(' model= \'' + dirQmod.replace('\\','/') + intname + ' \'; \n\n')
		f.write(' in= ' + inParTotB + '; \n\n')
		f.write(' out= ' + outParTotB + '; \n\n')
		f.write(' loops= ' + Loo[i] + '; \n\n')
		f.write(' loop_momentum= ; \n\n')
		f.write(' options= ' + Opt[i].replace(',noPVauto','').replace('noPVauto,','').replace('noPVauto','') + '; \n\n')
		if len(ParS[i]) != 0:
			for j in range(len(ParS[i])):
				ParS[i][j][0] = 'true' if ParS[i][j][0] == 'keep' else 'false'
				f.write(' ' + ParS[i][j][0] + '= iprop[' + ParS[i][j][1] + ',' + ParS[i][j][2] + ',' + ParS[i][j][3] + '] ; \n')
		f.close()

		# - - - - - - - - - - - - - - - - - We now generate the Run.m file. As the previous ones, this file is also automatically generated, and
		# - - - - - - - - - - - - - - - - - is basically the equivalent to a Mathematica Notebook, but is to be run automatically through a Windows
		# - - - - - - - - - - - - - - - - - batch file.
		f = open(''+dirNuc+'Run.m', 'w')
		f.write('dirHome = "' + dirSpe.replace('\\','/') + '"; \n')
		f.write('SetDirectory[dirHome]; \n')
		f.write('<<FeynCalc` \n')
		f.write('dirNuc = "' + dirNuc.replace('\\','/') + '";\n')
		f.write('dirFey = "' + dirFey.replace('\\','/') + '";\n')
		f.write('dirCT = "' + dirCT.replace('\\','/') + '";\n')
		f.write('<<Helper.m \n')
		f.write('Get["Feynman-Rules-Main.m", Path -> {dirFey}] \n')
		f.write('Get["FunctionsFM.m", Path -> {dirNuc}] \n')
		f.write('Get["Definitions.m", Path -> {dirNuc}] \n\n')
		f.write('compNwrite = True; \n\n')
		f.write('Get["Finals.m", Path -> {dirNuc}]; \n')
		f.write('If[RenoLogic,\n')
		f.write('Get["SupReno.m", Path -> {dirNuc}]] \n')
		f.write('Get["WriteToPreTeX.m", Path -> {dirNuc}] \n')
		f.close()

		# - - - - - - - - - - - - - - - - - Here we create the Notebook.m file, automatically generated as well, which is equivalent to Run.m, only
		# - - - - - - - - - - - - - - - - - this is a real Mathematica Notebook. This is useful if the user wants to have control over the Mathematica/
		# - - - - - - - - - - - - - - - - - FeynCalc results, in which case he or she should work (non automatically) with the Notebook here created
		lido=open(''+dirNuc+'Run.m', 'r')
		allLines = lido.read().splitlines()
		lido.close()
		auxwri='' if osswitch=='Mac' else '\\n'
		f = open(''+dirNuc+'Notebook.nb', 'w')
		f.write('Notebook[{Cell[BoxData["')
		for i7, i8 in enumerate(allLines):
			if i7>= (len(allLines)-1): break
			if i7 != len(allLines)-2:
				if i7 == 11:
					# To change compNwrite = True to False
					i8=i8.replace('True','False')
				f.write(i8.replace('"','\\"') + '\n' + auxwri)
			else:
				f.write(i8.replace('"','\\"'))
		f.write('"], "Input"]}')
		if osswitch == 'Mac':
			f.write(',\n')
			f.write('WindowSize->{720, 855},\n')
			f.write('WindowMargins->{{Automatic, 0}, {Automatic, 0}}\n')
		f.write(']')
		f.close()

		# - - - - - - - - - - - - - - - - - Finally, we create a big batch file. Here we run all the main programs (FeynRules excluded), and move the 
		# - - - - - - - - - - - - - - - - - files to different directories whenever necessary. The order of the main programs is: QGRAF, Amperate.py
		# - - - - - - - - - - - - - - - - - (which includes Drawing.py), and finally Mathematica/FeynCalc.
		os.chdir(dirQ)
		for file in glob.glob("*.f"):
			myqversion=file[:-2]		
		if osswitch == 'Windows':
			f = open(''+dirNuc+'recorrente.bat', 'w')
			f.write('@echo off \n')
			f.write('cd ' + dirQ + ' \n')
			f.write('if exist output-qgraf rename output-qgraf last-output \n')
			if not any(File.endswith(".exe") for File in os.listdir(".")):
			    f.write('ftn95 ' + myqversion + '.f \n')
			    f.write('slink \n')
			f.write('.\\' + myqversion + '.exe \n')
			f.write('move output-qgraf ' + dirNuc + '\n')
			f.write('cd ' + dirFey + ' \n')
			f.write('move Nclist.m ' + dirNuc + '\n')
			f.write('cd ' + dirNuc + ' \n')
			f.write('py Amperate.py output-qgraf ' + str(i) + '\n')
			f.write('if not exist ' + dirSpe + ' (mkdir ' + dirSpe + ') \n')
			f.write('if not exist ' + dirTeXDr + ' (mkdir ' + dirTeXDr + ') \n')
			f.write('if not exist ' + dirTeXWr + ' (mkdir ' + dirTeXWr + ') \n')
			f.write('if not exist ' + dirLists + ' (mkdir ' + dirLists + ') \n')
			f.write('move Amplitudes.m ' + dirSpe + '\n')
			f.write('move diagrams.tex ' + dirTeXDr + ' \n')
			f.write('move Helper.m ' + dirSpe + '\n')
			f.write('move Run.m ' + dirSpe + '\n')
			f.write('move Notebook.nb ' + dirSpe + '\n')
			f.write('move Nclist.m ' + dirFey + '\n')
			if FRinterLogic == True:
				dirFeyDraw = dirFey + 'TeXs-drawing\\'
				f.write('if not exist ' + dirFeyDraw + ' (mkdir ' + dirFeyDraw + ') \n')
				f.write('if exist PrePrintPropagators.m move PrePrintPropagators.m ' + dirFeyDraw + ' \n')
				f.write('if exist PrePrintRulesv3Higgs.m move PrePrintRulesv3Higgs.m ' + dirFeyDraw + ' \n')
				f.write('if exist PrePrintRulesv4Higgs.m move PrePrintRulesv4Higgs.m ' + dirFeyDraw + ' \n')
				f.write('if exist PrePrintRulesv3Gauge.m move PrePrintRulesv3Gauge.m ' + dirFeyDraw + ' \n')
				f.write('if exist PrePrintRulesv4Gauge.m move PrePrintRulesv4Gauge.m ' + dirFeyDraw + ' \n')
				f.write('if exist PrePrintRulesv3Fermions.m move PrePrintRulesv3Fermions.m ' + dirFeyDraw + ' \n')
				f.write('if exist PrePrintRulesv3Yukawa.m move PrePrintRulesv3Yukawa.m ' + dirFeyDraw + ' \n')
				f.write('if exist PrePrintRulesv3Ghosts.m move PrePrintRulesv3Ghosts.m ' + dirFeyDraw + ' \n')
				f.write('if exist PrePrintRulesv4Ghosts.m move PrePrintRulesv4Ghosts.m ' + dirFeyDraw + ' \n')
				f.write('if exist PrePrintRulesv3Beaks.m move PrePrintRulesv3Beaks.m ' + dirFeyDraw + ' \n')
				f.write('if exist PrePrintRulesv4Beaks.m move PrePrintRulesv4Beaks.m ' + dirFeyDraw + ' \n')
				f.write('if exist PrePropagators.m del PrePropagators.m \n')
				f.write('if exist PreRulesv3Higgs.m del PreRulesv3Higgs.m \n')
				f.write('if exist PreRulesv4Higgs.m del PreRulesv4Higgs.m \n')
				f.write('if exist PreRulesv3Gauge.m del PreRulesv3Gauge.m \n')
				f.write('if exist PreRulesv4Gauge.m del PreRulesv4Gauge.m \n')
				f.write('if exist PreRulesv3Fermions.m del PreRulesv3Fermions.m \n')
				f.write('if exist PreRulesv3Yukawa.m del PreRulesv3Yukawa.m \n')
				f.write('if exist PreRulesv3Ghosts.m del PreRulesv3Ghosts.m \n')
				f.write('if exist PreRulesv4Ghosts.m del PreRulesv4Ghosts.m \n')
				f.write('if exist PreRulesv3Beaks.m del PreRulesv3Beaks.m \n')
				f.write('if exist PreRulesv4Beaks.m del PreRulesv4Beaks.m \n')
				if RenoLogic == True:				
					dirCTDraw = dirCT + 'TeXs-drawing\\'
					f.write('if not exist ' + dirCTDraw + ' (mkdir ' + dirCTDraw + ') \n')
					f.write('if exist PrePrintCTRulesv1Tads.m move PrePrintCTRulesv1Tads.m ' + dirCTDraw + ' \n')
					f.write('if exist PrePrintCTRulesv2Props.m move PrePrintCTRulesv2Props.m ' + dirCTDraw + ' \n')
					f.write('if exist PrePrintCTRulesv3Higgs.m move PrePrintCTRulesv3Higgs.m ' + dirCTDraw + ' \n')
					f.write('if exist PrePrintCTRulesv4Higgs.m move PrePrintCTRulesv4Higgs.m ' + dirCTDraw + ' \n')
					f.write('if exist PrePrintCTRulesv3Gauge.m move PrePrintCTRulesv3Gauge.m ' + dirCTDraw + ' \n')
					f.write('if exist PrePrintCTRulesv4Gauge.m move PrePrintCTRulesv4Gauge.m ' + dirCTDraw + ' \n')
					f.write('if exist PrePrintCTRulesv3Fermions.m move PrePrintCTRulesv3Fermions.m ' + dirCTDraw + ' \n')
					f.write('if exist PrePrintCTRulesv3Yukawa.m move PrePrintCTRulesv3Yukawa.m ' + dirCTDraw + ' \n')
					f.write('if exist PrePrintCTRulesv3Ghosts.m move PrePrintCTRulesv3Ghosts.m ' + dirCTDraw + ' \n')
					f.write('if exist PrePrintCTRulesv4Ghosts.m move PrePrintCTRulesv4Ghosts.m ' + dirCTDraw + ' \n')                
			if Draw == True:
				f.write('cd ' + dirTeXDr + ' \n')
				f.write('pdflatex -interaction=nonstopmode --shell-escape diagrams.tex \n')
				f.write('pdflatex -interaction=nonstopmode --shell-escape diagrams.tex \n')
				f.write('start diagrams.pdf \n')
			if Comp == True:
				f.write('cd ' + dirSpe + ' \n')
				f.write('wolframscript -file Run.m \n')
				if FinLogic == False and DivLogic == False:
					f.write('del preexp.m \n')
				else:
					f.write('move preexp.m ' + dirNuc + ' \n')
					f.write('cd ' + dirNuc + ' \n')
					f.write('if not exist FRtoTeX.m (cd ' + dirFey + ' \n move FRtoTeX.m ' + dirNuc + ' \n cd ' + dirNuc + ') \n')
					f.write('py Converter.py \n')
					f.write('move exp.tex ' + dirTeXWr + ' \n')
					f.write('move preexp.m ' + dirTeXWr + ' \n')
					f.write('cd ' + dirTeXWr + ' \n')
					f.write('pdflatex exp.tex \n')
					f.write('start exp.pdf \n')
			f.write('cd ' + dirSpe + ' \n')
			f.write('del Run.m \n')
			f.write('cd ' + dirNuc + ' \n')
			f.write('if exist FRtoTeX.m move FRtoTeX.m ' + dirFey + ' \n')
			f.write('if exist IndicesList.m del IndicesList.m \n')
			f.write('rename output-qgraf last-output \n')
			f.write('move last-output ' + dirQ + ' \n')
			f.write('rmdir __pycache__ /S /Q \n')
			f.write('cd ' + dirFM + ' \n')
			f.write('copy Control.m ' + dirSpe + '\n')
			f.write('rmdir __pycache__ /S /Q \n')
			f.close()
		elif osswitch == 'Linux' or osswitch == 'Mac':
			f = open(''+dirNuc+'recorrente.sh', 'w')
			f.write('cd ' + dirQ + ' \n')
			f.write('if [ -f output-qgraf ]; then mv output-qgraf last-output; fi \n')
			f.write('./qgraf \n')
			f.write('mv output-qgraf ' + dirNuc + '\n')
			f.write('cd ' + dirFey + ' \n')
			f.write('mv Nclist.m ' + dirNuc + '\n')
			f.write('cd ' + dirNuc + ' \n')
			f.write('python3 Amperate.py output-qgraf ' + str(i) + '\n')
			f.write('mkdir -p ' + dirSpe + '\n')
			f.write('mkdir -p ' + dirTeXDr + '\n')
			f.write('mkdir -p ' + dirTeXWr + '\n')
			f.write('mkdir -p ' + dirLists + '\n')
			f.write('mv Amplitudes.m ' + dirSpe + '\n')
			f.write('mv diagrams.tex ' + dirTeXDr + ' \n')
			f.write('mv Helper.m ' + dirSpe + '\n')
			f.write('mv Run.m ' + dirSpe + '\n')
			f.write('mv Notebook.nb ' + dirSpe + '\n')
			f.write('mv Nclist.m ' + dirFey + '\n')
			if FRinterLogic == True:
				dirFeyDraw = dirFey + 'TeXs-drawing/'
				f.write('mkdir -p ' + dirFeyDraw + ' \n')
				f.write('if [ -f ./PrePrintPropagators.m ]; then mv PrePrintPropagators.m ' + dirFeyDraw + '; fi \n')
				f.write('if [ -f ./PrePrintRulesv3Higgs.m ]; then mv PrePrintRulesv3Higgs.m ' + dirFeyDraw + '; fi \n')
				f.write('if [ -f ./PrePrintRulesv4Higgs.m ]; then mv PrePrintRulesv4Higgs.m ' + dirFeyDraw + '; fi \n')
				f.write('if [ -f ./PrePrintRulesv3Gauge.m ]; then mv PrePrintRulesv3Gauge.m ' + dirFeyDraw + '; fi \n')
				f.write('if [ -f ./PrePrintRulesv4Gauge.m ]; then mv PrePrintRulesv4Gauge.m ' + dirFeyDraw + '; fi \n')
				f.write('if [ -f ./PrePrintRulesv3Fermions.m ]; then mv PrePrintRulesv3Fermions.m ' + dirFeyDraw + '; fi \n')
				f.write('if [ -f ./PrePrintRulesv3Yukawa.m ]; then mv PrePrintRulesv3Yukawa.m ' + dirFeyDraw + '; fi \n')
				f.write('if [ -f ./PrePrintRulesv3Ghosts.m ]; then mv PrePrintRulesv3Ghosts.m ' + dirFeyDraw + '; fi \n')
				f.write('if [ -f ./PrePrintRulesv4Ghosts.m ]; then mv PrePrintRulesv4Ghosts.m ' + dirFeyDraw + '; fi \n')
				f.write('if [ -f ./PrePrintRulesv3Beaks.m ]; then mv PrePrintRulesv3Beaks.m ' + dirFeyDraw + '; fi \n')
				f.write('if [ -f ./PrePrintRulesv4Beaks.m ]; then mv PrePrintRulesv4Beaks.m ' + dirFeyDraw + '; fi \n')
				f.write('rm -f PrePropagators.m \n')
				f.write('rm -f PreRulesv3Higgs.m \n')
				f.write('rm -f PreRulesv4Higgs.m \n')
				f.write('rm -f PreRulesv3Gauge.m \n')
				f.write('rm -f PreRulesv4Gauge.m \n')
				f.write('rm -f PreRulesv3Fermions.m \n')
				f.write('rm -f PreRulesv3Yukawa.m \n')
				f.write('rm -f PreRulesv3Ghosts.m \n')
				f.write('rm -f PreRulesv4Ghosts.m \n')
				f.write('rm -f PreRulesv3Beaks.m \n')
				f.write('rm -f PreRulesv4Beaks.m \n')
				if RenoLogic == True:				
					dirCTDraw = dirCT + 'TeXs-drawing/'
					f.write('mkdir -p ' + dirCTDraw + ' \n')                
					f.write('if [ -f ./PrePrintCTRulesv1Tads.m ]; then mv PrePrintCTRulesv1Tads.m ' + dirCTDraw + '; fi \n')
					f.write('if [ -f ./PrePrintCTRulesv2Props.m ]; then mv PrePrintCTRulesv2Props.m ' + dirCTDraw + '; fi \n')
					f.write('if [ -f ./PrePrintCTRulesv3Higgs.m ]; then mv PrePrintCTRulesv3Higgs.m ' + dirCTDraw + '; fi \n')
					f.write('if [ -f ./PrePrintCTRulesv4Higgs.m ]; then mv PrePrintCTRulesv4Higgs.m ' + dirCTDraw + '; fi \n')
					f.write('if [ -f ./PrePrintCTRulesv3Gauge.m ]; then mv PrePrintCTRulesv3Gauge.m ' + dirCTDraw + '; fi \n')
					f.write('if [ -f ./PrePrintCTRulesv4Gauge.m ]; then mv PrePrintCTRulesv4Gauge.m ' + dirCTDraw + '; fi \n')
					f.write('if [ -f ./PrePrintCTRulesv3Fermions.m ]; then mv PrePrintCTRulesv3Fermions.m ' + dirCTDraw + '; fi \n')
					f.write('if [ -f ./PrePrintCTRulesv3Yukawa.m ]; then mv PrePrintCTRulesv3Yukawa.m ' + dirCTDraw + '; fi \n')
					f.write('if [ -f ./PrePrintCTRulesv3Ghosts.m ]; then mv PrePrintCTRulesv3Ghosts.m ' + dirCTDraw + '; fi \n')      
					f.write('if [ -f ./PrePrintCTRulesv4Ghosts.m ]; then mv PrePrintCTRulesv4Ghosts.m ' + dirCTDraw + '; fi \n')      
			if Draw == True:
				f.write('cd ' + dirTeXDr + ' \n')
				f.write('pdflatex -interaction=nonstopmode --shell-escape diagrams.tex \n')
				f.write('pdflatex -interaction=nonstopmode --shell-escape diagrams.tex \n')
				if osswitch == 'Linux':
					f.write('evince diagrams.pdf & \n')
				elif osswitch == 'Mac':
					f.write('open diagrams.pdf & \n')
			if Comp == True:
				f.write('cd ' + dirSpe + ' \n')
				if osswitch == 'Linux':
					f.write('math -noprompt -script Run.m \n')
				elif osswitch == 'Mac':
					f.write('wolframscript -file Run.m \n')
				if FinLogic == False and DivLogic == False:
					f.write('rm preexp.m \n')
				else:
					f.write('mv preexp.m ' + dirNuc + ' \n')
					f.write('cd ' + dirNuc + ' \n')
					f.write('if [ ! -f ./FRtoTeX.m ]; then (cd ' + dirFey + ' \n mv FRtoTeX.m ' + dirNuc + ' \n cd ' + dirNuc + '); fi \n')
					f.write('python3 Converter.py \n')              
					f.write('mv exp.tex ' + dirTeXWr + ' \n')
					f.write('mv preexp.m ' + dirTeXWr + ' \n')
					f.write('cd ' + dirTeXWr + ' \n')
					f.write('pdflatex exp.tex > /dev/null \n')
					if osswitch == 'Linux':
						f.write('evince exp.pdf & \n')
					elif osswitch == 'Mac':
						f.write('open exp.pdf & \n')
			f.write('cd ' + dirSpe + ' \n')
			f.write('rm Run.m \n')
			f.write('cd ' + dirNuc + ' \n')
			f.write('if [ -f ./FRtoTeX.m ]; then mv FRtoTeX.m ' + dirFey + '; fi \n')
			f.write('rm -f IndicesList.m \n')
			f.write('mv output-qgraf last-output \n')
			f.write('mv last-output ' + dirQ + ' \n')
			f.write('rm -fr __pycache__ \n')
			f.write('cd ' + dirFM + ' \n')
			f.write('cp Control.m ' + dirSpe + '\n')
			f.write('rm -fr __pycache__ \n')
			f.close()

		# - - - - - - - - - - - - - - - - - To run the just created batch file
		if osswitch == 'Windows':
			from subprocess import Popen
			p = Popen(''+dirNuc+"recorrente.bat", cwd=r''+dirNuc+'')    
			stdout, stderr = p.communicate()
		elif osswitch == 'Linux' or osswitch == 'Mac':
			import os
			os.chmod(''+dirNuc+"recorrente.sh",0o764) 
			import subprocess
			subprocess.call(''+dirNuc+"recorrente.sh", shell=True)
	print('')
	endtime = time.time()
	totaltime = endtime - starttime
	totaltimestr="{0:.2f}".format(totaltime)
	print('End of the run.')
	print('Total time used:',totaltimestr,'seconds.')
	print('Thank you for using FeynMaster.\n')
	print('Please cite: Comput.Phys.Commun. 256 (2020) 107311, arXiv: 1909.05876.')
	print('Please do not forget to cite FeynRules, QGRAF and FeynCalc as well.\n')	

	# print('Please cite: Comput.Phys.Commun. 256 (2020) 107311,')
	# print('arXiv: 1909.05876. Please do not forget to cite')	
	# print('FeynRules, QGRAF and FeynCalc as well.\n')	
