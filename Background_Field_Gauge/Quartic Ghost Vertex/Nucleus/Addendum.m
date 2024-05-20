(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
This is the Addendum.m file, a Mathematica routine for FeynRules that creates external files which
will allow us to establish an interface between the FeynRules environment, on the one hand, and both
QGRAF and Amperate, on the other. For QGRAF, we generate the model file: the file which shall be read
by QGRAF as describing the model. As for Amperate, we generate several files with the Feynman rules 
of the model.

Created by: Duarte Fontes
Email: duartefontes@tecnico.ulisboa.pt
Last update: 21.07.2020
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)

(* Get the Feynman rules for the vertices*)
If[ToString[InputForm[LGauge]] != "LGauge", vertsGauge = FeynmanRules[LGauge]];
If[ToString[InputForm[LHiggs]] != "LHiggs", vertsHiggs = FeynmanRules[LHiggs]];
If[ToString[InputForm[LGhost]] != "LGhost", vertsGhosts = FeynmanRules[LGhost]];
If[ToString[InputForm[LFermions]] != "LFermions", vertsFermionsFlavor = FeynmanRules[WeylToDirac[LFermions], FlavorExpand -> True]];
If[ToString[InputForm[LYukawa]] != "LYukawa", vertsYukawa = FeynmanRules[WeylToDirac[LYukawa], FlavorExpand -> True]];
If[ToString[InputForm[LBeaks]] != "LBeaks", vertsBeaks = FeynmanRules[LBeaks, FlavorExpand -> True]];

