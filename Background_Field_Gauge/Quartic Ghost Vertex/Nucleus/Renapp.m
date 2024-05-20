(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
This is the Renapp.m file, a Mathematica routine for FeynRules where we define everything related
to the renormalization in the FeynRules environment.

Created by: Duarte Fontes
Email: duartefontes@tecnico.ulisboa.pt
Last update: 03.09.2020
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)

If[ToString[LCTGauge//InputForm]!="0",LCTGauge=GetCT[LEIGauge],LCTGauge=0];
If[ToString[LCTHiggs//InputForm]!="0",LCTHiggs=GetCT[LEIHiggs],LCTHiggs=0];
If[ToString[LCTGhost//InputForm]!="0",LCTGhost=GetCT[LEIGhost],LCTGhost=0];
If[ToString[LCTGF//InputForm]!="0",LCTGF=GetCT[LEIGF],LCTGF=0];
If[ToString[LCTFermions//InputForm]!="0",LCTFermions=GetCT[LEIFermions],LCTFermions=0];
If[ToString[LCTYukawa//InputForm]!="0",LCTYukawa=GetCT[LEIYukawa],LCTYukawa=0];

LoCTfin = LCTGauge + LCTHiggs + LCTGhost + LCTGF + LCTFermions + LCTYukawa;

If[DeBug, str7 = OpenWrite["MyProgressPos.m"]];
MDB[str7];
(* Write the final list of counterterms: *)
CTppplist = {};
Do[CTppplist = Append[CTppplist,(((Coefficient[LoCTfin, combetas[[i]]] /.cleanetas)* combetas[[i]]) /.gamrep) /.pprops /. assodots // InputForm], {i, 1, Length[combetas]}];
CTinilist=CTppplist /. MyRestr /. unitetas;
Clear[i];
MDB[str7];

(* Some details to include in the external file where CTinilist is to be written: *)
VList := ancCTve2tot
VoutL = {};
Do[
		auxVout = {};
		Do[auxVout = Append[auxVout,VList[[i,1,j,1]]],{j,1,Length[VList[[i,1]]]}];
		VoutL = Append[VoutL,auxVout];
		VoutL = VoutL,{i,1,Length[VList]}];
VoutL2 = {};
Do[VoutL2 = Append[VoutL2, {}], {i, 1, Length[VoutL]}];
Do[Do[VoutL2[[i]] = Append[VoutL2[[i]], ToString[InputForm[VoutL[[i, j]]]]], {j, 1, Length[VoutL[[i]]]}], {i, 1, Length[VoutL]}];
AoutL = {};
Do[If[ToString[ToExpression[palist2[[i, 2]]<>"bar"]/.antimap]==palist2[[i, 2]],
AoutL = Append[AoutL, palist3[[i,2]] -> ToExpression[palist2[[i,2]]<>"bar"]];
AoutL = Append[AoutL, ToExpression[palist2[[i,2]]<>"bar"] -> palist3[[i,2]]]],{i,1,Length[palist3]}];
MDB[str7];
CTpreord1 = combetas /. comeback;
CTpreord2 = {};
Do[ordaux = {};
  		If[Length[CTpreord1[[i]]] == 0,
   				ordaux = Append[ordaux, ToString[CTpreord1[[i]]]], 
   				If[Length[CTpreord1[[i]]] == 2 && IntegerQ[CTpreord1[[i, 2]]], 
    				Do[ordaux = Append[ordaux, ToString[CTpreord1[[i, 1]]]], {m, 1, CTpreord1[[i, 2]]}], 
    				Do[If[Length[CTpreord1[[i, j]]] > 0,
      							Do[ordaux = Append[ordaux, ToString[CTpreord1[[i, j, 1]]]], {k, 1, CTpreord1[[i, j, 2]]}],
      							ordaux = Append[ordaux, ToString[CTpreord1[[i, j]]]]], {j, 1, Length[CTpreord1[[i]]]}]]];
  		CTpreord2 = Append[CTpreord2, ordaux], {i, 1, Length[CTpreord1]}];
CTord = CTpreord2;
Do[Do[If[Sort[CTord[[i]]] === Sort[VoutL2[[j]]],
					CTord[[i]] = VoutL2[[j]]], {j, 1, Length[VoutL2]}], {i, 1, Length[CTord]}];
MDB[str7];

(* Finally, the external file to the FeynCalc envirnonment: *)
str = OpenWrite["CTpre.m"];
Do[WriteString[str, "+++++ "<>ToString[CTinilist[[i]]]<>"\n"],{i,1,Length[CTinilist]}];
WriteString[str, "\n"];
WriteString[str, "CTord := "];
WriteString[str, ToString[CTord]];
WriteString[str, "\n"];
WriteString[str, "cleanetas := "];
WriteString[str, ToString[cleanetas]];
WriteString[str, "\n"];
WriteString[str, "VertLi := "];
WriteString[str, ToString[VoutL]];
WriteString[str, "\n"];
WriteString[str, "AntiRep := "];
WriteString[str, ToString[AoutL]];
Close[str];
MDB[str7];

(* Now, we focus on the printing of the Feynman rules for the counterterms. *)
(* We start by creating some (more) lists, which will be very useful for the printing *)
palistbri1 = {};
Do[palistbri1 = Append[palistbri1, {palist3[[i, 2]]}];
  If[ToString[StandardForm[ToExpression[ToString[palist3[[i, 2]]] <> "bar"]]] != ToString[InputForm[ToExpression[ToString[palist3[[i, 2]]] <> "bar"]]], 
   palistbri1 = Append[palistbri1, {ToExpression[ToString[palist3[[i, 2]]] <> "bar"]}]], {i, 1, Length[palist3]}];
palistbri2 = {};
Do[palistbri2 = Append[palistbri2, {ToString[InputForm[palistbri1[[i, 1]]]]}], {i, 1, Length[palistbri1]}];
Do[If[StringLength[palistbri2[[i, 1]]] > 2 && StringTake[palistbri2[[i, 1]], -3] == "bar", 
   	   Do[If[StringDelete[palistbri2[[i, 1]], "bar"] == ToString[InputForm[palist3[[k, 2]]]], 
     				palistbri2[[i]] = Append[palistbri2[[i]], ToString[InputForm[palist3[[k, 1]]]]]; 
     				Break[]], {k, 1, Length[palist3]}], 
   		Do[If[palistbri2[[i, 1]] == ToString[InputForm[palist3[[k, 2]]]], 
                   palistbri2[[i]] = Append[palistbri2[[i]], ToString[InputForm[palist3[[k, 1]]]]]; 
     			   Break[]], {k, 1, Length[palist3]}]], {i, 1, Length[palistbri2]}];
palistbri3 = palistbri2 // ToExpression;
palistbri4 = palistbri3;
palistbri5 = {};
Do[palistbri5 = Append[palistbri5, {}], {i, 1, Length[palistbri4]}];
Do[palistbri5[[i]] = Append[palistbri5[[i]], ToString[palistbri4[[i, 1]]]];
       palistbri5[[i]] = Append[palistbri5[[i]], ToString[palistbri4[[i, 2]]]], {i, 1, Length[palistbri4]}];
MDB[str7];
CTbri1 = {};
Do[CTbri1 = Append[CTbri1, {}], {i, 1, Length[CTord]}];
Do[Do[Do[If[CTord[[i, j]] == palistbri5[[k, 1]], CTbri1[[i]] = Append[CTbri1[[i]], palistbri5[[k, 2]]]], {k, 1, Length[palistbri5]}], {j, 1, Length[CTord[[i]]]}], {i, 1, Length[CTord]}];
CTbri2 = {};
Do[CTbri2 = Append[CTbri2, {}], {i, 1, Length[CTbri1]}];
Do[Do[If[! MemberQ[CTbri2[[i]], CTbri1[[i, j]]], CTbri2[[i]] = Append[CTbri2[[i]], CTbri1[[i, j]]]], {j, 1, Length[CTbri1[[i]]]}], {i, 1, Length[CTbri1]}];
MDB[str7];
CTmidlist1 = {};
Do[CTmidlist1 = Append[CTmidlist1, ToString[CTinilist[[i]]]], {i, 1, Length[CTinilist]}];
CTmidlist2 = CTmidlist1 // ToExpression;
CTmidlist3 = (CTmidlist2 /. unitetas) /. MyRestr /. MyRestr;
CTmidlist4 = {};
Do[CTmidlist4 = Append[CTmidlist4, {ToString[InputForm[CTmidlist3[[i]]]]}], {i, 1, Length[CTmidlist3]}];
MDB[str7];

(* Now comes the printing part itself. We divide it by sections *)

(* PrePrintCTRulesv1Tads *)
PrePrintCTRulesv1Tads = {};
Do[If[Length[CTord[[i]]] == 1,
            PrePrintCTRulesv1Tads = Append[PrePrintCTRulesv1Tads, {}]], {i, 1, Length[CTord]}];
coin = 0;
Do[If[Length[CTord[[i]]] == 1,
   			coin = coin + 1;
   			PrePrintCTRulesv1Tads[[coin]] = Append[PrePrintCTRulesv1Tads[[coin]], CTord[[i]]];
   			PrePrintCTRulesv1Tads[[coin]] = Append[PrePrintCTRulesv1Tads[[coin]], CTmidlist4[[i]]]], {i, 1, Length[CTord]}];
If[PrePrintCTRulesv1Tads != {},
  	str1 = OpenWrite["PrePrintCTRulesv1Tads.m"];
    Do[WriteString[str1, "{{{{{{", PrePrintCTRulesv1Tads[[i, 1, 1]], "}}}}}},{{{{{{ ", 
    		PrePrintCTRulesv1Tads[[i, 2, 1]], " }}}}}}\n \n"], {i, 1, Length[PrePrintCTRulesv1Tads]}];
  	Close[str1]];

(* PrePrintCTRulesv2Props *)
PrePrintCTRulesv2Props = {};
Do[If[Length[CTord[[i]]] == 2,
            PrePrintCTRulesv2Props = Append[PrePrintCTRulesv2Props, {}]], {i, 1, Length[CTord]}];
coin = 0;
Do[If[Length[CTord[[i]]] == 2,
   			coin = coin + 1;
   			PrePrintCTRulesv2Props[[coin]] = Append[PrePrintCTRulesv2Props[[coin]], CTord[[i]]];
   			PrePrintCTRulesv2Props[[coin]] = Append[PrePrintCTRulesv2Props[[coin]], CTmidlist4[[i]]]], {i, 1, Length[CTord]}];
If[PrePrintCTRulesv2Props != {},
  	str1 = OpenWrite["PrePrintCTRulesv2Props.m"];
    Do[WriteString[str1, "{{{{{{", PrePrintCTRulesv2Props[[i, 1, 1]], ",", PrePrintCTRulesv2Props[[i, 1, 2]], "}}}}}},{{{{{{ ", 
    		PrePrintCTRulesv2Props[[i, 2, 1]], " }}}}}}\n \n"], {i, 1, Length[PrePrintCTRulesv2Props]}];
  	Close[str1]];

(* PrePrintCTRulesv3Gauge *)
PrePrintCTRulesv3Gauge = {};
Do[If[Length[CTord[[i]]] == 3 && CTbri2[[i]] == {"V"},
            PrePrintCTRulesv3Gauge = Append[PrePrintCTRulesv3Gauge, {}]], {i, 1, Length[CTord]}];
coin = 0;
Do[If[Length[CTord[[i]]] == 3 && CTbri2[[i]] == {"V"},
   			coin = coin + 1;
   			PrePrintCTRulesv3Gauge[[coin]] = Append[PrePrintCTRulesv3Gauge[[coin]], CTord[[i]]];
   			PrePrintCTRulesv3Gauge[[coin]] = Append[PrePrintCTRulesv3Gauge[[coin]], CTmidlist4[[i]]]], {i, 1, Length[CTord]}];
If[PrePrintCTRulesv3Gauge != {},
  	str1 = OpenWrite["PrePrintCTRulesv3Gauge.m"];
    Do[WriteString[str1, "{{{{{{", PrePrintCTRulesv3Gauge[[i, 1, 1]], ",", PrePrintCTRulesv3Gauge[[i, 1, 2]], ",", PrePrintCTRulesv3Gauge[[i, 1, 3]], "}}}}}},{{{{{{ ", 
    		PrePrintCTRulesv3Gauge[[i, 2, 1]], " }}}}}}\n \n"], {i, 1, Length[PrePrintCTRulesv3Gauge]}];
  	Close[str1]];

(* PrePrintCTRulesv4Gauge *)
PrePrintCTRulesv4Gauge = {};
Do[If[Length[CTord[[i]]] == 4 && CTbri2[[i]] == {"V"},
   			PrePrintCTRulesv4Gauge = Append[PrePrintCTRulesv4Gauge, {}]], {i, 1, Length[CTord]}];
coin = 0;
Do[If[Length[CTord[[i]]] == 4 && CTbri2[[i]] == {"V"},
   			coin = coin + 1;
   			PrePrintCTRulesv4Gauge[[coin]] = Append[PrePrintCTRulesv4Gauge[[coin]], CTord[[i]]];
   			PrePrintCTRulesv4Gauge[[coin]] = Append[PrePrintCTRulesv4Gauge[[coin]], CTmidlist4[[i]]]], {i, 1, Length[CTord]}];
If[PrePrintCTRulesv4Gauge != {},
  	str1 = OpenWrite["PrePrintCTRulesv4Gauge.m"];
  	Do[WriteString[str1, "{{{{{{", PrePrintCTRulesv4Gauge[[i, 1, 1]], ",", PrePrintCTRulesv4Gauge[[i, 1, 2]], ",", PrePrintCTRulesv4Gauge[[i, 1, 3]], ",", PrePrintCTRulesv4Gauge[[i, 1, 4]], "}}}}}},{{{{{{ ", 
    		PrePrintCTRulesv4Gauge[[i, 2, 1]], " }}}}}}\n \n"], {i, 1, Length[PrePrintCTRulesv4Gauge]}];
  Close[str1]];

(* PrePrintCTRulesv3Fermions *)
PrePrintCTRulesv3Fermions = {};
Do[If[Length[CTord[[i]]] == 3 && MemberQ[CTbri2[[i]], "F"] && ! MemberQ[CTbri2[[i]], "S"],
   			PrePrintCTRulesv3Fermions = Append[PrePrintCTRulesv3Fermions, {}]], {i, 1, Length[CTord]}];
coin = 0;
Do[If[Length[CTord[[i]]] == 3 && MemberQ[CTbri2[[i]], "F"] && ! MemberQ[CTbri2[[i]], "S"],
   			coin = coin + 1;
   			PrePrintCTRulesv3Fermions[[coin]] = Append[PrePrintCTRulesv3Fermions[[coin]], CTord[[i]]];
   			PrePrintCTRulesv3Fermions[[coin]] = Append[PrePrintCTRulesv3Fermions[[coin]], CTmidlist4[[i]]]], {i, 1, Length[CTord]}];
If[PrePrintCTRulesv3Fermions != {},
  	str1 = OpenWrite["PrePrintCTRulesv3Fermions.m"];
  	Do[WriteString[str1, "{{{{{{", PrePrintCTRulesv3Fermions[[i, 1, 1]], ",", PrePrintCTRulesv3Fermions[[i, 1, 2]], ",", PrePrintCTRulesv3Fermions[[i, 1, 3]], "}}}}}},{{{{{{ ", 
    		PrePrintCTRulesv3Fermions[[i, 2, 1]], " }}}}}}\n \n"], {i, 1, Length[PrePrintCTRulesv3Fermions]}];
  Close[str1]];

(* PrePrintCTRulesv3Yukawa *)
PrePrintCTRulesv3Yukawa = {};
Do[If[Length[CTord[[i]]] == 3 && MemberQ[CTbri2[[i]], "F"] && MemberQ[CTbri2[[i]], "S"],
   			PrePrintCTRulesv3Yukawa = Append[PrePrintCTRulesv3Yukawa, {}]], {i, 1, Length[CTord]}];
coin = 0;
Do[If[Length[CTord[[i]]] == 3 && MemberQ[CTbri2[[i]], "F"] && MemberQ[CTbri2[[i]], "S"],
   			coin = coin + 1;
   			PrePrintCTRulesv3Yukawa[[coin]] = Append[PrePrintCTRulesv3Yukawa[[coin]], CTord[[i]]];
   			PrePrintCTRulesv3Yukawa[[coin]] = Append[PrePrintCTRulesv3Yukawa[[coin]], CTmidlist4[[i]]]], {i, 1, Length[CTord]}];
If[PrePrintCTRulesv3Yukawa != {},
  	str1 = OpenWrite["PrePrintCTRulesv3Yukawa.m"];
  	Do[WriteString[str1, "{{{{{{", PrePrintCTRulesv3Yukawa[[i, 1, 1]], ",", PrePrintCTRulesv3Yukawa[[i, 1, 2]], ",", PrePrintCTRulesv3Yukawa[[i, 1, 3]], "}}}}}},{{{{{{ ", 
    		PrePrintCTRulesv3Yukawa[[i, 2, 1]], " }}}}}}\n \n"], {i, 1, Length[PrePrintCTRulesv3Yukawa]}];
  Close[str1]];

(* PrePrintCTRulesv3Higgs *)
PrePrintCTRulesv3Higgs = {};
Do[If[Length[CTord[[i]]] == 3 && MemberQ[CTbri2[[i]], "S"] && ! MemberQ[CTbri2[[i]], "F"] && ! MemberQ[CTbri2[[i]], "U"],
   PrePrintCTRulesv3Higgs = Append[PrePrintCTRulesv3Higgs, {}]], {i, 1, Length[CTord]}];
coin = 0;
Do[If[Length[CTord[[i]]] == 3 && MemberQ[CTbri2[[i]], "S"] && ! MemberQ[CTbri2[[i]], "F"] && ! MemberQ[CTbri2[[i]], "U"],
   			coin = coin + 1;
   			PrePrintCTRulesv3Higgs[[coin]] = Append[PrePrintCTRulesv3Higgs[[coin]], CTord[[i]]];
   			PrePrintCTRulesv3Higgs[[coin]] = Append[PrePrintCTRulesv3Higgs[[coin]], CTmidlist4[[i]]]], {i, 1, Length[CTord]}];
If[PrePrintCTRulesv3Higgs != {},
  	str1 = OpenWrite["PrePrintCTRulesv3Higgs.m"];
  	Do[WriteString[str1, "{{{{{{", PrePrintCTRulesv3Higgs[[i, 1, 1]], ",", PrePrintCTRulesv3Higgs[[i, 1, 2]], ",", PrePrintCTRulesv3Higgs[[i, 1, 3]], "}}}}}},{{{{{{ ", 
    		PrePrintCTRulesv3Higgs[[i, 2, 1]], " }}}}}}\n \n"], {i, 1, Length[PrePrintCTRulesv3Higgs]}];
  Close[str1]];

(* PrePrintCTRulesv4Higgs *)
PrePrintCTRulesv4Higgs = {};
Do[If[Length[CTord[[i]]] == 4 && (CTbri2[[i]] == {"S"} || (MemberQ[CTbri2[[i]], "S"] && MemberQ[CTbri2[[i]], "V"])),
   			PrePrintCTRulesv4Higgs = Append[PrePrintCTRulesv4Higgs, {}]], {i, 1, Length[CTord]}];
coin = 0;
Do[If[Length[CTord[[i]]] == 4 && (CTbri2[[i]] == {"S"} || (MemberQ[CTbri2[[i]], "S"] && MemberQ[CTbri2[[i]], "V"])),
   			coin = coin + 1;
   			PrePrintCTRulesv4Higgs[[coin]] = Append[PrePrintCTRulesv4Higgs[[coin]], CTord[[i]]];
   			PrePrintCTRulesv4Higgs[[coin]] = Append[PrePrintCTRulesv4Higgs[[coin]], CTmidlist4[[i]]]], {i, 1, Length[CTord]}];
If[PrePrintCTRulesv4Higgs != {},
  	str1 = OpenWrite["PrePrintCTRulesv4Higgs.m"];
  	Do[WriteString[str1, "{{{{{{", PrePrintCTRulesv4Higgs[[i, 1, 1]], ",", PrePrintCTRulesv4Higgs[[i, 1, 2]], ",", PrePrintCTRulesv4Higgs[[i, 1, 3]], ",", PrePrintCTRulesv4Higgs[[i, 1, 4]], "}}}}}},{{{{{{ ", 
    		PrePrintCTRulesv4Higgs[[i, 2, 1]], " }}}}}}\n \n"], {i, 1, Length[PrePrintCTRulesv4Higgs]}];
  Close[str1]];  

(* PrePrintCTRulesv3Ghosts *)
PrePrintCTRulesv3Ghosts = {};
Do[If[Length[CTord[[i]]] == 3 && MemberQ[CTbri2[[i]], "U"],
   			PrePrintCTRulesv3Ghosts = Append[PrePrintCTRulesv3Ghosts, {}]], {i, 1, Length[CTord]}];
coin = 0;
Do[If[Length[CTord[[i]]] == 3 && MemberQ[CTbri2[[i]], "U"],
   			coin = coin + 1;
   			PrePrintCTRulesv3Ghosts[[coin]] = Append[PrePrintCTRulesv3Ghosts[[coin]], CTord[[i]]];
   			PrePrintCTRulesv3Ghosts[[coin]] = Append[PrePrintCTRulesv3Ghosts[[coin]], CTmidlist4[[i]]]], {i, 1, Length[CTord]}];
If[PrePrintCTRulesv3Ghosts != {},
  	str1 = OpenWrite["PrePrintCTRulesv3Ghosts.m"];
  	Do[WriteString[str1, "{{{{{{", PrePrintCTRulesv3Ghosts[[i, 1, 1]], ",", PrePrintCTRulesv3Ghosts[[i, 1, 2]], ",", PrePrintCTRulesv3Ghosts[[i, 1, 3]], "}}}}}},{{{{{{ ", 
    		PrePrintCTRulesv3Ghosts[[i, 2, 1]], " }}}}}}\n \n"], {i, 1, Length[PrePrintCTRulesv3Ghosts]}];
  Close[str1]];
  
  
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

If[DeBug,Close[str7]];
