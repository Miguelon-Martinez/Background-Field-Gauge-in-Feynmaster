# > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
# This is ControlExtract.py, a Python routine to extract information from the FeynRules model.
#
# Created by: Duarte Fontes
# Email: duartefontes@tecnico.ulisboa.pt
# Last Update: 09.11.2021
# > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >

import os,sys,re
cwd = os.getcwd()

from sys import platform
if platform == "linux" or platform == "linux2":
    osswitch = 'Linux'
elif platform == "darwin":
    osswitch = 'Mac'
elif platform == "win32":
	osswitch = 'Windows'

if osswitch=='Mac' or osswitch=='Linux':
	sl='/'
else:
	'\\\\'

f = open('..'+sl+'Control.m', 'r')
allLines = f.read().splitlines()
f.close()

def mynestco(stri):
	coin=0;	y0=[]
	for i in range(len(stri)):
		if "".join(stri[i:i+2]) == '(*':
			coin+=1
		elif "".join(stri[i:i+2]) == '*)':
			coin = coin - 1
		y0.append(str(coin))
	return y0

def getcolon(bigstr,litstr):
	covals=mynestco(bigstr)
	anc = re.findall(r"(?<="+litstr+r")(\s*)\:(\s*)(.*?)(?=$)", bigstr)
	alist=list(bigstr)
	myaux=''
	if anc!=[]:
		for i in range(len(alist)):
			s0=''.join(alist[i:(i+len(litstr))])
			if s0 == litstr and covals[i]=='0':
				myaux=anc[0][2]
	return myaux

def getcolon2(bigstr,litstr):
	covals=mynestco(bigstr)
	anc = re.findall(r"(?<="+litstr+r")(\s*)\:(\s*)\"(.*?)\"", bigstr)
	alist=list(bigstr)
	myaux=''
	if anc!=[]:
		for i in range(len(alist)):
			s0=''.join(alist[i:(i+len(litstr))])
			if s0 == litstr and covals[i]=='0':
				myaux=anc[0][2]
	return myaux

def tobool(s):
	if s == 'True':
		return True
	elif s == 'False':
		return False

model=''

inparticles=[]
outparticles=[]
Loo=[]
parsel=[]
Fac=[]
Opt=[]

FRinterLogic=''
RenoLogic=''
Draw=''
Comp=''
FinLogic=''
DivLogic=''
SumLogic=''
MoCoLogic='' 
LoSpinors=''




coin=-1

for i in range(len(allLines)):
	aux=getcolon(allLines[i],'model')
	model=aux if aux!='' else model

	aux=getcolon(allLines[i],'inparticles')
	if aux!='':
		coin+=1
		aux2=aux.replace(' ','').split(',')
		inparticles.append(aux2)
		if coin != len(Loo):
			Loo.append('0')
		if coin != len(Opt):
			Opt.append('')
		if coin != len(Fac):
			Fac.append('1')
		if coin != len(parsel):
			parsel.append([])
		if coin != len(outparticles):
			outparticles.append([''])		

	aux=getcolon(allLines[i],'outparticles')
	if aux!='':
		aux2=aux.replace(' ','').split(',')
		outparticles.append(aux2)

	aux=getcolon(allLines[i],'loops')
	if aux!='':
		Loo.append(aux)

	aux=getcolon(allLines[i],'parsel')
	if aux!='':
		aux2=aux.replace(' ','')
		parsel.append(aux2)

	aux=getcolon(allLines[i],'factor')
	if aux!='':
		Fac.append(aux)

	aux=getcolon(allLines[i],'options')
	if aux!='':
		Opt.append(aux.replace(" ",""))

	aux=getcolon(allLines[i],'FRinterLogic')
	if aux!='':
		coin+=1
		FRinterLogic=aux
		if coin != len(Loo):
			Loo.append('0')
		if coin != len(Opt):
			Opt.append('')
		if coin != len(Fac):
			Fac.append('1')
		if coin != len(parsel):
			parsel.append([])
		if coin != len(outparticles):
			outparticles.append([''])	

	aux=getcolon(allLines[i],'RenoLogic')
	RenoLogic=aux if aux!='' else RenoLogic

	aux=getcolon(allLines[i],'Draw')
	Draw=aux if aux!='' else Draw
	
	aux=getcolon(allLines[i],'Comp')
	Comp=aux if aux!='' else Comp

	aux=getcolon(allLines[i],'FinLogic')
	FinLogic=aux if aux!='' else FinLogic

	aux=getcolon(allLines[i],'DivLogic')
	DivLogic=aux if aux!='' else DivLogic

	aux=getcolon(allLines[i],'SumLogic')
	SumLogic=aux if aux!='' else SumLogic

	aux=getcolon(allLines[i],'MoCoLogic')
	MoCoLogic=aux if aux!='' else MoCoLogic

	aux=getcolon(allLines[i],'LoSpinors')
	LoSpinors=aux if aux!='' else LoSpinors