propsrulestot={};
propsrulesexp={};
If[PrMassFL,
(* Determine the rules for the propagators in case the masses should be extracted from the Lagrangean *)
(* N.B.: the fermionic propagators are never determined in this way *)
LProppre = 0;
If[ToString[InputForm[LGauge]] != "LGauge", LProppre += ExpandIndices[LGauge]];
If[ToString[InputForm[LHiggs]] != "LHiggs", LProppre += ExpandIndices[LHiggs]];
If[ToString[InputForm[LGhost]] != "LGhost", LProppre += ExpandIndices[LGhost]];
If[ToString[InputForm[LGF]] != "LGF", LProppre += ExpandIndices[LGF]];
LProppre = Expand[LProppre];
LProp=ExpandIndices[LProppre, MaxParticles -> 2];
LP1 = LProp /. insetas;
LP2 = LP1 /. consrules;
LP3 = (LP2 /. stilletas) // Expand;
LP4a = LP3 /. consrules;
LP4b = LP4a /. repsetas /. repsetas /. repsetas /. repsetas;
LP5 = (LP4b /. proprep);
Do[
LP6a = (((Coefficient[LP5, propsetas[[i]]] // Simplify) /. MyRestr) // FullSimplify) /. MyRestr;
LP6b = ((LP6a // Expand) // FullSimplify) /. MyRestr;
LP6c = FullSimplify[LP6b/I];
If[ToString[InputForm[propstypes[[i]]]]=="S"||ToString[InputForm[propstypes[[i]]]]=="U",
LP7 = 1/LP6c;
LP8 = Parc[LP7 // Expand];
If[LP7 == LP8,
	LP9 = Denominator[LP8];
	If[Coefficient[LP9,p,2]==-1,propmass=mysqrt[LP9/.p->0],propmass=mysqrt[-LP9/.p->0]];
	If[colcoin!=0&&ToString[InputForm[propsnames[[i]]]]==ToString[InputForm[myglugh]],
		propsrulestot=Append[propsrulestot,"prop" <> propsnames[[i]] <> "[m_,p_,J1_,J2_]:= I Deno[p,"<>ToString[InputForm[propmass]]<>","<>propsnames[[i]]<>"] SUNDelta[Gluonize[J1], Gluonize[J2]]"];
		propsrulesexp=Append[propsrulesexp,"I Deno[p,"<>ToString[InputForm[propmass]]<>","<>propsnames[[i]]<>"] SUNDelta[Gluonize[J1], Gluonize[J2]]"],
		propsrulestot=Append[propsrulestot,"prop" <> propsnames[[i]] <> "[m_,p_,J1_,J2_]:= I Deno[p,"<>ToString[InputForm[propmass]]<>","<>propsnames[[i]]<>"]"];
		propsrulesexp=Append[propsrulesexp,"I Deno[p,"<>ToString[InputForm[propmass]]<>","<>propsnames[[i]]<>"]"]]],
If[ToString[InputForm[propstypes[[i]]]]=="V",
LP7=LP6b/.myprops;
LP8=(LP7*(myc3*ME[-J2, -J3] + myc4*FV[p, -J2] FV[p, -J3]) - ME[-J1, -J3] // Expand) // MyContract;
LP9a = LP8 /. FV[x_, y_] -> 0;
LP9b = ((MySolve[LP9a, myc3] // MyContract) // Simplify);
LP10a = ((MySolve[LP8 /. LP9b, myc4] // MyContract) // Simplify);
If[ToString[InputForm[LP10a[[2]]]]=="ComplexInfinity",LP10a=myc4->0];
LP11=(-1)*(((myc3*ME[-J1, -J2] + myc4*FV[p, -J1] FV[p, -J2]) /. LP9b) /. LP10a);
LP12 = Parc[LP11 // Expand];
propfinaux=0;
Do[
propDenoaux="";
LPDeno = LP12[[j]] // Denominator;
LPNume = LP12[[j]] // Numerator;
If[ToString[InputForm[Level[LPDeno, 1][[1]]*Level[LPDeno, 1][[2]]]] == ToString[InputForm[LPDeno]],
Do[If[Coefficient[Level[LPDeno, 1][[k]],p,2]==-1,propmass=mysqrt[Level[LPDeno, 1][[k]]/.p->0],propmass=mysqrt[-Level[LPDeno, 1][[k]]/.p->0]];
propDenoaux=propDenoaux<>"Deno[p,"<>ToString[InputForm[propmass]]<>","<>propsnames[[i]]<>"]*";
propDenoaux2=ToExpression[StringDrop[propDenoaux,-1]],{k,1,Length[Level[LPDeno, 1]]}],
If[ToString[InputForm[Level[LPDeno, 1][[1]] + Level[LPDeno, 1][[2]]]] == ToString[InputForm[LPDeno]],
myfac=1;
If[Coefficient[LPDeno,p,2]==-1,myfac=-1;propmass=mysqrt[LPDeno/.p->0],propmass=mysqrt[-LPDeno/.p->0]];
propDenoaux2 = myfac*Deno[p,propmass,ToExpression[propsnames[[i]]]],
If[ToString[InputForm[Level[LPDeno, 1][[1]]^Level[LPDeno, 1][[2]]]] == ToString[InputForm[LPDeno]],
If[Level[LPDeno, 1][[2]]==2,propDenoaux2=Deno[p,0,ToExpression[propsnames[[i]]]],If[Level[LPDeno, 1][[2]]==4,propDenoaux2=Deno[p,0,ToExpression[propsnames[[i]]]]^2]]]]];
propfinaux += LPNume*propDenoaux2,{j,1,Length[LP12]}];
If[colcoin!=0&&ToString[InputForm[propsnames[[i]]]]==ToString[InputForm[myglu]],
	propsrulestot=Append[propsrulestot,"prop" <> propsnames[[i]] <> "[m_,p_,J1_,J2_]:= "<>ToString[InputForm[FullSimplify[propfinaux]]] <>" SUNDelta[Gluonize[J1], Gluonize[J2]]"];
	propsrulesexp=Append[propsrulesexp,ToString[InputForm[FullSimplify[propfinaux]]] <>" SUNDelta[Gluonize[J1], Gluonize[J2]]"],
	propsrulestot=Append[propsrulestot,"prop" <> propsnames[[i]] <> "[m_,p_,J1_,J2_]:= "<>ToString[InputForm[FullSimplify[propfinaux]]]];
	propsrulesexp=Append[propsrulesexp,ToString[InputForm[FullSimplify[propfinaux]]]]]]],{i,1,Length[propsnames]}],

(* Determine the rules for the propagators in a simplified version *)
Do[
propmass = ToString[ToExpression["m"<>palist2[[i,2]]] /. masstrade];
If[palist2[[i,1]]=="S" || palist2[[i,1]]=="U",
	If[colcoin!=0&&ToString[InputForm[palist2[[i,2]]]]==ToString[InputForm[myglugh]],
		propsrulestot=Append[propsrulestot,"prop" <> palist2[[i,2]] <> "[m_,p_,J1_,J2_]:= I Deno[p,"<> propmass <>","<>palist2[[i,2]]<>"] SUNDelta[Gluonize[J1], Gluonize[J2]]"];
		propsrulesexp=Append[propsrulesexp,"I Deno[p,"<> propmass <>","<>palist2[[i,2]]<>"] SUNDelta[Gluonize[J1], Gluonize[J2]]"],
		propsrulestot=Append[propsrulestot,"prop" <> palist2[[i,2]] <> "[m_,p_,J1_,J2_]:= I Deno[p,"<> propmass <>","<>palist2[[i,2]]<>"]"];
		propsrulesexp=Append[propsrulesexp,"I Deno[p,"<> propmass <>","<>palist2[[i,2]]<>"]"]],
If[palist2[[i,1]]=="V",
	If[colcoin!=0&&ToString[InputForm[palist2[[i,2]]]]==ToString[InputForm[myglu]],
		propsrulestot=Append[propsrulestot,"prop" <> palist2[[i,2]] <> "[m_,p_,J1_,J2_]:= -I Deno[p,"<> propmass <>","<>palist2[[i,2]]<>"] ME[Index[Lorentz, Ext[1]], Index[Lorentz, Ext[2]]] SUNDelta[Gluonize[J1], Gluonize[J2]]"];
		propsrulesexp=Append[propsrulesexp,"-I Deno[p,"<> propmass <>","<>palist2[[i,2]]<>"] ME[Index[Lorentz, Ext[1]], Index[Lorentz, Ext[2]]] SUNDelta[Gluonize[J1], Gluonize[J2]]"],
		propsrulestot=Append[propsrulestot,"prop" <> palist2[[i,2]] <> "[m_,p_,J1_,J2_]:= -I Deno[p,"<> propmass <>","<>palist2[[i,2]]<>"] ME[Index[Lorentz, Ext[1]], Index[Lorentz, Ext[2]]]"];
		propsrulesexp=Append[propsrulesexp,"-I Deno[p,"<> propmass <>","<>palist2[[i,2]]<>"] ME[Index[Lorentz, Ext[1]], Index[Lorentz, Ext[2]]]"]]]],{i, 1, Length[palist2]}]
];

(* Determine the rules for the propagators in the unitary gauge *)
Do[
If[MemberQ[GaugeWithGold, palist3[[i, 2]]],
	propmass = ToString[ToExpression["m"<>palist2[[i,2]]] /. masstrade];
	propsrulestot=Append[propsrulestot,"prop" <> palist2[[i,2]] <> "UG[m_,p_,J1_,J2_]:= I Deno[p,"<> propmass <>","
	<>palist2[[i,2]]<>"] (-ME[Index[Lorentz, Ext[1]], Index[Lorentz, Ext[2]]] + fv[p,J1] fv[p,J2]/"<> propmass <>"^2)"]],{i, 1, Length[palist2]}];

(* Determine the rules for the fermionic propagators *)
Do[If[palist2[[i,1]]=="F",
propmass = ToString[ToExpression["m"<>palist2[[i,2]]] /. masstrade];
propsrulestot = Append[propsrulestot,"prop" <> palist2[[i,2]] <> "[m_,p_,J1_,J2_]:= I fprop[p," <> propmass <> "] Deno[p," <> propmass <> ","<>palist2[[i,2]]<>"]"];
propsrulesexp = Append[propsrulesexp,"I fprop[p," <> propmass <> "] Deno[p," <> propmass <> ","<>palist2[[i,2]]<>"]"];
propsnames = Append[propsnames,palist2[[i, 2]]]],{i, 1, Length[palist2]}];


(* * * * QGRAF INTERFACE * * * *)
fileQG = OpenWrite["built-model"];

Do[WriteString[fileQG, "[", auxprop[[i, 1]], ",", auxprop[[i, 2]], ",", auxprop[[i, 3]], "] \n"], {i, 1, Length[auxprop]}];
WriteString[fileQG, "\n \n"]

hand = vertsHiggs;
If[ToString[InputForm[hand]] != ToString[hand],
	CubicvertsHiggs = SelectVertices[vertsHiggs, MaxParticles -> 3];
	If[CubicvertsHiggs != {},
		zerov3 = {};
		Goodv3 = {};
		v3 = CubicvertsHiggs;
		Do[If[((v3[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov3 = Append[zerov3, i]], {i, 1,Length[v3]}];
		Do[If[! MemberQ[zerov3, i], 
			Goodv3 = Append[Goodv3, {v3[[i, 1]][[1, 1]], v3[[i, 1]][[2, 1]], v3[[i, 1]][[3, 1]]}]], {i, 1, Length[v3]}];
		Aux1v3 = Table[{Goodv3[[i, 1]], Goodv3[[i, 2]], Goodv3[[i, 3]]}, {i, 1, Length[Goodv3]}];
		v3HiggsQgraf = Aux1v3;
		Do[WriteString[fileQG, "[", v3HiggsQgraf[[i, 1]], ",", v3HiggsQgraf[[i, 2]], ",", v3HiggsQgraf[[i, 3]], "]\n"], {i, 1, Length[v3HiggsQgraf]}];]];

If[ToString[InputForm[hand]] != ToString[hand],
	QuarticvertsHiggs = SelectVertices[vertsHiggs, MinParticles -> 4];
	If[QuarticvertsHiggs != {},
		zerov4 = {};
		Goodv4 = {};
		v4 = QuarticvertsHiggs;
		Do[If[((v4[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov4 = Append[zerov4, i]], {i, 1, Length[v4]}];
		Do[If[! MemberQ[zerov4, i],
			Goodv4 = Append[Goodv4, {v4[[i, 1]][[1, 1]], v4[[i, 1]][[2, 1]], v4[[i, 1]][[3, 1]], v4[[i, 1]][[4, 1]]}]], {i, 1, Length[v4]}];
		Aux1v4 = Table[{Goodv4[[i, 1]], Goodv4[[i, 2]], Goodv4[[i, 3]], Goodv4[[i, 4]]}, {i, 1, Length[Goodv4]}];
		v4HiggsQgraf = Aux1v4;
		Do[WriteString[fileQG, "[", v4HiggsQgraf[[i, 1]], ",", v4HiggsQgraf[[i, 2]], ",", v4HiggsQgraf[[i, 3]], ",", v4HiggsQgraf[[i, 4]], "]\n"], {i, 1, Length[v4HiggsQgraf]}]]];

hand = vertsGauge;
If[ToString[InputForm[hand]] != ToString[hand],
	CubicvertsGauge = SelectVertices[vertsGauge, MaxParticles -> 3];
	If[CubicvertsGauge != {},
		zerov3 = {};
		Goodv3 = {};
		v3 = CubicvertsGauge;
		Do[If[((v3[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov3 = Append[zerov3, i]], {i, 1, Length[v3]}];
		Do[If[! MemberQ[zerov3, i], Goodv3 = Append[Goodv3, {v3[[i, 1]][[1, 1]], v3[[i, 1]][[2, 1]], v3[[i, 1]][[3, 1]]}]], {i, 1, Length[v3]}];
		Aux1v3 = Table[{Goodv3[[i, 1]], Goodv3[[i, 2]], Goodv3[[i, 3]]}, {i, 1, Length[Goodv3]}];
		v3GaugeQgraf = Aux1v3;
		Do[WriteString[fileQG, "[", v3GaugeQgraf[[i, 1]], ",", v3GaugeQgraf[[i, 2]], ",", v3GaugeQgraf[[i, 3]], "]\n"], {i, 1, Length[v3GaugeQgraf]}]]];

If[ToString[InputForm[hand]] != ToString[hand],
	QuarticvertsGauge = SelectVertices[vertsGauge, MinParticles -> 4];
	If[QuarticvertsGauge != {},
		zerov4 = {};
		Goodv4 = {};
		v4 = QuarticvertsGauge;
		Do[If[((v4[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov4 = Append[zerov4, i]], {i, 1, Length[v4]}];
		Do[If[! MemberQ[zerov4, i], 
			Goodv4 = Append[Goodv4, {v4[[i, 1]][[1, 1]], v4[[i, 1]][[2, 1]], v4[[i, 1]][[3, 1]], v4[[i, 1]][[4, 1]]}]], {i, 1, Length[v4]}];
		Aux1v4 = 	Table[{Goodv4[[i, 1]], Goodv4[[i, 2]], Goodv4[[i, 3]], Goodv4[[i, 4]]}, {i, 1, Length[Goodv4]}];
		v4GaugeQgraf = Aux1v4;
		Do[WriteString[fileQG, "[", v4GaugeQgraf[[i, 1]], ",", v4GaugeQgraf[[i, 2]], ",", v4GaugeQgraf[[i, 3]], ",", v4GaugeQgraf[[i, 4]], "]\n"], {i, 1, Length[v4GaugeQgraf]}]]];

hand = vertsFermionsFlavor;
If[ToString[InputForm[hand]] != ToString[hand],
	CubicvertsFermions = SelectVertices[vertsFermionsFlavor, MaxParticles -> 3];
	If[CubicvertsFermions != {},
		zerov3 = {};
		Goodv3 = {};
		v3 = CubicvertsFermions;
		Do[If[((v3[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov3 = Append[zerov3, i]], {i, 1, Length[v3]}];
		Do[If[! MemberQ[zerov3, i], Goodv3 = Append[Goodv3, {v3[[i, 1]][[1, 1]], v3[[i, 1]][[2, 1]], v3[[i, 1]][[3, 1]]}]], {i, 1, Length[v3]}];
		Aux1v3 = 	Table[{Goodv3[[i, 1]], Goodv3[[i, 2]], Goodv3[[i, 3]]}, {i, 1, Length[Goodv3]}];
		v3FermionsQgraf = Aux1v3;
		Do[WriteString[fileQG, "[", v3FermionsQgraf[[i, 1]], ",", v3FermionsQgraf[[i, 2]], ",", v3FermionsQgraf[[i, 3]], "]\n"], {i, 1, Length[v3FermionsQgraf]}]]];

hand = vertsYukawa;
If[ToString[InputForm[hand]] != ToString[hand],
	CubicvertsYukawa = SelectVertices[vertsYukawa, MaxParticles -> 3];
	If[CubicvertsYukawa != {},
		zerov3 = {};
		Goodv3 = {};
		v3 = CubicvertsYukawa;
		Do[If[((v3[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov3 = Append[zerov3, i]], {i, 1, Length[v3]}];
		Do[If[! MemberQ[zerov3, i], Goodv3 = Append[Goodv3, {v3[[i, 1]][[1, 1]], v3[[i, 1]][[2, 1]], v3[[i, 1]][[3, 1]]}]], {i, 1, Length[v3]}];
		Aux1v3 = Table[{Goodv3[[i, 1]], Goodv3[[i, 2]], Goodv3[[i, 3]]}, {i, 1, Length[Goodv3]}];
		v3YukawaQgraf = Aux1v3;
		Do[WriteString[fileQG, "[", v3YukawaQgraf[[i, 1]], ",", v3YukawaQgraf[[i, 2]], ",", v3YukawaQgraf[[i, 3]], "]\n"], {i, 1, Length[v3YukawaQgraf]}]]];

hand = vertsGhosts;
If[ToString[InputForm[hand]] != ToString[hand],
	CubicvertsGhosts = SelectVertices[vertsGhosts, MaxParticles -> 3];
	If[CubicvertsGhosts != {},
		zerov3 = {};
		Goodv3 = {};
		v3 = CubicvertsGhosts;
		Do[If[((v3[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov3 = Append[zerov3, i]], {i, 1, Length[v3]}];
		Do[If[! MemberQ[zerov3, i], Goodv3 = Append[Goodv3, {v3[[i, 1]][[1, 1]], v3[[i, 1]][[2, 1]], v3[[i, 1]][[3, 1]]}]], {i, 1, Length[v3]}];
		Aux1v3 = Table[{Goodv3[[i, 1]], Goodv3[[i, 2]], Goodv3[[i, 3]]}, {i, 1, Length[Goodv3]}];
		v3GhostsQgraf = 	Aux1v3;
		Do[WriteString[fileQG, "[", v3GhostsQgraf[[i, 1]], ",", v3GhostsQgraf[[i, 2]], ",", v3GhostsQgraf[[i, 3]], "]\n"], {i, 1, Length[v3GhostsQgraf]}]]];
		
If[ToString[InputForm[hand]] != ToString[hand],
	QuarticvertsGhosts = SelectVertices[vertsGhosts, MinParticles -> 4];
	If[QuarticvertsGhosts != {},
		zerov4 = {};
		Goodv4 = {};
		v4 = QuarticvertsGhosts;
		Do[If[((v4[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov4 = Append[zerov4, i]], {i, 1, Length[v4]}];
		Do[If[! MemberQ[zerov4, i], 
			Goodv4 = Append[Goodv4, {v4[[i, 1]][[1, 1]], v4[[i, 1]][[2, 1]], v4[[i, 1]][[3, 1]], v4[[i, 1]][[4, 1]]}]], {i, 1, Length[v4]}];
		Aux1v4 = 	Table[{Goodv4[[i, 1]], Goodv4[[i, 2]], Goodv4[[i, 3]], Goodv4[[i, 4]]}, {i, 1, Length[Goodv4]}];
		v4GhostsQgraf = Aux1v4;
		Do[WriteString[fileQG, "[", v4GhostsQgraf[[i, 1]], ",", v4GhostsQgraf[[i, 2]], ",", v4GhostsQgraf[[i, 3]], ",", v4GhostsQgraf[[i, 4]], "]\n"], {i, 1, Length[v4GhostsQgraf]}]]];
		
		
		

hand = vertsBeaks;
If[ToString[InputForm[hand]] != ToString[hand],
	CubicvertsBeaks = SelectVertices[vertsBeaks, MaxParticles -> 3];
	If[CubicvertsBeaks != {},
		zerov3 = {};
		Goodv3 = {};
		v3 = CubicvertsBeaks;
		Do[If[((v3[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov3 = Append[zerov3, i]], {i, 1, Length[v3]}];
		Do[If[! MemberQ[zerov3, i], Goodv3 = Append[Goodv3, {v3[[i, 1]][[1, 1]], v3[[i, 1]][[2, 1]], v3[[i, 1]][[3, 1]]}]], {i, 1, Length[v3]}];
		Aux1v3 = Table[{Goodv3[[i, 1]], Goodv3[[i, 2]], Goodv3[[i, 3]]}, {i, 1, Length[Goodv3]}];
		v3BeaksQgraf = 	Aux1v3;
		Do[WriteString[fileQG, "[", v3BeaksQgraf[[i, 1]], ",", v3BeaksQgraf[[i, 2]], ",", v3BeaksQgraf[[i, 3]], "]\n"], {i, 1, Length[v3BeaksQgraf]}]]];

If[ToString[InputForm[hand]] != ToString[hand],
	QuarticvertsBeaks = SelectVertices[vertsBeaks, MinParticles -> 4];
	If[QuarticvertsBeaks != {},
		zerov4 = {};
		Goodv4 = {};
		v4 = QuarticvertsBeaks;
		Do[If[((v4[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov4 = Append[zerov4, i]], {i, 1, Length[v4]}];
		Do[If[! MemberQ[zerov4, i],
			Goodv4 = Append[Goodv4, {v4[[i, 1]][[1, 1]], v4[[i, 1]][[2, 1]], v4[[i, 1]][[3, 1]], v4[[i, 1]][[4, 1]]}]], {i, 1, Length[v4]}];
		Aux1v4 = Table[{Goodv4[[i, 1]], Goodv4[[i, 2]], Goodv4[[i, 3]], Goodv4[[i, 4]]}, {i, 1, Length[Goodv4]}];
		v4BeaksQgraf = Aux1v4;
		Do[WriteString[fileQG, "[", v4BeaksQgraf[[i, 1]], ",", v4BeaksQgraf[[i, 2]], ",", v4BeaksQgraf[[i, 3]], ",", v4BeaksQgraf[[i, 4]], "]\n"], {i, 1, Length[v4BeaksQgraf]}]]];

Close[fileQG];


(* * * * AMPERATE INTERFACE * * * *)
stmp = OpenWrite["PrePropagators.m"];
Do[WriteString[stmp, propsrulestot[[i]]<>"\n \n"], {i, 1, Length[propsrulestot]}];
Close[stmp];



stmp2 = OpenWrite["PrePrintPropagators.m"];
Do[WriteString[stmp2, "{{{{{{", propsnames[[i]],",",propsnames[[i]],"}}}}}},{{{{{{ ", propsrulesexp[[i]], " }}}}}}\n \n"], {i, 1, Length[propsrulesexp]}];
Close[stmp2];

hand = vertsHiggs;
v3HiggsLogic = False;
If[ToString[InputForm[hand]] != ToString[hand],
	CubicvertsHiggs = SelectVertices[vertsHiggs, MaxParticles -> 3];
	If[CubicvertsHiggs != {},
		v3HiggsLogic = True;
		zerov3 = {};
		Goodv3 = {};
		Extv3 = {};
		v3 = CubicvertsHiggs;
		Do[If[((v3[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov3 = Append[zerov3, i]], {i, 1, Length[v3]}];
		Do[If[! MemberQ[zerov3, i], Goodv3 = Append[Goodv3, {v3[[i, 1]][[1, 1]], v3[[i, 1]][[2, 1]], v3[[i, 1]][[3, 1]]}];
		Extv3 = Append[Extv3, {ToString[InputForm[v3[[i, 2]]//Simplify]]}]], {i, 1, Length[v3]}];
		Ajuv3 = Table[{Extv3[[i, 1]]}, {i, 1, Length[Extv3]}];
		Aux1v3 = 	Table[{Goodv3[[i, 1]], Goodv3[[i, 2]], Goodv3[[i, 3]]}, {i, 1, Length[Goodv3]}];
		v3HiggsQgraf = Aux1v3;
		stmp = OpenWrite["PreRulesv3Higgs.m"];
		Do[WriteString[stmp, "vrtx", v3HiggsQgraf[[i, 1]], v3HiggsQgraf[[i, 2]], v3HiggsQgraf[[i, 3]],
										"[J1_,k1_,J2_,k2_,J3_,k3_]:= ", ToString[InputForm[(ToExpression[Ajuv3[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], "\n \n"], {i, 1, Length[v3HiggsQgraf]}];										
		Close[stmp];
		stmp2 = OpenWrite["PrePrintRulesv3Higgs.m"];
		Do[WriteString[stmp2, "{{{{{{", v3HiggsQgraf[[i, 1]],",",v3HiggsQgraf[[i, 2]],",",v3HiggsQgraf[[i, 3]], 
													"}}}}}},{{{{{{ ", ToString[InputForm[(ToExpression[Ajuv3[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], " }}}}}}\n \n"], {i, 1, Length[v3HiggsQgraf]}];
		Close[stmp2]]];

v4HiggsLogic = False;
If[ToString[InputForm[hand]] != ToString[hand],
	QuarticvertsHiggs = SelectVertices[vertsHiggs, MinParticles -> 4];
	If[QuarticvertsHiggs != {},
		v4HiggsLogic = True;
		zerov4 = {};
		Goodv4 = {};
		Extv4 = {};
		v4 = QuarticvertsHiggs;
		Do[If[((v4[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov4 = Append[zerov4, i]], {i, 1, Length[v4]}];
		Do[If[! MemberQ[zerov4, i],
			Goodv4 = Append[Goodv4, {v4[[i, 1]][[1, 1]],  v4[[i, 1]][[2, 1]], v4[[i, 1]][[3, 1]], v4[[i, 1]][[4, 1]]}];
			Extv4 = Append[Extv4, {ToString[InputForm[v4[[i, 2]]//Simplify]]}]], {i, 1, Length[v4]}];
		Aux1v4 = 	Table[{Goodv4[[i, 1]], Goodv4[[i, 2]], Goodv4[[i, 3]], Goodv4[[i, 4]]}, {i, 1, Length[Goodv4]}];
		Ajuv4 = Table[{Extv4[[i, 1]]}, {i, 1, Length[Extv4]}];
		v4HiggsQgraf = Aux1v4;
		stmp = OpenWrite["PreRulesv4Higgs.m"];
		Do[WriteString[stmp, "vrtx", v4HiggsQgraf[[i, 1]], v4HiggsQgraf[[i, 2]], v4HiggsQgraf[[i, 3]], v4HiggsQgraf[[i, 4]], 
													   "[J1_,k1_,J2_,k2_,J3_,k3_,J4_,k4_]:= ", ToString[InputForm[(ToExpression[Ajuv4[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], "\n \n"], {i, 1, Length[v4HiggsQgraf]}];
		Close[stmp];
		stmp2 = OpenWrite["PrePrintRulesv4Higgs.m"];
		Do[WriteString[stmp2, "{{{{{{", v4HiggsQgraf[[i, 1]],",",v4HiggsQgraf[[i, 2]],",",v4HiggsQgraf[[i, 3]],",",v4HiggsQgraf[[i, 4]], 
													   "}}}}}},{{{{{{ ", ToString[InputForm[(ToExpression[Ajuv4[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], " }}}}}}\n \n"], {i, 1, Length[v4HiggsQgraf]}];
		Close[stmp2]]];

hand = vertsGauge;
v3GaugeLogic = False;
If[ToString[InputForm[hand]] != ToString[hand],
	CubicvertsGauge = 	SelectVertices[vertsGauge, MaxParticles -> 3];
	If[CubicvertsGauge != {},
		v3GaugeLogic = True;
		zerov3 = {};
		Goodv3 = {};
		Extv3 = {};
		v3 = CubicvertsGauge;
		Do[If[((v3[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov3 = Append[zerov3, i]], {i, 1, Length[v3]}];
		Do[If[! MemberQ[zerov3, i], Goodv3 = Append[Goodv3, {v3[[i, 1]][[1, 1]], v3[[i, 1]][[2, 1]], v3[[i, 1]][[3, 1]]}];		  
			Extv3 = Append[Extv3, {ToString[InputForm[v3[[i, 2]]//Simplify]]}]], {i, 1, Length[v3]}];
		Ajuv3 = Table[{Extv3[[i, 1]]}, {i, 1, Length[Extv3]}];
		Aux1v3 = Table[{Goodv3[[i, 1]], Goodv3[[i, 2]], Goodv3[[i, 3]]}, {i, 1, Length[Goodv3]}];
		v3GaugeQgraf = Aux1v3;
		stmp = OpenWrite["PreRulesv3Gauge.m"];
		Do[WriteString[stmp, "vrtx", v3GaugeQgraf[[i, 1]], v3GaugeQgraf[[i, 2]], v3GaugeQgraf[[i, 3]], 
													   "[J1_,k1_,J2_,k2_,J3_,k3_]:= ", ToString[InputForm[(ToExpression[Ajuv3[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], "\n \n"], {i, 1, Length[v3GaugeQgraf]}];
		Close[stmp];
		stmp2 = OpenWrite["PrePrintRulesv3Gauge.m"];
		Do[WriteString[stmp2, "{{{{{{", v3GaugeQgraf[[i, 1]],",",v3GaugeQgraf[[i, 2]],",",v3GaugeQgraf[[i, 3]], 
													"}}}}}},{{{{{{ ", ToString[InputForm[(ToExpression[Ajuv3[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], " }}}}}}\n \n"], {i, 1, Length[v3GaugeQgraf]}];
		Close[stmp2]]];

v4GaugeLogic = False;
If[ToString[InputForm[hand]] != ToString[hand],
	QuarticvertsGauge = SelectVertices[vertsGauge, MinParticles -> 4];
	If[QuarticvertsGauge != {},
		v4GaugeLogic = True;
		zerov4 = {};
		Goodv4 = {};
		Extv4 = {};
		v4 = QuarticvertsGauge;
		Do[If[((v4[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov4 = Append[zerov4, i]], {i, 1, Length[v4]}];
		Do[If[! MemberQ[zerov4, i], Goodv4 = Append[Goodv4, {v4[[i, 1]][[1, 1]],  v4[[i, 1]][[2, 1]], v4[[i, 1]][[3, 1]], v4[[i, 1]][[4, 1]]}]; 
			Extv4 = Append[Extv4, {ToString[InputForm[v4[[i, 2]]//Simplify]]}]], {i, 1, Length[v4]}];
		Aux1v4 = 	Table[{Goodv4[[i, 1]], Goodv4[[i, 2]], Goodv4[[i, 3]], Goodv4[[i, 4]]}, {i, 1, Length[Goodv4]}];
		Ajuv4 = Table[{Extv4[[i, 1]]}, {i, 1, Length[Extv4]}];
		v4GaugeQgraf = Aux1v4;
		stmp = OpenWrite["PreRulesv4Gauge.m"];
		Do[WriteString[stmp, "vrtx", v4GaugeQgraf[[i, 1]], v4GaugeQgraf[[i, 2]], v4GaugeQgraf[[i, 3]], v4GaugeQgraf[[i, 4]], 
												   	"[J1_,k1_,J2_,k2_,J3_,k3_,J4_,k4_]:= ", ToString[InputForm[(ToExpression[Ajuv4[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], "\n \n"], {i, 1, Length[v4GaugeQgraf]}];
		Close[stmp];
		stmp2 = OpenWrite["PrePrintRulesv4Gauge.m"];
		Do[WriteString[stmp2, "{{{{{{", v4GaugeQgraf[[i, 1]],",",v4GaugeQgraf[[i, 2]],",",v4GaugeQgraf[[i, 3]],",",v4GaugeQgraf[[i, 4]], 
													   "}}}}}},{{{{{{ ", ToString[InputForm[(ToExpression[Ajuv4[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], " }}}}}}\n \n"], {i, 1, Length[v4GaugeQgraf]}];
		Close[stmp2]]];

hand = vertsFermionsFlavor;
v3FermionsLogic = False;
If[ToString[InputForm[hand]] != ToString[hand],
	CubicvertsFermions = SelectVertices[vertsFermionsFlavor, MaxParticles -> 3];
	If[CubicvertsFermions != {},
		v3FermionsLogic = True;
		zerov3 = {};
		Goodv3 = {};
		Extv3 = {};
		v3 = CubicvertsFermions;
		Do[If[((v3[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov3 = Append[zerov3, i]], {i, 1, Length[v3]}];
		Do[If[! MemberQ[zerov3, i], Goodv3 = Append[Goodv3, {v3[[i, 1]][[1, 1]], v3[[i, 1]][[2, 1]], v3[[i, 1]][[3, 1]]}];
			Extv3 = Append[Extv3, {ToString[InputForm[v3[[i, 2]]//Simplify]]}]], {i, 1, Length[v3]}];
		Ajuv3 = Table[{Extv3[[i, 1]]}, {i, 1, Length[Extv3]}];
		Aux1v3 = Table[{Goodv3[[i, 1]], Goodv3[[i, 2]], Goodv3[[i, 3]]}, {i, 1, Length[Goodv3]}];
		v3FermionsQgraf = Aux1v3;
		stmp = OpenWrite["PreRulesv3Fermions.m"];
		Do[WriteString[stmp, "vrtx", v3FermionsQgraf[[i, 1]], v3FermionsQgraf[[i, 2]], v3FermionsQgraf[[i, 3]], 
														"[J1_,k1_,J2_,k2_,J3_,k3_]:= ", ToString[InputForm[(ToExpression[Ajuv3[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], "\n \n"], {i, 1, Length[v3FermionsQgraf]}];
		Close[stmp];
		stmp2 = OpenWrite["PrePrintRulesv3Fermions.m"];
		Do[WriteString[stmp2, "{{{{{{", v3FermionsQgraf[[i, 1]],",",v3FermionsQgraf[[i, 2]],",",v3FermionsQgraf[[i, 3]], 
													"}}}}}},{{{{{{ ", ToString[InputForm[(ToExpression[Ajuv3[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], " }}}}}}\n \n"], {i, 1, Length[v3FermionsQgraf]}];
		Close[stmp2]]];

hand = vertsYukawa;
v3YukawaLogic = False;
If[ToString[InputForm[hand]] != ToString[hand],
	CubicvertsYukawa = SelectVertices[vertsYukawa, MaxParticles -> 3];
	If[CubicvertsYukawa != {},
		v3YukawaLogic = True;
		zerov3 = {};
		Goodv3 = {};
		Extv3 = {};
		v3 = CubicvertsYukawa;
		Do[If[((v3[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov3 = Append[zerov3, i]], {i, 1, Length[v3]}];
		Do[If[! MemberQ[zerov3, i], Goodv3 = Append[Goodv3, {v3[[i, 1]][[1, 1]], v3[[i, 1]][[2, 1]], v3[[i, 1]][[3, 1]]}];
			Extv3 = Append[Extv3, {ToString[InputForm[v3[[i, 2]]//Simplify]]}]], {i, 1, Length[v3]}];
		Ajuv3 = Table[{Extv3[[i, 1]]}, {i, 1, Length[Extv3]}];
		Aux1v3 = 	Table[{Goodv3[[i, 1]], Goodv3[[i, 2]], Goodv3[[i, 3]]}, {i, 1, Length[Goodv3]}];
		v3YukawaQgraf = Aux1v3;
		stmp = OpenWrite["PreRulesv3Yukawa.m"];
		Do[WriteString[stmp, "vrtx", v3YukawaQgraf[[i, 1]], v3YukawaQgraf[[i, 2]], v3YukawaQgraf[[i, 3]], 
													"[J1_,k1_,J2_,k2_,J3_,k3_]:= ", ToString[InputForm[(ToExpression[Ajuv3[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], "\n \n"], {i, 1, Length[v3YukawaQgraf]}];
		Close[stmp];
		stmp2 = OpenWrite["PrePrintRulesv3Yukawa.m"];
		Do[WriteString[stmp2, "{{{{{{", v3YukawaQgraf[[i, 1]],",",v3YukawaQgraf[[i, 2]],",",v3YukawaQgraf[[i, 3]], 
													"}}}}}},{{{{{{ ", ToString[InputForm[(ToExpression[Ajuv3[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], " }}}}}}\n \n"], {i, 1, Length[v3YukawaQgraf]}];
		Close[stmp2]]];

hand = vertsGhosts;
v3GhostsLogic = False;
If[ToString[InputForm[hand]] != ToString[hand],
	CubicvertsGhosts = SelectVertices[vertsGhosts, MaxParticles -> 3];
	If[CubicvertsGhosts != {},
	v3GhostsLogic = True;
	zerov3 = {};
	Goodv3 = {};
	Extv3 = {};
	v3 = CubicvertsGhosts;
	Do[If[((v3[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov3 = Append[zerov3, i]], {i, 1, Length[v3]}];
	Do[If[! MemberQ[zerov3, i], Goodv3 = Append[Goodv3, {v3[[i, 1]][[1, 1]], v3[[i, 1]][[2, 1]], v3[[i, 1]][[3, 1]]}];				  
		Extv3 = Append[Extv3, {ToString[InputForm[v3[[i, 2]]//Simplify]]}]], {i, 1, Length[v3]}];
	Ajuv3 = Table[{Extv3[[i, 1]]}, {i, 1, Length[Extv3]}];
	Aux1v3 = Table[{Goodv3[[i, 1]], Goodv3[[i, 2]], Goodv3[[i, 3]]}, {i, 1, Length[Goodv3]}];
	v3GhostsQgraf = Aux1v3;
	stmp = OpenWrite["PreRulesv3Ghosts.m"];
	Do[WriteString[stmp, "vrtx", v3GhostsQgraf[[i, 1]], v3GhostsQgraf[[i, 2]], v3GhostsQgraf[[i, 3]], 
												"[J1_,k1_,J2_,k2_,J3_,k3_]:= ", ToString[InputForm[(ToExpression[Ajuv3[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], "\n \n"], {i, 1, Length[v3GhostsQgraf]}];
	Close[stmp];
	stmp2 = OpenWrite["PrePrintRulesv3Ghosts.m"];
	Do[WriteString[stmp2, "{{{{{{", v3GhostsQgraf[[i, 1]],",",v3GhostsQgraf[[i, 2]],",",v3GhostsQgraf[[i, 3]], 
												"}}}}}},{{{{{{ ", ToString[InputForm[(ToExpression[Ajuv3[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], " }}}}}}\n \n"], {i, 1, Length[v3GhostsQgraf]}];
	Close[stmp2]]];
	
v4GhostsLogic = False;
If[ToString[InputForm[hand]] != ToString[hand],
	QuarticvertsGhosts = SelectVertices[vertsGhosts, MinParticles -> 4];
	If[QuarticvertsGhosts != {},
		v4GhostsLogic = True;
		zerov4 = {};
		Goodv4 = {};
		Extv4 = {};
		v4 = QuarticvertsGhosts;
		Do[If[((v4[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov4 = Append[zerov4, i]], {i, 1, Length[v4]}];
		Do[If[! MemberQ[zerov4, i], Goodv4 = Append[Goodv4, {v4[[i, 1]][[1, 1]],  v4[[i, 1]][[2, 1]], v4[[i, 1]][[3, 1]], v4[[i, 1]][[4, 1]]}]; 
			Extv4 = Append[Extv4, {ToString[InputForm[v4[[i, 2]]//Simplify]]}]], {i, 1, Length[v4]}];
		Aux1v4 = 	Table[{Goodv4[[i, 1]], Goodv4[[i, 2]], Goodv4[[i, 3]], Goodv4[[i, 4]]}, {i, 1, Length[Goodv4]}];
		Ajuv4 = Table[{Extv4[[i, 1]]}, {i, 1, Length[Extv4]}];
		v4GhostsQgraf = Aux1v4;
		stmp = OpenWrite["PreRulesv4Ghosts.m"];
		Do[WriteString[stmp, "vrtx", v4GhostsQgraf[[i, 1]], v4GhostsQgraf[[i, 2]], v4GhostsQgraf[[i, 3]], v4GhostsQgraf[[i, 4]], 
												   	"[J1_,k1_,J2_,k2_,J3_,k3_,J4_,k4_]:= ", ToString[InputForm[(ToExpression[Ajuv4[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], "\n \n"], {i, 1, Length[v4GhostsQgraf]}];
		Close[stmp];
		stmp2 = OpenWrite["PrePrintRulesv4Ghosts.m"];
		Do[WriteString[stmp2, "{{{{{{", v4GhostsQgraf[[i, 1]],",",v4GhostsQgraf[[i, 2]],",",v4GhostsQgraf[[i, 3]],",",v4GhostsQgraf[[i, 4]], 
													   "}}}}}},{{{{{{ ", ToString[InputForm[(ToExpression[Ajuv4[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], " }}}}}}\n \n"], {i, 1, Length[v4GhostsQgraf]}];
		Close[stmp2]]];

hand = vertsBeaks;
v3BeaksLogic = False;
If[ToString[InputForm[hand]] != ToString[hand],
	CubicvertsBeaks = SelectVertices[vertsBeaks, MaxParticles -> 3];
	If[CubicvertsBeaks != {},
	v3BeaksLogic = True;
	zerov3 = {};
	Goodv3 = {};
	Extv3 = {};
	v3 = CubicvertsBeaks;
	Do[If[((v3[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov3 = Append[zerov3, i]], {i, 1, Length[v3]}];
	Do[If[! MemberQ[zerov3, i], Goodv3 = Append[Goodv3, {v3[[i, 1]][[1, 1]], v3[[i, 1]][[2, 1]], v3[[i, 1]][[3, 1]]}];				  
		Extv3 = Append[Extv3, {ToString[InputForm[v3[[i, 2]]//Simplify]]}]], {i, 1, Length[v3]}];
	Ajuv3 = Table[{Extv3[[i, 1]]}, {i, 1, Length[Extv3]}];
	Aux1v3 = Table[{Goodv3[[i, 1]], Goodv3[[i, 2]], Goodv3[[i, 3]]}, {i, 1, Length[Goodv3]}];
	v3BeaksQgraf = Aux1v3;
	stmp = OpenWrite["PreRulesv3Beaks.m"];
	Do[WriteString[stmp, "vrtx", v3BeaksQgraf[[i, 1]], v3BeaksQgraf[[i, 2]], v3BeaksQgraf[[i, 3]], 
												"[J1_,k1_,J2_,k2_,J3_,k3_]:= ", ToString[InputForm[(ToExpression[Ajuv3[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], "\n \n"], {i, 1, Length[v3BeaksQgraf]}];
	Close[stmp];
	stmp2 = OpenWrite["PrePrintRulesv3Beaks.m"];
	Do[WriteString[stmp2, "{{{{{{", v3BeaksQgraf[[i, 1]],",",v3BeaksQgraf[[i, 2]],",",v3BeaksQgraf[[i, 3]], 
												"}}}}}},{{{{{{ ", ToString[InputForm[(ToExpression[Ajuv3[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], " }}}}}}\n \n"], {i, 1, Length[v3BeaksQgraf]}];
	Close[stmp2]]];

v4BeaksLogic = False;
If[ToString[InputForm[hand]] != ToString[hand],
	QuarticvertsBeaks = SelectVertices[vertsBeaks, MinParticles -> 4];
	If[QuarticvertsBeaks != {},
		v4BeaksLogic = True;
		zerov4 = {};
		Goodv4 = {};
		Extv4 = {};
		v4 = QuarticvertsBeaks;
		Do[If[((v4[[i, 2]] // Simplify) /. MyRestr /. MyRestr) == 0, zerov4 = Append[zerov4, i]], {i, 1, Length[v4]}];
		Do[If[! MemberQ[zerov4, i],
			Goodv4 = Append[Goodv4, {v4[[i, 1]][[1, 1]],  v4[[i, 1]][[2, 1]], v4[[i, 1]][[3, 1]], v4[[i, 1]][[4, 1]]}];
			Extv4 = Append[Extv4, {ToString[InputForm[v4[[i, 2]]//Simplify]]}]], {i, 1, Length[v4]}];
		Aux1v4 = 	Table[{Goodv4[[i, 1]], Goodv4[[i, 2]], Goodv4[[i, 3]], Goodv4[[i, 4]]}, {i, 1, Length[Goodv4]}];
		Ajuv4 = Table[{Extv4[[i, 1]]}, {i, 1, Length[Extv4]}];
		v4BeaksQgraf = Aux1v4;
		stmp = OpenWrite["PreRulesv4Beaks.m"];
		Do[WriteString[stmp, "vrtx", v4BeaksQgraf[[i, 1]], v4BeaksQgraf[[i, 2]], v4BeaksQgraf[[i, 3]], v4BeaksQgraf[[i, 4]], 
													   "[J1_,k1_,J2_,k2_,J3_,k3_,J4_,k4_]:= ", ToString[InputForm[(ToExpression[Ajuv4[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], "\n \n"], {i, 1, Length[v4BeaksQgraf]}];
		Close[stmp];
		stmp2 = OpenWrite["PrePrintRulesv4Beaks.m"];
		Do[WriteString[stmp2, "{{{{{{", v4BeaksQgraf[[i, 1]],",",v4BeaksQgraf[[i, 2]],",",v4BeaksQgraf[[i, 3]],",",v4BeaksQgraf[[i, 4]], 
													   "}}}}}},{{{{{{ ", ToString[InputForm[(ToExpression[Ajuv4[[i, 1]]] //Simplify) /. MyRestr /. MyRestr]], " }}}}}}\n \n"], {i, 1, Length[v4BeaksQgraf]}];
		Close[stmp2]]];

	Clear[r];


(* Writing the Feynman Rules main file *)
str = OpenWrite["Feynman-Rules-Main.m"];
WriteString[str, "(* ----------- Some Extras ----------- *) \n"];
(* Loading Extras like DecayWidths and Neutrinos list *)
WriteString[str, "Get[\"Extras.m\", Path -> {dirFey}]\n"];
WriteString[str, "\n"];
(* Deno is non-trivial should there be decay widths *)
WriteString[str, "(* ----------- Deno Function ----------- *) \n"];
WriteString[str, "Deno := Function[{k, m, PP}, Module[{mycoin, myres},\n"];
WriteString[str, "If[ToString[InputForm[k]] != \"-p1 - p2\",\n"];
WriteString[str, "	myres = FAD[{k, m}, Dimension -> D],\n"];
WriteString[str, "	mycoin = 0;\n"];
WriteString[str, "	Do[If[ToString[PP] == ToString[DWs[[i, 1]]],\n"];
WriteString[str, "			mycoin += 1;\n"];
WriteString[str, " 	 		myres = (SPD[k, k] - m^2 + I*m*DWs[[i, 2]])^(-1)], {i, 1, Length[DWs]}];\n"];
WriteString[str, "If[mycoin == 0, myres = FAD[{k, m}, Dimension -> D]]];\n"];
WriteString[str, "myres]]\n\n"];
(* We go on to some definitions *)
WriteString[str, "(* ----------- Definitions ----------- *)\n"];
WriteString[str, "dm[mu_]:=DiracMatrix[mu,Dimension->D] \n"];
WriteString[str, "dm[5]:=DiracMatrix[5] \n"];
WriteString[str, "ds[p_]:=DiracSlash[p, Dimension -> D] \n"];
WriteString[str, "fprop[p_,m_]:=ds[p] + m \n"];
WriteString[str, "fv[p_,mu_]:=FourVector[p,mu,Dimension->D] \n"];
WriteString[str, "po2[p_]:=Pair[Momentum[p], Momentum[p]] \n"];
WriteString[str, "mt[mu_,nu_]:=MetricTensor[mu,nu,Dimension->D] \n"];
WriteString[str, "sp[p_,q_]:=ScalarProduct[p,q] \n \n"];
WriteString[str, "(* ----------- Gluonize and mtom: useful functions for gluon indices ----------- *)\n"];
WriteString[str, "Gluonize = Function[exp, Module[{myres},\n"];
WriteString[str, "   If[StringTake[ToString[exp], 1] == \"-\", \n"];
WriteString[str, "      myres = ToExpression[\"-G\" <> StringDrop[ToString[exp], 2]],\n"];
WriteString[str, "      myres = ToExpression[\"G\" <> StringDrop[ToString[exp], 1]]];\n"];
WriteString[str, "      myres]];\n"];
WriteString[str, "mtom = Function[exp, Module[{myres},\n"];
WriteString[str, "   myres = ToExpression[StringReplace[exp, \"-\" -> \"m\"]];\n"];
WriteString[str, "   myres]];\n\n"];
WriteString[str, "(* ----------- Mass conversions ----------- *)\n"];
Do[If[ToString[masstrade[[i,1]]]!=ToString[masstrade[[i,2]]],
WriteString[str, ToString[masstrade[[i,1]]]<>":="<>ToString[masstrade[[i,2]]]<>"\n"]],{i,1,Length[masstrade]}];
WriteString[str, "\n"];
WriteString[str, "(* ----------- Set Tadpole momentum to zero ----------- *)\n"];
WriteString[str, "J0:=0 \n"];
WriteString[str, "\n"];
WriteString[str, "(* ----------- Feynman Rules ----------- *) \n"];
(* Loading the different Feynman rules files in the main file*)
WriteString[str, "Get[\"Propagators.m\", Path -> {dirFey}]\n"];
If[v3HiggsLogic,WriteString[str, "Get[\"Rulesv3Higgs.m\", Path -> {dirFey}]\n"]];
If[v4HiggsLogic,WriteString[str, "Get[\"Rulesv4Higgs.m\", Path -> {dirFey}]\n"]];
If[v3GaugeLogic,WriteString[str, "Get[\"Rulesv3Gauge.m\", Path -> {dirFey}]\n"]];
If[v4GaugeLogic,WriteString[str, "Get[\"Rulesv4Gauge.m\", Path -> {dirFey}]\n"]];
If[v3FermionsLogic,WriteString[str, "Get[\"Rulesv3Fermions.m\", Path -> {dirFey}]\n"]];
If[v3YukawaLogic,WriteString[str, "Get[\"Rulesv3Yukawa.m\", Path -> {dirFey}]\n"]];
If[v3GhostsLogic,WriteString[str, "Get[\"Rulesv3Ghosts.m\", Path -> {dirFey}]\n"]];
If[v4GhostsLogic,WriteString[str, "Get[\"Rulesv4Ghosts.m\", Path -> {dirFey}]\n"]];
If[v3BeaksLogic,WriteString[str, "Get[\"Rulesv3Beaks.m\", Path -> {dirFey}]\n"]];
If[v4BeaksLogic,WriteString[str, "Get[\"Rulesv4Beaks.m\", Path -> {dirFey}]\n"]];
WriteString[str, "\n"];
Close[str];
