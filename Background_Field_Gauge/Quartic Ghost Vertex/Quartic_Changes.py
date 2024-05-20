## In order to add the possibility of quartic ghost vertex in a theory, it is necessary to make some updates in the FeynMaster software. Here are the changes that must be made inside the FeynMaster/Nucleus folder.


## Addendum.m ##

## Add the following lines:


## Line 214

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
		
		
### Dimpués der v3GhostsLogic ### After v3GhostsLogic ( Line ~445 )

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
		
		
## In line ~ 575 (after the if v3GhostsLogic statement), add: 

If[v4GhostsLogic,WriteString[str, "Get[\"Rulesv4Ghosts.m\", Path -> {dirFey}]\n"]];





## Printer.py ##


## line 128, add: 
'PrePrintRulesv4Ghosts.m', 

## line 129, add: 
'PrePrintCTRulesv4Ghosts.m', 

## line 142,add: 
'Quartic Ghost vertex',




## Converter.py ##

## line 888, add: 
'PreRulesv4Ghosts.m',



## General.py ##

## From line 450 and so on add: 

			f.write('if exist PreRulesv4Ghosts.m del PreRulesv4Ghosts.m \n')
			f.write('if exist PrePrintRulesv4Ghosts.m del PrePrintRulesv4Ghosts.m \n')
			f.write('if exist PrePrintCTRulesv4Ghosts.m del PrePrintCTRulesv4Ghosts.m \n')
			
			
			
			
			f.write('if exist PreRulesv4Ghosts.m move PreRulesv4Ghosts.m ' + dirNuc + ' \n')
			f.write('if exist PrePrintRulesv4Ghosts.m move PrePrintRulesv4Ghosts.m ' + dirNuc + ' \n')
			
				if RenoLogic == True:
				f.write('if exist PrePrintCTRulesv4Ghosts.m move PrePrintCTRulesv4Ghosts.m ' + dirNuc + ' \n')
				
			f.write('if exist Rulesv4Ghosts.m move Rulesv4Ghosts.m ' + dirFey + ' \n')
			
			f.write('rm -f PreRulesv4Ghosts.m \n')
			f.write('rm -f PrePrintRulesv4Ghosts.m \n')
			f.write('rm -f PrePrintCTRulesv4Ghosts.m \n')
			
			f.write('if [ -f ./PreRulesv4Ghosts.m ]; then mv PreRulesv4Ghosts.m ' + dirNuc + '; fi \n')
			f.write('if [ -f ./PrePrintRulesv3Ghosts.m ]; then mv PrePrintRulesv3Ghosts.m ' + dirNuc + '; fi \n')
			
				if RenoLogic ==True:
				f.write('if [ -f ./PrePrintCTRulesv4Ghosts.m ]; then mv PrePrintCTRulesv4Ghosts.m ' + dirNuc + '; fi \n')
				
			f.write('if [ -f ./Rulesv4Ghosts.m ]; then mv Rulesv4Ghosts.m ' + dirFey + '; fi \n')
			
			
			## linea 982
			
			f.write('if exist PrePrintRulesv4Ghosts.m move PrePrintRulesv4Ghosts.m ' + dirFeyDraw + ' \n')
			f.write('if exist PreRulesv4Ghosts.m del PreRulesv4Ghosts.m \n')
			
				if RenoLogic == True:
				f.write('if exist PrePrintCTRulesv4Ghosts.m move PrePrintCTRulesv4Ghosts.m ' + dirCTDraw + ' \n') 
				
			
			## from line 1071 and so on, add:
			
			f.write('if [ -f ./PrePrintRulesv4Ghosts.m ]; then mv PrePrintRulesv4Ghosts.m ' + dirFeyDraw + '; fi \n')
			f.write('rm -f PreRulesv4Ghosts.m \n')


				if RenoLogic ==True:
				f.write('if [ -f ./PrePrintCTRulesv4Ghosts.m ]; then mv PrePrintCTRulesv4Ghosts.m ' + dirCTDraw + '; fi \n')  			




## Rneapp.m  ##

## line 253, add:

(* PrePrintCTRulesv4Ghosts *)
PrePrintCTRulesv4Ghosts = {};
Do[If[Length[CTord[[i]]] == 4 && (CTbri2[[i]] == {"S"} || (MemberQ[CTbri2[[i]], "S"] && MemberQ[CTbri2[[i]], "V"])),
   			PrePrintCTRulesv4Ghosts = Append[PrePrintCTRulesv4Ghosts, {}]], {i, 1, Length[CTord]}];
coin = 0;
Do[If[Length[CTord[[i]]] == 4 && (CTbri2[[i]] == {"S"} || (MemberQ[CTbri2[[i]], "S"] && MemberQ[CTbri2[[i]], "V"])),
   			coin = coin + 1;
   			PrePrintCTRulesv4Ghosts[[coin]] = Append[PrePrintCTRulesv4Ghosts[[coin]], CTord[[i]]];
   			PrePrintCTRulesv4Ghosts[[coin]] = Append[PrePrintCTRulesv4Ghosts[[coin]], CTmidlist4[[i]]]], {i, 1, Length[CTord]}];
If[PrePrintCTRulesv4Ghosts != {},
  	str1 = OpenWrite["PrePrintCTRulesv4Ghosts.m"];
  	Do[WriteString[str1, "{{{{{{", PrePrintCTRulesv4Ghosts[[i, 1, 1]], ",", PrePrintCTRulesv4Ghosts[[i, 1, 2]], ",", PrePrintCTRulesv4Ghosts[[i, 1, 3]], ",", PrePrintCTRulesv4Ghosts[[i, 1, 4]], "}}}}}},{{{{{{ ", 
    		PrePrintCTRulesv4Ghosts[[i, 2, 1]], " }}}}}}\n \n"], {i, 1, Length[PrePrintCTRulesv4Ghosts]}];
  Close[str1]];  














