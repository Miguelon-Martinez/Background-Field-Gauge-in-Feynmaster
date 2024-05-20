(* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
This is the RenoMS.m file, a Mathematica routine for FeynCalc where we deal with the MSbar renormalization.

Created by: Duarte Fontes
Email: duartefontes@tecnico.ulisboa.pt
Last update: 03.09.2020
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *)

mail=0;
noneed=0;
soundalarm=0;

CTcumulist = {};
Rtotfin2=((I*resDtot) /. ApplyMomCons);
If[Rtotfin2==0,noneed=1];
TheCT=ToString[InputForm[ToExpression["CT" <> ToString[inparticlesA] <> ToString[outparticlesA]]]];
TheCTstr="CT" <> ToString[inparticlesA] <> ToString[outparticlesA];
If[TheCT==TheCTstr,
	PreResReno = Rtotfin2,
	PreResReno = Rtotfin2 + ToExpression["CT" <> ToString[inparticlesA] <> ToString[outparticlesA]]];
ReadString[ToString[dirCT] <>"CTfin.m"] // ToExpression;
ResReno = Expand[(PreResReno //.CTfinlist)/.ApplyMomCons] /. {SP[p1,p1]->p1^2};

(* General function to calculate counterterms: *)
MySolve = Function[{exp, var}, Module[{x0, x1, x2},
    x0 = Coefficient[exp,var];
    x1 = x0 var;
    x2 = var -> -(exp-x1)/x0;
    Mkout = {{x2}};];
    Mkout];

(* Auxiliary function for the mass-like counterterms: *)
doifMass[]:=
(
If[ToString[InputForm[ResReno]]=="0",mail=1,
AuxG5Pre=AuxNoP;
Do[AuxG5Pre = AuxG5Pre /.CTcumulist[[i,1]],{i,1,Length[CTcumulist]}]; 
AuxG5 := Coefficient[AuxG5Pre, GA[5],1];
auxcumul1={};
Do[auxcumul1=Append[auxcumul1,CTfinlist[[i,1]]],{i, 1, Length[CTfinlist]}];
Do[auxcumul1=Append[auxcumul1,CTcumulist[[i,1,1,1]]],{i, 1, Length[CTcumulist]}];
auxcumul2={};
Do[auxcumul2=Append[auxcumul2,CTcumulist[[i,1,1]]],{i, 1, Length[CTcumulist]}];
danger=0;
Do[If[ToString[InputForm[Coefficient[Simplify[AuxG5 /. auxcumul2], renconslist[[i]]]]] != "0",danger=danger+1;],{i, 1, Length[renconslist]}];
If[danger==0&&ToString[InputForm[Simplify[AuxG5 /. auxcumul2]]]!="0",soundalarm=AuxG5];
AuxG5b=(AuxG5 /. auxcumul2)//Simplify;
Do[If[ToString[InputForm[Coefficient[AuxG5b, renconslist[[i]]]]] != "0" && !MemberQ[auxcumul1,renconslist[[i]]],
					ToExpression["ResRenoG5 = " <> ToString[Simplify[MySolve[AuxG5b, renconslist[[i]]]] // InputForm]]],{i, 1, Length[renconslist]}];
If[ToString[InputForm[ResRenoG5]] != "ResRenoG5",
Do[CTcumulist[[i]] = CTcumulist[[i]] /. ResRenoG5[[1,1]], {i, 1, Length[CTcumulist]}];
CTcumulist = Append[CTcumulist, ResRenoG5]];

AuxMPre=AuxNoP;
Do[AuxMPre = AuxMPre /.CTcumulist[[i,1]],{i,1,Length[CTcumulist]}]; 
AuxM = Coefficient[AuxMPre, GA[5],0];
auxcumul1={};
Do[auxcumul1=Append[auxcumul1,CTfinlist[[i,1]]],{i, 1, Length[CTfinlist]}];
Do[auxcumul1=Append[auxcumul1,CTcumulist[[i,1,1,1]]],{i, 1, Length[CTcumulist]}];
auxcumul2={};
Do[auxcumul2=Append[auxcumul2,CTcumulist[[i,1,1]]],{i, 1, Length[CTcumulist]}];
danger=0;
Do[If[ToString[InputForm[Coefficient[Simplify[AuxM /. auxcumul2], renconslist[[i]]]]] != "0",danger=danger+1;],{i, 1, Length[renconslist]}];
If[danger==0&&ToString[InputForm[Simplify[AuxM /. auxcumul2]]]!="0",soundalarm=AuxM];
AuxMb = (AuxM /. auxcumul2)//Simplify;
Do[If[ToString[InputForm[Coefficient[AuxMb, renconslist[[i]]]]] != "0" && !MemberQ[auxcumul1,renconslist[[i]]],
			ToExpression["ResRenoM = " <> ToString[Simplify[MySolve[AuxMb, renconslist[[i]]]] // InputForm]];
			Break[]],{i, 1, Length[renconslist]}];
If[ToString[InputForm[ResRenoM]] != "ResRenoM",
Do[CTcumulist[[i]] = CTcumulist[[i]] /. ResRenoM[[1,1]], {i, 1, Length[CTcumulist]}];
CTcumulist = Append[CTcumulist, ResRenoM]]];
)

(* Auxiliary function for the cases where the process is a self-energy and the particle is a fermion: *)
doSelfFerm[]:=
(
If[ToString[InputForm[ResReno]]=="0",mail=1,
ResRenoJustP = Coefficient[ResReno, GS[p1]];
auxcumul1={};
Do[auxcumul1=Append[auxcumul1,CTfinlist[[i,1]]],{i, 1, Length[CTfinlist]}];
Do[auxcumul1=Append[auxcumul1,CTcumulist[[i,1,1,1]]],{i, 1, Length[CTcumulist]}];
auxcumul2={};
Do[auxcumul2=Append[auxcumul2,CTcumulist[[i,1,1]]],{i, 1, Length[CTcumulist]}];
danger=0;
Do[If[ToString[InputForm[Coefficient[Simplify[ResRenoJustP /. auxcumul2], renconslist[[i]]]]] != "0",danger=danger+1;],{i, 1, Length[renconslist]}];
If[danger==0&&ToString[InputForm[Simplify[ResRenoJustP /. auxcumul2]]]!="0",soundalarm=ResRenoJustP GS[p1]];
ResRenoJustPb = (ResRenoJustP /. auxcumul2)//Simplify;
Do[If[ToString[InputForm[Coefficient[ResRenoJustPb, renconslist[[i]]]]] != "0" && !MemberQ[auxcumul1,renconslist[[i]]],
			ToExpression["ResRenoJustP2 = " <> ToString[Simplify[MySolve[ResRenoJustPb, renconslist[[i]]]] // InputForm]];
			Break[]],{i, 1, Length[renconslist]}];
If[ToString[InputForm[ResRenoJustP2]] != "ResRenoJustP2",
Do[CTcumulist[[i]] = CTcumulist[[i]] /. ResRenoJustP2[[1,1]], {i, 1, Length[CTcumulist]}];
CTcumulist = Append[CTcumulist, ResRenoJustP2]];

ResRenoPG5 = Coefficient[ResReno, GS[p1].GA[5]];
auxcumul1={};
Do[auxcumul1=Append[auxcumul1,CTfinlist[[i,1]]],{i, 1, Length[CTfinlist]}];
Do[auxcumul1=Append[auxcumul1,CTcumulist[[i,1,1,1]]],{i, 1, Length[CTcumulist]}];
auxcumul2={};
Do[auxcumul2=Append[auxcumul2,CTcumulist[[i,1,1]]],{i, 1, Length[CTcumulist]}];
danger=0;
Do[If[ToString[InputForm[Coefficient[Simplify[ResRenoPG5 /. auxcumul2], renconslist[[i]]]]] != "0",danger=danger+1;],{i, 1, Length[renconslist]}];
If[danger==0&&ToString[InputForm[Simplify[ResRenoPG5 /. auxcumul2]]]!="0",soundalarm=ResRenoPG5 GS[p1].GA[5]];
ResRenoPG5b = (ResRenoPG5  /. auxcumul2)//Simplify;
Do[If[ToString[InputForm[Coefficient[ResRenoPG5b, renconslist[[i]]]]] != "0" && !MemberQ[auxcumul1,renconslist[[i]]],
			ToExpression["ResRenoPG52 = " <> ToString[Simplify[MySolve[ResRenoPG5b, renconslist[[i]]]] // InputForm]];
			Break[]],{i, 1, Length[renconslist]}];
If[ToString[InputForm[ResRenoPG52]] != "ResRenoPG52",
Do[CTcumulist[[i]] = CTcumulist[[i]] /. ResRenoPG52[[1,1]], {i, 1, Length[CTcumulist]}];
CTcumulist = Append[CTcumulist, ResRenoPG52]];

AuxNoP = ResReno /. {GS[p1].GA[5] -> 0, GS[p1] -> 0};
If[ToString[AuxNoP // InputForm] != "0",doifMass[]]];
)

(* Auxiliary function for the cases where the process is a self-energy and the particle is a scalar or a gauge boson: *)
doSelfOthe[]:=
(
If[ToString[InputForm[ResReno]]=="0",mail=1,
If[YesGauge,
	ResRenoP = Coefficient[ResReno, p1^2 MT[-J1, -J2]],
	ResRenoP = Coefficient[ResReno, p1^2]];
auxcumul1={};
Do[auxcumul1=Append[auxcumul1,CTfinlist[[i,1]]],{i, 1, Length[CTfinlist]}];
Do[auxcumul1=Append[auxcumul1,CTcumulist[[i,1,1,1]]],{i, 1, Length[CTcumulist]}];
auxcumul2={};
Do[auxcumul2=Append[auxcumul2,CTcumulist[[i,1,1]]],{i, 1, Length[CTcumulist]}];
danger=0;
Do[If[ToString[InputForm[Coefficient[Simplify[ResRenoP /. auxcumul2], renconslist[[i]]]]] != "0",danger=danger+1;],{i, 1, Length[renconslist]}];
If[danger==0&&ToString[InputForm[Simplify[ResRenoP /. auxcumul2]]]!="0",soundalarm=ResRenoP p1^2];
ResRenoPb = (ResRenoP /. auxcumul2)//Simplify;
Do[If[ToString[InputForm[Coefficient[ResRenoPb, renconslist[[i]]]]] != "0" && !MemberQ[auxcumul1,renconslist[[i]]],
			ToExpression["ResRenoP2 = " <> ToString[Simplify[MySolve[ResRenoPb, renconslist[[i]]]] // InputForm]];
			Break[]],{i, 1, Length[renconslist]}];
If[ToString[InputForm[ResRenoP2]] != "ResRenoP2",
Do[CTcumulist[[i]] = CTcumulist[[i]] /. ResRenoP2[[1,1]], {i, 1, Length[CTcumulist]}];
CTcumulist = Append[CTcumulist, ResRenoP2]];
If[YesGauge,
	AuxNoP = Coefficient[ResReno /. {p1->0},MT[-J1, -J2]],
	AuxNoP = ResReno /. {p1->0}]
If[ToString[AuxNoP // InputForm] != "0",doifMass[]]];		
)

(* Auxiliary function for the cases where the process is a vertex involving one gauge field and two fermions: *)
doVertGaugeFermions[]:=
(
If[ToString[InputForm[ResReno]]=="0",mail=1,
Do[If[PartAuxIn[[i]]=="gauge",If[i==1,Ind=-J1,Ind=-J3]],{i,1,Length[PartAuxIn]}];
Do[If[PartAuxOut[[i]]=="gauge",If[i==1,Ind=-J2,Ind=-J4]],{i,1,Length[PartAuxOut]}];
ResRenoJustG = Coefficient[ResReno, GA[Ind]];
auxcumul1={};
Do[auxcumul1=Append[auxcumul1,CTfinlist[[i,1]]],{i, 1, Length[CTfinlist]}];
Do[auxcumul1=Append[auxcumul1,CTcumulist[[i,1,1,1]]],{i, 1, Length[CTcumulist]}];
auxcumul2={};
Do[auxcumul2=Append[auxcumul2,CTcumulist[[i,1,1]]],{i, 1, Length[CTcumulist]}];
danger=0;
Do[If[ToString[InputForm[Coefficient[Simplify[ResRenoJustG /. auxcumul2], renconslist[[i]]]]] != "0",danger=danger+1;],{i, 1, Length[renconslist]}];
If[danger==0&&ToString[InputForm[Simplify[ResRenoJustG /. auxcumul2]]]!="0",soundalarm=ResRenoJustG GA[Ind]];
ResRenoJustGb = (ResRenoJustG /. auxcumul2)//Simplify;
Do[If[ToString[InputForm[Coefficient[ResRenoJustGb, renconslist[[i]]]]] != "0" && !MemberQ[auxcumul1,renconslist[[i]]],
			ToExpression["ResRenoJustG2 = " <> ToString[Simplify[MySolve[ResRenoJustGb, renconslist[[i]]]] // InputForm]];
			Break[]],{i, 1, Length[renconslist]}];
If[ToString[InputForm[ResRenoJustG2]] != "ResRenoJustG2",
Do[CTcumulist[[i]] = CTcumulist[[i]] /. ResRenoJustG2[[1,1]], {i, 1, Length[CTcumulist]}];
CTcumulist = Append[CTcumulist, ResRenoJustG2]];

ResRenoGG5 = Coefficient[ResReno, GA[Ind].GA[5]];
auxcumul1={};
Do[auxcumul1=Append[auxcumul1,CTfinlist[[i,1]]],{i, 1, Length[CTfinlist]}];
Do[auxcumul1=Append[auxcumul1,CTcumulist[[i,1,1,1]]],{i, 1, Length[CTcumulist]}];
auxcumul2={};
Do[auxcumul2=Append[auxcumul2,CTcumulist[[i,1,1]]],{i, 1, Length[CTcumulist]}];
danger=0;
Do[If[ToString[InputForm[Coefficient[Simplify[ResRenoGG5 /. auxcumul2], renconslist[[i]]]]] != "0",danger=danger+1;],{i, 1, Length[renconslist]}];
If[danger==0&&ToString[InputForm[Simplify[ResRenoGG5 /. auxcumul2]]]!="0",soundalarm= ResRenoGG5 GA[Ind].GA[5]];
ResRenoGG5b = (ResRenoGG5 /. auxcumul2)//Simplify;
Do[If[ToString[InputForm[Coefficient[ResRenoGG5b, renconslist[[i]]]]] != "0" && !MemberQ[auxcumul1,renconslist[[i]]],
			ToExpression["ResRenoGG52 = " <> ToString[Simplify[MySolve[ResRenoGG5b, renconslist[[i]]]] // InputForm]];
			Break[]],{i, 1, Length[renconslist]}];
If[ToString[InputForm[ResRenoGG52]] != "ResRenoGG52",
Do[CTcumulist[[i]] = CTcumulist[[i]] /. ResRenoGG52[[1,1]], {i, 1, Length[CTcumulist]}];
CTcumulist = Append[CTcumulist, ResRenoGG52]]];
)

(* Auxiliary function for the cases where the process is a vertex involving a scalar field and fermions: *)
doVertScalarFermions[]:=
(
If[ToString[InputForm[ResReno]]=="0",mail=1,
ResRenoNoG5 = Coefficient[ResReno, GA[5],0];
auxcumul1={};
Do[auxcumul1=Append[auxcumul1,CTfinlist[[i,1]]],{i, 1, Length[CTfinlist]}];
Do[auxcumul1=Append[auxcumul1,CTcumulist[[i,1,1,1]]],{i, 1, Length[CTcumulist]}];
auxcumul2={};
Do[auxcumul2=Append[auxcumul2,CTcumulist[[i,1,1]]],{i, 1, Length[CTcumulist]}];
danger=0;
Do[If[ToString[InputForm[Coefficient[Simplify[ResRenoNoG5 /. auxcumul2], renconslist[[i]]]]] != "0",danger=danger+1;],{i, 1, Length[renconslist]}];
If[danger==0&&ToString[InputForm[Simplify[ResRenoNoG5 /. auxcumul2]]]!="0",soundalarm=ResRenoNoG5];
ResRenoNoG5b = (ResRenoNoG5 /. auxcumul2)//Simplify;
Do[If[ToString[InputForm[Coefficient[ResRenoNoG5b, renconslist[[i]]]]] != "0" && !MemberQ[auxcumul1,renconslist[[i]]],
			ToExpression["ResRenoNoG52 = " <> ToString[Simplify[MySolve[ResRenoNoG5b, renconslist[[i]]]] // InputForm]];
			Break[]],{i, 1, Length[renconslist]}];
If[ToString[InputForm[ResRenoNoG52]] != "ResRenoNoG52",
Do[CTcumulist[[i]] = CTcumulist[[i]] /. ResRenoNoG52[[1,1]], {i, 1, Length[CTcumulist]}];
CTcumulist = Append[CTcumulist, ResRenoNoG52]];

ResRenoG5 = Coefficient[ResReno, GA[5],1];
auxcumul1={};
Do[auxcumul1=Append[auxcumul1,CTfinlist[[i,1]]],{i, 1, Length[CTfinlist]}];
Do[auxcumul1=Append[auxcumul1,CTcumulist[[i,1,1,1]]],{i, 1, Length[CTcumulist]}];
auxcumul2={};
Do[auxcumul2=Append[auxcumul2,CTcumulist[[i,1,1]]],{i, 1, Length[CTcumulist]}];
danger=0;
Do[If[ToString[InputForm[Coefficient[Simplify[ResRenoG5 /. auxcumul2], renconslist[[i]]]]] != "0",danger=danger+1;],{i, 1, Length[renconslist]}];
If[danger==0&&ToString[InputForm[Simplify[ResRenoG5 /. auxcumul2]]]!="0",soundalarm= ResRenoG5 GA[5]];
ResRenoG5b = (ResRenoG5 /. auxcumul2)//Simplify;
Do[If[ToString[InputForm[Coefficient[ResRenoG5b, renconslist[[i]]]]] != "0" && !MemberQ[auxcumul1,renconslist[[i]]],
			ToExpression["ResRenoG52 = " <> ToString[Simplify[MySolve[ResRenoG5b, renconslist[[i]]]] // InputForm]];
			Break[]],{i, 1, Length[renconslist]}];
If[ToString[InputForm[ResRenoG52]] != "ResRenoG52",
Do[CTcumulist[[i]] = CTcumulist[[i]] /. ResRenoG52[[1,1]], {i, 1, Length[CTcumulist]}];
CTcumulist = Append[CTcumulist, ResRenoG52]]];
)

(* Auxiliary function for the remaining cases: *)
doGeneral[]:=
(
If[ToString[InputForm[ResReno]]=="0",mail=1,
auxcumul1={};
Do[auxcumul1=Append[auxcumul1,CTfinlist[[i,1]]],{i, 1, Length[CTfinlist]}];
Do[auxcumul1=Append[auxcumul1,CTcumulist[[i,1,1,1]]],{i, 1, Length[CTcumulist]}];
auxcumul2={};
Do[auxcumul2=Append[auxcumul2,CTcumulist[[i,1,1]]],{i, 1, Length[CTcumulist]}];
danger=0;
Do[If[ToString[InputForm[Coefficient[Simplify[ResReno /. auxcumul2], renconslist[[i]]]]] != "0",danger=danger+1;],{i, 1, Length[renconslist]}];
If[danger==0&&ToString[InputForm[Simplify[ResReno /. auxcumul2]]]!="0",soundalarm=ResReno];
ResRenob = (ResReno /. auxcumul2)//Simplify;
Do[If[ToString[InputForm[Coefficient[ResRenob, renconslist[[i]]]]] != "0" && !MemberQ[auxcumul1,renconslist[[i]]],
			ToExpression["ResRenoG = " <> ToString[Simplify[MySolve[ResRenob, renconslist[[i]]]] // InputForm]];
			Break[]],{i, 1, Length[renconslist]}];
If[ToString[InputForm[ResRenoG]] != "ResRenoG",
Do[CTcumulist[[i]] = CTcumulist[[i]] /. ResRenoG[[1,1]], {i, 1, Length[CTcumulist]}];
CTcumulist = Append[CTcumulist, ResRenoG]]];
)

(* Last things: *)
PartAuxIn = {};
Do[PartAuxIn = Append[PartAuxIn, ToString[intypes[[i]]]], {i, 1, Length[intypes]}];
PartAuxOut = {};
Do[PartAuxOut = Append[PartAuxOut, ToString[outtypes[[i]]]], {i, 1, Length[outtypes]}];

SelfEnergy = Length[inparticlesB] == 1 && Length[outparticlesB] == 1;
YesFermion = ContainsAny[PartAuxIn, {"fermion"}] || ContainsAny[PartAuxOut, {"fermion"}];
YesGauge = ContainsAny[PartAuxIn, {"gauge"}] || ContainsAny[PartAuxOut, {"gauge"}];

If[SelfEnergy,
	If[YesFermion,
		doSelfFerm[],
		doSelfOthe[]],
	If[YesFermion,
		If[YesGauge,
			doVertGaugeFermions[],
			doVertScalarFermions[]],
		doGeneral[]]]

CTcumulist = CTcumulist // Simplify
Do[If[StringContainsQ[ToString[CTcumulist[[i]]], "ResReno"] == False,CTfinlist = Append[CTfinlist, CTcumulist[[i,1,1]]]],{i,1,Length[CTcumulist]}];

PosResReno = Expand[(ResReno /.CTfinlist)/.ApplyMomCons];

completebell=0;
CTdejacomp = {};
Do[CTdejacomp = Append[CTdejacomp, CTfinlist[[i, 1]]], {i, 1, Length[CTfinlist]}];
If[Sort[CTdejacomp] == Sort[renconslist], completebell=1];

ancst = OpenWrite[ToString[dirCT] <>"CTfin.m"];
WriteString[ancst, "CTfinlist = " <> ToString[CTfinlist//InputForm] <> ";"];
Close[ancst];