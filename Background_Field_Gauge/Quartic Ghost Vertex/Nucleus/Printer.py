# > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
# This is PrintRules.py, a Python routine where we draw and print all the Feynman rules.
#
# Created by: Duarte Fontes
# Email: duartefontes@tecnico.ulisboa.pt
# Last Update: 25.11.2020
# > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >

import os,sys,re,os.path
import General
(Qlist,Qanlist,LAlist,LAanlist,csclT,felT,cgalT,ghlT,scl,gal,bealT) = General.somelists()

import Converter

import FRExtract
(nscl,cscl,ancscl,fel,anfel,ngal,cgal,ancgal,ghl,anghl,glul,beal,anbeal,LAnscl,LAcscl,LAancscl,LAfel,LAanfel,LAngal,LAcgal,LAancgal,LAghl,LAanghl,LAglul,LAbeal,LAanbeal) = FRExtract.FRlists()
(intname,extname,FCsimp,FCeqs,PrMassFL,GFreno,FRrestr,mygluon,gaugegslist,gslist,mycomplex) = FRExtract.FRextra()

import ControlExtract
(Seq,Loo,ParS,Fac,Opt) = ControlExtract.processes()
(FRinterLogic,Draw,Comp,FinLogic,DivLogic,RenoLogic,SumLogic,MoCoLogic,LoSpi) = ControlExtract.selection()


