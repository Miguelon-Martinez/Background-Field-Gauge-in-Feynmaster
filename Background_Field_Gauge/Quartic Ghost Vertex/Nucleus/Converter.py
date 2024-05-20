# > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
# This is Converter.py, a Python program to convert notations from different programs.
# Not only does it convert from FeynRules to FeynCalc, but also from the latter to LaTeX.
# Converter.py also writes the Feynman rules for FeynCalc to read.
#
# Created by: Duarte Fontes
# Email: duartefontes@tecnico.ulisboa.pt
# Last Update: 11.05.2021
# > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >

import os,sys,re,os.path
import General
renconsaddlist=General.toexport()

# myfindall is to find functions with nested squared parentheses
def myfindall(bigstr,litstr):
	stack = []; pro = []; sec = []; coin = 0; s1=''
	for i, c in enumerate(bigstr):
		if i >len(litstr)-1:
			s0=''.join(bigstr[i-len(litstr):i])
			if s0 == litstr:
				coin = 1
			if coin == 1:
				if c == '[':
					stack.append(i)
				elif c == ']' and stack:
					start = stack.pop()
					if len(stack) == 0:
						pro.append(bigstr[start + 1: i])
						s1=''.join(bigstr[i:len(bigstr)])
						f1=re.findall(r"(?<=\[)(.*?)(?=\])", s1)
						if f1 != []:
							f2 = f1[0]
							test=''.join(bigstr[i+1:i+len(f2)+3])
							if test == '['+f2+']':
								sec.append(f2)
							else:
								sec.append([])
						else:
							sec.append([])
						coin=0
	return [pro,sec]

# myfindall2 is the same as myfindall, but for the case where we want the string not
# to start with numbers or letters
def myfindall2(bigstr,litstr):
	stack = []; pro = []; sec = []; coin = 0; s1=''
	for i, c in enumerate(bigstr):
		if i >len(litstr)-1:
			s0=''.join(bigstr[i-len(litstr):i])
			sbe=bigstr[i-len(litstr)-1]
			if s0 == litstr and not sbe.isalnum():
				coin = 1
			if coin == 1:
				if c == '[':
					stack.append(i)
				elif c == ']' and stack:
					start = stack.pop()
					if len(stack) == 0:
						pro.append(bigstr[start + 1: i])
						s1=''.join(bigstr[i:len(bigstr)])
						f1=re.findall(r"(?<=\[)(.*?)(?=\])", s1)
						if f1 != []:
							f2 = f1[0]
							test=''.join(bigstr[i+1:i+len(f2)+3])
							if test == '['+f2+']':
								sec.append(f2)
							else:
								sec.append([])
						else:
							sec.append([])
						coin=0
	return [pro,sec]

# mynestpo is a function that, for each character, returns the value of nested curved parentheses
def mynestpo(stri):
	coin=0;	y0=[]
	for i in range(len(stri)):
		if stri[i] == '(':
			coin+=1
		elif stri[i] == ')':
			coin = coin - 1
		y0.append(str(coin))
	return y0

# What follows (IndL and all that) is a preparation for the replaments of the annoying Index structures
IndL=[]
fIL='IndicesList.m'
if os.path.isfile(fIL):
	f2 = open(fIL, 'r')
	AllL = f2.read().splitlines()
	f2.close()
	for j1 in range(len(AllL)):
		IndL.append(AllL[j1].split(','))
	for j1 in range(len(IndL)):
		if len(IndL[j1]) == 3:
			IndL[j1][0]=re.findall(r'Index\[(.*?)\]', IndL[j1][0])
			IndL[j1][1]=re.findall(r'Index\[(.*?)\]', IndL[j1][1])
			IndL[j1][2]=re.findall(r'Index\[(.*?)\]', IndL[j1][2])
		elif len(IndL[j1]) == 2:
			IndL[j1][0]=re.findall(r'Index\[(.*?)\]', IndL[j1][0])
			IndL[j1][1]=re.findall(r'Index\[(.*?)\]', IndL[j1][1])	
		elif len(IndL[j1]) == 1:
			IndL[j1][0]=re.findall(r'Index\[(.*?)\]', IndL[j1][0])