Seq=[]
for i in range(len(inparticles)):
	aux=[]
	aux.append(inparticles[i])
	aux.append(outparticles[i])
	Seq.append(aux)

ParS=[]
for i in range(len(inparticles)):
	if parsel[i]!=[]:
		aux=re.findall(r"(?<=\{)(.*?)(?=\})", parsel[i])
		aux3=[]
		for j in range(len(aux)):
			aux2=aux[j].split(',')
			aux3.append(aux2)
		ParS.append(aux3)
	else:
		ParS.append([])

if FRinterLogic=='F' or FRinterLogic=='f':
	FRinterLogic='False'
elif FRinterLogic=='T' or FRinterLogic=='t':
	FRinterLogic='True'

if RenoLogic=='F' or RenoLogic=='f':
	RenoLogic='False'
elif RenoLogic=='T' or RenoLogic=='t':
	RenoLogic='True'

if Draw=='F' or Draw=='f':
	Draw='False'
elif Draw=='T' or Draw=='t':
	Draw='True'

if Comp=='F' or Comp=='f':
	Comp='False'
elif Comp=='T' or Comp=='t':
	Comp='True'

if FinLogic=='F' or FinLogic=='f':
	FinLogic='False'
elif FinLogic=='T' or FinLogic=='t':
	FinLogic='True'

if DivLogic=='F' or DivLogic=='f':
	DivLogic='False'
elif DivLogic=='T' or DivLogic=='t':
	DivLogic='True'

if SumLogic=='F' or SumLogic=='f':
	SumLogic='False'
elif SumLogic=='T' or SumLogic=='t':
	SumLogic='True'
	
if MoCoLogic=='F' or MoCoLogic=='f':
	MoCoLogic='False'
elif MoCoLogic=='T' or MoCoLogic=='t':
	MoCoLogic='True'

if LoSpinors=='F' or LoSpinors=='f':
	LoSpinors='False'
elif LoSpinors=='T' or LoSpinors=='t':
	LoSpinors='True'

FRinterLogic=tobool(FRinterLogic)
RenoLogic=tobool(RenoLogic)
Draw=tobool(Draw)
Comp=tobool(Comp)
FinLogic=tobool(FinLogic)
DivLogic=tobool(DivLogic)
SumLogic=tobool(SumLogic)
MoCoLogic=tobool(MoCoLogic)
LoSpinors=tobool(LoSpinors)


# Now, the directories
dirFM=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')) + sl
dirFR=''
dirQ=''
dirFMout=''
myter='bat' if osswitch == 'Windows' else 'sh'
f = open('..'+sl+'RUN-FeynMaster.'+myter, 'r')
allLines = f.read().splitlines()
f.close()

for i in range(len(allLines)):
	aux=getcolon(allLines[i],'dirFM')
	dirFM=aux if aux!='' else dirFM
	aux=getcolon(allLines[i],'dirFR')
	dirFR=aux if aux!='' else dirFR
	aux=getcolon(allLines[i],'dirQ')
	dirQ=aux if aux!='' else dirQ
	aux=getcolon(allLines[i],'dirFMout')
	dirFMout=aux if aux!='' else dirFMout	

dirFRmod=dirFM+'Models'+sl+model+sl
dirQmod=dirQ+'Models'+sl

#we allow a model to be given as argument (instead of through Control)
if len(sys.argv) == 2:
	dirFRmodtest=dirFM+'Models'+sl+sys.argv[1]+sl
	if os.path.isdir(dirFRmodtest):
		model = sys.argv[1]
		dirFRmod=dirFM+'Models'+sl+model+sl

for i in range(len(allLines)):
	aux=getcolon(allLines[i],'dirFRmod')
	dirFRmod=aux+model+sl if aux!='' else dirFRmod

	aux=getcolon(allLines[i],'dirQmod')
	dirQmod=aux if aux!='' else dirQmod

dirMain=dirFMout+model+sl
dirPro=dirMain+'Processes'+sl
dirFey=dirMain+'FeynmanRules'+sl
dirCT=dirMain+'Counterterms'+sl


# Now, the functions to transmit all this info
def processes():
	return (Seq,Loo,ParS,Fac,Opt)
def selection():	
	return (FRinterLogic,Draw,Comp,FinLogic,DivLogic,RenoLogic,SumLogic,MoCoLogic,LoSpinors)
def directories():
	return (dirFM,dirFR,dirFRmod,dirMain,dirQ,dirQmod,dirPro,dirFey,dirCT)