# function to define different topologies
def Topology(vrtx,tipo,nome,CTLogic):
	whitestar=False
	for i in range(len(vrtx)):
		if any(vrtx[i] == x for x in bealT):
			whitestar=True
	if len(vrtx)==1:
		prdraw.write('\\fmfleft{nJ1}\n')
		prdraw.write('\\fmfright{o1}\n')		
		prdraw.write('\\fmflabel{$' + nome[0] + '$}{nJ1}\n')
		prdraw.write('\\fmf{' + tipo[0]+ ',tension=1}{nJ1,nJ1J1J2}\n')
		prdraw.write('\\fmf{phantom}{nJ1J1J2,o1}\n')
		prdraw.write('\\fmfv{decor.shape=pentagram,decor.filled=full,decor.size=6thick}{nJ1J1J2}\n')
	elif len(vrtx)==2:
		nome0=nome[0]; nome1=nome[1]; tipo0=tipo[0]; tipo1=tipo[1]
		if any(vrtx[0] == x for x in felT) and any(vrtx[0] == x for x in Qanlist) and any(vrtx[1] == x for x in Qlist):
			nome0=nome[1]; nome1=nome[0]; tipo0=tipo[1]; tipo1=tipo[0]
		prdraw.write('\\fmfleft{nJ1}\n')
		prdraw.write('\\fmfright{nJ2}\n')		
		prdraw.write('\\fmflabel{$' + nome0 + '$}{nJ1}\n')
		prdraw.write('\\fmflabel{$' + nome1 + '$}{nJ2}\n')
		prdraw.write('\\fmf{' + tipo0+ ',tension=3}{nJ1,nJ1nJ2}\n')
		prdraw.write('\\fmf{' + tipo1+ ',tension=3}{nJ1nJ2,nJ2}\n')
		if any(vrtx[0] == x for x in cgalT):
			prdraw.write('\\fmf{phantom_arrow,tension=0}{nJ1,nJ1nJ2}\n')
		if any(vrtx[1] == x for x in cgalT):
			prdraw.write('\\fmf{phantom_arrow,tension=0}{nJ1nJ2,nJ2}\n')
		if CTLogic == True:
			prdraw.write('\\fmfv{decor.shape=pentagram,decor.filled=full,decor.size=6thick}{nJ1nJ2}\n')
	elif len(vrtx)==3:
		if any(vrtx[0] == x for x in felT) or any(vrtx[0] == x for x in ghlT):
			prdraw.write('\\fmfleft{nJ1}\n')
			prdraw.write('\\fmfright{nJ2,nJ4}\n')		
			prdraw.write('\\fmflabel{$' + nome[2] + '$}{nJ1}\n')
			prdraw.write('\\fmflabel{$' + nome[0] + '$}{nJ2}\n')
			prdraw.write('\\fmflabel{$' + nome[1] + '$}{nJ4}\n')
			prdraw.write('\\fmf{' + tipo[2]+ ',tension=3}{nJ1,nJ2nJ4nJ1}\n')
			prdraw.write('\\fmf{' + tipo[0]+ ',tension=3}{nJ2nJ4nJ1,nJ2}\n')
			prdraw.write('\\fmf{' + tipo[1]+ ',tension=3}{nJ4,nJ2nJ4nJ1}\n')
			if any(vrtx[2] == x for x in cgalT):
				prdraw.write('\\fmf{phantom_arrow,tension=0}{nJ1,nJ2nJ4nJ1}\n')
			if CTLogic == True:
				prdraw.write('\\fmfv{decor.shape=pentagram,decor.filled=full,decor.size=6thick}{nJ2nJ4nJ1}\n')
		else:
			prdraw.write('\\fmfleft{nJ1}\n')
			prdraw.write('\\fmfright{nJ2,nJ4}\n')
			prdraw.write('\\fmflabel{$' + nome[0] + '$}{nJ1}\n')
			prdraw.write('\\fmflabel{$' + nome[1] + '$}{nJ2}\n')
			prdraw.write('\\fmflabel{$' + nome[2] + '$}{nJ4}\n')
			prdraw.write('\\fmf{' + tipo[0]+ ',tension=3}{nJ1,nJ2nJ4nJ1}\n')
			prdraw.write('\\fmf{' + tipo[1]+ ',tension=3}{nJ2,nJ2nJ4nJ1}\n')
			prdraw.write('\\fmf{' + tipo[2]+ ',tension=3}{nJ4,nJ2nJ4nJ1}\n')
			if any(vrtx[0] == x for x in cgalT):
				prdraw.write('\\fmf{phantom_arrow,tension=0}{nJ1,nJ2nJ4nJ1}\n')
			if any(vrtx[1] == x for x in cgalT):
				prdraw.write('\\fmf{phantom_arrow,tension=0}{nJ2,nJ2nJ4nJ1}\n')
			if any(vrtx[2] == x for x in cgalT):
				prdraw.write('\\fmf{phantom_arrow,tension=0}{nJ4,nJ2nJ4nJ1}\n')
			if CTLogic == True:
				prdraw.write('\\fmfv{decor.shape=pentagram,decor.filled=full,decor.size=6thick}{nJ2nJ4nJ1}\n')
		if whitestar==True:
			prdraw.write('\\fmfv{decor.shape=pentagram,decor.filled=empty,decor.size=6thick}{nJ2nJ4nJ1}\n')
	elif len(vrtx)==4:
		prdraw.write('\\fmfleft{nJ1,nJ3}\n')
		prdraw.write('\\fmfright{nJ2,nJ4}\n')
		ze=0; um=1; do=2; tr=3
		if any('phantom' == x for x in tipo):
			auxti=[]; auxtiy=[]; auxtin=[]; auxti3=[]
			for i in range(len(tipo)):
				auxti.append(tipo[i])
			for i in range(len(auxti)):
				if auxti[i] == 'phantom':
					auxtiy.append(i)
				else:
					auxtin.append(i)
			for i in range(len(auxtiy)):
				auxti3.append(auxtiy[i])
			for i in range(len(auxtin)):
				auxti3.append(auxtin[i])
			ze=auxti3[0]; um=auxti3[1]; do=auxti3[2]; tr=auxti3[3]
		prdraw.write('\\fmflabel{$' + nome[ze] + '$}{nJ1}\n')
		prdraw.write('\\fmflabel{$' + nome[um] + '$}{nJ3}\n')
		prdraw.write('\\fmflabel{$' + nome[do] + '$}{nJ2}\n')
		prdraw.write('\\fmflabel{$' + nome[tr] + '$}{nJ4}\n')
		prdraw.write('\\fmf{' + tipo[ze]+ ',tension=3}{nJ1,nJ1nJ3nJ2nJ4}\n')
		prdraw.write('\\fmf{' + tipo[um]+ ',tension=3}{nJ3,nJ1nJ3nJ2nJ4}\n')
		sta='nJ2'; fin='nJ1nJ3nJ2nJ4'
		if any(vrtx[do] == x for x in felT) and vrtx[do][0].isupper():
			fin='nJ2'; sta='nJ1nJ3nJ2nJ4'
		prdraw.write('\\fmf{' + tipo[do]+ ',tension=3}{' + sta + ',' + fin + '}\n')
		prdraw.write('\\fmf{' + tipo[tr]+ ',tension=3}{nJ4,nJ1nJ3nJ2nJ4}\n')
		if any(vrtx[ze] == x for x in cgalT):
			prdraw.write('\\fmf{phantom_arrow,tension=0}{nJ1,nJ1nJ3nJ2nJ4}\n')
		if any(vrtx[um] == x for x in cgalT):
			prdraw.write('\\fmf{phantom_arrow,tension=0}{nJ3,nJ1nJ3nJ2nJ4}\n')
		if any(vrtx[do] == x for x in cgalT):
			prdraw.write('\\fmf{phantom_arrow,tension=0}{' + sta + ',' + fin + '}\n')
		if any(vrtx[tr] == x for x in cgalT):
			prdraw.write('\\fmf{phantom_arrow,tension=0}{nJ4,nJ1nJ3nJ2nJ4}\n')
		if CTLogic == True:
			prdraw.write('\\fmfv{decor.shape=pentagram,decor.filled=full,decor.size=6thick}{nJ1nJ3nJ2nJ4}\n')
		if whitestar==True:
			prdraw.write('\\fmfv{decor.shape=pentagram,decor.filled=empty,decor.size=6thick}{nJ1nJ3nJ2nJ4}\n')