# Now we define the main function destined to convert from FeynRules to FeynCalc
def FRtoFC(arg):
	auxblo2 = re.findall(r'\[(\d+), (\d+)\]', arg)
	for i in range(len(auxblo2)):
		arg=arg.replace('['+auxblo2[i][0]+', '+auxblo2[i][1]+']','['+auxblo2[i][0]+','+auxblo2[i][1]+']')
	auxfv = re.findall(r'FV\[(.*?), Index\[Lorentz, Ext\[(.*?)\]\]\]', arg)
	for i in range(len(auxfv)):
		arg=arg.replace('FV['+auxfv[i][0]+', Index[Lorentz, Ext['+auxfv[i][1]+']]]','fv[k'+auxfv[i][0]+',J'+auxfv[i][1]+']')
	auxfv = re.findall(r'FV\[(.*?), (.*?)\]', arg)
	for i in range(len(auxfv)):
		arg=arg.replace('FV['+auxfv[i][0]+', '+auxfv[i][1]+']','fv['+auxfv[i][0]+','+auxfv[i][1].replace('-','')+']')
	auxmt = re.findall(r'ME\[Index\[Lorentz, Ext\[(.*?)\]\], Index\[Lorentz, Ext\[(.*?)\]\]\]', arg)
	for i in range(len(auxmt)):
		arg=arg.replace('ME[Index[Lorentz, Ext[' + auxmt[i][0] + ']], Index[Lorentz, Ext['+ auxmt[i][1] + ']]]','mt[J'+auxmt[i][0]+',J'+auxmt[i][1]+']')
	auxmt = re.findall(r'ME\[Index\[Lorentz, (.*?)\], Index\[Lorentz, (.*?)\]\]', arg)
	for i in range(len(auxmt)):
		arg=arg.replace('ME[Index[Lorentz, ' + auxmt[i][0] + '], Index[Lorentz, '+ auxmt[i][1] + ']]','mt['+auxmt[i][0].replace('-','')+','+auxmt[i][1].replace('-','')+']')		
	auxgl1 = re.findall(r'f\[Index\[Gluon, Ext\[(.*?)\]\], Index\[Gluon, Ext\[(.*?)\]\], Index\[Gluon, Ext\[(.*?)\]\]\]', arg)
	for i in range(len(auxgl1)):
		arg=arg.replace('f[Index[Gluon, Ext[' + auxgl1[i][0] + ']], Index[Gluon, Ext[' + auxgl1[i][1] + ']], Index[Gluon, Ext[' + auxgl1[i][2] + ']]]','SUNF[Gluonize[J'+auxgl1[i][0]+'],Gluonize[J'+auxgl1[i][1]+'],Gluonize[J'+auxgl1[i][2]+']]')
	auxgl2 = re.findall(r'f\[Index\[Gluon, Ext\[(.*?)\]\], Index\[Gluon, Ext\[(.*?)\]\], Index\[Gluon, (.*?)\]\]', arg)
	for i in range(len(auxgl2)):
		arg=arg.replace('f[Index[Gluon, Ext[' + auxgl2[i][0] + ']], Index[Gluon, Ext[' + auxgl2[i][1] + ']], Index[Gluon, ' + auxgl2[i][2] + ']]','SUNF[Gluonize[J'+auxgl2[i][0]+'],Gluonize[J'+auxgl2[i][1]+'],mtom[ToString[G]<>ToString[J1]<>ToString[J2]<>ToString[J3]<>ToString[J4]]]')
	auxgl3 = re.findall(r'T\[Index\[Gluon, Ext\[(.*?)\]\], Index\[Colour, Ext\[(.*?)\]\], Index\[Colour, Ext\[(.*?)\]\]\]', arg)
	for i in range(len(auxgl3)):
		if len(auxgl3[i][0])==1 and len(auxgl3[i][1])==1 and len(auxgl3[i][2])==1:
			arg=arg.replace('T[Index[Gluon, Ext[' + auxgl3[i][0] + ']], Index[Colour, Ext[' + auxgl3[i][1] + ']], Index[Colour, Ext[' + auxgl3[i][2] + ']]]','SUNT[Gluonize[J'+auxgl3[i][0]+']]')
	auxgl4 = re.findall(r'T\[Index\[Gluon, Ext\[(.*?)\]\]\]', arg)
	for i in range(len(auxgl4)):
		arg=arg.replace('T[Index[Gluon, Ext[' + auxgl4[i] + ']]]','SUNT[Gluonize[J' + auxgl4[i] + ']]')
	auxin1 = re.findall(r'\[Index\[Spin, Ext\[(.*?)\]\], Index\[Spin, Ext\[(.*?)\]\]\]', arg)
	for i in range(len(auxin1)):
		arg=arg.replace('[Index[Spin, Ext[' + auxin1[i][0] + ']], Index[Spin, Ext[' + auxin1[i][1] + ']]]','')
	auxin2 = re.findall(r'\[Index\[Colour, Ext\[(.*?)\]\], Index\[Colour, Ext\[(.*?)\]\]\]', arg)
	for i in range(len(auxin2)):
		arg=arg.replace('[Index[Colour, Ext[' + auxin2[i][0] + ']], Index[Colour, Ext[' + auxin2[i][1] + ']]]','')
	if IndL != []:
		for j1 in range(len(IndL)):
			if len(IndL[j1]) == 3:
				auxna20=IndL[j1][0][0]
				auxna21=IndL[j1][1][0]
				auxna22=IndL[j1][2][0]
				auxin3 = re.findall(r'\[Index\[' + auxna20 + ', (.)\], Index\[' + auxna21 + ', (.)\], Index\[' + auxna22 + ', (.)\]\]', arg)
				for j2 in range(len(auxin3)):
					arg=arg.replace('[Index[' + auxna20 + ', ' + auxin3[j2][0]+ '], Index[' + auxna21 + ', ' + auxin3[j2][1] + '], Index[' + auxna22 + ', ' + auxin3[j2][2] + ']]','[' + auxin3[j2][0] + ',' + auxin3[j2][1] + ',' + auxin3[j2][2] + ']')			
			elif len(IndL[j1]) == 2:
				auxna20=IndL[j1][0][0]
				auxna21=IndL[j1][1][0]
				auxin3 = re.findall(r'\[Index\[' + auxna20 + ', (.)\], Index\[' + auxna21 + ', (.)\]\]', arg)
				for j2 in range(len(auxin3)):
					arg=arg.replace('[Index[' + auxna20 + ', ' + auxin3[j2][0]+ '], Index[' + auxna21 + ', ' + auxin3[j2][1] + ']]','[' + auxin3[j2][0] + ',' + auxin3[j2][1] + ']')
			elif len(IndL[j1]) == 1:
				auxna1=IndL[j1][0][0]
				auxin4 = re.findall(r'\[Index\[' + auxna1 + ', (.)\]\]', arg)
				for j2 in range(len(auxin4)):
					arg=arg.replace('[Index[' + auxna1 + ', ' + auxin4[j2][0]+ ']]','[' + auxin4[j2][0] + ']')			

	auxdm1 = re.findall(r'Ga\[Index\[Lorentz, Ext\[(.*?)\]\], Index\[Spin, Ext\[(.*?)\]\], Index\[Spin, Ext\[(.*?)\]\]\]', arg)
	for i in range(len(auxdm1)):
		arg=arg.replace('Ga[Index[Lorentz, Ext[' + auxdm1[i][0] + ']], Index[Spin, Ext[' + auxdm1[i][1] + ']], Index[Spin, Ext[' + auxdm1[i][2] + ']]]','dm[J' + auxdm1[i][0] + ']')	
	auxdm2 = re.findall(r'Ga\[Index\[Lorentz, Ext\[(.*?)\]\]\]', arg)
	for i in range(len(auxdm2)):
		arg=arg.replace('Ga[Index[Lorentz, Ext[' + auxdm2[i] + ']]]','dm[J' + auxdm2[i] + ']')
	auxdm2b = re.findall(r'Ga\[Index\[Lorentz, (.*?)\]\]', arg)
	for i in range(len(auxdm2b)):
		arg=arg.replace('Ga[Index[Lorentz, ' + auxdm2b[i] + ']]','dm[' + auxdm2b[i] + ']')
	auxdm3 = re.findall(r'Ga\[5, Index\[Spin, Ext\[(.*?)\]\], Index\[Spin, Ext\[(.*?)\]\]\]', arg)
	for i in range(len(auxdm3)):
		arg=arg.replace('Ga[5, Index[Spin, Ext[' + auxdm3[i][0] + ']], Index[Spin, Ext[' + auxdm3[i][1] + ']]]','dm[5]')

	auxin1 = re.findall(r'\[Index\[Spin, (.*?)\]\]', arg)
	for i in range(len(auxin1)):
		arg=arg.replace('[Index[Spin, ' + auxin1[i] + ']]','')

	auxtdot = myfindall(arg,'TensDot')
	for i in range(len(auxtdot[0])):
		anc1=auxtdot[0][i].split(', ')
		if auxtdot[1][i] != []:
			anc2=auxtdot[1][i].split(',')
		if auxtdot[1][i] == [] and ('ProjM' in auxtdot[0][i] or 'ProjP' in auxtdot[0][i]):
			arg=arg.replace('TensDot[' + auxtdot[0][i] + ']', anc1[0] + '.' + anc1[1])
		elif len(anc1)==2:
			arg=arg.replace('TensDot[' + auxtdot[0][i] + '][' + auxtdot[1][i] + ']',   anc1[0]+'['+anc2[0]+',k] '+anc1[1]+'[k,'+anc2[1]+']')
		elif len(anc1)==3:
			arg=arg.replace('TensDot[' + auxtdot[0][i] + '][' + auxtdot[1][i] + ']',   anc1[0]+'['+anc2[0]+',k] '+anc1[1]+'[k,l] '+anc1[2]+'[l,'+anc2[1]+']')

	# Extra replacements for Lagrangean terms
	auxdel = myfindall(arg,'del')
	for i in range(len(auxdel[0])):
		anc1=auxdel[0][i].split(', Index[Lorentz,')
		if auxdel[1][i] == []:
			arg=arg.replace('del[' + auxdel[0][i] + ']', '\\partial^{'+ anc1[1][:-1] + '} ' + anc1[0])
	auxin1 = re.findall(r'\[Index\[Lorentz, (.*?)\]\]', arg)
	for i in range(len(auxin1)):
		arg=arg.replace('[Index[Lorentz, ' + auxin1[i] + ']]' , '_{' + auxin1[i] + '}')

	arg=arg.replace('ProjM','(1-dm[5])/2'); arg=arg.replace('ProjP','(1+dm[5])/2'); arg=arg.replace('IndexDelta','1'); arg=arg.replace('*1',''); arg=arg.replace('(1*','(')
	return arg

