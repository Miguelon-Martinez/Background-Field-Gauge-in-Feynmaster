# > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
# This is FRExtract.py, a Python routine to extract information from the FeynRules model.
#
# Created by: Duarte Fontes
# Email: duartefontes@tecnico.ulisboa.pt
# Last Update: 16.07.2021
# > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
##
### Initial definitions
##
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
import os,sys,re

import ControlExtract
intname=ControlExtract.model

(Seq,Loo,ParS,Fac,Opt) = ControlExtract.processes()
(FRinterLogic,Draw,Comp,FinLogic,DivLogic,RenoLogic,SumLogic,MoCoLogic,LoSpinors) = ControlExtract.selection()
(dirFM,dirFR,dirFRmod,dirMain,dirQ,dirQmod,dirPro,dirFey,dirCT) = ControlExtract.directories()

f = open(dirFRmod + intname + '.fr', 'r')
gen = f.read().replace("\n"," ")
f.close()

mygets = re.findall(r"(?<=Get\[\")(.*?)\"", gen)
for i in range(len(mygets)):
	f = open(dirFRmod + mygets[i], 'r')
	gen += f.read().replace("\n"," ")
	f.close()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
##
### General functions
##
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# mynestco is a function that, for each character, returns the value of nested commentaries
def mynestco(stri):
	coin=0;	y0=[]
	for i in range(len(stri)):
		if "".join(stri[i:i+2]) == '(*':
			coin+=1
		elif "".join(stri[i:i+2]) == '*)':
			coin = coin - 1
		y0.append(str(coin))
	return y0
genvaluesco=mynestco(gen)

# myfindall is to find functions with nested bracket parentheses
def myfindall(bigstr,litstr):
	stack = []; pro = []; sec = []; coin = 0; s1=''
	for i, c in enumerate(bigstr):
		if i >len(litstr)-1:
			s0=''.join(bigstr[i-len(litstr):i])
			if s0 == litstr:
				coin = 1
			if coin == 1:
				if c == '{':
					stack.append(i)
				elif c == '}' and stack:
					start = stack.pop()
					if len(stack) == 0:
						pro.append(bigstr[start + 1: i])
						s1=''.join(bigstr[i:len(bigstr)])
						f1=re.findall(r"(?<=\{)(.*?)(?=\})", s1)
						if f1 != []:
							f2 = f1[0]
							test=''.join(bigstr[i+1:i+len(f2)+3])
							if test == '{'+f2+'}':
								sec.append(f2)
							else:
								sec.append([])
						else:
							sec.append([])
						coin=0
	return [pro,sec]

#clean deletes quotations marks (") and replaces \\ for \ and 
def clean(stri):
	return stri.replace("\\\\","\\").replace("\"","")

#rmcom removes commentaries
def rmcom(stri):
	auxrm = re.findall(r"(?<=\(\*)(.*?)\*\)", stri)
	for i in range(len(auxrm)):
		stri=stri.replace('(*'+auxrm[i] +'*)','')
	stri=stri.replace('(*','')
	stri=stri.replace('*)','')
	return stri

# myset extracts the elements and their descriptions in the FeynRules M$ sets
def myset(bigstr,litstr):
	set = myfindall(bigstr,litstr)[0][0]
	myaux0 = myfindall(set,'==')[0]
	myaux1 = set.split('==')
	myaux2=[]
	myaux2.append(myaux1[0])
	for i in range(len(myaux1)):	
		if i > 0:
			myaux2.append(myaux1[i].replace('{'+myaux0[i-1]+'},',''))
	desc=[]
	tojump=[]
	for i in range(len(myaux0)):
		if gen.find(myaux0[i]) != -1:
			if genvaluesco[gen.find(myaux0[i])] == '0':
				desc.append(myaux0[i].replace("\t",""))
			else:
				tojump.append(i)
	elem=[]
	for i in range(len(myaux2)):
		if i in tojump:
			continue
		if i != (len(myaux2)-1):
			elem.append(rmcom(myaux2[i]).replace(" ", "").replace("\t", ""))
	return [elem,desc]