fnames=['PrePrintPropagators.m','PrePrintRulesv3Gauge.m','PrePrintRulesv4Gauge.m','PrePrintRulesv3Fermions.m','PrePrintRulesv3Yukawa.m','PrePrintRulesv3Higgs.m','PrePrintRulesv4Higgs.m','PrePrintRulesv3Ghosts.m','PrePrintRulesv4Ghosts.m','PrePrintRulesv3Beaks.m','PrePrintRulesv4Beaks.m']
CTnames=['PrePrintCTRulesv1Tads.m','PrePrintCTRulesv2Props.m','PrePrintCTRulesv3Gauge.m','PrePrintCTRulesv4Gauge.m','PrePrintCTRulesv3Fermions.m','PrePrintCTRulesv3Yukawa.m','PrePrintCTRulesv3Higgs.m','PrePrintCTRulesv4Higgs.m','PrePrintCTRulesv3Ghosts.m','PrePrintCTRulesv4Ghosts.m']

totnames=[]
totnames.append(fnames)
totnames.append(CTnames)

for h in range(len(totnames)):
	Tlist = []
	Vlist=[]
	Rlist=[]
	namestoprint=[]
	if h ==1:
		namestoprint.extend(['Tadpoles'])
	namestoprint.extend(['Propagators','Cubic pure gauge','Quartic pure gauge','Fermion-gauge','Fermion-scalar and fermion-goldstone','Cubic scalar-scalar and gauge-scalar','Quartic scalar-scalar and gauge-scalar','Ghosts','Quartic Ghost vertex','Bosonic Beaks','Fermionic Beaks'])
	for i in range(len(totnames[h])):
		Vlist.append([])
		Rlist.append([])
		Tlist.append([])
	for i in range(len(totnames[h])):	
		if os.path.isfile(totnames[h][i]):
			f = open(totnames[h][i], 'r')
			allLines = f.read().splitlines()
			f.close()
			for l in allLines:
				if len(l)<3: continue
				else: Tlist[i].append(l)


				
	for i in range(len(Tlist)):
		if len(Tlist[i]) != 0:
			for j in range(len(Tlist[i])):
				divid = re.findall(r"(?<=\{\{\{\{\{\{)(.*?)(?=\}\}\}\}\}\})", Tlist[i][j])
				Vlist[i].append(divid[0].split(','))
				Rlist[i].append(divid[1])

	Vtylist = []        #  - - - - - the types
	for i in range(len(Vlist)):
		Vtylist.append([])
	for i in range(len(Vlist)):
		for j in range(len(Vlist[i])):
			Vtylist[i].append([])
	for i in range(len(Vlist)):
		for j in range(len(Vlist[i])):
			for k in range(len(Vlist[i][j])):
				if any(Vlist[i][j][k] == x for x in nscl):
					Vtylist[i][j].append('dashes')
				elif any(Vlist[i][j][k] == x for x in csclT):
					Vtylist[i][j].append('scalar')
				elif any(Vlist[i][j][k] == x for x in felT):
					Vtylist[i][j].append('fermion')
				elif any(Vlist[i][j][k] == x for x in gal):
					Vtylist[i][j].append('photon')
				elif any(Vlist[i][j][k] == x for x in ghlT):
					Vtylist[i][j].append('ghost')
				elif any(Vlist[i][j][k] == x for x in glul):
					Vtylist[i][j].append('curly')
				elif any(Vlist[i][j][k] == x for x in bealT):
					Vtylist[i][j].append('phantom')
	Loreinds = ['\\mu','\\nu','\\rho','\\sigma']
	Colinds = ['a','b','c','d']

	Nlist=[]
	for i in range(len(Vlist)):
		Nlist.append([])
	for i in range(len(Vlist)):
		for j in range(len(Vlist[i])):
			Nlist[i].append([])	
	for i in range(len(Vlist)):
		if len(Vlist[i]) != 0:
			for j in range(len(Vlist[i])):
				auxgh=[]
				boldgh=0
				flaggl=0
				for k in range(len(Vlist[i][j])):
					#if any(Vlist[i][j][k] == x for x in glul):
					if 'f[' in Rlist[i][j] or 'T[' in Rlist[i][j] or 'SUNDelta' in Rlist[i][j]:
						flaggl=1
					elif any(Vlist[i][j][k] == x for x in ghlT):
						for m in range(len(Qlist)):
							if (Vlist[i][j][k]==Qlist[m] and Qanlist[m] in auxgh) or (Vlist[i][j][k]==Qanlist[m] and Qlist[m] in auxgh):
								boldgh=1
							else:
								auxgh.append(Vlist[i][j][k])
				for k in range(len(Vlist[i][j])):
					if any(Vlist[i][j][k] == x for x in Qlist):
						for m in range(len(Qlist)):
							if Vlist[i][j][k]==Qlist[m]:
								if any(Vlist[i][j][k] == x for x in gal):
									Nlist[i][j].append(LAlist[m] + '_{' + Loreinds[k] + '}')
								elif any(Vlist[i][j][k] == x for x in glul):
									Nlist[i][j].append(LAlist[m] + '_{' + Loreinds[k] + ', ' + Colinds[k] + '}')
								elif any(Vlist[i][j][k] == x for x in ghlT) and flaggl==1:
									Nlist[i][j].append(LAlist[m] + '^{' + Colinds[k] + '}')									
								elif any(Vlist[i][j][k] == x for x in ghlT) and boldgh==1 and k==1 and 'FV[' in Rlist[i][j]:
									Nlist[i][j].append('\\pmb{'+LAlist[m]+'}')
								else:
									Nlist[i][j].append(LAlist[m])
					elif any(Vlist[i][j][k] == x for x in Qanlist):
						for m in range(len(Qanlist)):
							if Vlist[i][j][k]==Qanlist[m]:
								if any(Vlist[i][j][k] == x for x in felT) or any(Vlist[i][j][k] == x for x in ghlT):
									if any(Vlist[i][j][k] == x for x in ghlT) and flaggl==1:
										Nlist[i][j].append(LAlist[m] + '^{' + Colinds[k] + '}')									
									else:
										Nlist[i][j].append(LAlist[m])
								else:
									if len(Vlist[i][j])==2:
										if any(Vlist[i][j][k] == x for x in gal):
											Nlist[i][j].append(LAlist[m] + '_{' + Loreinds[k] + '}')											
										else:
											Nlist[i][j].append(LAlist[m])										
									else:
										if any(Vlist[i][j][k] == x for x in gal):
											Nlist[i][j].append(LAanlist[m] + '_{' + Loreinds[k] + '}')
										else:
											Nlist[i][j].append(LAanlist[m])			

	swi = '' if h == 0 else 'CT'
	prdraw = open('Draw' + swi + 'Rules.tex', 'w')
	prdraw.write('\\documentclass[a4paper,12pt,twoside]{report} \n \n')
	prdraw.write('\\usepackage{subcaption,feynmp-auto,color,xcolor,slashed,amsbsy} \n\n')
	prdraw.write('\\let\\oldcdot\\cdot \n')
	prdraw.write('\\usepackage{breqn} \n')
	prdraw.write('\\let\\cdot\\oldcdot \n')
	prdraw.write('% \n')
	prdraw.write('\\makeatletter \n')
	prdraw.write('\\setlength{\@fptop}{10pt} \n')
	prdraw.write('\\makeatother \n \n')
	prdraw.write('\\definecolor{dgreen}{rgb}{0,0.2,0} \n')	
	prdraw.write('\\definecolor{mille}{rgb}{0.67,0.608,0.388} \n')
	prdraw.write('\\definecolor{sbrown}{RGB}{139,69,19} \n')
	prdraw.write('\\def\\bd{\\begin{dmath}} \n')
	prdraw.write('\\def\\ed{\\end{dmath}} \n')
	prdraw.write('\\begin{document} \n \n')
	prdraw.write('\\begin{center} \n')
	swi = 'tree-level' if h==0 else 'counterterms'
	prdraw.write('\\textbf{\\large \\color{dgreen} Complete set of Feynman rules for the ' + swi + ' interactions in ' + extname + '}\n\n')
	prdraw.write('\\vspace{1mm}\n\n')
	prdraw.write('{\\footnotesize \\color{gray} (all momenta are entering the vertex, except when the particle-flow arrow is outgoing)}\n\n')
	if h==0:
		prdraw.write('{\\footnotesize \\color{gray} (the $ i \\epsilon $ in the denominators of propagators is omited)}\n\n')	
	prdraw.write('\\vspace{2mm}\n\n')
	prdraw.write('\\end{center}\n\n')
	ind=0
	for i2 in range(len(Tlist)):
		if len(Tlist[i2]) != 0:
			if namestoprint[i2] == 'Tadpoles' or namestoprint[i2] == 'Propagators':
				prdraw.write('\\subsubsection*{\\hspace{-9mm} \\color{sbrown} ' + namestoprint[i2] + '}\n')
			else:
				prdraw.write('\\subsubsection*{\\hspace{-9mm} \\color{sbrown} ' + namestoprint[i2] + ' interactions}\n')
			prdraw.write('\\vspace{-3mm}\n\n')
		for j2 in range(len(Tlist[i2])):
			ind=ind+1
			if namestoprint[i2] != 'Tadpoles' and namestoprint[i2] != 'Propagators':
				prdraw.write('\\vspace{10mm}\n\n')
			prdraw.write('\\noindent\n')
			prdraw.write('\\begin{minipage}[h]{.40\\textwidth}\n')
			prdraw.write('\\begin{picture}(0,80)\n')
			prdraw.write('\\begin{fmffile}{' + str(ind) + '}\n')
			prdraw.write('\\begin{fmfgraph*}(70,70)\n')
			prdraw.write('\\fmfset{arrow_len}{3mm}\n')
			prdraw.write('\\fmfset{arrow_ang}{20}\n')
			swi = False if h==0 else True
			Topology(Vlist[i2][j2],Vtylist[i2][j2],Nlist[i2][j2],swi)
			prdraw.write('\\end{fmfgraph*}\n')
			prdraw.write('\\end{fmffile}\n')    
			prdraw.write('\\end{picture}\n')
			prdraw.write('\\end{minipage}\n')
			prdraw.write('% \n')
			prdraw.write('\\hspace{-25mm} \n')
			prdraw.write('\\begin{minipage}[h]{.80\\textwidth}\n')
			prdraw.write('\\begin{small}\n')
			prdraw.write('\\bd\n')
			prescri=Converter.FRtoFC(Rlist[i2][j2])
			#print(prescri)
			scribendum=Converter.FCtoTEX(prescri,Nlist[i2][j2])
			#print(scribendum)
			prdraw.write(scribendum+'\n')		
			prdraw.write('\\ed\n')
			prdraw.write('\\end{small}\n')
			prdraw.write('\\end{minipage}\n\n')
			if namestoprint[i2] != 'Tadpoles' and namestoprint[i2] != 'Propagators':
				prdraw.write('\\vspace{10mm}\n\n')			
	prdraw.write('\\vspace{1cm}\n')
	prdraw.write('\\raggedright\n')
	prdraw.write('FeynMaster,\\\\[1mm]\n')
	prdraw.write('\\today \n')	
	prdraw.write('\\end{document} \n \n')
