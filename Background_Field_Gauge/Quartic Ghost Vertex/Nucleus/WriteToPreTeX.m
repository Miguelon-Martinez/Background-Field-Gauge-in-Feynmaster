(* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
This is the WriteToTex.m file, a Mathematica routine for FeynCalc where we generate a LaTeX file with the final expressions.

Created by: Duarte Fontes
Email: duartefontes@tecnico.ulisboa.pt
Last update: 03.04.2020
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *)

str = OpenWrite["preexp.m"]; 

If[FinLogic,
ser1 = {};
For[i = 1, i < imax, i++, ser1 = Append[ser1, {ToString[StringForm["res``" , i]]}]]];

If[DivLogic,
ser2 = {};
For[i = 1, i < imax, i++, ser2 = Append[ser2, {ToString[StringForm["resD``" , i]]}]]];

StrPar = inparticlesLA <> "," <> outparticlesLA;

WriteString[str, "\\documentclass[fleqn]{article}\n"];
WriteString[str, "\\usepackage{amsmath,mathtools,amssymb,geometry,graphics,setspace,slashed,dashrule}\n"];
WriteString[str, "\\usepackage{color,xcolor}\n"];
WriteString[str, "% \n"];
WriteString[str, "\\let\\oldcdot\\cdot \n"];
WriteString[str, "\\usepackage{breqn} \n"];
WriteString[str, "\\let\\cdot\\oldcdot \n"];
WriteString[str, "% \n"];
WriteString[str, "\\allowdisplaybreaks \n"];
WriteString[str, "\\definecolor{dgreen}{rgb}{0,0.2,0} \n"]	
WriteString[str, "\\geometry{tmargin=2.5cm,bmargin=2.5cm,lmargin=2.5cm,rmargin=2.5cm} \n"];
WriteString[str, "\\setlength{\\mathindent}{0pt}\n\n"];
WriteString[str, "\\def\\bd{\\begin{dmath*}} \n"];
WriteString[str, "\\def\\ed{\\end{dmath*}} \n"];
WriteString[str, "\\def\\bs{\\begin{dseries*}} \n"];
WriteString[str, "\\def\\es{\\end{dseries*}} \n"];
WriteString[str, "\\def\\vs{\\vspace{-2mm}} \n"];
WriteString[str, "\\def\\vsb{\\vspace{-4mm}} \n"];
WriteString[str, "\\def\\vsc{\\vspace{3mm}} \n"];
WriteString[str, "\\def\\frac{\\dfrac}\n\n"];
WriteString[str, "\\begin{document}\n\n"];

If[Qoptions=="onepi",Qextra="1PI",Qextra=""];
If[ParselLen == 0,
OptText1=ToString[StringForm["complete set of " <> Qextra <> " diagrams contributing to the"]];
OptText2=ToString[StringForm[""]],
OptText1=ToString[StringForm["selected set of " <> Qextra <> " diagrams contributing to the"]];
OptText2=ToString[StringForm["of the selected set"]]];
Lfac=ToString[loops];
Llet="s";
If[Lfac=="1",Llet=""];
If[Lfac!="0",
WriteString[str, ToString[StringForm["\\subsection*{Final expressions for the " <> OptText1 <> " process $" <> ToString[inparticlesLA] <>
	" \\to " <> ToString[outparticlesLA] <> "$ at " <> Lfac <> " loop" <> Llet <> " in " <> ToString[modelname] <> "} \n \n"]]],
WriteString[str, ToString[StringForm["\\subsection*{Final expressions for the " <> OptText1 <> " process $" <> ToString[inparticlesLA] <>
	" \\to " <> ToString[outparticlesLA] <> "$ at tree-level in " <> ToString[modelname] <> "} \n \n"]]]]