# getarrow1 shows the value after an arrow -> and ends up in comma or end of the line
def getarrow1(bigstr,litstr):
	covals=mynestco(bigstr)
	anc = re.findall(r"(?<="+litstr+r")(\s*)\-\>(\s*)(.*?)(?=,|$)", bigstr)
	alist=list(bigstr)
	myaux=''
	if anc!=[]:
		for i in range(len(alist)):
			s0=''.join(alist[i:(i+len(litstr))])
			if s0 == litstr and covals[i]=='0':
				myaux=anc[0][2]
	return myaux

# getarrow2 shows the value after an arrow -> and ends up with }
def getarrow2(bigstr,litstr):
	covals=mynestco(bigstr)
	stack = []; pro = ''; sec = []; coin = 0;
	for i, c in enumerate(bigstr):
		if i >len(litstr)-1:
			s0=''.join(bigstr[i-len(litstr):i])
			if s0 == litstr and covals[i]=='0':
				coin = 1
			if coin == 1:
				if c == '{':
					stack.append(i)
				elif c == '}' and stack:
					start = stack.pop()
					if len(stack) == 0:
						pro+=bigstr[start + 1: i]
						# pro+=bigstr[start: i+1]
						coin=0
			if coin==1 and len(stack)==0 and bigstr[i]==',':
				break
	return pro

# getarrowmix gives getarrow2 if the str starts with {, else getarrow1
def getarrowmix(bigstr,litstr):
	myaux=''
	aux1=getarrow1(bigstr,litstr)
	if aux1 != '':
		aux2 = aux1[0]
		if aux2!='{':
			myaux = aux1
		else:
			myaux = getarrow2(bigstr,litstr)
	return myaux

# getarrow3 shows the value after an arrow -> and ends up in " 
def getarrow3(bigstr,litstr):
	covals=mynestco(bigstr)
	anc = re.findall(r"(?<="+litstr+r")(\s*)\-\>(\s*)\"(.*?)(?=\")", bigstr)
	alist=list(bigstr)
	myaux=''
	if anc!=[]:
		for i in range(len(alist)):
			s0=''.join(alist[i:(i+len(litstr))])
			if s0 == litstr and covals[i]=='0':		
				myaux=anc[0][2]
	return myaux

# getarrowmix2 gives getarrow2 if the str starts with {, else getarrow3
def getarrowmix2(bigstr,litstr):
	myaux=''
	aux1=getarrow1(bigstr,litstr)
	if aux1 != '':
		aux2 = aux1[0]
		if aux2!='{':
			myaux = getarrow3(bigstr,litstr)
		else:
			myaux = getarrow2(bigstr,litstr)
	return myaux

# tobool converts strings into boolean
def tobool(s):
	if s == 'True':
		return True
	elif s == 'False':
		return False


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
##
### Groups, classes and so on
##
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
indexaux = re.findall(r"(?<=IndexRange\[)(\s*)Index\[(\s*)(.*?)(\s*)\](\s*)\](\s*)\=(.*?)Range\[(.*?)\]", gen)
indexlist=[]
for i in range(len(indexaux)):
	indexlist.append([])
	indexlist[i].append(indexaux[i][2])
	indexlist[i].append(indexaux[i][7])

myparams=myset(gen,'M$Parameters')[0]
myparamsdescs=myset(gen,'M$Parameters')[1]

myparts = myset(gen,'M$ClassesDescription')[0]
mypartsdescs = myset(gen,'M$ClassesDescription')[1]

mygroups = myset(gen,'M$GaugeGroups')[0]
mygroupsdescs = myset(gen,'M$GaugeGroups')[1]

# mygluon: finding the name of the gluon
mygluon=''
for i in range(len(mygroups)):
	if getarrow1(mygroupsdescs[i],'StructureConstant')=='f':
		mygluon=getarrow1(mygroupsdescs[i],'GaugeBoson')
		glind=getarrow2(mygroupsdescs[i],'Representations')


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
##
### Parameters informations
##
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
valsaux=[]
mytexs=[]
for i in range(len(myparamsdescs)):
	vauxpre=getarrowmix(myparamsdescs[i],'NumValue')
	valsaux.append(vauxpre)
	mytexs.append(clean(getarrow3(myparamsdescs[i],'TeXName')))

myvals=[]
for i in range(len(myparamsdescs)):
	if valsaux[i]!='':
		myvals.append(myparams[i]+'='+valsaux[i])