# Now we define the main function destined to convert from FeynCalc to TeX
def FCtoTEX(arg,nome):
	arg=arg+' '
	alist=list(arg)
	for i in range(len(alist)):
		if alist[i] == 'I' and not alist[i-1].isalnum() and not alist[i+1].isalnum() and alist[i-1]!='_' and alist[i-1]!='^':
			alist[i]='i'
		if alist[i] == '(' and "".join(alist[(i-4):i])!='left':
			alist[i]='\\left('
		if alist[i] == ')' and "".join(alist[(i-5):i])!='right':
			alist[i]='\\right)'
	arg="".join(alist)
	auxgl1 = myfindall(arg,'Gluonize')
	for i in range(len(auxgl1[0])):
		arg=arg.replace('Gluonize['+auxgl1[0][i] + ']','G'+auxgl1[0][i].replace('J',''))	
	arg=arg.replace('\\left(',' \\left( '); arg=arg.replace('\\right)',' \\right) ');
	arg=arg.replace('-J1','\\mu'); arg=arg.replace('-J2','\\nu');  arg=arg.replace('-J3','\\rho'); arg=arg.replace('-J4','\\sigma')
	arg=arg.replace('-G1','a'); arg=arg.replace('-G2','b');  arg=arg.replace('-G3','c'); arg=arg.replace('-G4','d')
	arg=arg.replace('\\[Mu]1','\\mu'); arg=arg.replace('\\[Mu]2','\\nu'); arg=arg.replace('\\[Mu]3','\\rho'); arg=arg.replace('\\[Mu]4','\\sigma')
	arg=arg.replace('mtom[ToString[G]<>ToString[J1]<>ToString[J2]<>ToString[J3]<>ToString[J4]]','e')
	arg=arg.replace('GmJ1mJ3mJ2mJ4','e')
	tuenda=['J1','J2','J3','J4','G1','G2','G3','G4','Pi','div']
	if nome=='express':
		creanda=[r'\\mu',r'\\nu',r'\\rho',r'\\sigma','f','g','h','i',r'\\pi',r'\\omega_{\\epsilon}']
	else:
		creanda=[r'\\mu',r'\\nu',r'\\rho',r'\\sigma','a','b','c','d',r'\\pi',r'\\omega_{\\epsilon}']
	for i in range(len(tuenda)):
		arg = re.sub(r'(?<![a-zA-Z0-9])'+tuenda[i]+r'(?![a-zA-Z0-9])',creanda[i],arg)
	arg = re.sub(r'(?<![a-zA-Z0-9])'+'Nc'+r'(?![a-zA-Z0-9])','N_c',arg)		
	tuenda=['p1','p2','q1','q2','k1']; creanda=['p_1','p_2','q_1','q_2','k_1']
	for i in range(len(tuenda)):
		arg = re.sub(r'(?<![a-zA-Z0-9])'+tuenda[i]+r'(?![a-zA-Z0-9])',creanda[i],arg)
	arg=arg.replace('(1-dm[5])/2','\\frac{1-\\gamma_5}{2}'); arg=arg.replace('(1+dm[5])/2','\\frac{1+\\gamma_5}{2}');	
	auxsq = re.findall(r"(?<="+'Sqrt'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxsq)):
		arg=arg.replace('Sqrt['+auxsq[i] + ']','\\sqrt{'+auxsq[i]+'}')
	auxtrig = re.findall(r"(?<="+'Sin'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxtrig)):
		arg=arg.replace('Sin['+auxtrig[i] + ']','\\sin('+auxtrig[i]+')')
	auxtrig = re.findall(r"(?<="+'Cos'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxtrig)):
		arg=arg.replace('Cos['+auxtrig[i] + ']','\\cos('+auxtrig[i]+')')
	auxtrig = re.findall(r"(?<="+'Tan'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxtrig)):
		arg=arg.replace('Tan['+auxtrig[i] + ']','\\tan('+auxtrig[i]+')')
	auxtrig = re.findall(r"(?<="+'Cot'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxtrig)):
		arg=arg.replace('Cot['+auxtrig[i] + ']','\\cot('+auxtrig[i]+')')
	auxtrig = re.findall(r"(?<="+'Sec'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxtrig)):
		arg=arg.replace('Sec['+auxtrig[i] + ']','\\sec('+auxtrig[i]+')')
	auxtrig = re.findall(r"(?<="+'Csc'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxtrig)):
		arg=arg.replace('Csc['+auxtrig[i] + ']','\\csc('+auxtrig[i]+')')

	auxden = re.findall(r'Deno\[(.*?),(.*?),(.*?)\]', arg)
	for i in range(len(auxden)):
		if auxden[i][1] == "0" or auxden[i][1] == " 0":
			arg=arg.replace('Deno[' + auxden[i][0] + ',' + auxden[i][1] + ',' + auxden[i][2] + ']','\\frac{1}{' + auxden[i][0] + '^2}')
		else:
			if 'sqrt' in auxden[i][1]:
				auxdsq=auxden[i][1].split('\\sqrt{')
				arg=arg.replace('Deno[' + auxden[i][0] + ',' + auxden[i][1] + ',' + auxden[i][2] + ']','\\frac{1}{' + auxden[i][0] + '^2 - ' + auxdsq[1][:-1] + ' ' + auxdsq[0][:-1] + '^2}')
			else:
				arg=arg.replace('Deno[' + auxden[i][0] + ',' + auxden[i][1] + ',' + auxden[i][2] + ']','\\frac{1}{' + auxden[i][0] + '^2 - ' + auxden[i][1] + '^2}')

	arg=arg.replace('.',' \\, '); arg=arg.replace('*',' \\, ')

	auxco=myfindall(arg,'Conjugate')
	for i in range(len(auxco[0])):
		arg=arg.replace('Conjugate['+auxco[0][i] + ']','{{'+auxco[0][i]+'}^*}')

	auxfp = re.findall(r'fprop\[(.*?),(.*?)\]', arg)
	for i in range(len(auxfp)):
		if auxfp[i][1] == "0" or auxfp[i][1] == " 0":
			arg=arg.replace('fprop[' + auxfp[i][0] + ',' + auxfp[i][1] + ']','\\slashed{' + auxfp[i][0] + '}')
		else:
			arg=arg.replace('fprop[' + auxfp[i][0] + ',' + auxfp[i][1] + ']','\\left(\\slashed{' + auxfp[i][0] + '} + ' + auxfp[i][1] + '\\right)')
	auxsun = re.findall(r'SUNDelta\[(.*?), (.*?)\]', arg)
	for i in range(len(auxsun)):
		arg=arg.replace('SUNDelta[' + auxsun[i][0] + ', ' + auxsun[i][1] + ']','\\delta_{' + auxsun[i][0] + auxsun[i][1] + '}')
	auxsun = re.findall(r'SD\[(.*?), (.*?)\]', arg)
	for i in range(len(auxsun)):
		arg=arg.replace('SD[' + auxsun[i][0] + ', ' + auxsun[i][1] + ']','\\delta_{' + auxsun[i][0] + auxsun[i][1] + '}')
	auxgl1 = myfindall(arg,'SUNF')
	for i in range(len(auxgl1[0])):
		arg=arg.replace('SUNF['+auxgl1[0][i] + ']','f_{'+auxgl1[0][i].replace(',','')+'}')	
	auxgl2 = myfindall(arg,'SUNIndex')
	for i in range(len(auxgl2[0])):
		arg=arg.replace('SUNIndex['+auxgl2[0][i] + ']',auxgl2[0][i])
	auxgl2 = myfindall(arg,'SUNTrace')
	for i in range(len(auxgl2[0])):
		arg=arg.replace('SUNTrace['+auxgl2[0][i] + ']','\\textrm{Tr}\\left['+auxgl2[0][i]+' \\right]')	
	auxgl2 = myfindall(arg,'SUNT')
	for i in range(len(auxgl2[0])):
		arg=arg.replace('SUNT['+auxgl2[0][i] + ']','T^{'+auxgl2[0][i]+'}')
	auxga = re.findall(r"(?<="+'dm'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxga)):
		arg=arg.replace('dm['+auxga[i] + ']','\\gamma^{'+auxga[i]+'}')
	auxga = re.findall(r"(?<="+'GA'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxga)):
		arg=arg.replace('GA['+auxga[i] + ']','\\gamma^{'+auxga[i]+'}')
	auxsl = re.findall(r"(?<="+'DiracGamma\[Momentum'+r"\[)(.*?)(?=\]\])", arg)
	for i in range(len(auxsl)):
		arg=arg.replace('DiracGamma[Momentum['+auxsl[i] + ']]','\\slashed{'+auxsl[i]+'}')
	auxFAD = re.findall(r'FAD\[{(.*?)}, Dimension -> 4\]', arg)
	for i in range(len(auxFAD)):
		auxFAD2=auxFAD[i].split(', ')
		arg=arg.replace('FAD[{'+auxFAD[i] + '}, Dimension -> 4]','\\dfrac{1}{('+auxFAD2[0]+')^2 - {'+auxFAD2[1]+'}^2}')
	auxFAD = re.findall(r'FAD\[(.*?), Dimension -> 4\]', arg)
	for i in range(len(auxFAD)):
		arg=arg.replace('FAD['+auxFAD[i] + ', Dimension -> 4]','\\dfrac{1}{('+auxFAD[i]+')^2}')
	auxFAD = re.findall(r'FAD\[{(.*?)}\]', arg)
	for i in range(len(auxFAD)):
		auxFAD2=auxFAD[i].split(', ')
		arg=arg.replace('FAD[{'+auxFAD[i] + '}]','\\dfrac{1}{('+auxFAD2[0]+')^2 - {'+auxFAD2[1]+'}^2}')
	auxFAD = re.findall(r'FAD\[(.*?)\]', arg)
	for i in range(len(auxFAD)):
		if not ',' in auxFAD[i]:
			arg=arg.replace('FAD['+auxFAD[i] + ']','\\dfrac{1}{('+auxFAD[i]+')^2}')
	auxsl2 = re.findall(r"(?<="+'GS'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxsl2)):
		arg=arg.replace('GS['+auxsl2[i] + ']','\\slashed{'+auxsl2[i]+'}')
	auxsl2 = re.findall(r"(?<="+'GSD'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxsl2)):
		arg=arg.replace('GSD['+auxsl2[i] + ']','\\slashed{'+auxsl2[i]+'}')		

	#Replacement of scalar products
	auxsp = re.findall(r'/SP\[(.*?), (.*?)\]', arg)
	for i in range(len(auxsp)):
		if ('+' in auxsp[i][0]) or ('-' in auxsp[i][0]):
			auxspi0=' \\left( '+auxsp[i][0]+' \\right) '
		else:
			auxspi0=auxsp[i][0]
		if ('+' in auxsp[i][1]) or ('-' in auxsp[i][1]):
			auxspi1=' \\left( '+auxsp[i][1]+' \\right) '
		else:
			auxspi1=auxsp[i][1]
		if auxsp[i][0] == auxsp[i][1]:
			arg=arg.replace('SP[' + auxsp[i][0] + ', ' + auxsp[i][1] + ']',' \\left( '+auxspi0+'^2'+' \\right) ')
		else:
			arg=arg.replace('SP[' + auxsp[i][0] + ', ' + auxsp[i][1] + ']',' \\left( '+auxspi0+'.'+auxspi1+' \\right) ')
	auxsp = re.findall(r'SP\[(.*?), (.*?)\]', arg)
	for i in range(len(auxsp)):
		if ('+' in auxsp[i][0]) or ('-' in auxsp[i][0]):
			auxspi0=' \\left( '+auxsp[i][0]+' \\right) '
		else:
			auxspi0=auxsp[i][0]
		if ('+' in auxsp[i][1]) or ('-' in auxsp[i][1]):
			auxspi1=' \\left( '+auxsp[i][1]+' \\right) '
		else:
			auxspi1=auxsp[i][1]
		if auxsp[i][0] == auxsp[i][1]:
			arg=arg.replace('SP[' + auxsp[i][0] + ', ' + auxsp[i][1] + ']',auxspi0+'^2')
		else:
			arg=arg.replace('SP[' + auxsp[i][0] + ', ' + auxsp[i][1] + ']',auxspi0+'.'+auxspi1)
	auxsp = re.findall(r'/SPD\[(.*?), (.*?)\]', arg)
	for i in range(len(auxsp)):
		if ('+' in auxsp[i][0]) or ('-' in auxsp[i][0]):
			auxspi0=' \\left( '+auxsp[i][0]+' \\right) '
		else:
			auxspi0=auxsp[i][0]
		if ('+' in auxsp[i][1]) or ('-' in auxsp[i][1]):
			auxspi1=' \\left( '+auxsp[i][1]+' \\right) '
		else:
			auxspi1=auxsp[i][1]
		if auxsp[i][0] == auxsp[i][1]:
			arg=arg.replace('SPD[' + auxsp[i][0] + ', ' + auxsp[i][1] + ']',' \\left( '+auxspi0+'^2'+' \\right) ')
		else:
			arg=arg.replace('SPD[' + auxsp[i][0] + ', ' + auxsp[i][1] + ']',' \\left( '+auxspi0+'.'+auxspi1+' \\right) ')
	auxsp = re.findall(r'SPD\[(.*?), (.*?)\]', arg)
	for i in range(len(auxsp)):
		if ('+' in auxsp[i][0]) or ('-' in auxsp[i][0]):
			auxspi0=' \\left( '+auxsp[i][0]+' \\right) '
		else:
			auxspi0=auxsp[i][0]
		if ('+' in auxsp[i][1]) or ('-' in auxsp[i][1]):
			auxspi1=' \\left( '+auxsp[i][1]+' \\right) '
		else:
			auxspi1=auxsp[i][1]
		if auxsp[i][0] == auxsp[i][1]:
			arg=arg.replace('SPD[' + auxsp[i][0] + ', ' + auxsp[i][1] + ']',auxspi0+'^2')
		else:
			arg=arg.replace('SPD[' + auxsp[i][0] + ', ' + auxsp[i][1] + ']',auxspi0+'.'+auxspi1)

	arg=arg.replace('GA[5]','\\gamma_5');
	auxmt = re.findall(r"(?<="+'mt'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxmt)):
		auxmt2=auxmt[i].split(',')
		arg=arg.replace('mt['+auxmt[i] + ']','g^{'+auxmt2[0]+auxmt2[1]+'}')
	auxmt = re.findall(r"(?<="+'MT'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxmt)):
		auxmt2=auxmt[i].split(',')
		arg=arg.replace('MT['+auxmt[i] + ']','g^{'+auxmt2[0]+auxmt2[1]+'}')
	auxmt = re.findall(r"(?<="+'MTD'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxmt)):
		auxmt2=auxmt[i].split(',')
		arg=arg.replace('MTD['+auxmt[i] + ']','g^{'+auxmt2[0]+auxmt2[1]+'}')		
	auxfv = re.findall(r"(?<="+'FV'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxfv)):
		auxfv2=auxfv[i].split(',')
		arg=arg.replace('FV['+auxfv[i] + ']',auxfv2[0]+'^{'+auxfv2[1]+'}')
	auxfv = re.findall(r"(?<="+'FVD'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxfv)):
		auxfv2=auxfv[i].split(',')
		arg=arg.replace('FVD['+auxfv[i] + ']',auxfv2[0]+'^{'+auxfv2[1]+'}')		
	auxfv = re.findall(r"(?<="+'fv'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxfv)):
		auxfv2=auxfv[i].split(',')
		auxfv3=re.findall(r'[0-9]+', auxfv2[0])
		if auxfv3 != []:
			auxfv4=nome[int(auxfv3[0])-1]
			arg=arg.replace('fv['+auxfv[i] + ']','p_{' + auxfv4 + '}^{'+auxfv2[1]+'}')
		else:
			auxfv4=''
			arg=arg.replace('fv['+auxfv[i] + ']','p^{'+auxfv2[1]+'}')
	auxmo = re.findall(r'Momentum\[(.*?)\]', arg)
	for i in range(len(auxmo)):
		arg=arg.replace('Momentum['+auxmo[i] + ']',auxmo[i])
	auxsp = re.findall(r'Spinor\[(.*?), (.*?), (.*?)\]', arg)
	for i in range(len(auxsp)):
		aux4=auxsp[i][0]
		if auxsp[i][0][0] == '-':
			letter='v'
			aux1=auxsp[i][0].replace('-','*')
			aux2=aux1.replace('+','-')
			aux3=aux2.replace('*','+')
			aux4=aux3.replace('+','')
		else:
			letter='u'
		auxi=arg.find('Spinor[' + auxsp[i][0] + ', ' + auxsp[i][1] + ', ' + auxsp[i][2] + ']')
		auxcomp=''.join(arg[(auxi-4):auxi])
		if auxcomp!='\,  ':
			letter='\\bar{'+letter+'}'
		arg=arg.replace('Spinor[' + auxsp[i][0] + ', ' + auxsp[i][1] + ', ' + auxsp[i][2] + ']',letter+'('+aux4+','+auxsp[i][1]+')')

	# A conversion directly from FeynRules to TeX
	fCV='FRtoTeX.m'
	TotCVlist = []
	auxCV= []
	if os.path.isfile(fCV):
		f = open(fCV, 'r');	allLines = f.read().splitlines();	f.close()
		for l in allLines:
			TotCVlist.append(l)
		for i in range(len(TotCVlist)):
			auxCV.append(TotCVlist[i].split(' -> '))
	for j in range(len(auxCV)):
		myreg = r"(?<![a-zA-Z0-9]|\\)" + re.escape(str(auxCV[j][0])) + r"(?![a-zA-Z0-9])"
		if re.search(myreg, arg):
			arg = re.sub(myreg,str(auxCV[j][1]).replace('\\','\\\\'), arg)

	# Matricial elements
	auxgr = re.findall(r"(?<=\\\[)(.*?)(?=\])", arg)
	for i in range(len(auxgr)):
		arg=arg.replace('\\['+auxgr[i] + ']','\\'+auxgr[i].lower()+' ')		
	auxblo2 = re.findall(r'\[(.), (.)\]', arg)
	for i in range(len(auxblo2)):
		arg=arg.replace('['+auxblo2[i][0]+', '+auxblo2[i][1]+']','_{'+auxblo2[i][0]+auxblo2[i][1]+'}')
	auxblo2 = re.findall(r'\[(.),(.)\]', arg)
	for i in range(len(auxblo2)):
		arg=arg.replace('['+auxblo2[i][0]+','+auxblo2[i][1]+']','_{'+auxblo2[i][0]+auxblo2[i][1]+'}')
	auxblo3 = re.findall(r'\[(.), (.), (.)\]', arg)
	for i in range(len(auxblo3)):
		arg=arg.replace('['+auxblo3[i][0]+', '+auxblo3[i][1]+', '+auxblo3[i][2]+']','_{'+auxblo3[i][0]+auxblo3[i][1]+auxblo3[i][2]+'}')
	auxblo3 = re.findall(r'\[(.),(.),(.)\]', arg)
	for i in range(len(auxblo3)):
		arg=arg.replace('['+auxblo3[i][0]+','+auxblo3[i][1]+','+auxblo3[i][2]+']','_{'+auxblo3[i][0]+auxblo3[i][1]+auxblo3[i][2]+'}')
	auxblo1 = re.findall(r'\[(.)\]', arg)
	for i in range(len(auxblo1)):
		arg=arg.replace('['+auxblo1[i][0]+']','_{'+auxblo1[i][0]+'}')

	# Passarino Veltman integrals
	arg=arg.replace(', PaVeAutoOrder -> True, PaVeAutoReduce -> True','')
	auxPV = re.findall(r'([A-Z]?)0\[(.*?)\]', arg)
	for i in range(len(auxPV)):
		arg=arg.replace(auxPV[i][0] + '0[' + auxPV[i][1] + ']',auxPV[i][0]+'_0\\left('+auxPV[i][1] +'\\right)')
	auxPV = re.findall(r'([A-Z]?)1\[(.*?)\]', arg)
	for i in range(len(auxPV)):
		arg=arg.replace(auxPV[i][0] + '1[' + auxPV[i][1] + ']',auxPV[i][0]+'_1\\left('+auxPV[i][1] +'\\right)')			
	auxPV = re.findall(r'PaVe\[(.*?), {(.*?)}, {(.*?)}\]', arg)
	for i in range(len(auxPV)):
		letter='C'
		numb=auxPV[i][1].split('],')
		if len(numb)>3:
			letter='D'
		auxPVs=auxPV[i][0].split(', ')
		if auxPVs != []:
			auxPVf=''
			for j in range(len(auxPVs)):
				auxPVf = auxPVf + auxPVs[j]
			arg=arg.replace('PaVe[' + auxPV[i][0] + ', {' + auxPV[i][1] + '}, {' + auxPV[i][2] + '}]',letter+'_{' + auxPVf + '}\\left('+auxPV[i][1]+','+auxPV[i][2]+'\\right)')			
		else:
			arg=arg.replace('PaVe[' + auxPV[i][0] + ', {' + auxPV[i][1] + '}, {' + auxPV[i][2] + '}]',letter+'_{' + auxPV[i][0] + '}\\left('+auxPV[i][1]+','+auxPV[i][2]+'\\right)')
	arg=arg.replace('^2^2','^4')
	arg=arg.replace('text{','mathrm{')

	# What follows concerns the replacement rules for quocients
	before='';	after='';	bigrep=[]; alist=list(arg); indrep=-1
	for i in range(len(alist)):
		if alist[i]=='/':
			indrep=indrep+1
			bigrep.append([])
			indbar=i
			if ''.join(alist[i-2:i])==') ':
				indbef=1
				strbefo="".join(alist[0:i-1])
				blist=list(strbefo)
				coin=1
				for j in range(len(blist)-2,-1,-1):
					if blist[j]==')':
						coin=coin+1
					elif blist[j]=='(':
						coin=coin-1
					if coin==0:
						before="".join(blist[j:len(blist)-1])
						before=' \left'+before+') '
						break
			elif alist[i-1]=='}':
				indbef=0
				strbefo="".join(alist[0:i])
				blist=list(strbefo)
				coin=1
				for j in range(len(blist)-2,-1,-1):
					if blist[j]=='}':
						coin=coin+1
					elif blist[j]=='{':
						coin=coin-1
					if coin==0:
						before="".join(blist[j:len(blist)])
						break
			else:
				indbef=0
				strbefo="".join(alist[0:i])
				blist=list(strbefo)
				for j in range(len(blist)-1,-1,-1):
					if blist[j]==' ':
						before="".join(blist[(j+1):len(blist)])
						break
			if "".join(alist[(i+1):(i+8)])==' \left(':
				indaf=1
				straft="".join(alist[(i+8):(len(alist))])
				blist=list(straft)
				coin=1
				for j in range(len(blist)):
					if blist[j]=='(':
						coin=coin+1
					elif blist[j]==')':
						coin=coin-1
					if coin==0:
						after="".join(blist[0:j])
						after=' \left('+after+') '
						break
			elif alist[i+1]=='{':				
				indaf=0
				straft="".join(alist[(i+1):(len(alist))])			
				blist=list(straft)				
				coin=1
				for j in range(1,len(blist)+1):				
					if blist[j]=='{':
						coin=coin+1
					elif blist[j]=='}':
						coin=coin-1
					if coin==0:
						if j==len(blist):
							after="".join(blist[0:j])
						elif blist[j+1]!='^':
							after="".join(blist[0:j])
						else:
							after="".join(blist[0:(j+3)])								
						break					
			else:
				indaf=0
				straft="".join(alist[(i+1):(len(alist))])
				blist=list(straft)
				for j in range(len(blist)):
					if blist[j]==' ':
						after="".join(blist[0:j])
						break	
			bigrep[indrep].append(before); bigrep[indrep].append(after); bigrep[indrep].append(indbef); bigrep[indrep].append(indaf)				
	for i in range(len(bigrep)-1,-1,-1):
		vor=bigrep[i][0]+'/'+bigrep[i][1]
		if bigrep[i][2]==0 and bigrep[i][3]==0:
			nach='\\dfrac{'+bigrep[i][0]+'}{'+bigrep[i][1]+'}'
		elif bigrep[i][2]==0 and bigrep[i][3]==1:
			nach='\\dfrac{'+bigrep[i][0]+'}{'+''.join(bigrep[i][1][8:(len(bigrep[i][1])-9)])+'}'
		elif bigrep[i][2]==1 and bigrep[i][3]==0:
			nach='\\dfrac{'+''.join(bigrep[i][0][8:(len(bigrep[i][0])-9)])+'}{'+bigrep[i][1]+'}'
		elif bigrep[i][2]==1 and bigrep[i][3]==1:
			nach='\\dfrac{'+''.join(bigrep[i][0][8:(len(bigrep[i][0])-9)])+'}{'+''.join(bigrep[i][1][8:(len(bigrep[i][1])-9)])+'}'
		# if the quocient at stake happens inside a file destined to print Feynman Rules, the maximum lenght of the string
		# shall be 200; otherwise, 250.	
		if nome == 'express':
			if len(bigrep[i][0])<250:
				arg=arg.replace(vor,nach)
		else:
			if len(bigrep[i][0])<200:
				arg=arg.replace(vor,nach)

	# What follows concerns avoiding things like {m_H}^2, which should be converted into m_H^2
	before='';	beftot = []; alist=list(arg)
	for i in range(len(alist)):
		if "".join(alist[i:i+2])=='}^':
			bigrep.append([])
			indbar=i
			strbefo="".join(alist[0:i])
			blist=list(strbefo)
			coin=1
			for j in range(len(blist)-1,-1,-1):
				if blist[j]=='}':
					coin=coin+1
				elif blist[j]=='{':
					coin=coin-1
				if coin==0:
					before="".join(blist[j:len(blist)])
					if '_' in before and '^' not in before and blist[j-1]!='_':
						beftot.append(before)
					break
	for i in range(len(beftot)):
		arg=arg.replace(beftot[i]+'}^',beftot[i][1:]+'^')

	# The same, but for things like {m^2}_i
	before='';	beftot = []; alist=list(arg)
	for i in range(len(alist)):
		if "".join(alist[i:i+2])=='}_':
			bigrep.append([])
			indbar=i
			strbefo="".join(alist[0:i])
			blist=list(strbefo)
			coin=1
			for j in range(len(blist)-1,-1,-1):
				if blist[j]=='}':
					coin=coin+1
				elif blist[j]=='{':
					coin=coin-1
				if coin==0:
					before="".join(blist[j:len(blist)])
					if '^' in before and '_' not in before and blist[j-1]!='^':
						beftot.append(before)
					break
	for i in range(len(beftot)):
		arg=arg.replace(beftot[i]+'}_',beftot[i][1:]+'_')

	return arg