WriteString[str, "\\vspace{1mm} \n \n"];
WriteString[str, "\\vspace{1mm} \n \n"];
If[ToString[factor // TeXForm]!="1",
WriteString[str, ToString[StringForm["\\noindent The quantity $" <> ToString[factor // TeXForm] <> "$ is being factored out. \n "]]]];
WriteString[str, ToString[StringForm["\\noindent We define $" <> ToString[" \\omega_{\\epsilon} := \\dfrac{1}{2} \\left( \\dfrac{2}{\\epsilon} - \\gamma + \\ln 4\\pi \\right)."] <> "$ \n \n"]]];

If[FinLogic,
	WriteString[str, "\\vsc\n\\bs \n \\underline{Total expressions}: \n\\es \n"];
	Do[If[ToString[ToExpression[ser1[[j, 1]]]  // InputForm] != ser1[[j, 1]],
		ser1Deno=Denominator[(ToExpression[ser1[[j, 1]]] // Simplify) /.FCsimp];
		ser1Num=Numerator[(ToExpression[ser1[[j, 1]]] // Simplify) /.FCsimp];
		ser1Basic=ToString[InputForm[(ToExpression[ser1[[j, 1]]] // Simplify) /.FCsimp]];
		If[ToString[ser1Deno // InputForm] !="1" && StringLength[ser1Basic]>130,
			WriteString[str, "\\vs\n\\bd \n\\text{" <> ToString[ser1[[j, 1]]] <> "} = \\dfrac{1}{" <> ToString[InputForm[ser1Deno]] <> "} \\left[ \\vphantom{\\dfrac{A^B}{C^D}}" <> ToString[InputForm[ser1Num]] <> " \\right] \n\\ed \n"],
			WriteString[str, "\\vs\n\\bd \n\\text{" <> ToString[ser1[[j, 1]]] <> "} = " <> (ser1Basic) <> " \n\\ed \n"]]], {j, 1, Length[ser1]}];
	If[SumLogic,
		WriteString[str, "\\bs \nHence, the sum of total expressions " <> OptText2 <> " is: \n\\es \n"];
			restotDeno=Denominator[(restot// Simplify) /.FCsimp];
			restotNum=Numerator[(restot // Simplify) /.FCsimp];
			restotBasic=ToString[InputForm[(restot // Simplify) /.FCsimp]];
			If[ToString[restotDeno // InputForm] !="1" && StringLength[restotBasic]>130,
				XNFin=ToString[InputForm[restotNum]];
				WriteString[str, "\\vsb\n\\bd \n\\Sigma^{" <> StrPar <> "}_{\\text{loop}} = \\dfrac{1}{" <> ToString[InputForm[restotDeno]] <> "} \\left[ \\vphantom{\\dfrac{A^B}{C^D}}" <> (XNFin) <> " \\right] \n\\ed \n"],
				WriteString[str, "\\vsb\n\\bd \n\\Sigma^{" <> StrPar <> "}_{\\text{loop}} = " <> (restotBasic) <> " \n\\ed \n"]]]];
If[DivLogic,
	WriteString[str, "\\vsc\n\\bs \n\\underline{Divergent parts}: \n\\es \n"];
	Do[If[ToString[ToExpression[ser2[[j, 1]]] // InputForm] != ser2[[j, 1]], 
		ser2Deno=Denominator[(ToExpression[ser2[[j, 1]]]// Simplify) /.FCsimp];
		ser2Num=Numerator[(ToExpression[ser2[[j, 1]]] // Simplify) /.FCsimp];
		ser2Basic=ToString[InputForm[(ToExpression[ser2[[j, 1]]] // Simplify) /.FCsimp]];
		If[ToString[ser2Deno // InputForm] !="1" && StringLength[ser2Basic]>130,
			WriteString[str, "\\vs\n\\bd \n\\text{" <> ToString[ser2[[j, 1]]] <> "} = \\dfrac{1}{" <> ToString[InputForm[ser2Deno]] <> "} \\left[ \\vphantom{\\dfrac{A^B}{C^D}}" <> ToString[InputForm[ser2Num]] <> " \\right] \n\\ed \n"],
			WriteString[str, "\\vs\n\\bd \n\\text{" <> ToString[ser2[[j, 1]]] <> "} = " <> (ser2Basic) <> " \n\\ed \n"]]], {j, 1, Length[ser2]}];
	If[SumLogic,
		WriteString[str, "\\bs \nHence, the sum of divergent parts " <> OptText2 <> " is: \n\\es \n"];
			resDtotDeno=Denominator[(resDtot // Simplify) /.FCsimp];
			resDtotNum=Numerator[(resDtot // Simplify) /.FCsimp];
			resDtotBasic=ToString[InputForm[(resDtot // Simplify) /.FCsimp]];
			If[ToString[resDtotDeno // InputForm] !="1" && StringLength[resDtotBasic]>130,
				WriteString[str, "\\vsb\n\\bd \n \\text{Div} \\left[ \\Sigma^{" <> StrPar <> "}_{\\text{loop}} \\right] = \\dfrac{1}{" <> ToString[InputForm[resDtotDeno]] <> "} \\left[ \\vphantom{\\dfrac{A^B}{C^D}}" <> ToString[InputForm[resDtotNum]] <> " \\right] \n\\ed \n"],
				WriteString[str, "\\vsb\n\\bd \n \\text{Div} \\left[ \\Sigma^{" <> StrPar <> "}_{\\text{loop}} \\right] = " <> (resDtotBasic) <> " \n\\ed \n"]]]];
If[RenoLogic,
	WriteString[str, "\n\n \\vsc\n\\noindent \\hdashrule[0.5ex]{16cm}{0.2pt}{1mm}\n\\vsc\n\n"];
	WriteString[str, "\\bs \nNow, the renormalized final amplitude at 1-loop is: \n\\es \n"];
	WriteString[str, "\\vs\n\\bd \n\\hat{\\Sigma}^{"<> StrPar <> "}_{\\text{loop}} = \\Sigma^{" <> StrPar <> "}_{\\text{loop}} + \\Sigma^{"
							<> StrPar <> "}_{CT}"];
	TheCT2=ToString[InputForm[Simplify[ToExpression["CT" <> ToString[inparticlesA] <> ToString[outparticlesA]]]/.FCsimp]];
	If[TheCT2==TheCTstr,
		WriteString[str, "= \\Sigma^{" <> StrPar <> "}_{\\text{loop}} \n\\ed \n"],
		WriteString[str, "= \\Sigma^{" <> StrPar <> "}_{\\text{loop}} + " <>  TheCT2 <> "  \n\\ed \n"]];
	WriteString[str, "%\n\\bs \n Therefore, in the $\\overline{\\text{MS}}$ renormalization scheme, \n\\es \n"];
	If[ToString[InputForm[soundalarm]]!="0",
		WriteString[str, "\n\\bs \nthere seems to be a problem! There are divergences that cannot be cancelled by the counterterms. \n\\es \n"];
		WriteString[str, "\\bs \nThose divergences are: \n\\es \n"];
		WriteString[str, "\\vs\n\\bd \n"  <> ToString[InputForm[soundalarm]] <> " \n\\ed \n"],
	If[noneed==1 && TheCT2==TheCTstr,WriteString[str, "\\bs \nthere is no counterterm to compute -- which is not a problem, since the process at stake has no divergent part. \n\\es \n"],
	If[mail==1, WriteString[str, "\\bs \nthe counterterms of the theory are such that the renormalized final amplitude at stake has no divergent part.  \n\\es \n"],
		Do[If[StringContainsQ[ToString[CTcumulist[[i]]], "ResReno"] == False,
		CTDeno=Denominator[CTcumulist[[i,1,1,2]]] /.FCsimp;
		CTNum=Numerator[CTcumulist[[i,1,1,2]]] /.FCsimp;
		CTBasic=ToString[InputForm[CTcumulist[[i,1,1,2]] /.FCsimp]];
		If[ToString[CTDeno // InputForm] !="1" && StringLength[CTBasic]>130,
				WriteString[str, "\\vs\n\\bd \n"<> ToString[InputForm[CTcumulist[[i,1,1,1]]]] <> " = \\dfrac{1}{" <> ToString[InputForm[CTDeno]] <> "} \\left[ \\vphantom{\\dfrac{A^B}{C^D}}" <> ToString[InputForm[CTNum]] <> " \\right] \n\\ed \n"],
				WriteString[str, "\\vs\n\\bd \n"<> ToString[InputForm[CTcumulist[[i,1,1,1]]]] <> " = " <> (CTBasic) <> " \n\\ed \n"]]],{i,1,Length[CTcumulist]}];
		If[completebell==1,
			WriteString[str, "\n\\bs \nThis completes the renormalization of the model. The full list of counterterms is:\n\\es \n"];
			Do[
			CTDeno=Denominator[CTfinlist[[i,2]]] /.FCsimp;
			CTNum=Numerator[CTfinlist[[i,2]]] /.FCsimp;
			CTBasic=ToString[InputForm[CTfinlist[[i,2]] /.FCsimp]];
			If[ToString[CTDeno // InputForm] !="1" && StringLength[CTBasic]>130,
					WriteString[str, "\\vs\n\\bd \n"<> ToString[InputForm[CTfinlist[[i,1]]]] <> " = \\dfrac{1}{" <> ToString[InputForm[CTDeno]] <> "} \\left[ \\vphantom{\\dfrac{A^B}{C^D}}" <> ToString[InputForm[CTNum]] <> " \\right] \n\\ed \n"],
					WriteString[str, "\\vs\n\\bd \n"<> ToString[InputForm[CTfinlist[[i,1]]]] <> " = " <> (CTBasic) <> " \n\\ed \n"]],{i,1,Length[CTfinlist]}]]]]]];
WriteString[str, "\\vspace{1cm} \n"];
WriteString[str, "FeynMaster, \\\\[1mm] \n"];
WriteString[str, "\\today \n \n"];
WriteString[str, "\\end{document}\n"];
Close[str];