indlist=[]
mymatinds=[]
j=0
for i in range(len(myparamsdescs)):
	auxind=getarrow2(myparamsdescs[i],'Indices')
	if auxind!= '' and auxind not in indlist:
		indlist.append('{'+auxind+'}')	
	if auxind!='':
		mymatinds.append([])
		mymatinds[j].append(myparams[i])
		auxind2=auxind.split(',')
		for k in range(len(auxind2)):
			auxind3=re.findall(r"(?<=\[)(.*?)\]", auxind2[k])[0]
			for m in range(len(indexlist)):
				if auxind3 == indexlist[m][0]:
					auxind4 = indexlist[m][1]
					break
			mymatinds[j].append(auxind4)
		j+=1

# Renormalization:
CTtot=[]
j=0
for i in range(len(myparamsdescs)):
	CTaux=getarrow1(myparamsdescs[i],'Counterterm')
	if CTaux!='':
		CTtot.append([])
		CTtot[j].append(myparams[i])
		CTtot[j].append(myparamsdescs[i])
		j+=1

CTtotelems=[]
for i in range(len(CTtot)):
	CTtotelems.append(CTtot[i][0])

renconsnum=[]
LArenconsnum=[]
renconstens=[]
LArenconstens=[]
renconstensdims=[]
j=0
for i in range(len(CTtot)):
	auxtex=getarrow3(CTtot[i][1],'TeXName')
	auxind=getarrow2(CTtot[i][1],'Indices')
	if auxind=='':
		renconsnum.append(CTtot[i][0])
		LArenconsnum.append(clean(auxtex))
	else:
		renconstens.append(CTtot[i][0])
		LArenconstens.append(clean(auxtex))
		renconstensdims.append([])
		auxind2=auxind.split(',')
		for k in range(len(auxind2)):
			auxind3=re.findall(r"(?<=\[)(.*?)\]", auxind2[k])[0]
			for m in range(len(indexlist)):
				if auxind3 == indexlist[m][0]:
					auxind4 = indexlist[m][1]
					break
			renconstensdims[j].append(auxind4)
		j+=1

renoparams=[]
CTelsparams=[]
mycomplex=[]
praux=[]
for i in range(len(myparamsdescs)):
	auxcp=getarrow1(myparamsdescs[i],'ComplexParameter')
	auxind=getarrow2(myparamsdescs[i],'Indices')
	if auxcp != '':
		if auxind == '':
			mycomplex.append(myparams[i])
		else:
			for j in range(len(mymatinds)):
				if myparams[i]==mymatinds[j][0]:
					if len(mymatinds[j])-1 == 1:
						for j1 in range(int(mymatinds[j][1])):
							mycomplex.append(myparams[i]+str(j1+1))
					elif len(mymatinds[j])-1 == 2:
						for j1 in range(int(mymatinds[j][1])):
							for j2 in range(int(mymatinds[j][2])):
								mycomplex.append(myparams[i]+str(j1+1)+str(j2+1))

	auxreno=getarrow2(myparamsdescs[i],'Renormalization')
	if auxreno != '':
		renoparams.append(auxreno)
		if auxcp == 'True':
			# We start by taking care of possible points
			alist=list(auxreno)
			for k in range(len(alist)):
				if alist[k]=='.':
					for m in range(len(alist[:k])-1,-1,-1):
						if not alist[m].isalnum():
							ibef=m+1
							break
					mybef="".join(alist[ibef:k])
					for m in range(len(alist[k+1:])):
						if not alist[k+1+m].isalnum():
							iaft=k+m+1
							break
						else:
							iaft=k+m+2
					myaft="".join(alist[(k+1):iaft])
					aux0="".join(alist[:ibef])
					aux1="".join(alist[iaft:])
					auxreno = aux0 + myaft + '.' + mybef + aux1
			# Now, we take care of the I's
			alist=list(auxreno)
			for k in range(len(alist)):
				if alist[k] == 'I' and not alist[k-1].isalnum() and not alist[k+1].isalnum():
					alist[k]='(-I)'
			# Now, everything else
			auxreno="".join(alist)
			auxreno2 = re.findall(r"[\w']+", auxreno)
			for k in range(len(auxreno2)):
				for l in range(len(myparamsdescs)):
					if auxreno2[k] == myparams[l]:
						auxind=getarrow2(myparamsdescs[l],'Indices')
						toadd = 'HC' if auxind != '' else 'Conjugate'
						if auxreno2[k] not in praux:
							praux.append(auxreno2[k])
							mylen=len(auxreno2[k])
							alist=list(auxreno)
							for m in range(len(alist)):
								if ''.join(alist[m:(m+mylen)]) == auxreno2[k]:
									if m!=0 and m < (len(alist)-mylen):
										if not alist[m-1].isalnum() and not alist[m+mylen].isalnum():
											alist[m-1]+=toadd+'['
											alist[m+mylen-1]+=']'
									elif m==0:
										if not alist[m+mylen].isalnum():
											alist[m]=toadd+'['+alist[m]
											alist[m+mylen-1]+=']'
									elif m==(len(alist)-mylen):
										if not alist[m-1].isalnum():
											alist[m-1]+=toadd+'['
											alist[m+mylen-1]+=']'
							auxreno="".join(alist)
			renoparams.append(auxreno)