# Now we define the main function destined to convert from FeynCalc to Fortran
def FCtoFT(arg,myretil):
	myreal = 'REAL' if myretil == True else ''
	arg=arg.replace(', PaVeAutoOrder -> True, PaVeAutoReduce -> True','')
	arg=arg.replace(', PaVeAutoOrder -> True, PaVeAutoReduce -> False','')
	auxPV = re.findall(r'PaVe\[(.*?), {(.*?)}, {(.*?)}\]', arg)
	for i in range(len(auxPV)):
		pvaux=auxPV[i][2].split(', ')
		if len(pvaux)==1:
			let1='a0i'
			let2='aa'
		elif len(pvaux)==2:
			let1='b0i'
			let2='bb'
		elif len(pvaux)==3:
			let1='c0i'
			let2='cc'
		elif len(pvaux)==4:
			let1='d0i'
			let2='dd'
		auxPVs=auxPV[i][0].split(', ')
		if auxPVs != []:
			auxPVf=''
			for j in range(len(auxPVs)):
				auxPVf = auxPVf + auxPVs[j]
		else:
			auxPVf=auxPV[i][0]
		if auxPV[i][1] != [] and auxPV[i][1] != '':
			middle = ',' + auxPV[i][1] + ',' if (auxPV[i][1] != [] and auxPV[i][1] != '') else ''
		elif auxPV[i][1] == '':
			middle = ','
		else:
			middle = ''
		arg=arg.replace('PaVe[' + auxPV[i][0] + ', {' + auxPV[i][1] + '}, {' + auxPV[i][2] + '}]', myreal + '(' + let1 + '[' + let2 + auxPVf + middle + auxPV[i][2] + '])')

	if myretil == True:
		thepv1=['A0','A00']
		thepv2=['B0','B1','B00','B11','B001','B111']
		thepv3=['DB0','DB1','DB00','DB11','DB001','DB111']
		thepv4=['C0','D0','E0']
		thepv=thepv1+thepv2+thepv3+thepv4
		for i in range(len(thepv)):
			auxpvpre = myfindall2(arg,thepv[i])[0]
			auxpv=list(dict.fromkeys(auxpvpre)) # to remove repeated items
			for j in range(len(auxpv)):
				prepvclean=auxpv[j]
				prepv=prepvclean
				prepv=prepv.replace('\\','\\\\'); prepv=prepv.replace('[','\['); 
				prepv=prepv.replace('^','\^'); prepv=prepv.replace('.','\.');
				prepv=prepv.replace('*','\*'); prepv=prepv.replace('+','\+');
				prepv=prepv.replace('(','\('); prepv=prepv.replace(')','\)');
				arg = re.sub(r'(?<![a-zA-Z0-9])'+thepv[i]+'\['+prepv+'\]','REAL('+thepv[i]+'['+prepvclean+']'+')',arg)

	auxmt = re.findall(r"(?<="+'Cot'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxmt)):
		auxmt2=auxmt[i]
		arg=arg.replace('Cot['+auxmt2 + ']','[Cos['+auxmt2+']/Sin['+auxmt2+']]')
	auxmt = re.findall(r"(?<="+'Sec'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxmt)):
		auxmt2=auxmt[i]
		arg=arg.replace('Sec['+auxmt2 + ']','[1/Cos['+auxmt2+']]')
	auxmt = re.findall(r"(?<="+'Csc'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxmt)):
		auxmt2=auxmt[i]
		arg=arg.replace('Csc['+auxmt2 + ']','[1/Sin['+auxmt2+']]')
	auxPL = re.findall(r"(?<="+'PolyLog'+r"\[)(.*?)(?=\])", arg)
	for i in range(len(auxPL)):
		auxPLb = auxPL[i]
		auxPLc = auxPLb.split(', ')
		arg=arg.replace('PolyLog[' + auxPLb + ']','Li'+auxPLc[0]+'['+auxPLc[1]+']')
	arg=arg.replace('*^','*10^')
	arg=arg.replace('E^','2.718281828459045**')
	arg=arg.replace('Re[','REAL['); arg=arg.replace('Im[','AIMAG[');
	arg=arg.replace('^','**'); arg=arg.replace('[','('); arg=arg.replace(']',')');
	arg=arg.replace('***','**');
	arg=arg.replace('Sqrt','sqrt'); arg=arg.replace('Conjugate','CONJG');

	alist=list(arg)
	for i in range(len(alist)):
		if alist[i] == 'I':
			if i==0 or i==len(alist)-1:
				alist[i]='(0,1)'
			else:
				if not alist[i-1].isalnum() and not alist[i+1].isalnum():
					alist[i]='(0,1)'
	arg="".join(alist)

	Myd0='d0' # For normal precision, choose Myd0='d0'
	#Myd0='q0' # For quadrupole precision, choose Myd0='q0'

	arg = re.sub(r'(?<![a-zA-Z0-9])'+'0, ','0'+Myd0+', ',arg) #we do this because, apparently, when I ask him to find '0.', Python also finds '0,'
	# arg = re.sub(r'(?<![a-zA-Z0-9])'+'0), ','0d0), ',arg) #we do this because, apparently, when I ask him to find '0.', Python also finds '0,'

	zecapre = re.findall(r'(?<![a-zA-Z0-9])'+'0\.'+r'(\d+\.?(?<![a-z])\d*)', arg) # also an incompreehensible Python need
	zeca=list(dict.fromkeys(zecapre)) # to remove repeated items
	for i in range(len(zeca)):
		arg = re.sub(r'(?<![a-zA-Z0-9])'+'0\.'+zeca[i]+r'(?![0-9])','0.'+zeca[i]+Myd0,arg)

	zecapre = re.findall(r'(?<![a-zA-Z0-9])'+'1\.'+r'(\d+\.?(?<![a-z])\d*)', arg) # also an incompreehensible Python need
	zeca=list(dict.fromkeys(zecapre)) # to remove repeated items
	for i in range(len(zeca)):
		arg = re.sub(r'(?<![a-zA-Z0-9])'+'1\.'+zeca[i]+r'(?![0-9])','1.'+zeca[i]+Myd0,arg)

	auxdot = re.findall(r'(?<![a-zA-Z0-9])(\d+\.?(?<![a-z])\d*)', arg)

	auxdot2=[];
	for i in range(len(auxdot)):
		if auxdot[i] not in auxdot2:
			auxdot2.append(auxdot[i])

	for i in range(len(auxdot2)):
		mysafe=auxdot2[i]
		mynew=mysafe
		mynew=mynew.replace('\\','\\\\'); mynew=mynew.replace('[','\[');
		mynew=mynew.replace('^','\^'); mynew=mynew.replace('.','\.');
		mynew=mynew.replace('*','\*'); mynew=mynew.replace('+','\+');
		mynew=mynew.replace('(','\('); mynew=mynew.replace(')','\)');
		uaux=re.findall(r'(?<![a-zA-Z0-9])'+mynew+r'(?![a-zA-Z0-9.])',arg)
		arg = re.sub(r'(?<![a-zA-Z0-9])'+mynew+r'(?![a-zA-Z0-9.])',mysafe+Myd0,arg)
	arg=arg.replace('0'+Myd0+'.'+Myd0,'0'+Myd0)
	arg=arg.replace(Myd0+'.','.')

	zecapre = re.findall(r'(?<=[0-9])'+'\*\*-'+r'(\d+\.?)'+Myd0, arg) # also an incompreehensible Python need
	zeca=list(dict.fromkeys(zecapre)) # to remove repeated items
	for i in range(len(zeca)):
		arg = re.sub(r'(?<=[0-9])'+'\*\*-'+zeca[i]+Myd0,'**(-'+zeca[i]+Myd0+')',arg)

	fCV="auxFT.m"
	toutcourt = []; auxCV= [];
	if os.path.isfile(fCV):
		f = open(fCV, 'r');	allLines = f.read().splitlines();	f.close()
		for l in allLines:
			toutcourt.append(l)
		for i in range(len(toutcourt)):
			auxCV.append(toutcourt[i].split(' -> '))
		for i in range(len(auxCV)):
			arg = re.sub(r'(?<![a-zA-Z0-9])'+auxCV[i][0]+r'(?![a-zA-Z0-9])',auxCV[i][1],arg)

	nc=56; nlmax=2000; kflag=0;
	danger=['aa','bb','cc','dd']
	arr=[];
	coinaux=mynestpo(arg)
	coinstr=''.join(coinaux)

	for k in range(0,nlmax):
		nl = 100
		jind=0; forbid=0; cool=0;
		arg2='      Out('+str(k+1)+')=\n     &'
		linind = 0
		oldtab=0
		argfix=arg
		for i in range(0,len(argfix), nc):
			ii=i+oldtab
			ring=arg[ii+nc-3:ii+nc+1]
			# Check if we must change k as a result of having achieved the maximum number of lines
			if linind > nl:
				arg=arg[(ii-(nc-jind)):len(arg)]
				coinstr=coinstr[(ii-(nc-jind)):len(coinstr)]
				arr.append(arg2)
				break	
			else:
				# The most normal scenario
				if (len(arg)-(ii))>nc and linind!=nl:
					newtab=3 if any(x in ring for x in danger) else 0
					arg2=arg2+arg[ii:ii+newtab+nc]+'\n     &'
					oldtab+=newtab
					linind+= 1
				# The scenario in which we have achieved the last line
				elif (len(arg)-(ii))>nc and linind==nl:
					x0=arg[ii:ii+nc]
					x1=coinstr[ii:ii+nc]
					for j in range(len(x0)):
						if (x0[j] == '+' or x0[j] == '-') and x1[j]=='0':
							jind=j
							arg2=arg2+arg[ii:ii+j]
							cool+=1
							break
					# When the supposed last line cannot be broken, then it must be
					# written down, and the following line becomes the last line
					if cool==0:
						newtab=3 if any(x in ring for x in danger) else 0
						arg2=arg2+arg[ii:ii+newtab+nc]+'\n     &'
						oldtab+=newtab						
						nl+=1
					linind+= 1
				# When the string that should be written is finishing
				else:
					kflag=k
					if arg!='':
						arg2=arg2+arg[ii:ii+nc]
					else:
						arg2=arg2
					arg=''
					arr.append(arg2)
				
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
	fCV='FRtoTeX.m'
	toutcourt = []; auxCV= []; finalA=[]; finalS='';
	if os.path.isfile(fCV):
		f = open(fCV, 'r');	allLines = f.read().splitlines();	f.close()
		for l in allLines:
			toutcourt.append(l)
		for i in range(len(toutcourt)):
			auxCV.append(toutcourt[i].split(' -> '))
		for j in range(len(auxCV)):
			# if not any(auxCV[j][0] == x for x in renconsaddlist):
			if not any(auxCV[j][0] == x for x in matnames):
				finalA.append(auxCV[j][0])
			else:
				for k in range(len(matnames)):
					if auxCV[j][0]==matnames[k]:
						for k1 in range(int(rowaux2[k][1])):
							if len(rowaux2[k])>2: 
								for k2 in range(int(rowaux2[k][2])):
									finalA.append(auxCV[j][0]+str(k1+1)+str(k2+1))
							else:
								finalA.append(auxCV[j][0]+str(k1+1))
		for j in range(len(finalA)):
			finalS=finalS + finalA[j] + ','
		finalS = finalS [:-1]
		finalS = finalS + ',S,Theta'
	kflag=kflag+1
	return (arr,kflag,finalS)



