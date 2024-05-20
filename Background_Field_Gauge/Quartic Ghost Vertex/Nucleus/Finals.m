(* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
This is Finals.m, a Mathematica routine for FeynCalc to take care of the final expressions.

Created by: Duarte Fontes
Email: duartefontes@tecnico.ulisboa.pt
Last update: 09.10.2020
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *)
(* --- The total number of amplitudes  --- *)
If[FileExistsQ["Amplitudes.m"],
If[ToString[ReadString["Amplitudes.m"]]=="EndOfFile",
imax=1,
imax=1+(StringCases[ReadString["Amplitudes.m"], Longest[{"\n" | "\r"} ..]] // Length)],
imax=500];

anc1 = {}; amp = {}; 
For[i = 1, i < imax, i++, anc1 = Append[anc1, {ToString[StringForm["amp``", i]]}]];
(*
NOTE: I am commenting what follows, since I rarely need this, and this takes
quite some time whenever there are several amplitudes. I still need to find
a clever way to create the list amp:
Do[amp = Append[amp,ToExpression[anc1[[j, 1]]]], {j, 1, Length[anc1]}];
*)

(* --- Compute the final expressions  --- *)
If[compNwrite,
(* then *)
anc2 = {}; anc3 = {}; anc4 = {};
ans = {}; res = {}; resD = {};
Do[ anc2 = Append[anc2, ToString[StringForm["ans``=GetAns[amp``,k1]", j, j]]];
	anc3 = Append[anc3, ToString[StringForm["res``=FCE[GetRes[ans``] /. FCsimp /. ApplyMomCons]", j, j]]];
	anc4 = Append[anc4, ToString[StringForm["resD``=FCE[GetDiv[res``] /. FCsimp /. ApplyMomCons]", j, j]]], {j, 1, Length[anc1]}];
Do[	ToExpression[anc2[[j]]];
	ans= Append[ans,ToExpression[anc2[[j]]]];
	res= Append[res,ToExpression[anc3[[j]]]];
	resD= Append[resD,ToExpression[anc4[[j]]]],{j, 1,Length[anc2]}];
res >> "Lists/res.in";
resD >> "Lists/resD.in";
If[SumLogic,
		restot = Total[res] /. FCsimp /. ApplyMomCons;
		restot >> "Lists/restot.in"];
If[SumLogic || RenoLogic,
		resDtot = Total[resD] /. FCsimp /. ApplyMomCons;
		resDtot >> "Lists/resDtot.in"],
(* else *)
If[FileExistsQ["Lists/res.in"],res = << "Lists/res.in"];
If[FileExistsQ["Lists/resD.in"],resD = << "Lists/resD.in"];
If[FileExistsQ["Lists/restot.in"],restot = << "Lists/restot.in"];
If[FileExistsQ["Lists/resDtot.in"],resDtot = << "Lists/resDtot.in"];

Do[ToExpression[ToString[StringForm["res``=res[[``]];", i, i]]];
   ToExpression[ToString[StringForm["resD``=resD[[``]];", i, i]]],{i,1,Length[res]}]];

(* We now begin an introduction to renormalization: we essentially determine the counterterm for the process at stake.
The renormalization on MSbar subtraction scheme will only be accomplished if RenoLogic is set to True. *)
If[FileExistsQ[dirCT <> "CTini.m"],
Get["CTini.m", Path -> {dirCT}];

CTparts=CTlist[[All,1]];
CTrules=CTlist[[All,2,1]];

(* What follows concerns the momenta and indices replacement rules from Feynrules to QGRAF&Control&FeynCalc *)
abCon={};
Do[abCon=Append[abCon,inparticlesB[[i]]],{i,1,Length[inparticlesB]}];
Do[abCon=Append[abCon,outparticlesB[[i]]/.AntiRep],{i,1,Length[outparticlesB]}];
abFey={};
Do[If[Total[abCon] == Total[VertLi[[i]]], abFey = VertLi[[i]]],{i,1,Length[VertLi]}];
ajuL0 = {};
Qrep = {};
Do[ajuL1 = Position[abCon, abFey[[i]]];
	  Do[If[! MemberQ[ajuL0, ajuL1[[j, 1]]],
		    ajuL0 = Append[ajuL0, ajuL1[[j, 1]]];
		    ajuL2 = {};
		    ajuL2 = Append[ajuL2, i];
		    ajuL2 = Append[ajuL2, ajuL1[[j, 1]]];
		    Qrep = Append[Qrep, ajuL2];
		    Break[]], {j, 1, Length[ajuL1]}], {i, 1, Length[abFey]}];
servConTot = {};
Do[servIn = {};
	  servIn = Append[servIn, StringForm["-J``", 2*i - 1]];
	  servIn = Append[servIn, StringForm["p``", i]];
	  servConTot = Append[servConTot, servIn], {i, 1, Length[inparticlesB]}];
Do[servOut = {};
	  servOut = Append[servOut, StringForm["-J``", 2*i]];
	  servOut = Append[servOut, StringForm["-q``", i]];
	  servConTot = Append[servConTot, servOut], {i, 1, Length[outparticlesB]}];
servFeyTot = {};
Do[servFeyPar = {}; 
		servFeyPar = Append[servFeyPar, StringForm["\[Mu]``", i]];
		servFeyPar = Append[servFeyPar, StringForm["p``", i]];
		servFeyTot = Append[servFeyTot, servFeyPar], {i, 1, Length[abFey]}];
QFrule = {};
Do[QFrule = Append[QFrule, ToExpression[ToString[servFeyTot[[Qrep[[i, 1]], 1]]]] -> ToExpression[ToString[servConTot[[Qrep[[i, 2]], 1]]]]];
		QFrule = Append[QFrule, ToExpression[ToString[servFeyTot[[Qrep[[i, 1]], 2]]]] -> ToExpression[ToString[servConTot[[Qrep[[i, 2]], 2]]]]], {i, 1, Length[Qrep]}];

StepBack={J1 -> \[Mu]1, J2 -> \[Mu]2, J3 -> \[Mu]3, J4 -> \[Mu]4};

flagCT=0;

If[QFrule!={},CTnach=CTrules /. StepBack /. QFrule,CTnach=CTrules];
Do[If[Sort[CTparts[[i]]] === Sort[abCon],
	flagCT=1;
	CTnach2=Expand[ChangeTo4[FCE[(CTnach[[i]]) /. {p^2-> SP[p,p]} /. {p -> p1}]] /. distG5];
	ToExpression["CT" <> ToString[inparticlesA] <> ToString[outparticlesA] <> " := " 
					  <> ToString[(Expand[CTnach2 /. distG5] /.{D->4} /. stilldot ) // InputForm]];
	Break],{i,1,Length[CTparts]}];
If[flagCT==0,
ToExpression["CT" <> ToString[inparticlesA] <> ToString[outparticlesA] <> " := 0"]];
]