for i in range(len(renoparams)):
	for j in range(len(CTtotelems)):
		auxcp=getarrow1(CTtot[j][1],'ComplexParameter')
		auxind=getarrow2(CTtot[j][1],'Indices')
		toadd = 'HC' if auxind != '' else 'Conjugate'		
		if CTtotelems[j] in renoparams[i] and not any(CTtotelems[j] == x for x in CTelsparams):
			CTelsparams.append(CTtotelems[j])
			if auxcp != '':
				CTelsparams.append(toadd+'['+CTtotelems[j]+']')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
##
### Particles informations
##
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
clconjlist=[]
clnamelist=[]
clmemberslist=[]
clanmemberslist=[]
cltexlist=[]
clantexlist=[]
clrenolist=[]
dwlist=[]
ntlist=[]

nscl=[]
cscl=[]
ancscl=[]
fel=[]
anfel=[]
ngal=[]
cgal=[]
ancgal=[]
ghl=[]
anghl=[]
glul=[]
beal=[]
anbeal=[]

LAnscl=[]
LAcscl=[]
LAancscl=[]
LAfel=[]
LAanfel=[]
LAngal=[]
LAcgal=[]
LAancgal=[]
LAghl=[]
LAanghl=[]
LAglul=[]
LAbeal=[]
LAanbeal=[]

clflat = []
nclist=[]
gaugegslist=[]
gslist=[]