if __name__ == '__main__':
	fnames=['PrePropagators.m','PreRulesv3Gauge.m','PreRulesv4Gauge.m','PreRulesv3Fermions.m','PreRulesv3Yukawa.m','PreRulesv3Higgs.m','PreRulesv4Higgs.m','PreRulesv3Ghosts.m','PreRulesv4Ghosts.m','PreRulesv3Beaks.m','PreRulesv4Beaks.m']
	Totlist = []
	for i in range(len(fnames)):
		Totlist.append([])
	for i in range(len(fnames)):	
		if os.path.isfile(fnames[i]):
			f = open(fnames[i], 'r')
			allLines = f.read().splitlines()
			f.close()
			for l in allLines:
				if len(l)<3: continue
				else: Totlist[i].append(l)
	for i in range(len(fnames)):
		if os.path.isfile(fnames[i]):
			newru = open(fnames[i][3:], 'w')
			for j in range(len(Totlist[i])):
				newru.write(FRtoFC(Totlist[i][j])+'\n\n')
			newru.close()

	fCT='CTpre.m'
	TotCTlist = []
	if os.path.isfile(fCT):
		f = open(fCT, 'r')
		allLines = f.read().splitlines()
		f.close()
		for l in allLines:
			if len(l)<3: continue
			else: TotCTlist.append(l)
		newru = open('CTini.m', 'w')
		# newru.write('CTinilist := {')
		MyCTrules=[]
		MyRest=[]
		for k in range(len(TotCTlist)):
			if TotCTlist[k][:5] == '+++++':
				MyCTrules.append(FRtoFC(TotCTlist[k][6:]).replace('fv[k','fv[p'))
			elif TotCTlist[k][:9] == 'CTord := ':
				zun1=TotCTlist[k][10:-1]
				zun2=zun1.split(', {')
				zun3=[]
				for k2 in range(len(zun2)):
					zun3.append(zun2[k2]) if k2==0 else zun3.append('{'+zun2[k2])
			else:
				MyRest.append(TotCTlist[k])
		newru.write('CTlist := {\n\n')
		if len(MyCTrules)==len(zun3):
			for k3 in range(len(zun3)):
				newru.write('{' + zun3[k3] + ', {' + MyCTrules[k3] + '}}')
				newru.write(',\n\n') if k3!=(len(zun3)-1) else newru.write('\n\n')
			newru.write('}\n\n')
		for k3 in range(len(MyRest)):
			newru.write(MyRest[k3]+'\n')
		newru.close()	

	fPE='preexp.m'
	TotPElist = []
	if os.path.isfile(fPE):
		f = open(fPE, 'r');	allLines = f.read().splitlines();	f.close()
		for l in allLines:
			TotPElist.append(l)
		newru = open('exp.tex', 'w')
		for k in range(len(TotPElist)):
			if k<33:
				newru.write(TotPElist[k]+'\n')
			elif k == len(TotPElist):
				newru.write(TotPElist[k]+'\n')
			else:
				if TotPElist[k-1]=='\\bd ' and TotPElist[k+1]=='\\ed ':
					scribendum=FCtoTEX(TotPElist[k],'express')
					newru.write(scribendum+'\n')						
				else:
					newru.write(TotPElist[k]+'\n')
		newru.close()	