ii=-1
for i in range(len(myparts)):
	#
	# Aux variables:
	cnameaux=getarrow1(mypartsdescs[i],'ClassName')
	indaux=getarrow2(mypartsdescs[i],'Indices')
	sconjaux=getarrow1(mypartsdescs[i],'SelfConjugate')
	sconjaux = '' if sconjaux == 'True' else sconjaux 
	renoaux=getarrow1(mypartsdescs[i],'Renormalization')
	membaux=getarrow2(mypartsdescs[i],'ClassMembers')
	unphysaux=getarrow1(mypartsdescs[i],'Unphysical')
	tnameaux=getarrowmix2(mypartsdescs[i],'TeXName')
	tannameaux=getarrowmix2(mypartsdescs[i],'TeXAntiName')
	dwaux=getarrowmix(mypartsdescs[i],'DecayWidth')
	ntaux=getarrow1(mypartsdescs[i],'Neutrino')
	gsaux=getarrow1(mypartsdescs[i],'Goldstone')
	if unphysaux == 'True':
		continue
	else:
		ii+=1
	if tnameaux == '':
		if membaux != '':
			tnameaux = membaux
		else:
			tnameaux = cnameaux
	if tannameaux == '':
		if membaux != '':
			tannameaux = membaux
		else:
			tannameaux = cnameaux		
	#
	# ClassName:
	clnamelist.append(cnameaux)
	#
	# SelfConjugate:
	if sconjaux!='':
		clconjlist.append(sconjaux)
	else:
		clconjlist.append('True')	
	#
	# Renormalization:
	clrenolist.append(renoaux)
	#
	# ClassMembers, TeXName and TeXAntiName:
	clmemberslist.append([])
	clanmemberslist.append([])
	cltexlist.append([])
	clantexlist.append([])
	#
	if membaux=='':
		clmemberslist[ii].append(cnameaux)
		if sconjaux!='':
			clanmemberslist[ii].append(cnameaux+'bar')
		else:
			clanmemberslist[ii].append(cnameaux)
		cltexlist[ii].append(clean(tnameaux))
		if tannameaux!='':
			clantexlist[ii].append(clean(tannameaux))
		else:
			clantexlist[ii].append(clean(tnameaux))
	else:
		membaux2=membaux.replace(" ","").split(',')
		tnameaux2=tnameaux.split(',')
		tannameaux2=tannameaux.split(',') if tannameaux!='' else tnameaux2
		for j in range(len(membaux2)):
			clmemberslist[ii].append(membaux2[j])
			if sconjaux!='':
				clanmemberslist[ii].append(membaux2[j]+'bar')
			else:
				clanmemberslist[ii].append(membaux2[j])
			cltexlist[ii].append(clean(tnameaux2[j]))
			clantexlist[ii].append(clean(tannameaux2[j]))
	#
	# Colour factor:
	indaux2=indaux.replace("Index","").replace("[","").replace("]","")
	indaux3=indaux2.split(',')
	for j in range(len(indaux3)):
		indaux4=indaux3[j].replace(' ','')
		if indaux4 != '' and indaux4 in glind:
			for j in range(len(clmemberslist[ii])):
				nclist.append(clmemberslist[ii][j])
	#
	# Decay Widths:
	if dwaux != '':
		dwaux2=dwaux.split(',')
		for j in range(len(clmemberslist[ii])):
			dwlist.append(clmemberslist[ii][j] + ' -> ' + dwaux2[j])
	#
	# Neutrinos:
	if ntaux != '':
		for j in range(len(clmemberslist[ii])):
			ntlist.append(clmemberslist[ii][j])
			if clanmemberslist[ii][j] != clmemberslist[ii][j]:
				ntlist.append(clanmemberslist[ii][j])
	#
	# Goldstones: identifying the respecrtive gauge bosons
	if gsaux != '':
		gaugegslist.append(gsaux)
		gslist.append(clnamelist[ii])
	#
	#
	# Now we turn to the lists for FM
	#
	for j in range(len(clmemberslist[ii])):
		clflat.append(clmemberslist[ii][j])
		if "S" in myparts[i]:
			if clconjlist[ii] == "True":
				nscl.append(clmemberslist[ii][j])
				LAnscl.append(cltexlist[ii][j])
			else:
				cscl.append(clmemberslist[ii][j])
				LAcscl.append(cltexlist[ii][j])
				ancscl.append(clmemberslist[ii][j]+'bar')
				LAancscl.append(clantexlist[ii][j])
		elif "F" in myparts[i]:
			fel.append(clmemberslist[ii][j])
			LAfel.append(cltexlist[ii][j])
			anfel.append(clmemberslist[ii][j]+'bar')
			LAanfel.append(clantexlist[ii][j])
		elif "V" in myparts[i]:
			if clmemberslist[ii][j]==mygluon:
				glul.append(clmemberslist[ii][j])
				LAglul.append(cltexlist[ii][j])
			else:
				if clconjlist[ii] == "True":
					ngal.append(clmemberslist[ii][j])
					LAngal.append(cltexlist[ii][j])
				else:
					cgal.append(clmemberslist[ii][j])
					LAcgal.append(cltexlist[ii][j])
					ancgal.append(clmemberslist[ii][j]+'bar')
					LAancgal.append(clantexlist[ii][j])
		elif "U" in myparts[i]:
			ghl.append(clmemberslist[ii][j])
			LAghl.append(cltexlist[ii][j])
			anghl.append(clmemberslist[ii][j]+'bar')
			LAanghl.append(clantexlist[ii][j])

#
# We take care of the decay width of Goldstone bosons
#
for i in range(len(myparts)):
	dwaux=getarrowmix(mypartsdescs[i],'DecayWidth')
	if dwaux != '':
		dwaux2=dwaux.split(',')
		for j in range(len(clmemberslist[i])):
			for k in range(len(myparts)):
				auxgold=getarrowmix(mypartsdescs[k],'Goldstone')
				for l in range(len(auxgold)):
					if clmemberslist[i][j] == auxgold[l]:
						dwlist.append(clmemberslist[k][l] + ' -> ' + dwaux2[j])

#
# Now we turn to the renormalization
#
renoparts=[]
for i in range(len(myparts)):
	pairs = []
	sconjaux=getarrow1(mypartsdescs[i],'SelfConjugate')
	sconjaux = '' if sconjaux == 'True' else sconjaux 	
	auxreno=getarrow2(mypartsdescs[i],'Renormalization')
	if auxreno != '':
		renoparts.append(auxreno)
		# If the particle is not its own self-conjugate
		if sconjaux != '':
			# We start by taking care of possible points
			alist=list(auxreno)
			for k in range(len(alist)):
				if alist[k]=='.':
					for m in range(len(alist[:k])-1,-1,-1):
						if not alist[m].isalnum():
							ibef=m+1
							break
					mybef="".join(alist[ibef:k])
					for m in range(len(alist[k+1:])):
						if not alist[k+1+m].isalnum():
							iaft=k+m+1
							break
						else:
							iaft=k+m+2
					myaft="".join(alist[(k+1):iaft])
					aux0="".join(alist[:ibef])
					aux1="".join(alist[iaft:])
					auxreno = aux0 + myaft + '.' + mybef + aux1
			# Now, we take care of the I's
			alist=list(auxreno)
			for k in range(len(alist)):
				if alist[k] == 'I' and not alist[k-1].isalnum() and not alist[k+1].isalnum():
					alist[k]='(-I)'
			# Now, everything else
			auxreno="".join(alist)
			auxreno2 = re.findall(r"[\w']+", auxreno)
			for k in range(len(auxreno2)):
				for m in range(len(CTtot)):
					if auxreno2[k] == CTtot[m][0]:
						auxind=getarrow2(CTtot[m][1],'Indices')
						if auxind != '':
							auxreno=auxreno.replace(auxreno2[k],'HC['+auxreno2[k]+']')
						else:
							auxreno=auxreno.replace(auxreno2[k],'Conjugate['+auxreno2[k]+']')
				if any(auxreno2[k] == x for x in clnamelist):
					pairsaux=[]
					pairsaux.append(auxreno2[k])
					pairsaux.append(auxreno2[k]+'bar')
					if pairsaux not in pairs:
						pairs.append(pairsaux)
						mylen=len(auxreno2[k])
						alist=list(auxreno)
						for m in range(len(alist)):
							if ''.join(alist[m:(m+mylen)]) == auxreno2[k]:
								if m!=0 and m < (len(alist)-mylen):
									if not alist[m-1].isalnum() and not alist[m+mylen].isalnum():
										alist[m+mylen-1]+='bar'									
								elif m==0:
									if not alist[m+mylen].isalnum():
										alist[m+mylen-1]+='bar'
								elif m==(len(alist)-mylen):
									if not alist[m-1].isalnum():
										alist[m+mylen-1]+='bar'
						auxreno="".join(alist)
			renoparts.append(auxreno)
renorrules=renoparams+renoparts


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
##
### Extra informations
##
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# extname: the name of the model that is printed in the pdf files
extname = intname
myaux = re.compile(r"(?<=M\$ModelExtName)(\s*)\=(\s*)\"(.*?)\"")
myaux2 = myaux.findall(gen)
myj=0
for m in myaux.finditer(gen):
    if(genvaluesco[m.start()]=='0'):
    	extname = myaux2[myj][2]
    myj+=1

# FCsimp: replacement rules to simplify FeynCalc expressions
FCsimp = '{}'
myaux = re.compile(r"(?<=M\$FCsimp)(\s*)\=(\s*)\{(.*?)\}")
myaux2 = myaux.findall(gen)
myj=0
for m in myaux.finditer(gen):
	if(genvaluesco[m.start()]=='0'):
		FCsimp = '{'+myaux2[myj][2]+'}'
	myj+=1

# FCeqs: equalities to simplify FeynCalc expressions
FCeqs = []
myaux = re.compile(r"(?<=M\$FCeqs)(\s*)\=(\s*)\{(.*?)\}")
myaux2 = myaux.findall(gen)
myj=0
for m in myaux.finditer(gen):
    if(genvaluesco[m.start()]=='0'):
    	aux1 = myaux2[myj][2]
    	aux2 = aux1.replace("->","=").replace("  ","")
    	FCeqs = aux2.split(',')
    myj+=1
for m in range(len(FCeqs)):
	if FCeqs[m][0]==' ':
		FCeqs[m] = FCeqs[m][1:]

# PrMassFL: whether the masses in the propagators should be extract from the Lagrangean
PrMassFL=True
myaux = re.compile(r"(?<=M\$PrMassFL)(\s*)\=(\s*)(.*?)(?=;|\s)")
myaux2 = myaux.findall(gen)
myj=0
for m in myaux.finditer(gen):
	if(genvaluesco[m.start()]=='0'):
		PrMassFL = tobool(myaux2[myj][2])
	myj+=1

# GFreno: whether the Gauge Fixing terms should be renormalized
GFreno = False
myaux = re.compile(r"(?<=M\$GFreno)(\s*)\=(\s*)(.*?)(?=;|\s)")
myaux2 = myaux.findall(gen)
myj=0
for m in myaux.finditer(gen):
	if(genvaluesco[m.start()]=='0'):
		GFreno = tobool(myaux2[myj][2])
	myj+=1

# FRrestr: name of the restrictions file
FRrestr = ''
myaux = re.compile(r"(?<=M\$RestFile)(\s*)\=(\s*)(.*?)(?=;|\s)")
myaux2 = myaux.findall(gen)
myj=0
for m in myaux.finditer(gen):
	if(genvaluesco[m.start()]=='0'):
		FRrestr = myaux2[myj][2]
	myj+=1


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
##
### Functions to transmit to General.py
##
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def FRlists():
	return(nscl,cscl,ancscl,fel,anfel,ngal,cgal,ancgal,ghl,anghl,glul,beal,anbeal,LAnscl,LAcscl,LAancscl,LAfel,LAanfel,LAngal,LAcgal,LAancgal,LAghl,LAanghl,LAglul,LAbeal,LAanbeal)
def FRreno():
	return(CTtot,renoparams,CTelsparams,renconsnum,LArenconsnum,renconstens,LArenconstens,renconstensdims,renorrules)
def FRextra():
	return(intname,extname,FCsimp,FCeqs,PrMassFL,GFreno,FRrestr,mygluon,gaugegslist,gslist,mycomplex)

 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
##
### Actions to perform if and only if if FRExtract.py is not
### imported by other routines
##
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
if __name__ == '__main__':
	#
	# Writing FRtoTeX.m:
	#
	FRT = open('FRtoTeX.m', 'w')
	for i in range(len(myparams)):
		scrib=myparams[i] + ' -> {' + mytexs[i] + '}\n'
		FRT.write(scrib)
	FRT.close()
	#
	# Writing Matrixind.m:
	#
	MTI = open('Matrixind.m', 'w')
	for i in range(len(mymatinds)):
		scrib=''
		for j in range(len(mymatinds[i])):
			scrib += mymatinds[i][j] + ', '
		scrib=scrib[:-2]+'\n'
		MTI.write(scrib)
	MTI.close()
	#
	# Writing Matrixind.m:
	#
	IL = open('IndicesList.m', 'w')
	for i in range(len(indlist)):
		scrib=indlist[i]+'\n'
		IL.write(scrib)
	IL.close()
	#
	# Writing Nclist.m:
	#
	NC = open('Nclist.m', 'w')
	scrib='{'
	for i in range(len(nclist)):
		scrib+=nclist[i]+', '
	scrib=scrib[:-2] if nclist!=[] else scrib
	scrib+='}'
	NC.write(scrib)
	NC.close()
	#
	# Writing ParamsValues.m:
	#
	PV = open('ParamsValues.m', 'w')
	for i in range(len(myvals)):
		scrib=myvals[i]+'\n'
		PV.write(scrib)
	PV.close()
	#
	# Writing Extras.m:
	#
	EX = open('Extras.m', 'w')
	scrib='DWs = {'
	for i in range(len(dwlist)):
		scrib+=dwlist[i]+', '
	scrib=scrib[:-2] if dwlist!=[] else scrib
	scrib+='};\n'
	scrib+='Neutrinos = {'
	for i in range(len(ntlist)):
		scrib+=ntlist[i]+', '
	scrib=scrib[:-2] if ntlist!=[] else scrib
	scrib+='};'
	EX.write(scrib)
	EX.close()	
