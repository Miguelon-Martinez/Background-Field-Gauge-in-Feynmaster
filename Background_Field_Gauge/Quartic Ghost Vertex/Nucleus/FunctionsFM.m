(* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
This is the FunctionsFM.m file, a Mathematica routine with functions.

Created by: Jorge C. Romão and Duarte Fontes
Emails: jorge.romao@tecnico.ulisboa.pt, duartefontes@tecnico.ulisboa.pt
Last update: 28.09.2021

Content and usage:

  MyTeXForm[exp]
  FCtoFT[exp]
  FacToDecay[exp]
  DecayWidth[exp]
  DiffXS[exp]
  Coef2[exp, a, b]
  Coef3[exp, a, b, c]
  Coef4[exp, a, b, c, d]
  NoDirac[exp]
  GetDirac[exp]
  RepDirac[exp]
  ChangeToB0Unique[exp]
  GetDiv[exp]
  GetFinite[exp]
  OneLoopTID[k,amp]
  Dabcd[a,b,c,d]
  GetPars[k,xamp,verbose]
  IndividualFVkD[k,exp]
  IndividualFVk[k,exp]
  OneLoop4k[k,amp]
  OneLoop4kMod[k,amp]
  MyOneLoop[k,amp]
  MyOneLoopMod[k,amp]
  OneLoopMod[k,amp]
  OneLoopModMon[k,amp]
  GetDenominator[amp]
  GetNumerator[amp]
  TCALoopExp=[exp, Denos, Powk, k1, P, C]
  ChangeToD[exp]
  ChangeTo4[exp]
  TrG5[exp]
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *)


(*---------------------------------------------------------------------*)
(* MyTeXForm: convert expressions into LaTeX style *)
(* Created by: Duarte Fontes
   Email: duartefontes@tecnico.ulisboa.pt 
   Last Update: 28.07.2020

   Objective: convert expressions into LaTeX style.
   Note: MyTeXForm uses Python, as well as FeynMaster inner information.
*)

MyTeXForm::"usage"="MyTeXForm[expr] converts expr into LaTeX style. It uses Python, as well as FeynMaster inner information.
            It prints the LaTeX form of the expression given as argument not only on the screen, but also in an external file named
            MyTeXForm-last-output.tex in the directory where the notebook lies.";

MyTeXForm = Function[exp, Module[{},
  str = OpenWrite["dataFC.m"];
  WriteString[str, InputForm[exp // FCE]];
  Close[str];
  If[osswitch=="Windows",
      str = OpenWrite["MyBatch.bat"];
      WriteString[str, "@echo off \n"];
      WriteString[str, "move dataFC.m ",StringReplace[dirNuc,"/"->"\\"],"\n"];
      WriteString[str, "cd ",StringReplace[dirFey,"/"->"\\"],"\n"];
        WriteString[str, "move FRtoTeX.m ",StringReplace[dirNuc,"/"->"\\"],"\n"];
        WriteString[str, "cd ",StringReplace[dirNuc,"/"->"\\"],"\n"];
        WriteString[str, "py JustConvert.py \n"];
        WriteString[str, "del dataFC.m \n"];
        WriteString[str, "move FRtoTeX.m ",StringReplace[dirFey,"/"->"\\"],"\n"];
        WriteString[str, "move MyTeXForm-last-output.tex ",StringReplace[dirHome,"/"->"\\"],"\n"];
        WriteString[str, "rmdir __pycache__ /S /Q \n"];
        WriteString[str, "cd ",StringReplace[dirFM,"/"->"\\"],"\n"];
        WriteString[str, "rmdir __pycache__ /S /Q \n"];
        (* For debugging, uncomment the line below *)  
      (* WriteString[str, "pause \n"]; *)
        Close[str];
        Run["MyBatch.bat"];
        DeleteFile["MyBatch.bat"];
        ReadString["MyTeXForm-last-output.tex"],
  If[osswitch=="Linux"||osswitch=="Mac",
      str = OpenWrite["MyBatch.sh"];
      WriteString[str, "mv dataFC.m ",dirNuc,"\n"];
      WriteString[str, "cd ",dirFey,"\n"];
        WriteString[str, "mv FRtoTeX.m ",dirNuc,"\n"];
        WriteString[str, "cd ",dirNuc,"\n"];
        WriteString[str, "python3 JustConvert.py \n"];
        WriteString[str, "rm dataFC.m \n"]; 
        WriteString[str, "mv FRtoTeX.m ",dirFey,"\n"];
        WriteString[str, "mv MyTeXForm-last-output.tex ",dirHome,"\n"];
        WriteString[str, "rm -fr __pycache__  \n"];
        WriteString[str, "cd ",dirFM,"\n"];
        WriteString[str, "rm -fr __pycache__  \n"];
        Close[str];
        Run["sh MyBatch.sh"];
        DeleteFile["MyBatch.sh"];
        ReadString["MyTeXForm-last-output.tex"]]]]];
(*---------------------------------------------------------------------*)


(*---------------------------------------------------------------------*)
(* FCtoFT: convert expressions to Fortran *)
(* Created by: Duarte Fontes
   Email: duartefontes@tecnico.ulisboa.pt 
   Last Update: 03.09.2020

   Objective: convert expressions to Fortran in a practical way.
   Notes:

   1) FCtoFT allows the numerical interface of FM; when applied to an expression exp, it generates a directory named newfiles,
      inside which there are at least five files: MainFT.F, Myexp.F, MyVariables.h, MyParameters.h and Makefile-template;
      the first one, MainFT.F, is the beginning of a main Fortran program, which must be completed according to the user's will;
      MainFT.F calls the function Myexp, which is the Fortran version of exp, and which is written in the file Myexp.F
      (according to the size of the expression at stake, and in order to render the compilation faster, one or several files
      named MyAux_exp_i.F --- with i corresponding to the index of the file --- may be generated; these files are consistently
      and automatically called by Myexp.F). In turn, MyVariables.h and MyParameters.h respectively contain the variables and the
      numerical values associated to the different parameters in the FeynMaster model file. Finally, Makefile-template contains
      a skeleton of a makefile (whenever MyAux_exp_i.F files are generated, Makefile-template automatically includes those files,
      so that the compilation becomes easier). In the case of cross sections, the integration routine Int_gauss.f is also generated
      and called in MainFT.F.
      FCtoFT admits a second (optional) argument, as we now explain. Suppose the expression exp is a complicated expression, but such that it can be
      written in a simple way using three form factors, F1, F2, F3; that is, exp=f(F1,F2,F3), where f is a simple function, while F1, F2 and F3
      correspond to complicated expressions. In cases like this, it is convenient to write FCtoFT with two arguments: the first one is the expression
      exp, but written in terms of auxiliary variables F1aux, F2aux and F3aux instead of the complicated expressions F1, F2 and F3 (that is,
      exp=f(F1aux,F2aux,F3aux)); the second argument is a list of the replacements between the auxiliary variables and their corresponding form
      factor (in this example, {F1aux -> F1, F2aux -> F2, F3aux -> F3}).
   2) Is uses Python, as well as FeynMaster inner information.
*)

FCtoFT::"usage"="FCtoFT[exp] converts expr into Fortran. It uses Python, as well as FeynMaster inner information.
        When applied to an expression exp, it generates a directory named newfiles,
        inside which there are at least five files: MainFT.F, Myexp.F, MyVariables.h, MyParameters.h and Makefile-template;
        the first one, MainFT.F, is the beginning of a main Fortran program, which must be completed according to the user's will;
        MainFT.F calls the function Myexp, which is the Fortran version of exp, and which is written in the file Myexp.F
        (according to the size of the expression at stake, and in order to render the compilation faster, one or several files
        named MyAux_exp_i.F --- with i corresponding to the index of the file --- may be generated; these files are consistently
        and automatically called by Myexp.F). In turn, MyVariables.h and MyParameters.h respectively contain the variables and the
        numerical values associated to the different parameters in the FeynMaster model file. Finally, Makefile-template contains
        a skeleton of a makefile (whenever MyAux_exp_i.F files are generated, Makefile-template automatically includes those files,
        so that the compilation becomes easier). In the case of cross sections, the integration routine Int_gauss.f is also generated
        and called in MainFT.F.
        FCtoFT admits a second (optional) argument, as we now explain. Suppose the expression exp is a complicated expression, but such that it can be
        written in a simple way using three form factors, F1, F2, F3; that is, exp=f(F1,F2,F3), where f is a simple function, while F1, F2 and F3
        correspond to complicated expressions. In cases like this, it is convenient to write FCtoFT with two arguments: the first one is the expression
        exp, but written in terms of auxiliary variables F1aux, F2aux and F3aux instead of the complicated expressions F1, F2 and F3 (that is,
        exp=f(F1aux,F2aux,F3aux)); the second argument is a list of the replacements between the auxiliary variables and their corresponding form
        factor (in this example, {F1aux -> F1, F2aux -> F2, F3aux -> F3}).

        Note that, by default, the Passarino-Veltman functions will be converted as complex. This can be modified by defining retil=True";

FCtoFT=Function[Null,Hold[##]/._[exp_,what_: {}]:>Module[{},
  str=OpenWrite["dataFT.m"];
    If[loops==0,toadd="tree-level",If[loops==1,toadd="1 loop",toadd=loops<>"loops"]];
    WriteString[str, HoldForm[exp]];
    WriteString[str,"; "];
    WriteString[str,"Process "<>inparticlesC<>" to "<>outparticlesC<>" at "<>toadd<>" in "<>modelname<>"\n\n"];
    If[ToString[InputForm[retil]]=="True",myretil="True",myretil="False"];
    WriteString[str,"retil: "<>myretil<>"\n\n"];
    WriteString[str,InputForm[exp//Expand//FCE]];
    If[ToString[InputForm[what]]!="{}",WriteString[str,"\n\n"];
    Do[whatspe=what[[i]]//Expand;
    WriteString[str,InputForm[whatspe//FCE]];
    If[i!=Length[what],WriteString[str,"\n\n"]],{i,1,Length[what]}]];
  Close[str];
  str=OpenWrite["auxFT.m"];
    MyFCList=Import[StringJoin[dirFey,"FRtoTeX.m"],"List"];
    MyListaux={};
    Do[MyListaux=Append[MyListaux,StringDrop[StringSplit[MyFCList[[i]],"->"][[1]],-1]],{i,1,Length[MyFCList]}];
    FCeqsrev={};
    Do[If[!NumberQ[FCeqsaux[[i,2]]]&&Length[Level[FCeqsaux[[i,2]],1]]==0&&!MemberQ[MyListaux,ToString[FCeqsaux[[i,2]]]],
      FCeqsrev=Append[FCeqsrev,ToString[FCeqsaux[[i,2]]]->FCeqsaux[[i,1]]]],{i,1,Length[FCeqsaux]}];
    Do[WriteString[str,FCeqsrev[[i]],"\n"],{i,1,Length[FCeqsrev]}];
  Close[str];
  If[osswitch=="Windows",
    str=OpenWrite["MyBatch.bat"];
      WriteString[str,"@echo off \n"];
      WriteString[str,"copy Control.m ",StringDrop[StringReplace[dirNuc,"/"->"\\"],-8],"\n"];
      WriteString[str,"move dataFT.m ",StringReplace[dirNuc,"/"->"\\"],"\n"];
      WriteString[str,"move auxFT.m ",StringReplace[dirNuc,"/"->"\\"],"\n"];
      WriteString[str,"cd ",StringReplace[dirFey,"/"->"\\"],"\n"];
      WriteString[str,"move FRtoTeX.m ",StringReplace[dirNuc,"/"->"\\"],"\n"];
      WriteString[str,"move ParamsValues.m ",StringReplace[dirNuc,"/"->"\\"],"\n"];
      WriteString[str,"move Matrixind.m ",StringReplace[dirNuc,"/"->"\\"],"\n"];
      WriteString[str,"cd ",StringReplace[dirNuc,"/"->"\\"],"\n"];
      WriteString[str,"py JustConvert.py \n"];
      WriteString[str,"del dataFT.m \n"];
      WriteString[str,"del auxFT.m \n"];
      WriteString[str,"move FRtoTeX.m ",StringReplace[dirFey,"/"->"\\"],"\n"];
      WriteString[str,"move ParamsValues.m ",StringReplace[dirFey,"/"->"\\"],"\n"];
      WriteString[str,"move Matrixind.m ",StringReplace[dirFey,"/"->"\\"],"\n"];
      WriteString[str,"move movendum.zip ",StringReplace[dirHome,"/"->"\\"],"\n"];
      WriteString[str,"rmdir __pycache__ /S /Q \n"];
      WriteString[str,"cd ",StringReplace[dirFM,"/"->"\\"],"\n"];
      WriteString[str,"rmdir __pycache__ /S /Q \n"];
      (*WriteString[str,"pause \n"];*)
    Close[str];
    Run["MyBatch.bat"];
    DeleteFile["MyBatch.bat"],
  If[osswitch=="Linux"||osswitch=="Mac",
    str=OpenWrite["MyBatch.sh"];
      WriteString[str,"cp Control.m ",StringDrop[dirNuc,-8],"\n"];
      WriteString[str,"mv dataFT.m ",dirNuc,"\n"];
      WriteString[str,"mv auxFT.m ",dirNuc,"\n"];
      WriteString[str,"cd ",dirFey,"\n"];
      WriteString[str,"mv FRtoTeX.m ",dirNuc,"\n"];
      WriteString[str,"mv ParamsValues.m ",dirNuc,"\n"];
      WriteString[str,"mv Matrixind.m ",dirNuc,"\n"];
      WriteString[str,"cd ",dirNuc,"\n"];
      WriteString[str,"python3 JustConvert.py \n"];
      WriteString[str,"rm dataFT.m \n"];
      WriteString[str,"rm auxFT.m \n"];
      WriteString[str,"mv FRtoTeX.m ",dirFey,"\n"];
      WriteString[str,"mv ParamsValues.m ",dirFey,"\n"];
      WriteString[str,"mv Matrixind.m ",dirFey,"\n"];
      WriteString[str,"mv movendum.zip ",dirHome,"\n"];
      WriteString[str,"rm -fr __pycache__  \n"];
      WriteString[str,"cd ",dirFM,"\n"];
      WriteString[str,"rm -fr __pycache__  \n"];
      WriteString[str,"cd ",dirHome,"\n"];
      WriteString[str,"rm -fr newfiles \n"];
      WriteString[str,"unzip -q movendum.zip -d newfiles \n"];
      WriteString[str,"rm movendum.zip \n"];
    Close[str];
  Run["sh MyBatch.sh"];
  DeleteFile["MyBatch.sh"]]]],
  HoldAll];
(*---------------------------------------------------------------------*)




(*---------------------------------------------------------------------*)
(* FacToDecay: factorize expressions for decays *)
(* Created by: Duarte Fontes
   Email: duartefontes@tecnico.ulisboa.pt 
   Last Update: 28.07.2020

   Objective: simplify expressions in order to calculate the decay width. 
   Notes:
   1) FacToDecay yields a two-element list: the first element is the argument, but rewritten in terms of form factors;
      the second is a list with analytical expression for each form factor.
   2) It is only prepared for at maximum two external gauge bosons, and is not yet prepared for external fermions.
*)

FacToDecay::"usage"="FacToDecay[expr] simplifies expr for decays.
            It yields a two-element list: the first element is the argument, but rewritten in terms of form factors;
            the second is a list with analytical expression for each form factor (written using the kinematics of the process).
            The form factors are defined as complex parameters in the options of the FeynCalc function ComplexConjugate, which
            will be important to calculate the DecayWidth. FacToDecay is only prepared for at maximum two external gauge bosons.";

FacToDecay=Function[exp,Module[{M0,i,inew,m1,m2,kin,numind,fermflag,mya,myff,myanew,mybank,mybankpre,auxrep,
                                sl,sr,anl,anr,myres,myfin,gi,myexp},

If[!(NumberIn == 1 &&  NumberOut == 2), Print["Error: FacToDecay only works for two-body decays"]; Abort[]];

M0 = ToExpression["m"<> ToString[inparticlesB2[[1]]]];
m1 = ToExpression["m"<> ToString[outparticlesB2[[1]]]];
m2 = ToExpression["m"<> ToString[outparticlesB2[[2]]]];
kin={SP[p1, p1] -> M0^2, SP[q1, q1] -> m1^2, SP[q2, q2] -> m2^2,SP[p1, q1] -> 1/2(M0^2+m1^2-m2^2),
          SP[p1, q2] -> 1/2(M0^2+m2^2-m1^2), SP[q1, q2] -> 1/2(M0^2-m1^2-m2^2)};

numind=0;
If[ToString[intypes[[1]]]=="gauge",numind+=1];
If[ToString[outtypes[[1]]]=="gauge",numind+=1];
If[ToString[outtypes[[2]]]=="gauge",numind+=1];
fermflag=0;
If[ToString[intypes[[1]]]=="fermion" || ToString[outtypes[[1]]]=="fermion" || ToString[outtypes[[2]]]=="fermion",fermflag=1];
If[fermflag==1 && LoSpinors == False,Print["Error: LoSpinors must be True"]; Abort[]];

(* Auxiliary information for the cases with fermions: *)
If[ToString[intypes[[1]]] == "fermion" && ToString[outtypes[[1]]] == "fermion", 
    sl = Spinor[Momentum[q1], m1, 1];
    sr = Spinor[Momentum[p1], M0, 1];
    anl = ToString[InputForm[inparticlesB[[1]]]];
    anr = ToString[InputForm[outparticlesB[[1]]]];
    If[StringLength[anl] > 3 && StringLength[anr] > 3, 
      If[StringTake[anl, -3] == "bar" && StringTake[anr, -3] == "bar",
        sl = Spinor[-Momentum[p1], M0, 1];
        sr = Spinor[-Momentum[q1], m1, 1]]], 
If[ToString[intypes[[1]]] == "fermion" && ToString[outtypes[[2]]] == "fermion", 
    sl = Spinor[Momentum[q2], m2, 1];
    sr = Spinor[Momentum[p1], M0, 1];
    anl = ToString[InputForm[inparticlesB[[1]]]];
    anr = ToString[InputForm[outparticlesB[[2]]]];
    If[StringLength[anl] > 3 && StringLength[anr] > 3, 
      If[StringTake[anl, -3] == "bar" && StringTake[anr, -3] == "bar",
        sl = Spinor[-Momentum[p1], M0, 1];
        sr = Spinor[-Momentum[q2], m2, 1]]], 
If[ToString[outtypes[[1]]] == "fermion" && ToString[outtypes[[2]]] == "fermion", 
    sl = Spinor[Momentum[q1], m1, 1];
    sr = Spinor[-Momentum[q2], m2, 1];
    anl = ToString[InputForm[outparticlesB[[1]]]];
    If[StringLength[anl] > 3,If[StringTake[anl, -3] == "bar",
      sl = Spinor[Momentum[q2], m2, 1];
      sr = Spinor[-Momentum[q1], m1, 1]]]]]];

(* --- Processes without fermions --- *)
If[fermflag==0,
myexp=exp;

(* No fermions and no Lorentz indices: *)
If[numind==0,
mybank={},

(* No fermions and one Lorentz index: *)
If[numind==1,
mybank={FV[q1, -J1],FV[q1, -J2],FV[q1, -J4],
        FV[q2, -J1],FV[q2, -J2],FV[q2, -J4],
        FV[p1, -J1],FV[p1, -J2],FV[p1, -J4]},

(* No fermions and two Lorentz indices: *)
If[numind==2,
mybank={MT[-J1,-J2], MT[-J1,-J4], MT[-J2,-J4],
        FV[p1, -J1] FV[p1, -J2], FV[p1, -J1] FV[p1, -J4], FV[p1, -J2] FV[p1, -J4],
        FV[p1, -J1] FV[q1, -J2], FV[p1, -J1] FV[q1, -J4], FV[p1, -J2] FV[q1, -J4],
        FV[p1, -J1] FV[q2, -J2], FV[p1, -J1] FV[q2, -J4], FV[p1, -J2] FV[q2, -J4],
        FV[q1, -J1] FV[p1, -J2], FV[q1, -J1] FV[p1, -J4], FV[q1, -J2] FV[p1, -J4],
        FV[q1, -J1] FV[q1, -J2], FV[q1, -J1] FV[q1, -J4], FV[q1, -J2] FV[q1, -J4],
        FV[q1, -J1] FV[q2, -J2], FV[q1, -J1] FV[q2, -J4], FV[q1, -J2] FV[q2, -J4],
        FV[q2, -J1] FV[p1, -J2], FV[q2, -J1] FV[p1, -J4], FV[q2, -J2] FV[p1, -J4],
        FV[q2, -J1] FV[q1, -J2], FV[q2, -J1] FV[q1, -J4], FV[q2, -J2] FV[q1, -J4],
        FV[q2, -J1] FV[q2, -J2], FV[q2, -J1] FV[q2, -J4], FV[q2, -J2] FV[q2, -J4],
        LC[-J1, -J2][p1, q1], LC[-J1, -J4][p1, q1], LC[-J2, -J4][p1, q1],
        LC[-J1, -J2][q1, p1], LC[-J1, -J4][q1, p1], LC[-J2, -J4][q1, p1],
        LC[-J1, -J2][p1, q2], LC[-J1, -J4][p1, q2], LC[-J2, -J4][p1, q2],
        LC[-J1, -J2][q2, p1], LC[-J1, -J4][q2, p1], LC[-J2, -J4][q2, p1],
        LC[-J1, -J2][q1, q2], LC[-J1, -J4][q1, q2], LC[-J2, -J4][q1, q2],
        LC[-J1, -J2][q2, q1], LC[-J1, -J4][q2, q1], LC[-J2, -J4][q2, q1]}]]],

(* --- Processes with fermions --- *)
myexp = exp // DiracOrder // FCE;

(* Two fermions and no Lorentz indices: *)
If[numind==0,
mybankpre={GA[5],
        GS[p1], GS[q1], GS[q2],
        GS[p1].GA[5], GS[q1].GA[5], GS[q2].GA[5],
        GS[p1].GS[q1], GS[p1].GS[q2], GS[q1].GS[q2], 
        GS[p1].GS[q1].GA[5], GS[p1].GS[q2].GA[5], GS[q1].GS[q2].GA[5],
        GS[p1].GS[q1].GS[q2],GS[p1].GS[q1].GS[q2].GA[5]};
mybank={};
Do[AppendTo[mybank,sl.mybankpre[[i]].sr],{i,1,Length[mybankpre]}];
AppendTo[mybank,sl.sr],

(* Two fermions and one Lorentz index: *)
If[ToString[intypes[[1]]]=="gauge",gi=-J1,
If[ToString[outtypes[[1]]]=="gauge",gi=-J2,
If[ToString[outtypes[[2]]]=="gauge",gi=-J4]]];
mybank={FV[p1,gi] sl.sr, FV[q1,gi] sl.sr, FV[q2,gi] sl.sr,
        sl.GA[gi].sr, sl.GA[gi].GA[5].sr,
        sl.GA[gi].GS[p1].sr, sl.GA[gi].GS[q1].sr, sl.GA[gi].GS[q2].sr,
        sl.GA[gi].GS[p1].GA[5].sr, sl.GA[gi].GS[q1].GA[5].sr, sl.GA[gi].GS[q2].GA[5].sr, 
        sl.GA[gi].GS[p1].GS[q1].sr, sl.GA[gi].GS[p1].GS[q2].sr, sl.GA[gi].GS[q1].GS[q2].sr,
        sl.GA[gi].GS[p1].GS[q1].GA[5].sr, sl.GA[gi].GS[p1].GS[q2].GA[5].sr, sl.GA[gi].GS[q1].GS[q2].GA[5].sr,
        sl.GA[gi].GS[p1].GS[q1].GS[q2].sr,sl.GA[gi].GS[p1].GS[q1].GS[q2].GA[5].sr,
        FV[p1,gi] sl.GA[5].sr, FV[q1,gi] sl.GA[5].sr, FV[q2,gi] sl.GA[5].sr,
        sl.GS[p1].sr FV[p1,gi], sl.GS[p1].sr FV[q1,gi], sl.GS[p1].sr FV[q2,gi],
        sl.GS[q1].sr FV[p1,gi], sl.GS[q1].sr FV[q1,gi], sl.GS[q1].sr FV[q2,gi],
        sl.GS[q2].sr FV[p1,gi], sl.GS[q2].sr FV[q1,gi], sl.GS[q2].sr FV[q2,gi],
        sl.GS[p1].GA[5].sr FV[p1,gi], sl.GS[p1].GA[5].sr FV[q1,gi], sl.GS[p1].GA[5].sr FV[q2,gi],
        sl.GS[q1].GA[5].sr FV[p1,gi], sl.GS[q1].GA[5].sr FV[q1,gi], sl.GS[q1].GA[5].sr FV[q2,gi],
        sl.GS[q2].GA[5].sr FV[p1,gi], sl.GS[q2].GA[5].sr FV[q1,gi], sl.GS[q2].GA[5].sr FV[q2,gi]}]];

(* Final things *)
myfflist={};
If[mybank=={},
  myres=ff1;
  myfflist={ff1};
  auxrep={ff1->exp},
    mya={};
    myres=0;
    auxrep={};
    Do[
      mya=Append[mya,Coefficient[myexp,mybank[[i]]]];
      myff=ToExpression[ToString[StringForm["ff``",i]]];
      AppendTo[myfflist,myff];
      If[ToString[InputForm[mya[[i]]]]!="0",
        myres+= myff mybank[[i]];
        auxrep=Append[auxrep,myff->mya[[i]]]],{i,1,Length[mybank]}]];
SetOptions[ComplexConjugate, Conjugate -> myfflist];
auxrep2=auxrep/.kin;
myfin={myres,auxrep2}]];
(*---------------------------------------------------------------------*)


(*---------------------------------------------------------------------*)
(* DecayWidth: compute the decay width *)
(* Created by: Duarte Fontes
   Email: duartefontes@tecnico.ulisboa.pt 
   Last Update: 28.07.2020

   Objective: compute the decay width.
   Notes:
   1) It depends on the number of polarizations of the decaying particle. Scalars and neutrinos have only one
      (for FeynMaster to know that a particle is a neutrino, the attribute Neutrino should be set to True in the definition
      of the particle at stake in the FeynMaster model file), the remaining fermions have two, and massive gauge bosons have three.
      We did not consider the case of decaying massless particles, which can never be physical.
   2) For a complicated expression, it is recomended to simplify it first with FacToDecay, which rewrites it in terms of form factors,
      and only then use the DecayWidth.
*)

DecayWidth::"usage"="DecayWidth[expr] computes the decay width of expr. It only works for decays in two-bodies.
            It depends on the number of polarizations of the decaying particle;
            scalars and neutrinos have only one (for FeynMaster to know that a particle is a neutrino, the attribute Neutrino should
            be set to True in the definition of the particle at stake in the FeynMaster model file), the remaining fermions have two,
            and massive gauge bosons have three. We did not consider the case of decaying massless particles, which can never be
            physical. For a complicated expression, it is recomended to simplify it first with FacToDecay, which rewrites it in terms
            of form factors, and only then use the DecayWidth. Finally, DecayWidth takes by default one simple argument, corresponding
            to the expression (say, E) which DecayWidth is to be applied to; the final result is then proportional to E^2; DecayWidth
            also accepts an argument correponding to a two-element list (e.g., DecayWidth[{E0, E1}]); in this case, the result is proportional
            to 2 Re [E0,Conjugate[E1]]";

DecayWidth = Function[{exp}, 
                          Module[{kin,ApplyTrace,indrepint1,indrepint2,indrep1a,M0,m1,m2,
                                    indrep2a,indrep3a,indrep1b,indrep2b,indrep3b,
                                    XX0,XX0c,XX1,XX2,p1m,inifac,finfac,BarSqModM,DW},                           
If[!(NumberIn == 1 &&  NumberOut == 2), Print["Error: DecayWidth only works for two-body decays"]; Abort[]];
M0 = ToExpression["m"<> ToString[inparticlesB2[[1]]]];
m1 = ToExpression["m"<> ToString[outparticlesB2[[1]]]];
m2 = ToExpression["m"<> ToString[outparticlesB2[[2]]]];
Nclist=Get["Nclist.m", Path -> {dirFey}];
ApplyTrace = {DiracTrace[x_] -> TrG5[x]};
kin={SP[p1, p1] -> M0^2, SP[q1, q1] -> m1^2, SP[q2, q2] -> m2^2,SP[p1, q1] -> 1/2(M0^2+m1^2-m2^2),
          SP[p1, q2] -> 1/2(M0^2+m2^2-m1^2), SP[q1, q2] -> 1/2(M0^2-m1^2-m2^2)};
indrep1a={};indrep2a={};indrep3a={};indrep1b={};indrep2b={};indrep3b={};
indrepint1={$MU[1]->indm1,$MU[2]->indm2,$MU[3]->indm3,$MU[4]->indm4,J1->ind1,J2->ind2,J3->ind3,J4->ind4,J5->ind5,J6->ind6,J7->ind7,J8->ind8,J9->ind9,J10->ind10,J11->ind11,J12->ind12};
indrepint2={indm1->indm1b,indm2->indm2b,indm3->indm3b,indm4->indm4b,ind1->ind1b,ind2->ind2b,ind3->ind3b,ind4->ind4b,ind5->ind5b,ind6->ind6b,ind7->ind7b,ind8->ind8b,ind9->ind9b,ind10->ind10b,ind11->ind11b,ind12->ind12b};
If[ToString[intypes[[1]]]=="gauge"||ToString[intypes[[1]]]=="gluon", indrep1a={-J1->\[Mu]a}; indrep1b={\[Mu]a->\[Mu]b}];
If[ToString[outtypes[[1]]]=="gauge"||ToString[outtypes[[1]]]=="gluon", indrep2a={-J2->\[Nu]a}; indrep2b={\[Nu]a->\[Nu]b}];
If[ToString[outtypes[[2]]]=="gauge"||ToString[outtypes[[2]]]=="gluon", indrep3a={-J4->\[Sigma]a}; indrep3b={\[Sigma]a->\[Sigma]b}];
  If[ToString[intypes[[1]]]=="fermion" || ToString[outtypes[[1]]]=="fermion" || ToString[outtypes[[2]]]=="fermion",
  If[LoSpinors == False, Print["Error: LoSpinors should be set to True to compute the decay width"]; Abort[]]];
  If[MoCoLogic == True, Print["Error: MoCoLogic should be set to False to compute the decay width"]; Abort[]];

If[ToString[exp // Head] != "List",
XX0 = exp /. indrep1a /. indrep2a /. indrep3a /. indrepint1;
XX0c = ComplexConjugate[XX0]  /. indrep1b /. indrep2b /. indrep3b /. indrepint2;
XX1 = ((ChangeTo4[FermionSpinSum[XX0c XX0]]) /. ApplyTrace) // FCE,
(* *)
XX0 = ComplexConjugate[exp[[1]]] /. indrep1a /. indrep2a /. indrep3a /. indrepint1;
XX0c = (exp[[2]] /. indrep1a /. indrep2a /. indrep3a /. indrepint1) /. indrep1b /. indrep2b /. indrep3b /. indrepint2;
XX1 = ((ChangeTo4[FermionSpinSum[XX0c XX0]]) /. ApplyTrace) // FCE];

If[ToString[intypes[[1]]]=="gauge"||ToString[intypes[[1]]]=="gluon",
  If[ToString[InputForm[M0]] != "0",
    XX1 = Simplify[XX1*(-MT[\[Mu]a, \[Mu]b] + FV[p1, \[Mu]a] FV[p1, \[Mu]b]/M0^2) // Calc] // FCE,
    XX1 = Simplify[XX1*(-MT[\[Mu]a, \[Mu]b]) // Calc] // FCE],
  XX1 = Simplify[XX1 // Calc] // FCE];
If[ToString[outtypes[[1]]]=="gauge"||ToString[outtypes[[1]]]=="gluon",
  If[ToString[InputForm[m1]] != "0",
    XX1 = Simplify[XX1*(-MT[\[Nu]a, \[Nu]b] + FV[q1, \[Nu]a] FV[q1, \[Nu]b]/m1^2) // Calc] // FCE,
    XX1 = Simplify[XX1*(-MT[\[Nu]a, \[Nu]b]) // Calc] // FCE],
  XX1 = Simplify[XX1 // Calc] // FCE];
If[ToString[outtypes[[2]]]=="gauge"||ToString[outtypes[[2]]]=="gluon",
  If[ToString[InputForm[m2]] != "0",
    XX1 = Simplify[XX1*(-MT[\[Sigma]a, \[Sigma]b] + FV[q2, \[Sigma]a] FV[q2, \[Sigma]b]/m2^2) // Calc] // FCE,
    XX1 = Simplify[XX1*(-MT[\[Sigma]a, \[Sigma]b]) // Calc] // FCE],
  XX1 = Simplify[XX1 // Calc] // FCE];
XX2 = Simplify[XX1 /. kin];
(* Ok, what we did so far was the sum over spins and polarizations of the squared modulus of the total amplitude. Now, the rest: *)
p1m=MyKallen[M0^2,m1^2,m2^2]/(2 M0);
If[ToString[intypes[[1]]]=="fermion" && !MemberQ[Neutrinos, inparticlesA],
inifac=1/2,
If[ToString[intypes[[1]]]=="gauge",inifac=1/3,
inifac=1]];
If[ToString[outparticlesB[[1]]]==ToString[outparticlesB[[2]]],finfac=1/2,finfac=1];
If[MemberQ[Nclist,outparticlesB2[[1]]]&&MemberQ[Nclist,outparticlesB2[[2]]],finfac=finfac*3];
If[ToString[exp // Head] != "List",
BarSqModM=inifac*XX2*finfac,
BarSqModM=2*inifac*Re[XX2]*finfac];
DW=(4 Pi)*(1/(32 Pi^2))*p1m/(M0^2)*BarSqModM/. {Sqrt[a_^4]->a^2, Sqrt[a_^2]->a}]];
(*---------------------------------------------------------------------*)


(*---------------------------------------------------------------------*)
(* DiffXS: compute the differencial cross section *)
(* Created by: Duarte Fontes
   Email: duartefontes@tecnico.ulisboa.pt 
   Modified by: Jorge Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 04.08.2020

   Objective: compute the differencial cross section.
   Notes:
   1) It depends on the number of polarizations of the initial particles. Scalars and neutrinos have only one
      (for FeynMaster to know that a particle is a neutrino, the attribute Neutrino should be set to True in the definition
      of the particle at stake in the FeynMaster model file), the remaining fermions have two, and massive gauge bosons have three.
      We did not consider the case of initial massless particles.
   2) The expression is written in terms of the center-of-mass energy S.
*)

DiffXS::"usage"="DiffXS[exp] compute the differencial cross section of expr.
        The expression is written in terms of the center-of-mass energy S.
        It depends on the number of polarizations of the initial particles; scalars and neutrinos have only one
        (for FeynMaster to know that a particle is a neutrino, the attribute Neutrino should be set to True in
        the Definition of the particle at stake in the FeynMaster model file), the remaining fermions have two,
        and massive gauge bosons have three. We did not yet consider the case of initial massless particles.";

DiffXS = Function[{exp}, 
                          Module[{kin,ApplyTrace,Ene1,Ene2,Ene3,Ene4,p1m,p2m,p3m,p4m,m1,m2,m3,m4, (*Modified jcr 04.08.2020*)
                                    indrep1a,indrep2a,indrep3a,indrep4a,
                                    indrep1b,indrep2b,indrep3b,indrep4b,
                                    indrepint1,indrepint2,
                                    XX0,XX0c,XX1pre,XX1,XX2,inifac,finfac,BarSqModM,DXS},
If[!(NumberIn == 2 &&  NumberOut == 2), Print["Error: DiffXS only works for 2x2 scatterings"]; Abort[]];                                    
m1 = ToExpression["m"<> ToString[inparticlesB2[[1]]]];
m2 = ToExpression["m"<> ToString[inparticlesB2[[2]]]];
m3 = ToExpression["m"<> ToString[outparticlesB2[[1]]]];
m4 = ToExpression["m"<> ToString[outparticlesB2[[2]]]];
Nclist=Get["Nclist.m", Path -> {dirFey}];
ApplyTrace = {DiracTrace[x_] -> TrG5[x]};
Ene1 = (S+m1^2-m2^2)/(2*Sqrt[S]);
Ene2 = (S+m2^2-m1^2)/(2*Sqrt[S]);
Ene3 = (S+m3^2-m4^2)/(2*Sqrt[S]);
Ene4 = (S+m4^2-m3^2)/(2*Sqrt[S]);
p1m = MyKallen[S,m1^2,m2^2]/(2*Sqrt[S]);
p2m = MyKallen[S,m1^2,m2^2]/(2*Sqrt[S]);
q1m = MyKallen[S,m3^2,m4^2]/(2*Sqrt[S]);
q2m = MyKallen[S,m3^2,m4^2]/(2*Sqrt[S]);
kin={SP[p1, p1] -> m1^2, SP[p2, p2] -> m2^2, SP[q1, q1] -> m3^2, SP[q2, q2] -> m4^2,
          SP[p1, p2] -> Ene1 Ene2 + p1m p2m, 
          SP[p1, q1] -> Ene1 Ene3 - p1m q1m Cos[Theta],
          SP[p1, q2] -> Ene1 Ene4 + p1m q2m Cos[Theta],
          SP[p2, q1] -> Ene2 Ene3 + p2m q1m Cos[Theta],
          SP[p2, q2] -> Ene2 Ene4 - p1m q2m Cos[Theta],
          SP[q1, q2] -> Ene3 Ene4 + q1m q2m};
indrep1a={};indrep2a={};indrep3a={};indrep4a={};indrep1b={};indrep2b={};indrep3b={};indrep4b={};
indrepint1={$MU[1]->indm1,$MU[2]->indm2,$MU[3]->indm3,$MU[4]->indm4,J1->ind1,J2->ind2,J3->ind3,J4->ind4,J5->ind5,J6->ind6,J7->ind7,J8->ind8,J9->ind9,J10->ind10,J11->ind11,J12->ind12};
indrepint2={indm1->indm1b,indm2->indm2b,indm3->indm3b,indm4->indm4b,ind1->ind1b,ind2->ind2b,ind3->ind3b,ind4->ind4b,ind5->ind5b,ind6->ind6b,ind7->ind7b,ind8->ind8b,ind9->ind9b,ind10->ind10b,ind11->ind11b,ind12->ind12b};
If[ToString[intypes[[1]]]=="gauge"||ToString[intypes[[1]]]=="gluon", indrep1a={-J1->\[Mu]a}; indrep1b={\[Mu]a->\[Mu]b}];
If[ToString[intypes[[2]]]=="gauge"||ToString[intypes[[2]]]=="gluon", indrep2a={-J3->\[Rho]a}; indrep2b={\[Rho]a->\[Rho]b}];
If[ToString[outtypes[[1]]]=="gauge"||ToString[outtypes[[1]]]=="gluon", indrep3a={-J2->\[Nu]a}; indrep3b={\[Nu]a->\[Nu]b}];
If[ToString[outtypes[[2]]]=="gauge"||ToString[outtypes[[2]]]=="gluon", indrep4a={-J4->\[Sigma]a}; indrep4b={\[Sigma]a->\[Sigma]b}];
  If[ToString[intypes[[1]]]=="fermion" || ToString[intypes[[2]]]=="fermion" || ToString[outtypes[[1]]]=="fermion" || ToString[outtypes[[1]]]=="fermion",
  If[LoSpinors == False, Print["Error: LoSpinors should be set to True to compute the differential cross section"]; Abort[]]];
  If[MoCoLogic == True, Print["Error: MoCoLogic should be set to False to compute the differential cross section"]; Abort[]];
XX0a = exp //MyFADExplicit ; (*Modified jcr 04.08.2020*)
XX0 = XX0a /. indrep1a /. indrep2a /. indrep3a /. indrep4a /. indrepint1;
XX0c = ComplexConjugate[XX0]  /. indrep1b /. indrep2b /. indrep3b /. indrep4b /. indrepint2;
XX1pre = ((ChangeTo4[FermionSpinSum[XX0c XX0]]) /. ApplyTrace) // FCE;
XX1pre2 = ((XX1pre) /. expsp) /. expsp;
XX1=(XX1pre2//Calc)//FCE;  (*Modified jcr 04.08.2020*)
MyNewX=XX1;
If[ToString[intypes[[1]]]=="gauge"||ToString[intypes[[1]]]=="gluon",
  If[ToString[InputForm[m1]] != "0",
    XX1 = (XX1*(-MT[\[Mu]a, \[Mu]b] + FV[p1, \[Mu]a] FV[p1, \[Mu]b]/m1^2) // Calc) // FCE,
    XX1 = (XX1*(-MT[\[Mu]a, \[Mu]b]) // Calc) // FCE]];
If[ToString[intypes[[2]]]=="gauge"||ToString[intypes[[2]]]=="gluon",
  If[ToString[InputForm[m2]] != "0",
    XX1 = (XX1*(-MT[\[Rho]a, \[Rho]b] + FV[p2, \[Rho]a] FV[p2, \[Rho]b]/m2^2) // Calc) // FCE,
    XX1 = (XX1*(-MT[\[Rho]a, \[Rho]b]) // Calc) // FCE]]; 
If[ToString[outtypes[[1]]]=="gauge"||ToString[outtypes[[1]]]=="gluon",
  If[ToString[InputForm[m3]] != "0",
    XX1 = (XX1*(-MT[\[Nu]a, \[Nu]b] + FV[q1, \[Nu]a] FV[q1, \[Nu]b]/m3^2) // Calc) // FCE,
    XX1 = (XX1*(-MT[\[Nu]a, \[Nu]b]) // Calc) // FCE]];
If[ToString[outtypes[[2]]]=="gauge"||ToString[outtypes[[2]]]=="gluon",
  If[ToString[InputForm[m4]] != "0",
    XX1 = (XX1*(-MT[\[Sigma]a, \[Sigma]b] + FV[q2, \[Sigma]a] FV[q2, \[Sigma]b]/m4^2) // Calc) // FCE,
    XX1 = (XX1*(-MT[\[Sigma]a, \[Sigma]b]) // Calc) // FCE]];
XX2 = XX1 /. kin;
(* Ok, what we did so far was the sum over spins and polarizations of the squared modulus of the total amplitude. Now, the rest: *)

If[ToString[intypes[[1]]]=="fermion"&&!MemberQ[Neutrinos,inparticlesB[[1]]],pol1=2,If[ToString[intypes[[1]]]=="gauge",pol1=3,pol1=1]];
If[ToString[intypes[[2]]]=="fermion"&&!MemberQ[Neutrinos,inparticlesB[[2]]],pol2=2,If[ToString[intypes[[2]]]=="gauge",pol2=3,pol2=1]];
inifac=1/(pol1*pol2);
If[ToString[outparticlesB[[1]]]==ToString[outparticlesB[[2]]],finfac=1/2,finfac=1];
If[MemberQ[Nclist,outparticlesB2[[1]]]&&MemberQ[Nclist,outparticlesB2[[2]]],finfac=finfac*3];
BarSqModM=inifac*XX2*finfac;
DXS=(1/(64 Pi^2 S))*q1m/p1m*BarSqModM]];
(*---------------------------------------------------------------------*)


(*---------------------------------------------------------------------*)
(* Get coefficients for 2 , 3 and 4 terms *)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Functions to extract coefficients up to 4 terms
*)

Coef4 =Function[{expr, a, b, c, d}, Coefficient[Coefficient[Coefficient[Coefficient[expr, a], b], c], d]];
Coef4::"usage"="Coef4[expr, a, b, c, d] extracts the coefficients of expr with respect to a, b, c, d";

Coef3 =Function[{expr, a, b, c}, Coefficient[Coefficient[Coefficient[expr, a], b], c]];
Coef3::"usage"="Coef3[expr, a, b, c] extracts the coefficients of expr with respect to a, b, c";

Coef2 =Function[{expr, a, b}, Coefficient[Coefficient[expr, a], b]];
Coef2::"usage"="Coef2[expr, a, b] extracts the coefficients of expr with respect to a, b";
(*---------------------------------------------------------------------*)


(*---------------------------------------------------------------------*)
(* NoDirac: Annul the Dirac structures *)
(* Created by: Duarte Fontes
   Email: duartefontes@tecnico.ulisboa.pt 
   Last Update: 08.10.2020

   Objective: Keeps only the terms with no Dirac structure. 
*)

NoDirac::"usage"="AnullDirac[expr] keeps only the terms with no Dirac structure.";

NoDirac=Function[exp,Module[{aux1,aux2},
Clear[StandardMatrixElement];
aux1=DiracOrder[exp] // ToStandardMatrixElement;
aux2=FCE[aux1 /. {StandardMatrixElement[x_] -> 0}]]];  
(*---------------------------------------------------------------------*)


  
(*---------------------------------------------------------------------*)
(* GetDirac: Get the Dirac structures *)
(* Created by: Jorge C. Romao and Duarte Fontes
   Email: jorge.romao@tecnico.ulisboa.pt, duartefontes@tecnico.ulisboa.pt 
   Last Update: 29.07.2020

   Objective: Gets and prints the Standard Matrix Elements. This is useful to work with amplitudes with spinors
              in the external lines.
*)

GetDirac::"usage"="GetDirac[expr] yields the Dirac structures of expr as a list. This is useful to work with amplitudes with fermions in the external lines.";

GetDirac=Function[exp,Module[{aux1,aux2,aux3,aux4,aux5,exp0,exp1,ListDirac},
exp0=exp//DiracSimplify;
exp1=exp0//DiracOrder;
Clear[StandardMatrixElement];
aux1=FCDiracIsolate[exp1, Head -> StandardMatrixElement] // Expand2[#, {StandardMatrixElement, Pair}] & //   Collect2[#, StandardMatrixElement] &;
aux2 = Select[Variables[aux1], (Head[#] === StandardMatrixElement) &];
ListDirac = Table[
aux3 = ToString[aux2[[i]]];
aux4 = StringPosition[aux3, "]"];
aux5 = StringTake[aux3, {23, aux4[[Length[aux4]]][[1]] - 1}];
ToExpression[aux5]//FCE, {i, 1, Length[aux2]}]]];  
(*---------------------------------------------------------------------*)
  

(*---------------------------------------------------------------------*)
(* RepDirac: Substitute the Dirac structures *)
(* Created by: Jorge C. Romao and Duarte Fontes
   Email: jorge.romao@tecnico.ulisboa.pt 
   Modified by Duarte Fontes
   Email: duartefontes@tecnico.ulisboa.pt 
   Last Update: 29.07.2020

   Objective: RepDirac[expr] replaces the Standard Matrix Elements of expr with elements ME[j].
              This is useful to work with amplitudes with fermions in the external lines.
              RepDirac admits a second (optional) argument, consisting of a list of Dirac structures (ex: {GA[p1],GS[q1]}).
              The correspondance between ME[j] elements and Dirac structures can obey one of two rules:
              either only one argument is given to RepDirac, in which case the ME[j] elements follow the order of the Dirac structures yielded by GetDirac[expr],
              or a list of Dirac structures is given as a second argument of RepDirac, in which case the ME[j] elements follow the order of that list.
*)

RepDirac::"usage"="RepDirac[expr] replaces the Dirac structures of expr with elements ME[j].
                This is useful to work with amplitudes with fermions in the external lines.
                RepDirac admits a second (optional) argument, consisting of a list of Dirac structures (ex: {GA[p1],GS[q1]}).
                The correspondance between ME[j] elements and Dirac structures can obey one of two rules:
                either only one argument is given to RepDirac, in which case the ME[j] elements follow the order of the Dirac structures yielded by GetDirac[expr],
                or a list of Dirac structures is given as a second argument of RepDirac, in which case the ME[j] elements follow the order of that list.";

RepDirac = {##} /. {exp_, what_: {}} :> Module[{aux,exp0,exp1,trigger,varaux,a,b},
Clear[StandardMatrixElement];
exp0=exp//DiracSimplify;
exp1=exp0//DiracOrder;
aux = FCDiracIsolate[exp1, Head -> StandardMatrixElement] // Expand2[#, {StandardMatrixElement, Pair}] & // Collect2[#, StandardMatrixElement] &;
If[ToString[InputForm[what]] == "{}",
varaux = Select[Variables[aux], (Head[#] === StandardMatrixElement) &],
varaux = FCDiracIsolate[what, Head -> StandardMatrixElement] // Expand2[#, {StandardMatrixElement, Pair}] & // Collect2[#, StandardMatrixElement] &];
Set @@ {varaux, Table[ME[j], {j, 1, Length[varaux]}]};
aux//FCE] &;
(*---------------------------------------------------------------------*)  


(*---------------------------------------------------------------------*)  
(* ChangeToB0Unique: Change to B0Unique => B0(0,m^2,m^2) *)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Transforms equivalente forms of B0 into an unique form : B0(0,m^2,m^2)
*)

ChangeToB0Unique::"usage"="ChangeToB0Unique[expr] changes the various equivalent forms of A0[m^2], B0[0,m^2,m^2], B0[m^2,0,m^2] and B0[0,0,m^2] to a unique  B0[m^2,0,m^2]";

ChangeToB0Unique = 
  Function[exp, Module[{subrule1,subrule2,x,y,z,xx,yy,zz,res},
  subrule1= {PaVe[0, {}, {x_}]->A0[x], PaVe[0, {x_}, {y_,z_}] -> B0[x,y,z], PaVe[1, {x_}, {y_,z_}] -> B1[x,y,z]};
  subrule2={B0[0, 0, xx_] -> B0[0, xx, xx] + 1, 
    B0[yy_, 0, yy_] -> B0[0, yy, yy] + 2, 
    A0[zz_] -> zz ( B0[0,zz, zz] + 1)};
    res=(exp /. subrule1)/.subrule2]];
(*---------------------------------------------------------------------*)


(*---------------------------------------------------------------------*)  
(* GetDiv: Get the divergent Part of Loop Integrals *)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 12.09.2020

   Objective: Obtains the coefficient of the divergent part o PaVe functions.
   Notes:
   1) div= 1/epsilon

*)

GetDivtest::"usage"="GetDiv1[expr] obtains the coefficient of the divergent part named div= 1/\[Epsilon] where \[Epsilon] = 4 -D. Uses the FeynCalc functions PaVeUVPart.";

GetDivtest=Function[expr,FCE[Coefficient[PaVeUVPart[expr], D - 4, -1] (-div)]];


(*---------------------------------------------------------------------*)  
(* GetDiv: Get the divergent Part of Loop Integrals *)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 29.01.2020

   Objective: Obtains the coefficient of the divergent part. 
   Notes:
   1) div= 1/epsilon
   2) Warns if Div of higer rank not implemented

   Needs: WhichPV, PVList, 
   Explanation:
   WhichPV: returns a list of the form {nids,nmom} where nids is the number of 
   numbers before the momenta and nmom the number of momenta. For instance
   PaVe[0,{p},{m1,m2}] has nids=1, nmom=1, and PaVe[0,0,{p1,p2,p3},{m1,m2,m3}] 
   has nids=2,nmom=3
   GetPVList: If an expression has a sum of several terms it gives a list of {nids,nmom} for 
   each term.
   CheckIfImplemented: Returns True if implemented, False otherwise. Implemented means that
   it gives the divergent part. Some higher momenta divergent integrals whose divergent part
   is proportional to the momenta are not included. These rarely appear in a gauge theory at
   one-loop order. For example PaVe[0,0,0,p1^2,m0^2,m1^2]. For a complete list see Denner and
   Dittmaier hep-ph/0509141.
*)


GetDiv::"usage"="GetDiv[expr] obtains the coefficient of the divergent part named div= 1/\[Epsilon] where \[Epsilon] = 4 -D. If the divergent PaVe function is not implemented it gives a warning.";

GetDiv=Function[exp,Module[{xx,yy,zz,ww,vv,subDiv},
PVList=GetPVList[exp];
CheckIfImplemented[PVList];
If[Implemented,  
subDiv=
{ PaVe[0,{},{xx_}]-> 2 xx div,
 A0[xx_]-> 2 xx div, 
 PaVe[0,0,{},{xx_}]-> 2 xx^2/D div,
 PaVe[0,0,{},{xx_},zz_,ww_]-> 1 xx^2/2 div,
 PaVe[0,{xx_},{yy_,zz_}]-> 2 div,
 B0[xx_,yy_,zz_]-> 2 div,
 PaVe[1,{xx_},{yy_,zz_}]-> - div,
 PaVe[1,{xx_},{yy_,zz_},ww_,vv_]-> - div,
 B1[xx_,yy_,zz_]-> - div,
 B00[xx_,yy_,zz_]->1/6 div (3 yy + 3 zz -xx),
 PaVe[0,0,{xx_},{yy_,zz_}]-> 1/6 div (3 yy + 3 zz -xx),
 PaVe[0,0,{xx_},{yy_,zz_},ww_,vv_]-> 1/6 div (3 yy + 3 zz -xx),
 B11[xx_,yy_,zz_]-> 2/3 div, 
 PaVe[1,1,{xx_},{yy_,zz_}]-> 2/3 div,
 PaVe[1,1,{xx_},{yy_,zz_},ww_,vv_]-> 2/3 div,
 PaVe[0,0,1,{xx_},{yy_,zz_}]-> div/12  (xx -2 yy -4 zz),
 PaVe[0,0,1,{xx_},{yy_,zz_},ww_,vv_]-> div/12  (xx -2 yy -4 zz),
 PaVe[1,1,1,{xx_},{yy_,zz_}]-> -1/2 div,
 PaVe[1,1,1,{xx_},{yy_,zz_},ww_,vv_]-> -1/2 div,
 PaVe[0,0,{a_,b_,c_},{xx_,yy_,zz_}]-> 1/2 div,
 PaVe[0,0,{a_,b_,c_},{xx_,yy_,zz_},ww_,v_]-> 1/2 div,
 PaVe[0,0,1,{a_,b_,c_},{xx_,yy_,zz_}]-> -1/6 div,
 PaVe[0,0,1,{a_,b_,c_},{xx_,yy_,zz_},ww_,vv_]-> -1/6 div,
 PaVe[0,0,2,{a_,b_,c_},{xx_,yy_,zz_}]-> -1/6 div,
 PaVe[0,0,2,{a_,b_,c_},{xx_,yy_,zz_},ww_,vv_]->-1/6 div,
 PaVe[0,0,0,0,{xx1_,xx2_,xx3_,xx4_,xx5_,xx6_},{yy1_,yy2_,yy3_,yy4_}]-> 1/12 div,
 PaVe[0,0,0,0,{xx1_,xx2_,xx3_,xx4_,xx5_,xx6_},{yy1_,yy2_,yy3_,yy4_},ww_,vv_]-> 1/12 div};
  div Coefficient[exp /.subDiv,div],
Print["Warning: There are PV functions of higher rank for which GetDiv is not yet implemented"]]
  ]] ;

WhichPV::"usage"="WhichPV[expr] returns a list of the form {nids,nmom} where nids is the number of numbers before the momenta and nmom the number of momenta. For instance PaVe[0,{p},{m1,m2}] has nids=1, nmom=1, and PaVe[0,0,{p1,p2,p3},{m1,m2,m3}] has nids=2,nmom=3.";

WhichPV=Function[exp,Module[{aux0,aux1,aux2,aux3,aux4,aux5,aux6,aux7},
aux0=Expand[exp];
aux1=ToString[aux0];
aux2=StringPosition[aux1, "PaVe["];
If[Length[aux2] !=0,  
aux3=StringTake[aux1, {aux2[[1, 2]], StringLength[aux1]}];
aux4=StringPosition[aux3, "{"];
aux5=StringPosition[aux3, "}"];
aux6=StringTake[aux3, {aux4[[1, 1]], aux5[[1, 1]]}];
nmom=Length[ToExpression[aux6]];
aux7=StringTake[aux3, {2, aux4[[1, 2]] - 3}];
nids=Length[ToExpression[StringJoin["{", aux7, "}"]]];
{nids,nmom},{0,2}]
]];  

CheckIfImplemented::"usage"="CheckIfImplemented[PVList] checks if the divergent PaVe functions in PVList are implemented. Returns Implemented=True or False.";

CheckIfImplemented=Function[lista,Implemented=True;
Do[If[lista[[i,2]] >6,  Implemented=False];
If[lista[[i,2]] == 6&&lista[[i,1]]>4,  Implemented=False];
If[lista[[i,2]] == 3&&lista[[i,1]]>3,  Implemented=False];
If[lista[[i,2]] == 1&&lista[[i,1]]>3,  Implemented=False];
,{i,1,Length[lista]}];Implemented];

GetPVList::"usage"="GetPVList[expr] gives a list of {nids,nmom} for each term of an expression that is a sum of several terms.";

GetPVList=Function[exp,Module[{aux0,ListL,LenList,Lenaux0,auxFinal0,auxFinal1,aux0i,Lenaux0i,auxi,auxList},
aux0=exp//Expand;  
ListL=False;  
If[Head[exp] === List,LenList=Length[exp];ListL=True;];
If[ListL === False,  
If[Head[aux0] === Plus, Lenaux0 = Length[aux0], Lenaux0 = 1];
If[Lenaux0 == 1, auxFinal0 = {WhichPV[aux0]}, 
    auxFinal0=Table[WhichPV[aux0[[i]]], {i, 1, Lenaux0}]];
,
auxList={};    
Do[aux0i=aux0[[i]];
If[Head[aux0i] === Plus, Lenaux0i = Length[aux0i], Lenaux0i = 1];
If[Lenaux0i == 1, auxi={WhichPV[aux0i]};auxList=Append[auxList,auxi];, 
      auxi=Table[WhichPV[aux0i[[j]]], {j, 1, Lenaux0i}];
      auxList=Append[auxList,auxi];];
,{i,1,LenList}];
    ];
If[ListL,
auxFinal1={};
    Do[auxFinal1=Append[auxFinal1,auxList[[i]][[j]]],{i,1,LenList},{j,1,Length[auxList[[i]]]}];
    auxFinal=auxFinal1;,auxFinal=auxFinal0;
    ];
auxFinal
    ]];
(*---------------------------------------------------------------------*)


(*---------------------------------------------------------------------*)
(* GetFinite: Get the finite term from the divergent Part *)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Obtains the finite term coming from the epsilon x 1/epslion terms.
*)


GetFinite::"usage"="GetFinite[expr] obtains the finite term coming from the \[Epsilon] x 1/\[Epsilon] terms. Typically the 1/\[Epsilon] will come from the divergent parts and the \[Epsilon] from the D=4-\[Epsilon].";

GetFinite=Function[exp, Module[{aux0,aux1,aux3,aux4,aux5,SpinorBackToD},
aux0=exp//FCE;
aux1=GetDiv[aux0];
aux3=aux1 /. {D-> 4-eps,div-> 1/eps};
SpinorBackToD = {Momentum[qq_, 4 - eps] -> Momentum[qq, D]};
aux4=aux3/. SpinorBackToD;
aux5=Coefficient[Normal[Series[aux4,{eps,0,1}]],eps,0];
aux5]];
(*---------------------------------------------------------------------*)



(*---------------------------------------------------------------------*)
(* TakeReal: Apply the operator Re to the Passarino-Veltman functions *)
(* Created by: Duarte Fontes
   Last Update: 26.11.2020

   Objective: Apply the operator Re to the Passarino-Veltman functions
*)

TakeReal::"usage"="TakeReal[expr] applies the operator Re to the Passarino-Veltman functions. If a certain function is not implemented, TakeReal gives a warning.";

TakeReal=Function[exp,Module[{xx,yy,zz,ww,vv,replist},
PVList=GetPVList[exp];
CheckIfImplemented[PVList];
If[Implemented,  
replist=
{PaVe[0,{},{xx_}]-> Re[PaVe[0,{},{xx}]],
 A0[xx_]-> Re[A0[xx]], 
 PaVe[0,0,{},{xx_}]-> Re[PaVe[0,0,{},{xx}]],
 PaVe[0,0,{},{xx_},zz_,ww_]-> Re[PaVe[0,0,{},{xx},zz,ww]],
 PaVe[0,{xx_},{yy_,zz_}]-> Re[PaVe[0,{xx},{yy,zz}]],
 B0[xx_,yy_,zz_]-> Re[B0[xx,yy,zz]],
 DB0[xx_, yy_, zz_]-> Re[DB0[xx, yy, zz]],
 PaVe[1,{xx_},{yy_,zz_}]-> Re[PaVe[1,{xx},{yy,zz}]],
 PaVe[1,{xx_},{yy_,zz_},ww_,vv_]-> Re[PaVe[1,{xx},{yy,zz},ww,vv]],
 B1[xx_,yy_,zz_]-> Re[B1[xx,yy,zz]],
 B00[xx_,yy_,zz_]-> Re[B00[xx,yy,zz]],
 PaVe[0,0,{xx_},{yy_,zz_}]-> Re[PaVe[0,0,{xx},{yy,zz}]],
 PaVe[0,0,{xx_},{yy_,zz_},ww_,vv_]-> Re[PaVe[0,0,{xx},{yy,zz},ww,vv]],
 B11[xx_,yy_,zz_]-> Re[B11[xx,yy,zz]], 
 PaVe[1,1,{xx_},{yy_,zz_}]-> Re[PaVe[1,1,{xx},{yy,zz}]],
 PaVe[1,1,{xx_},{yy_,zz_},ww_,vv_]-> Re[PaVe[1,1,{xx},{yy,zz},ww,vv]],
 PaVe[0,0,1,{xx_},{yy_,zz_}]-> Re[PaVe[0,0,1,{xx},{yy,zz}]],
 PaVe[0,0,1,{xx_},{yy_,zz_},ww_,vv_]-> Re[PaVe[0,0,1,{xx},{yy,zz},ww,vv]],
 PaVe[1,1,1,{xx_},{yy_,zz_}]-> Re[PaVe[1,1,1,{xx},{yy,zz}]],
 PaVe[1,1,1,{xx_},{yy_,zz_},ww_,vv_]-> Re[PaVe[1,1,1,{xx},{yy,zz},ww,vv]],
 PaVe[0,0,{a_,b_,c_},{xx_,yy_,zz_}]-> Re[PaVe[0,0,{a,b,c},{xx,yy,zz}]],
 PaVe[0,0,{a_,b_,c_},{xx_,yy_,zz_},ww_,v_]-> Re[PaVe[0,0,{a,b,c},{xx,yy,zz},ww,v]],
 PaVe[0,0,1,{a_,b_,c_},{xx_,yy_,zz_}]-> Re[PaVe[0,0,1,{a,b,c},{xx,yy,zz}]],
 PaVe[0,0,1,{a_,b_,c_},{xx_,yy_,zz_},ww_,vv_]-> Re[PaVe[0,0,1,{a,b,c},{xx,yy,zz},ww,vv]],
 PaVe[0,0,2,{a_,b_,c_},{xx_,yy_,zz_}]-> Re[PaVe[0,0,2,{a,b,c},{xx,yy,zz}]],
 PaVe[0,0,2,{a_,b_,c_},{xx_,yy_,zz_},ww_,vv_]-> Re[PaVe[0,0,2,{a,b,c},{xx,yy,zz},ww,vv]],
 PaVe[0,0,0,0,{xx1_,xx2_,xx3_,xx4_,xx5_,xx6_},{yy1_,yy2_,yy3_,yy4_}]-> Re[PaVe[0,0,0,0,{xx1,xx2,xx3,xx4,xx5,xx6},{yy1,yy2,yy3,yy4}]],
 PaVe[0,0,0,0,{xx1_,xx2_,xx3_,xx4_,xx5_,xx6_},{yy1_,yy2_,yy3_,yy4_},ww_,vv_]-> Re[PaVe[0,0,0,0,{xx1,xx2,xx3,xx4,xx5,xx6},{yy1,yy2,yy3,yy4},ww,vv]]};
  exp //.replist ,
Print["Warning: There are PV functions of higher rank for which GetDiv is not yet implemented"]]
  ]] ;
(*---------------------------------------------------------------------*)









  
(*---------------------------------------------------------------------*)
(* OneLoopTID: OneLoop Function that uses TID *)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 03.02.2020

   Objective: Implements the TID decomposition method and it is called with the same conventions as OneLoop[k,amp].
   As OneLoop is old and has problems with spinors that probably will never be fixed in those cases it is better
   to use OneLoopTID as default.
*)

OneLoopTID::"usage"="OneLoopTID[k,amp] implements the TID decomposition method to do the One Loop integration of the amplitude amp for a loop with momentum k.
                     For compatibility, it is called with the same conventions as OneLoop[k,amp]. It should be looked as a replacement of OneLoop (which has some problems and limitations).
                     By default, it uses the option UsePaVeBasis -> True in TID, unless the option noPVauto is selected in Control.m.";

pvopt=0;
If[ToString[InputForm[Qoptions]] != "Qoptions", If[StringContainsQ[Qoptions, "noPVauto"],pvopt=1]];

OneLoopTID = Function[{k, amp},
If[pvopt==0,
TID[amp, k, UsePaVeBasis -> True, ToPaVe -> True],
TID[amp, k, UsePaVeBasis -> True, ToPaVe -> True, PaVeAutoReduce -> False]]
];

(*---------------------------------------------------------------------*)


(*---------------------------------------------------------------------*)  
(* Definition of Dabcd with the conventions of LoopTools *)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: In FeynCalc, the OneLoop function does not allow to have four momenta in the Numerator.
   This function defines the tensor Dabcd with the conventions of LoopTools for the inplementaion of OneLoop4k that
   does integrals of boxes with 4 momenta in the numerator. Warning: only works for 4 denominators (boxes).
   For other cases use OneLoopTID.
*)

Dabcd::"usage"="Dabcd[\[Alpha],\[Beta],\[Mu],\[Nu],L1,L2] implements the tensor decomposition for integrals with four denominators and four momenta in the numerator. It uses the LoopTools conventions for the Passarino Veltman integrals. \[Alpha],\[Beta],\[Mu] and \[Nu] are Lorentz Indices, L1={SPD[r1,r1],SPD[r1-r2,r1-r2],SPD[r2-r3,r2-r3],SPD[r3,r3],SPD[r2,r2],SPD[r1-r3,r1-r3]} the list of momenta invariants, and L2={m0^2,m1^2,m2^2,m3^2} the list of masses squared.";
  
LL1aux={SPD[r1,r1],SPD[r1-r2,r1-r2],SPD[r2-r3,r2-r3],SPD[r3,r3],SPD[r2,r2],SPD[r1-r3,r1-r3]}

LL1=Calc[LL1aux]

LL2={m0^2,m1^2,m2^2,m3^2}

ri=Function[a,{FVD[r1,a],FVD[r2,a],FVD[r3,a]}]
pvijk=Function[{i,j,k},PaVe[i,j,k,LL1,LL2]]
pvijkl=Function[{i,j,k,l},PaVe[i,j,k,l,LL1,LL2]]

Dabcd=Function[{a,b,c,d,LL1,LL2}, Term1= (MTD[a,b] MTD[c,d] + MTD[a,c] MTD[b,d] +MTD[a,d] MTD[b,c]) pvijkl[0,0,0,0]; Term2=Sum[(MTD[a,b] ri[c][[i]] ri[d][[j]]+ MTD[b,c] ri[a][[i]] ri[d][[j]]+ MTD[a,c] ri[b][[i]] ri[d][[j]] + MTD[a,d] ri[b][[i]] ri[c][[j]] +  MTD[b,d] ri[a][[i]] ri[c][[j]] + MTD[c,d] ri[a][[i]] ri[b][[j]])  pvijkl[0,0,i,j],{i,1,3},{j,1,3}]; Term3=Sum[ri[a][[i]] ri[b][[j]] ri[c][[k]] ri[d][[l]] pvijkl[i,j,k,l],{i,1,3},{j,1,3},{k,1,3},{l,1,3}];Term1+Term2+Term3];
(*---------------------------------------------------------------------*)

  
(*---------------------------------------------------------------------*)				 
(* GetPars; Get paramenter r1,r2,r3,m0,m1,m2,m3 for the Loop integral with LoopTools conventions *) 
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Obtain the loop paramenters  r1,r2,r3,m0,m1,m2,m3 neeed for the inplementaion of OneLoop4k
   Warning: Only Implemented for four denominators. For other cases use OneLoopTID.

   Internal Parameters: aux1,aux2,aux3,aux4,aux5,aux6,aux7,aux8,qq1,qq2,qq3,qq4,qqq1,qqq2,qqq3,qqq4,mmm0,mmm1,mmm2,mmm3,Den1,Den2,Den3,Den4,Den1Comma,Den2Comma,Den3Comma,Den4Comma

*)

GetPars::"usage"="GetPars[k,xamp,verbose] obtains the loop paramenters  r1,r2,r3,m0,m1,m2,m3 neeed for the inplementaion of OneLoop4k. Warning: Only Implemented for four denominators. For other cases use OneLoopTID. The default is verbose = False. It returns Error=True if not called with 4 denominators.";

GetPars=Function[{k,xamp,verbose},Module[{aux1,aux2,aux3,aux4,aux5,aux6,aux7,aux8,qq1,qq2,qq3,qq4,qqq1,qqq2,qqq3,qqq4,mmm0,mmm1,mmm2,mmm3,Den1,Den2,Den3,Den4,Den1Comma,Den2Comma,Den3Comma,Den4Comma},
aux1=InputForm[Calc[xamp]//FCE//Simplify];			       
aux5=GetDenominator[aux1];
If[Length[aux5]!=4,
Error="True",
Error="False";
aux6=aux5//FCI;
aux7=ToString[aux6];
aux8 = StringPosition[aux7, "PropagatorDenominator["];
len=StringLength[aux7];

Den1=StringTake[aux7, {aux8[[1]][[2]] + 1, aux8[[2]][[1]] - 4}];
Den2=StringTake[aux7, {aux8[[2]][[2]] + 1, aux8[[3]][[1]] - 4}];
Den3=StringTake[aux7, {aux8[[3]][[2]] + 1, aux8[[4]][[1]] - 4}];
Den4=StringTake[aux7, {aux8[[4]][[2]] + 1, len - 2}];

Den1Comma=StringPosition[Den1, ","];
Den2Comma=StringPosition[Den2, ","];
Den3Comma=StringPosition[Den3, ","];
Den4Comma=StringPosition[Den4, ","];
  
qqq1=ToExpression[StringTake[Den1,{1, Den1Comma[[Length[Den1Comma]]][[1]]-1}]];
qqq2=ToExpression[StringTake[Den2,{1, Den2Comma[[Length[Den2Comma]]][[1]]-1}]];
qqq3=ToExpression[StringTake[Den3,{1, Den3Comma[[Length[Den3Comma]]][[1]]-1}]];
qqq4=ToExpression[StringTake[Den4,{1, Den4Comma[[Length[Den4Comma]]][[1]]-1}]];

mmm0 = ToExpression[StringTake[Den1, {Den1Comma[[Length[Den1Comma]]][[1]] + 1, StringLength[Den1]}]];
mmm1 = ToExpression[StringTake[Den2, {Den2Comma[[Length[Den2Comma]]][[1]] + 1, StringLength[Den2]}]];
mmm2 = ToExpression[StringTake[Den3, {Den3Comma[[Length[Den3Comma]]][[1]] + 1, StringLength[Den3]}]];
mmm3 = ToExpression[StringTake[Den4, {Den4Comma[[Length[Den4Comma]]][[1]] + 1, StringLength[Den4]}]];
       
If[(ToString[(qqq1-Momentum[k,D])]  == "0")|| (ToString[(qqq1+Momentum[k,D])]  == "0"),
   qq1=qqq1;
   qq2=qqq2;
   qq3=qqq3;
   qq4=qqq4;
   mm0=mmm0;
   mm1=mmm1;
   mm2=mmm2;
   mm3=mmm3;
   ];

If[(ToString[(qqq2-Momentum[k,D])]  == "0")|| (ToString[(qqq2+Momentum[k,D])]  == "0"),
   qq1=qqq2;
   qq2=qqq1;
   qq3=qqq3;
   qq4=qqq4;
   mm0=mmm1;
   mm1=mmm0;
   mm2=mmm2;
   mm3=mmm3;
   ];

If[(ToString[(qqq3-Momentum[k,D])]  == "0")|| (ToString[(qqq3+Momentum[k,D])]  == "0"),
   qq1=qqq3;
   qq2=qqq1;
   qq3=qqq2;
   qq4=qqq4;
   mm0=mmm2;
   mm1=mmm0;
   mm2=mmm1;
   mm3=mmm3;
   ];

If[(ToString[(qqq4-Momentum[k,D])]  == "0")|| (ToString[(qqq4+Momentum[k,D])]  == "0"),
   qq1=qqq4;
   qq2=qqq1;
   qq3=qqq2;
   qq4=qqq3;
   mm0=mmm3;
   mm1=mmm0;
   mm2=mmm1;
   mm3=mmm2;
   ];
	       
If[Coefficient[qq2-qq1,Momentum[k,D]]!=0,qq2=-qq2];
If[Coefficient[qq3-qq1,Momentum[k,D]]!=0,qq3=-qq3];
If[Coefficient[qq4-qq1,Momentum[k,D]]!=0,qq4=-qq4];	       	       
    
rr1=qq2-qq1;
rr2=qq3-qq1;
rr3=qq4-qq1;	       
If[verbose,Print["r1=",rr1,", r2=",rr2,", r3=",rr3,", m0=",mm0,", m1=",mm1,", m2=",mm2,", m3=",mm3]]      
]]]
(*---------------------------------------------------------------------*) 

  
(*---------------------------------------------------------------------*) 
(* IndividualFVkD: Transform Numerator into individual momenta in Dimension D*)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 29.02.2020

   Objective: Transform Numerator into individual momenta in Dimension D
   Notes: 
   1) Present index= i60
   2) Correct up to k^6
   3) Correct up to (\gamma . k)^3 in one fermion line		      
   4) Correct up to  two (\gamma . k) in two fermion lines
   Note: This Function is needed for a different implementation of OneLoop, MyOneLoop to avoid the
   problems on the OneLoop standard function. Probably will be discontinued in the future as
   OneLoopTID already does that.
*)

IndividualFVkD::"usage"="IndividualFVkD[k,amp] transforms the numerator of the amplitude amp into explicit individual loop momenta k. For instance SPD[p,k] will be FVD[q,\[Alpha]] FVD[k,\[Alpha]], SPD[k,k] transforms into FVD[k,\[Alpha]] FVD[k,\[Alpha]] MTD[\[Alpha],\[Beta]] and so on. This is useful for the implementation of the functions OneLoopMod and MyOneLoopMod. Only implemented up to k^6 and (GAD[\[Alpha]] FVD[k,\[Alpha]])^3.";

IndividualFVkD=Function[{k,exp}, Module[{expAux,expAux0,expAux1,expAux2,expAux3,expAux4,expAux5,expAux6,expAux7,expAux8,expAux9,expAux10,expAux11,expAux12,expAux13,expAux14,expAux15,expAux16,MatAux1,MatAux2},

expAux=exp//FCI//Expand;

expAux0a=expAux/. Pair[Momentum[k,D], Momentum[k,D]]^4 ->MTD[i54, i55] Pair[LorentzIndex[i54,D], Momentum[k,D]] Pair[LorentzIndex[i55,D],Momentum[k,D]] Pair[Momentum[k,D], Momentum[k,D]]^3;

expAux0b=expAux0a/. Pair[Momentum[k,D], Momentum[k,D]]^3 ->MTD[i1, i2] Pair[LorentzIndex[i1,D], Momentum[k,D]] Pair[LorentzIndex[i2,D],Momentum[k,D]] Pair[Momentum[k,D], Momentum[k,D]]^2;

expAux1=expAux0b/. Pair[Momentum[k,D], Momentum[k,D]]^2 -> 
  MTD[i3, i4] Pair[LorentzIndex[i3,D], Momentum[k,D]] Pair[LorentzIndex[i4,D],
 Momentum[k,D]] Pair[Momentum[k,D], Momentum[k,D]];
					
expAux2 = expAux1 /. Pair[Momentum[k,D], Momentum[k,D]] -> MTD[i5, i6] Pair[LorentzIndex[i5,D], Momentum[k,D]] Pair[LorentzIndex[i6,D], Momentum[k,D]];
					
expAux3a = expAux2 /. Pair[Momentum[k,D], Momentum[q_,D]]^4 ->Pair[LorentzIndex[i46,D], Momentum[k,D]] Pair[LorentzIndex[i46,D], Momentum[q,D]] Pair[LorentzIndex[i47,D], Momentum[k,D]] Pair[LorentzIndex[i47,D],  Momentum[q,D]] Pair[LorentzIndex[i48,D], Momentum[k,D]] Pair[LorentzIndex[i48,D],  Momentum[q,D]] Pair[LorentzIndex[i49,D], Momentum[k,D]] Pair[LorentzIndex[i49,D],  Momentum[q,D]];

expAux3b = expAux3a /. Pair[Momentum[k,D], Momentum[p_,D]]^2 Pair[Momentum[k,D], Momentum[q_,D]]^2 ->Pair[LorentzIndex[i50,D], Momentum[k,D]] Pair[LorentzIndex[i50,D], Momentum[q,D]] Pair[LorentzIndex[i51,D], Momentum[k,D]] Pair[LorentzIndex[i51,D],  Momentum[q,D]] Pair[LorentzIndex[i52,D], Momentum[k,D]] Pair[LorentzIndex[i52,D],  Momentum[p,D]] Pair[LorentzIndex[i53,D], Momentum[k,D]] Pair[LorentzIndex[i53,D],  Momentum[p,D]];
			
expAux3c = expAux3b /. Pair[Momentum[k,D], Momentum[q_,D]]^3 ->Pair[LorentzIndex[i43,D], Momentum[k,D]] Pair[LorentzIndex[i43,D], Momentum[q,D]] Pair[LorentzIndex[i44,D], Momentum[k,D]] Pair[LorentzIndex[i44,D],  Momentum[q,D]] Pair[LorentzIndex[i45,D], Momentum[k,D]] Pair[LorentzIndex[i45,D],  Momentum[q,D]];

expAux3d = expAux3c /. Pair[Momentum[k,D], Momentum[q_,D]]^2 ->Pair[LorentzIndex[i7,D], Momentum[k,D]] Pair[LorentzIndex[i7,D], Momentum[q,D]] Pair[LorentzIndex[i8,D], Momentum[k,D]] Pair[LorentzIndex[i8,D],  Momentum[q,D]];

expAux3e = expAux3d /. Pair[Momentum[k,D], Momentum[q_,D]] Pair[Momentum[k,D], Momentum[p_,D]] ->Pair[LorentzIndex[i41,D], Momentum[k,D]] Pair[LorentzIndex[i41,D], Momentum[q,D]] Pair[LorentzIndex[i42,D], Momentum[k,D]] Pair[LorentzIndex[i42,D],  Momentum[p,D]];
					
expAux4 = expAux3e /. Pair[Momentum[k,D], Momentum[q_,D]]-> Pair[LorentzIndex[i9,D], Momentum[k,D]] Pair[LorentzIndex[i9,D], Momentum[q,D]];

expAux5=expAux4 /.   MatAux1_ . DiracGamma[Momentum[k,D],D] .	DiracGamma[Momentum[k,D],D] . DiracGamma[Momentum[k,D],D] . MatAux2_ ->   MatAux1 . DiracGamma[LorentzIndex[i10,D],D] .	DiracGamma[LorentzIndex[i11,D],D] . DiracGamma[LorentzIndex[i12,D],D] . MatAux2 Pair[LorentzIndex[i10,D], Momentum[k,D]] Pair[LorentzIndex[i11,D], Momentum[k,D]] Pair[LorentzIndex[i12,D], Momentum[k,D]];

expAux6=expAux5 /.    DiracGamma[Momentum[k,D],D] . DiracGamma[Momentum[k,D],D] . DiracGamma[Momentum[k,D],D] . MatAux2_ ->   DiracGamma[LorentzIndex[i13,D],D] . DiracGamma[LorentzIndex[i14,D],D] . DiracGamma[LorentzIndex[i15,D],D] . MatAux2 Pair[LorentzIndex[i13,D], Momentum[k,D]] Pair[LorentzIndex[i14,D], Momentum[k,D]] Pair[LorentzIndex[i15,D], Momentum[k,D]];					

expAux7=expAux6 /.  MatAux1_ . DiracGamma[Momentum[k,D],D] . DiracGamma[Momentum[k,D],D] . DiracGamma[Momentum[k,D],D]  ->  MatAux1.  DiracGamma[LorentzIndex[i16,D],D] . DiracGamma[LorentzIndex[i17,D],D] . DiracGamma[LorentzIndex[i18,D],D]  Pair[LorentzIndex[i16,D], Momentum[k,D]] Pair[LorentzIndex[i17,D], Momentum[k,D]] Pair[LorentzIndex[i18,D], Momentum[k,D]];					
					
expAux8=expAux7 /.   DiracGamma[Momentum[k,D],D] . DiracGamma[Momentum[k,D],D] . DiracGamma[Momentum[k,D],D]  ->  DiracGamma[LorentzIndex[i19,D],D] .	DiracGamma[LorentzIndex[i20,D],D] . DiracGamma[LorentzIndex[i21,D],D]  Pair[LorentzIndex[i19,D], Momentum[k,D]] Pair[LorentzIndex[i20,D], Momentum[k,D]] Pair[LorentzIndex[i21,D], Momentum[k,D]];					

expAux9=expAux8 /.   MatAux1_ . DiracGamma[Momentum[k,D],D] . DiracGamma[Momentum[k,D],D] . MatAux2_ ->   MatAux1 . DiracGamma[LorentzIndex[i21,D],D] .	DiracGamma[LorentzIndex[i22,D],D]  . MatAux2 Pair[LorentzIndex[i21,D], Momentum[k,D]] Pair[LorentzIndex[i22,D], Momentum[k,D]] ;
							
expAux10=expAux9 /.   MatAux1_ . DiracGamma[Momentum[k,D],D] . DiracGamma[Momentum[k,D],D] ->   MatAux1 . DiracGamma[LorentzIndex[i23,D],D] .	DiracGamma[LorentzIndex[i24,D],D]   Pair[LorentzIndex[i23,D], Momentum[k,D]] Pair[LorentzIndex[i24,D], Momentum[k,D]] ;
							
expAux11=expAux10 /.    DiracGamma[Momentum[k,D],D] . DiracGamma[Momentum[k,D],D] . MatAux2_ ->    DiracGamma[LorentzIndex[i25,D],D] . DiracGamma[LorentzIndex[i26,D],D]  . MatAux2 Pair[LorentzIndex[i25,D], Momentum[k,D]] Pair[LorentzIndex[i26,D], Momentum[k,D]] ;
							
expAux12=expAux11 /.   DiracGamma[Momentum[k,D],D] . DiracGamma[Momentum[k,D],D]  ->   DiracGamma[LorentzIndex[i27,D],D] . DiracGamma[LorentzIndex[i28,D],D]  Pair[LorentzIndex[i27,D], Momentum[k,D]] Pair[LorentzIndex[i28,D], Momentum[k,D]] ;

expAux12a=expAux12 /. MatAux1_ . DiracGamma[Momentum[k,D],D] . MatAux2_  MatAux3_ . DiracGamma[Momentum[k,D],D] . MatAux4_-> MatAux1 . DiracGamma[LorentzIndex[i28,D],D] . MatAux2 MatAux3 . DiracGamma[LorentzIndex[i60,D],D] . MatAux4  Pair[LorentzIndex[i28,D], Momentum[k,D]] Pair[LorentzIndex[i60,D], Momentum[k,D]];
		
expAux13=expAux12a /. MatAux1_ . DiracGamma[Momentum[k,D],D] . MatAux2_-> MatAux1 . DiracGamma[LorentzIndex[i28,D],D] . MatAux2  Pair[LorentzIndex[i28,D], Momentum[k,D]];

expAux14=expAux13 /. MatAux1_ . DiracGamma[Momentum[k,D],D] -> MatAux1 . DiracGamma[LorentzIndex[i29,D],D]  Pair[LorentzIndex[i29,D], Momentum[k,D]];

expAux15=expAux14 /.  DiracGamma[Momentum[k,D],D] . MatAux2_->  DiracGamma[LorentzIndex[i30,D],D] . MatAux2  Pair[LorentzIndex[i30,D], Momentum[k,D]];

expAux16=expAux15 /.  DiracGamma[Momentum[k,D],D] ->  DiracGamma[LorentzIndex[i31,D],D]  Pair[LorentzIndex[i31,D], Momentum[k,D]];
				
(* 
Next four entries are because of Levi-Civita Eps. Notice that it is in D=4. 
Hence we had to modify the derD definition for this case.
This only works when there is only one Momentum[k] in the Eps 
20.09.2018 jcr
*)
  
expAux17=expAux16 /. Eps[Momentum[k],li1_,li2_,li3_]-> Eps[LorentzIndex[i56],li1,li2,li3]  Pair[LorentzIndex[i56],Momentum[k]];

expAux18=expAux17 /. Eps[li1_,Momentum[k],li2_,li3_]-> Eps[li1,LorentzIndex[i57],li2,li3]  Pair[LorentzIndex[i57],Momentum[k]];

expAux19=expAux18 /. Eps[li1_,li2_,Momentum[k],li3_]-> Eps[li1,li2,LorentzIndex[i58],li3]  Pair[LorentzIndex[i58],Momentum[k]];

expAux20=expAux19 /. Eps[li1_,li2_,li3_,Momentum[k]]-> Eps[li1,li2,li3,LorentzIndex[i59]]  Pair[LorentzIndex[i59],Momentum[k]];  expAux20]];
(*---------------------------------------------------------------------*) 	

  
(*---------------------------------------------------------------------*) 
(* Definitions of derivatives with respect to 4-momenta in D dimensions*)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Defines the derivatives of the expression with respect to 4-momenta in Dimension D.
   Notes:
   1) Modified for epsilon terms in 01.08.2019
   2) This Function is needed for a different implementation of OneLoop, MyOneLoop to avoid the
   problems on the OneLoop standard function. Probably will be discontinued in the future as
   OneLoopTID already does that.
*)
  
derD[Pair[LorentzIndex[i_,D], Momentum[k_,D]], 
      Pair[LorentzIndex[j_,D], Momentum[k_,D]]] := MTD[i, j]

derD[Pair[LorentzIndex[i_], Momentum[k_]], 
Pair[LorentzIndex[j_,D], Momentum[k_,D]]] := MT[i, j]

derD[a_  b_, Pair[LorentzIndex[i_,D], Momentum[k_,D]]] := 
derD[a, Pair[LorentzIndex[i,D], Momentum[k,D]]] b + 
a derD[b, Pair[LorentzIndex[i,D], Momentum[k,D]]]

derD[a_ + b_, Pair[LorentzIndex[i_,D], Momentum[k_,D]]] := 
derD[a, Pair[LorentzIndex[i,D], Momentum[k,D]]]  + 
derD[b, Pair[LorentzIndex[i,D], Momentum[k,D]]]

		 
derD[c_, Pair[LorentzIndex[i_,D], Momentum[k_,D]]] := 
0 /; FreeQ[c, Pair[LorentzIndex[i,D], Momentum[k,D]]]
(*---------------------------------------------------------------------*) 


(*---------------------------------------------------------------------*) 		 
(* IndividualFVk: Transform Numerator into individual momenta in Dimension D=4 *)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Transform Numerator into individual momenta in Dimension D=4
   Notes: 
   1) Present index= i59
   2) Correct up to k^6 
   3) Not completely checked in D=4, but this not important as in the code is used the Dimension D version
   4) This Function is needed for a different implementation of OneLoop, MyOneLoop to avoid the
   problems on the OneLoop standard function. Probably will be discontinued in the future as
   OneLoopTID already does that

*)

IndividualFVk::"usage"="IndividualFV[k,amp] performs the same as IndividualFVkD but for D=4.";

IndividualFVk=Function[{k,exp}, Module[{expAux,expAux0,expAux1,expAux2,expAux3,expAux4,expAux5,expAux6,expAux7,expAux8,expAux9,expAux10,expAux11,expAux12,expAux13,expAux14,expAux15,expAux16,MatAux1,MatAux2},

expAux=exp//FCI//Expand;
				       
expAux0a=expAux/. Pair[Momentum[k], Momentum[k]]^4 ->MT[i54, i55] Pair[LorentzIndex[i54], Momentum[k]] Pair[LorentzIndex[i55],Momentum[k]] Pair[Momentum[k], Momentum[k]]^3;

expAux0b=expAux0a/. Pair[Momentum[k], Momentum[k]]^3 ->MT[i1, i2] Pair[LorentzIndex[i1], Momentum[k]] Pair[LorentzIndex[i2],Momentum[k]] Pair[Momentum[k], Momentum[k]]^2;

expAux1=expAux0b/. Pair[Momentum[k], Momentum[k]]^2 -> 
  MT[i3, i4] Pair[LorentzIndex[i3], Momentum[k]] Pair[LorentzIndex[i4],
 Momentum[k]] Pair[Momentum[k], Momentum[k]];
					
expAux2 = expAux1 /. Pair[Momentum[k], Momentum[k]] -> MT[i5, i6] Pair[LorentzIndex[i5], Momentum[k]] Pair[LorentzIndex[i6], Momentum[k]];

expAux3a1 = expAux2 /. Pair[Momentum[k], Momentum[q_]]^6 ->Pair[LorentzIndex[i60], Momentum[k]] Pair[LorentzIndex[i60], Momentum[q]] Pair[LorentzIndex[i61], Momentum[k]] Pair[LorentzIndex[i61],  Momentum[q]] Pair[LorentzIndex[i62], Momentum[k]] Pair[LorentzIndex[i62],  Momentum[q]] Pair[LorentzIndex[i63], Momentum[k]] Pair[LorentzIndex[i63],  Momentum[q]] Pair[LorentzIndex[i64], Momentum[k]] Pair[LorentzIndex[i64],  Momentum[q]] Pair[LorentzIndex[i65], Momentum[k]] Pair[LorentzIndex[i65],  Momentum[q]];

expAux3a2 = expAux3a1 /. Pair[Momentum[k], Momentum[q_]]^3 Pair[Momentum[k], Momentum[p_]]^3 ->Pair[LorentzIndex[i71], Momentum[k]] Pair[LorentzIndex[i71], Momentum[q]] Pair[LorentzIndex[i72], Momentum[k]] Pair[LorentzIndex[i72],  Momentum[q]] Pair[LorentzIndex[i73], Momentum[k]] Pair[LorentzIndex[i73],  Momentum[q]] Pair[LorentzIndex[i74], Momentum[k]] Pair[LorentzIndex[i74],  Momentum[p]] Pair[LorentzIndex[i75], Momentum[k]] Pair[LorentzIndex[i75],  Momentum[p]] Pair[LorentzIndex[i76], Momentum[k]] Pair[LorentzIndex[i76],  Momentum[p]];
				       
expAux3a3 = expAux3a2 /. Pair[Momentum[k], Momentum[q_]]^5 ->Pair[LorentzIndex[i66], Momentum[k]] Pair[LorentzIndex[i66], Momentum[q]] Pair[LorentzIndex[i67], Momentum[k]] Pair[LorentzIndex[i67],  Momentum[q]] Pair[LorentzIndex[i68], Momentum[k]] Pair[LorentzIndex[i68],  Momentum[q]] Pair[LorentzIndex[i69], Momentum[k]] Pair[LorentzIndex[i69],  Momentum[q]] Pair[LorentzIndex[i70], Momentum[k]] Pair[LorentzIndex[i70],  Momentum[q]];
		       	       
expAux3a = expAux3a3 /. Pair[Momentum[k], Momentum[q_]]^4 ->Pair[LorentzIndex[i46], Momentum[k]] Pair[LorentzIndex[i46], Momentum[q]] Pair[LorentzIndex[i47], Momentum[k]] Pair[LorentzIndex[i47],  Momentum[q]] Pair[LorentzIndex[i48], Momentum[k]] Pair[LorentzIndex[i48],  Momentum[q]] Pair[LorentzIndex[i49], Momentum[k]] Pair[LorentzIndex[i49],  Momentum[q]];

expAux3b = expAux3a /. Pair[Momentum[k], Momentum[p_]]^2 Pair[Momentum[k], Momentum[q_]]^2 ->Pair[LorentzIndex[i50], Momentum[k]] Pair[LorentzIndex[i50], Momentum[q]] Pair[LorentzIndex[i51], Momentum[k]] Pair[LorentzIndex[i51],  Momentum[q]] Pair[LorentzIndex[i52], Momentum[k]] Pair[LorentzIndex[i52],  Momentum[p]] Pair[LorentzIndex[i53], Momentum[k]] Pair[LorentzIndex[i53],  Momentum[p]];
			
expAux3c = expAux3b /. Pair[Momentum[k], Momentum[q_]]^3 ->Pair[LorentzIndex[i43], Momentum[k]] Pair[LorentzIndex[i43], Momentum[q]] Pair[LorentzIndex[i44], Momentum[k]] Pair[LorentzIndex[i44],  Momentum[q]] Pair[LorentzIndex[i45], Momentum[k]] Pair[LorentzIndex[i45],  Momentum[q]];

expAux3d = expAux3c /. Pair[Momentum[k], Momentum[q_]]^2 ->Pair[LorentzIndex[i7], Momentum[k]] Pair[LorentzIndex[i7], Momentum[q]] Pair[LorentzIndex[i8], Momentum[k]] Pair[LorentzIndex[i8],  Momentum[q]];

expAux3e = expAux3d /. Pair[Momentum[k], Momentum[q_]] Pair[Momentum[k], Momentum[p_]] ->Pair[LorentzIndex[i41], Momentum[k]] Pair[LorentzIndex[i41], Momentum[q]] Pair[LorentzIndex[i42], Momentum[k]] Pair[LorentzIndex[i42],  Momentum[p]];
					
expAux4 = expAux3e /. Pair[Momentum[k], Momentum[q_]]-> Pair[LorentzIndex[i9], Momentum[k]] Pair[LorentzIndex[i9], Momentum[q]];

expAux5=expAux4 /.   MatAux1_ . DiracGamma[Momentum[k]] .	DiracGamma[Momentum[k]] . DiracGamma[Momentum[k]] . MatAux2_ ->   MatAux1 . DiracGamma[LorentzIndex[i10]] .	DiracGamma[LorentzIndex[i11]] . DiracGamma[LorentzIndex[i12]] . MatAux2 Pair[LorentzIndex[i10], Momentum[k]] Pair[LorentzIndex[i11], Momentum[k]] Pair[LorentzIndex[i12], Momentum[k]];

expAux6=expAux5 /.    DiracGamma[Momentum[k]] . DiracGamma[Momentum[k]] . DiracGamma[Momentum[k]] . MatAux2_ ->   DiracGamma[LorentzIndex[i13]] . DiracGamma[LorentzIndex[i14]] . DiracGamma[LorentzIndex[i15]] . MatAux2 Pair[LorentzIndex[i13], Momentum[k]] Pair[LorentzIndex[i14], Momentum[k]] Pair[LorentzIndex[i15], Momentum[k]];					

expAux7=expAux6 /.  MatAux1_ . DiracGamma[Momentum[k]] . DiracGamma[Momentum[k]] . DiracGamma[Momentum[k]]  ->  MatAux1.  DiracGamma[LorentzIndex[i16]] . DiracGamma[LorentzIndex[i17]] . DiracGamma[LorentzIndex[i18]]  Pair[LorentzIndex[i16], Momentum[k]] Pair[LorentzIndex[i17], Momentum[k]] Pair[LorentzIndex[i18], Momentum[k]];					
					
expAux8=expAux7 /.   DiracGamma[Momentum[k]] . DiracGamma[Momentum[k]] . DiracGamma[Momentum[k]]  ->  DiracGamma[LorentzIndex[i19]] .	DiracGamma[LorentzIndex[i20]] . DiracGamma[LorentzIndex[i21]]  Pair[LorentzIndex[i19], Momentum[k]] Pair[LorentzIndex[i20], Momentum[k]] Pair[LorentzIndex[i21], Momentum[k]];					

expAux9=expAux8 /.   MatAux1_ . DiracGamma[Momentum[k]] . DiracGamma[Momentum[k]] . MatAux2_ ->   MatAux1 . DiracGamma[LorentzIndex[i21]] .	DiracGamma[LorentzIndex[i22]]  . MatAux2 Pair[LorentzIndex[i21], Momentum[k]] Pair[LorentzIndex[i22], Momentum[k]] ;
							
expAux10=expAux9 /.   MatAux1_ . DiracGamma[Momentum[k]] . DiracGamma[Momentum[k]] ->   MatAux1 . DiracGamma[LorentzIndex[i23]] .	DiracGamma[LorentzIndex[i24]]   Pair[LorentzIndex[i23], Momentum[k]] Pair[LorentzIndex[i24], Momentum[k]] ;
							
expAux11=expAux10 /.    DiracGamma[Momentum[k]] . DiracGamma[Momentum[k]] . MatAux2_ ->    DiracGamma[LorentzIndex[i25]] . DiracGamma[LorentzIndex[i26]]  . MatAux2 Pair[LorentzIndex[i25], Momentum[k]] Pair[LorentzIndex[i26], Momentum[k]] ;
							
expAux12=expAux11 /.   DiracGamma[Momentum[k]] . DiracGamma[Momentum[k]]  ->   DiracGamma[LorentzIndex[i27]] . DiracGamma[LorentzIndex[i28]]  Pair[LorentzIndex[i27], Momentum[k]] Pair[LorentzIndex[i28], Momentum[k]] ;

expAux13=expAux12 /. MatAux1_ . DiracGamma[Momentum[k]] . MatAux2_-> MatAux1 . DiracGamma[LorentzIndex[i28]] . MatAux2  Pair[LorentzIndex[i28], Momentum[k]];

expAux14=expAux13 /. MatAux1_ . DiracGamma[Momentum[k]] -> MatAux1 . DiracGamma[LorentzIndex[i29]]  Pair[LorentzIndex[i29], Momentum[k]];

expAux15=expAux14 /.  DiracGamma[Momentum[k]] . MatAux2_->  DiracGamma[LorentzIndex[i30]] . MatAux2  Pair[LorentzIndex[i30], Momentum[k]];

expAux16=expAux15 /.  DiracGamma[Momentum[k]] ->  DiracGamma[LorentzIndex[i31]]  Pair[LorentzIndex[i31], Momentum[k]];

(* 
Next four entries are because of Levi-Civita Eps. Notice that it is in D=4. 
Hence we had to modify the derD definition for this case.
This only works when there is only one Momentum[k] in the Eps 
20.09.2018 jcr
*)
  
expAux17=expAux16 /. Eps[Momentum[k],li1_,li2_,li3_]-> Eps[LorentzIndex[i56],li1,li2,li3]  Pair[LorentzIndex[i56],Momentum[k]];

expAux18=expAux17 /. Eps[li1_,Momentum[k],li2_,li3_]-> Eps[li1,LorentzIndex[i57],li2,li3]  Pair[LorentzIndex[i57],Momentum[k]];

expAux19=expAux18 /. Eps[li1_,li2_,Momentum[k],li3_]-> Eps[li1,li2,LorentzIndex[i58],li3]  Pair[LorentzIndex[i58],Momentum[k]];

expAux20=expAux19 /. Eps[li1_,li2_,li3_,Momentum[k]]-> Eps[li1,li2,li3,LorentzIndex[i59]]  Pair[LorentzIndex[i59],Momentum[k]];  expAux20]];
(*---------------------------------------------------------------------*)                	
                 
	 
(*---------------------------------------------------------------------*)                
(* Definitions of derivatives with respect to 4-momenta in D=4*)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Defines the derivatives of the expression with respect to 4-momenta in D=4.
   
   Note: This Function is needed for a different implementation of OneLoop, MyOneLoop to avoid the
   problems on the OneLoop standard function. Probably will be discontinued in the future as
   OneLoopTID already does that.
*)
   
der[Pair[LorentzIndex[i_], Momentum[k_]], 
  Pair[LorentzIndex[j_], Momentum[k_]]] := MT[i, j]

der[a_  b_, Pair[LorentzIndex[i_], Momentum[k_]]] := 
 der[a, Pair[LorentzIndex[i], Momentum[k]]] b + 
  a der[b, Pair[LorentzIndex[i], Momentum[k]]]

der[a_ + b_, Pair[LorentzIndex[i_], Momentum[k_]]] := 
 der[a, Pair[LorentzIndex[i], Momentum[k]]]  + 
   der[b, Pair[LorentzIndex[i], Momentum[k]]]

der[(DiracGamma[LorentzIndex[i_]] Pair[LorentzIndex[j_], 
     Momentum[k_]]), Pair[LorentzIndex[l_], Momentum[k_]]] :=
DiracGamma[LorentzIndex[i]] MT[j,l]

der[ A_ . (DiracGamma[LorentzIndex[i_]] Pair[LorentzIndex[j_], 
     Momentum[k_]]), Pair[LorentzIndex[l_], Momentum[k_]]] :=
A . DiracGamma[LorentzIndex[i]] MT[j,l]

der[c_, Pair[LorentzIndex[i_], Momentum[k_]]] := 
 0 /; FreeQ[c, Pair[LorentzIndex[i], Momentum[k]]]
(*---------------------------------------------------------------------*)

		
(*---------------------------------------------------------------------*)
(* OneLoop4k: Function to calculate OneLoop Integrals with 4 momenta*)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Extends the OneLoop function of FC to the case of 
   4 momenta in the numerator.
   
   Internal variables: aux1,aux2,amp3k,amp4k,aux3,aux4,aux5,subPars

   Note: This Function is needed for a different implementation of OneLoop, MyOneLoop to avoid the
   problems on the OneLoop standard function. Probably will be discontinued in the future as
   OneLoopTID already does that.
*)

OneLoop4k::"usage"="OneLoop4k[k,amp] extends the OneLoop[k,amp] function of FC to the case of 4 momenta in the numerator and four denominators. To be discontinued being replaced by OneLoopTID[k,m]";

OneLoop4k=Function[{k,amp},Module[{aux1,aux2,amp3k,amp4k,aux3,aux4,aux5,subPars},
aux1=Calc[amp]//FCI;
aux2=aux1 /. Momentum[k, D] -> x Momentum[k, D];
amp4k=Coefficient[aux2, x, 4] /. x -> 1 // FCE;			  
amp3k=Calc[(aux1 - amp4k)]//Simplify;
GetPars[k,amp4k,False];
If[Error=="False",  
If[ToString[amp3k] != "0", Res3k=OneLoop[k,amp3k],Res3k=0;];
Num4k=GetNumerator[amp4k];
subPars={Momentum[r1,D] -> Momentum[rr1,D], Momentum[r2,D]->Momentum[rr2,D],Momentum[r3,D]->Momentum[rr3,D] ,m0->mm0,m1->mm1,m2->mm2,m3->mm3} ;
aux3=IndividualFVkD[k,Num4k] ;
aux4 = 
  derD[derD[
      derD[derD[aux3, Pair[LorentzIndex[j1, D], Momentum[k, D]]], 
      Pair[LorentzIndex[j2, D], Momentum[k, D]]], 
      Pair[LorentzIndex[j3, D], Momentum[k, D]]], 
      Pair[LorentzIndex[j4, D], Momentum[k, D]]]/4! // Expand;
aux5 = Calc[aux4 Dabcd[j1, j2, j3, j4, LL1, LL2]];
Res4kD=aux5 /. subPars;
Res3k + (I Pi^2) Res4kD
,Print["Warning: Tensor integrals of rank higher than 3 only implemented for 4 denominators. Use other method."]
]  
]
]
(*---------------------------------------------------------------------*)


(*---------------------------------------------------------------------*)
(* OneLoop4kMod: Function to calculate OneLoop Integrals with 4 momenta and integrates with OneLopMod *)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Calculate the One Loop integral for the full expression. Extends the OneLoop function of FC to the case 
              of 4 momenta in the numerator.

   Note: This Function is needed for a different implementation of OneLoop, MyOneLoop to avoid the
   problems on the OneLoop standard function. Probably will be discontinued in the future as
   OneLoopTID already does that.
*)

OneLoop4kMod::"usage"="OneLoop4kMod[k,amp] extends the OneLoop[k,amp] function of FC to the case of 4 momenta in the numerator and four denominators. To be discontinued being replaced by OneLoopTID[k,m]";

OneLoop4kMod=Function[{k,amp},Module[{aux1,aux2,amp3k,amp4k,aux3,aux4,aux5,Res3k,Res4kD,subPars},
aux1=Calc[amp]//FCI;
aux2=aux1 /. Momentum[k, D] -> x Momentum[k, D];
amp4k=Coefficient[aux2, x, 4] /. x -> 1 // FCE;			  
amp3k=Calc[(aux1 - amp4k)]//Simplify;
GetPars[k,amp4k,False];
If[Error=="False",
If[ToString[amp3k] != "0", Res3k=OneLoopMod[k,amp3k],Res3k=0;];
Num4k=GetNumerator[amp4k];
subPars={Momentum[r1,D] -> Momentum[rr1,D], Momentum[r2,D]->Momentum[rr2,D],Momentum[r3,D]->Momentum[rr3,D] ,m0->mm0,m1->mm1,m2->mm2,m3->mm3} ;
aux3=IndividualFVkD[k,Num4k] ;
aux4 = 
  derD[derD[
      derD[derD[aux3, Pair[LorentzIndex[j1, D], Momentum[k, D]]], 
      Pair[LorentzIndex[j2, D], Momentum[k, D]]], 
      Pair[LorentzIndex[j3, D], Momentum[k, D]]], 
      Pair[LorentzIndex[j4, D], Momentum[k, D]]]/4! // Expand;
aux5 = Calc[aux4 Dabcd[j1, j2, j3, j4, LL1, LL2]];
Res4kD=aux5 /. subPars;
Res3k + (I Pi^2) Res4kD				    
,Print["Warning: Tensor integrals of rank higher than 3 only implemented for 4 denominators. Use other method."]
]
]
]
(*---------------------------------------------------------------------*)

  
(*---------------------------------------------------------------------*)				 
(* MyOneLoop: Function that integrates OneLoop with OneLoop4k *)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Calculate the One Loop integral for the full expression. 
   Extends the OneLoop function of FC to the case  of 4 momenta 
   in the numerator.

   Note: This Function is needed for a different implementation of OneLoop, MyOneLoop to avoid the
   problems on the OneLoop standard function. Probably will be discontinued in the future as
   OneLoopTID already does that
*)

MyOneLoop::"usage"="MyOneLoop[k,amp] extends the OneLoop[k,amp] function of FC to the case of 4 momenta in the numerator (only for four denominators). Uses OneLoop4k[k,amp]. To be discontinued being replaced by OneLoopTID[k,m] that has no limitation.";


MyOneLoop=Function[{k,amp},Module[{aux1,aux2,amp4k,Loop4k,ResLoop},
Clear[x];				  
aux1=Calc[amp]//FCI;
aux2=aux1 /. Momentum[k, D] -> x Momentum[k, D];
amp4k=Coefficient[aux2, x, 4] /. x -> 1 // FCE;
If[ToString[amp4k] != "0",Loop4k=1,Loop4k=0];
If[Loop4k==1,ResLoop=OneLoop4k[k,amp];,ResLoop=OneLoop[k,amp]];
ResLoop
]
]
(*---------------------------------------------------------------------*)

  
(*---------------------------------------------------------------------*)
(* MyOneLoopMod: Function that integrates OneLoopMod with OneLoop4kMod *)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Calculate the One Loop integral for the full expression. 
              Uses OneLoopMod for the part with 3 momenta and
              OneLoop4kMod for the 4 momenta case.

   Note: This Function is needed for a different implementation of OneLoop, MyOneLoop to avoid the
   problems on the OneLoop standard function. Probably will be discontinued in the future as
   OneLoopTID already does that
*)

MyOneLoopMod::"usage"="MyOneLoopMod[k,amp] extends the OneLoop[k,amp] function of FC. Uses OneLoopMod[k,amp] for the part up to 3 momenta and OneLoop4kMod for the 4 momenta case. To be discontinued being replaced by OneLoopTID[k,m] that has no limitation.";
		 
MyOneLoopMod=Function[{k,amp},Module[{aux1,aux2,amp4k,ResLoop,Loop4k},
aux1=Calc[amp]//FCI;
If[ToString[aux1] == "0",ResLoop=0];
If[ToString[aux1] != "0",
        aux2=aux1 /. Momentum[k, D] -> x Momentum[k, D];
	amp8k=Coefficient[aux2, x, 8] /. x -> 1 // FCE;
	amp7k=Coefficient[aux2, x, 7] /. x -> 1 // FCE;
	amp6k=Coefficient[aux2, x, 6] /. x -> 1 // FCE;
	amp5k=Coefficient[aux2, x, 5] /. x -> 1 // FCE;
        amp4k=Coefficient[aux2, x, 4] /. x -> 1 // FCE;];
If[ToString[amp8k] != "0"||  ToString[amp7k] != "0"
   || ToString[amp6k] != "0" || ToString[amp5k] != "0",Print["Warning: Tensor integrals of rank higher than 3 only implemented for 4 denominators. Use other method."],   
   If[ToString[amp4k] != "0",Loop4k=1,Loop4k=0];
    If[Loop4k==1,ResLoop=OneLoop4kMod[k,amp];,ResLoop=OneLoopMod[k,amp]];
    ResLoop]
]
]
(*---------------------------------------------------------------------*)
  

(*---------------------------------------------------------------------*)
(* OneLoopMod: Function to calculate OneLoop Integrals up to 3 momenta.
   Method:
   1) Expand the expression in monomials. 
   2) Use the function OneLoopModMon for each monomial
   3) Sum everything 
*)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Calculate the One Loop integral for the full expression. 
              It is limited to 3 momenta because of the limitation
              in the FC function OneLoop that it uses.

   Note: This Function is needed for a different implementation of OneLoop, MyOneLoop to avoid the
   problems on the OneLoop standard function. Probably will be discontinued in the future as
   OneLoopTID already does that.
*)

OneLoopMod::"usage"="OneLoopMod[k,amp] calculates the one-loop integral for the full expression. It is limited to 3 momenta because of the limitation in the FC function OneLoop. Uses OneLoopModMon[k,amp]. To be discontinued being replaced by OneLoopTID[k,m] that has no limitation.";

OneLoopMod=Function[{k,amp},Module[{aux0,aux1,aux2},
  aux0=Expand[amp];
  If[Head[aux0]===Plus,
  aux1=Table[OneLoopModMon[k,aux0[[i]]],{i,1,Length[aux0]}];
  aux2=Sum[aux1[[i]],{i,1,Length[aux0]}];];
  If[Head[aux0]===Times,aux2=OneLoopModMon[k,aux0];];
  Res=aux2]]
(*---------------------------------------------------------------------*)      

  
(*---------------------------------------------------------------------*)
(* OneLoopModMon: Function to calculate OneLoop Integrals up to 3 momenta.
                  Might exist problems for expressions with both terms with 
                  and without epsilons it should be used inside OneLoopMod 
                  for each monomial.
*)
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Calculate the One Loop integral for each monomial of the 
   expression. It is limited to 3 momenta because of the limitation 
   in the FC function OneLoop that it uses.

   Note: This Function is needed for a different implementation of OneLoop, MyOneLoop to avoid the
   problems on the OneLoop standard function. Probably will be discontinued in the future as
   OneLoopTID already does that.

*)

OneLoopModMon::"usage"="OneLoopModMon[k,amp] calculate the one-loop integral for each monomial in the numerator of amp. Needed by MyOneLoopMod[k,amp]. To be discontinued being replaced by OneLoopTID[k,m] that has no limitation.";

OneLoopModMon=Function[{k,amp},Module[{test,aux0,aux1,aux2,aux3,aux4a,aux4b,aux5,aux6,aux7,aux8,aux9,aux10,aux11,subToD,Num0k,Num1k,Num2k,Num3k,Num4k,DenAmp,NumAmp,Res0kD,Res1kD,Res3kD,Res},
				   
subToD = {LorentzIndex[iLo_] -> LorentzIndex[iLo, D], 
	  Momentum[xmom_] -> Momentum[xmom, D]};

test=Calc[amp];

If[ToString[test]!="0",                                   
DenAmp=GetDenominator[amp];
NumAmp=GetNumerator[amp];				   
aux0=Calc[NumAmp]//FCI;
aux1=aux0 /. {Momentum[k] -> xId Momentum[k],Momentum[k, D] -> xId Momentum[k, D]};
aux2=Calc[aux1];				   
Num4k=Coefficient[aux2, xId, 4] /. xId -> 1 // FCI//Expand;  
Num3k=Coefficient[aux2, xId, 3] /. xId -> 1 // FCI//Expand;
Num2k=Coefficient[aux2, xId, 2] /. xId -> 1 // FCI//Expand;
Num1k=Coefficient[aux2, xId, 1] /. xId -> 1 // FCI//Expand;
Num0k=Coefficient[aux2, xId, 0] /. xId -> 1 // FCI//Expand;
, Num0k=0;Num1k=0;Num2k=0;Num3k=0;Num4k=0;];

Res0kD=0;
If[ToString[Num0k]!="0", 
Res0kD=(Num0k OneLoop[k,DenAmp]//FCI)/. subToD;];
   
Res1kD=0;
If[ToString[Num1k]!="0",		   
aux3=IndividualFVkD[k,Num1k] ;
aux4a = 
derD[aux3, Pair[LorentzIndex[j1, D], Momentum[k, D]]]/1! // Expand;
aux4b=(OneLoop[k,FVD[k,j1] DenAmp]//FCI)/.subToD;
aux5 = Calc[aux4a aux4b];
Res1kD=aux5;
];
   
Res2kD=0;
If[ToString[Num2k]!="0",
aux6=IndividualFVkD[k,Num2k] ;
aux7a = derD[
       derD[aux6, Pair[LorentzIndex[j1, D], Momentum[k, D]]],
  Pair[LorentzIndex[j2, D], Momentum[k, D]]]/2! // Expand;
aux7b = (OneLoop[k,FVD[k,j1] FVD[k,j2] DenAmp]//FCI)/. subToD;
aux8 = Calc[aux7a aux7b];
Res2kD=aux8;
];

Res3kD=0;
If[ToString[Num3k]!="0",
aux9=IndividualFVkD[k,Num3k] ;
aux10a = derD[derD[
  derD[aux9, Pair[LorentzIndex[j1, D], Momentum[k, D]]],
  Pair[LorentzIndex[j2, D], Momentum[k, D]]],
  Pair[LorentzIndex[j3, D], Momentum[k, D]]]/3! // Expand;
aux10b = (OneLoop[k,FVD[k,j1] FVD[k,j2] FVD[k,j3] DenAmp]//FCI)/.subToD;
aux11 = Calc[aux10a aux10b];   
Res3kD=aux11;
   ];		   
Res=Res0kD + Res1kD + Res2kD + Res3kD			    
]
]
(*---------------------------------------------------------------------*)

  
(*---------------------------------------------------------------------*)
(* GetDenominator: Get denominator of the Loop integral *) 
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Get the Denominator of the Feynman Integral. Has problems if there are both epsilon terms and terms without
              epsilons. Therefore when used with OneLoopMod one has to separate the integral in monomials.

   Note: This Function is needed for a different implementation of OneLoop, MyOneLoop to avoid the
   problems on the OneLoop standard function. Probably will be discontinued in the future as
   OneLoopTID already does that.

*)

GetDenominator::"usage"="GetDenominator[amp] gets the denominator of the Feynman amplitude amp. Needed by MyOneLoop[k,amp].";

GetDenominator=Function[{xamp},Module[{aux1,aux2,aux3,aux4,aux5,aux6,posi,posf,icount},
aux1=((Calc[xamp]//FeynAmpDenominatorCombine)//Simplify)//FCE;
aux2=InputForm[aux1];			       
aux3=ToString[aux2];
aux4=StringPosition[aux3, "FAD["];
aux5=StringPosition[aux3,"]"];
posi=aux4[[1]][[1]];
icount=0;
Do[If[aux5[[j]][[1]] > posi, icount = icount + 1; 
If[icount == 1, posf = aux5[[j]][[1]]]], {j, 1, Length[aux5]}];
aux6=StringTake[aux3, {posi,posf}];
ToExpression[aux6]				    
]];
(*---------------------------------------------------------------------*) 

  
(*---------------------------------------------------------------------*) 				      
(* GetNumerator: Get numerator of the Loop integral *) 
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Get the Numerator of the Feynman Integral. Has problems if there are both epsilon terms and terms without
              epsilons. Therefore when used with OneLoopMod one has to separate the integral in monomials.

   Note: This Function is needed for a different implementation of OneLoop, MyOneLoop to avoid the
   problems on the OneLoop standard function. Probably will be discontinued in the future as
   OneLoopTID already does that.
*)

GetNumerator::"usage"="GetNumerator[amp] gets the numerator of the Feynman amplitude amp. Needed by MyOneLoop[k,amp].";
  
GetNumerator=Function[{xamp},Module[{aux0,aux1,aux2,aux3,aux4,aux5,aux6,LS,posi,posf,case,ix},
aux0=((Calc[xamp]//FeynAmpDenominatorCombine)//Simplify)//FCE;
aux1=InputForm[aux0];			       
aux2=ToString[aux1];
LS=StringLength[aux2];				    
aux3=StringPosition[aux2, {"FAD[", "]"}];

ix = 1;
While[Length[aux3] - ix >= 0, 
  If[StringTake[aux2, {aux3[[ix]][[1]], aux3[[ix]][[2]]}] == "FAD[", 
   posi = aux3[[ix]][[1]]; posf = aux3[[ix + 1]][[1]]]; ix++];  
	    
If[posi == 1 && posf == LS,case=1];
If[posi == 1 && posf < LS,case=2];
If[posi > 1 && posf == LS,case=3];
If[posi > 1 && posf < LS,case=4];

If[case==1, aux6="1";];

If[case==2, aux6=StringTake[aux2, {posf+2,LS}]];

If[case==3, aux6=StringTake[aux2, {1, posi-2}]];
				    
If[case==4, aux4=StringTake[aux2, {1, posi-1}];
aux5=StringTake[aux2, {posf+1,LS}];
aux6=StringJoin[aux4," 1 ",aux5];];

ToExpression[aux6]				    
 ]];
(*---------------------------------------------------------------------*) 


(*---------------------------------------------------------------------*)               
(* TCALoopExp: Replace four-vectors (of loop momentum) with expressions from Jorge's TCA appendix *) 
(* Created by: Duarte Fontes
  Email: duartefontes@tecnico.ulisboa.pt 
  Last Update: 20.12.2019
  Notes:
  1) this function has 6 arguments: {exp, Denos, Powk, k1, P, C}, where:
        -> exp is the expression to be acted on,
        -> Denos is the number of denominators,
        -> Powk is the power of loop momenta in the numerator of the loop integral,
        -> k1 is the loop momentum,
        -> P and C are the P and C variables from Jorge's TCA appendix;
  2) I am not including the factor I/(16 Pi^2); it should be included by hand;
  3) I am already including the Gamma factors; for example, with 3 denominators, I am already including the Gamma[3]=2;
  4) the expressions are written for D-dimensional objects; hence, we have MTD[a,b], and not MT[a,b], for example.
*)

TCALoopExp::"usage"="TCALoopExp[exp, Denos, k, P, C] returns the divergent part of one-loop integrals in the notation of Appendix C of https://porthos.tecnico.ulisboa.pt/Public/textos/tca.pdf by Jorge C. Romao.";

TCALoopExp=Function[{exp, Denos, Powk, k1, P, C}, Module[{X0,G,EP,mu,nu,a,b,d,myrep},
EP=\[CapitalDelta]\[Epsilon];
(* One denominator *)
If[Denos==1,
G=1;
If[Powk==0, myrep = d_ -> d*G*C*(1 + EP - Log[C]),
If[Powk==1, myrep = FVD[k1,mu_] -> 0,
If[Powk==2, myrep = FVD[k1,mu_] FVD[k1,nu_] -> G*(1/8) C^2 MTD[mu,nu](3 + 2*EP - 2*Log[C])]]],
(* Two denominators *)
If[Denos==2,
G=1;
If[Powk==0, myrep = d_ -> d*G*(EP - Log[C]),
If[Powk==1, myrep = FVD[k1,mu_] -> G*(-EP + Log[C]) FVD[P,mu],
If[Powk==2, myrep = FVD[k1,mu_] FVD[k1,nu_] -> G*(1/2)*(C MTD[mu,nu] (1 + EP - Log[C]) + 2*(EP - Log[C]) FVD[P,mu] FVD[P,nu]),
If[Powk==3, myrep = FVD[k1,mu_] FVD[k1,nu_] FVD[k1,a_] -> G*(1/2) (-C MTD[mu,nu] (1 + EP - Log[C]) FVD[P,a] - C MTD[nu,a] * (1
                      + EP - Log[C]) FVD[P,mu] - C MTD[mu,a] (1 + EP - Log[C]) FVD[P,nu] - 2 FVD[P,a] FVD[P,mu] FVD[P,nu] (EP - Log[C]))]]]],
(* Three denominators *)
If[Denos==3,
G=2;
If[Powk==0, myrep = d_ -> d*G*(-1)/(2*C),
If[Powk==1, myrep = FVD[k1,mu_] -> G*FVD[P, mu]/(2*C),
If[Powk==2, myrep = FVD[k1,mu_] FVD[k1,nu_] -> G*1/(4*C)*(C*MTD[mu,nu] (EP - Log[C]) - 2*FVD[P,mu] FVD[P,nu]),
If[Powk==3, myrep = FVD[k1,mu_] FVD[k1,nu_] FVD[k1,a_] -> G*1/(4*C)*(C*MTD[mu,nu] (-EP + Log[C]) FVD[P,a] + C*MTD[nu,a] (-EP + Log[C]) FVD[P,mu]
                                                                                        + C*MTD[mu,a] (-EP + Log[C]) FVD[P,nu] + 2 FVD[P,a] FVD[P,mu] FVD[P,nu]),
If[Powk==4, myrep = FVD[k1,mu_] FVD[k1,nu_] FVD[k1,a_] FVD[k1,b_] -> G*1/(8*C)*(C^2 (1 + EP - Log[C]) (MTD[mu,a] MTD[nu,b] + MTD[mu,b] MTD[nu,a]
                                                                                                                + MTD[a,b] MTD[mu,nu])
                                                        + 2*C (EP - Log[C])*(MTD[mu,nu] FVD[P,a] FVD[P,b] + MTD[nu,b] FVD[P,a] FVD[P,mu] + MTD[nu,a] FVD[P,b] FVD[P,mu]
                                                                                               + MTD[mu,a] FVD[P,b] FVD[P,nu] + MTD[mu,b] FVD[P,a] FVD[P,nu] + MTD[a,b] FVD[P,mu] FVD[P,nu])
                                                        - 4 FVD[P,a] FVD[P,b] FVD[P,mu] FVD[P,nu])]]]]],
(* Four denominators *)
If[Denos==4,
G=6;
If[Powk==0, myrep = d_ -> d*G*1/(6*C^2),
If[Powk==1, myrep = FVD[k1,mu_] -> G*(-1)/(6*C^2) FVD[P,mu],
If[Powk==2, myrep = FVD[k1,mu_] FVD[k1,nu_] -> G*(-1)/(12*C^2) (C MTD[mu,nu] - 2 FVD[P,mu] FVD[P,nu]),
If[Powk==3, myrep = FVD[k1,mu_] FVD[k1,nu_] FVD[k1,a_] -> G*1/(12*C^2) (C*(MTD[mu,nu] FVD[P,a] + MTD[nu,a] FVD[P,mu] + MTD[mu,a] FVD[P,nu])
                                                                                      - 2 FVD[P,a] FVD[P,mu] FVD[P,nu]),
If[Powk==4, myrep = FVD[k1,mu_] FVD[k1,nu_] FVD[k1,a_] FVD[k1,b_] -> G*1/(24*C^2) (C^2 (EP - Log[C]) (MTD[mu,a] MTD[nu,b] + MTD[mu,b] MTD[nu,a]
                                                                                                                + MTD[a,b] MTD[mu,nu])
                                                  -2*C*(MTD[mu,nu] FVD[P,a] FVD[P,b] + MTD[nu,b] FVD[P,a] FVD[P,mu] + MTD[nu,a] FVD[P,b] FVD[P,mu]
                                                                                            + MTD[mu,a] FVD[P,b] FVD[P,nu] + MTD[mu,b] FVD[P,a] FVD[P,nu] + MTD[a,b] FVD[P,mu] FVD[P,nu])
                                                  + 4 FVD[P,a] FVD[P,b] FVD[P,mu] FVD[P,nu])]]]]]]]]];
X0=exp/.myrep]];
(*---------------------------------------------------------------------*) 


(*---------------------------------------------------------------------*) 
(* Change expression to D Dimensions *) 
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Changes all the Lorentz quantitues to Dimension D
*)

ChangeToD::"usage"="ChangeToD[expr] changes all the Lorentz quantities (vectors, matrices, spinors) to Dimension D.";


ChangeToD=Function[{exp},Module[{aux1,aux2,aux3,aux4,subToD,pp,qq,rr,pp1,pp2,iL1,iL2,iL3,iL4,zz1, zz2, zz3, zz4, zz5, zz6, zz7, zz8, zz9, zz10, zz11, zz12, zz13, zz14, zz15, zz16, zz17, zz18, zz19,  zz20, zz21},
aux1=exp//FCE;
subToD ={FV[pp_, iL1_] -> FVD[pp, iL1], SP[qq_, rr_] -> SPD[qq, rr], GS[pp1_,pp2_] -> GSD[pp1,pp2], MT[iL2_, iL3_] -> MTD[iL2, iL3]};
aux2=(aux1 /. subToD) // FCI;
aux3=aux2/.{DiracGamma[Momentum[pp1_]] -> DiracGamma[Momentum[pp1, D], D],
            DiracGamma[LorentzIndex[iL4_]] -> DiracGamma[LorentzIndex[iL4,D],D]};  
aux4=(aux3 // FCE) /. {
FAD[zz21_] -> FAD[zz21, Dimension -> D],
FAD[{zz1_, zz2_}] -> FAD[{zz1, zz2}, Dimension -> D], 
FAD[{zz3_, zz4_}, {zz5_, zz6_}] -> FAD[{zz3, zz4}, {zz5, zz6}, Dimension -> D],
FAD[{zz7_, zz8_}, {zz9_, zz10_}, {zz11_, zz12_}] -> FAD[{zz7, zz8}, {zz9, zz10}, {zz11, zz12}, Dimension -> D],
FAD[{zz13_, zz14_}, {zz15_, zz16_}, {zz17_, zz18_}, {zz19_, zz20_}] -> FAD[{zz13, zz14}, {zz15, zz16}, {zz17, zz18}, {zz19, zz20}, Dimension -> D]}]];
(*---------------------------------------------------------------------*) 


(*---------------------------------------------------------------------*)   
(* Change expression to 4 Dimensions *) 
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Changes all the Lorentz quantitues to D=4
*)

ChangeTo4::"usage"="ChangeTo4[expr] changes all the Lorentz quantities (vectors, matrices, spinors) to Dimension D=4.";

ChangeTo4 = Function[{exp}, Module[{aux1, aux2, aux3, zz1, zz2, zz3, zz4, zz5, zz6, zz7, zz8, zz9, zz10, zz11, zz12, zz13, zz14, zz15, zz16, zz17, zz18, zz19,  zz20, zz21},
aux1 = ChangeToD[exp] // FCI;
aux2 = (aux1 /. D -> 4) // FCE;
aux3 =  aux2 /. {
FAD[zz21_, Dimension -> 4] -> FAD[zz21],
FAD[{zz1_, zz2_}, Dimension -> 4] -> FAD[{zz1, zz2}], 
FAD[{zz3_, zz4_}, {zz5_, zz6_}, Dimension -> 4] -> FAD[{zz3, zz4}, {zz5, zz6}],
FAD[{zz7_, zz8_}, {zz9_, zz10_}, {zz11_, zz12_}, Dimension -> 4] -> FAD[{zz7, zz8}, {zz9, zz10}, {zz11, zz12}],
FAD[{zz13_, zz14_}, {zz15_, zz16_}, {zz17_, zz18_}, {zz19_, zz20_}, Dimension -> 4] -> FAD[{zz13, zz14}, {zz15, zz16}, {zz17, zz18}, {zz19, zz20}]}]];
(*---------------------------------------------------------------------*) 


(*---------------------------------------------------------------------*)   
(* Functions to handle Traces with Gamma5*) 
(* Created by: Jorge C. Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 01.08.2019

   Objective: Given a fermion line this set of functions separate the part with
   Gamma5 to do that trace in D=4.
*)

FermionLineNoG5::"usage"="FermionLineNoG5[fline] separates from a fermion line the part with no \[Gamma]5.";

FermionLineNoG5 = 
 Function[line,Module[{aux1,aux2,yy},
    aux1 = DiracSimplify[line] // FCE; 
   aux2 = DiracSimplify[aux1 /. GA[5] -> yy GA[5]]; 
   Coefficient[aux2, yy, 0]]];

FermionLineG5::"usage"="FermionLineG5[fline] separates from a fermion line the part with \[Gamma]5.";

FermionLineG5 = 
  Function[line,Module[{aux1,aux2,yy},
  aux1 = DiracSimplify[line] // FCE; 
   aux2 = DiracSimplify[aux1 /. GA[5] -> yy GA[5]]; 
   Coefficient[aux2, yy, 1]]];

TrG5::"usage"="TrG5[fline] calculates the trace of fline separating the part with \[Gamma]5 that is calculated in D=4. Uses FermionLineNoG5 and FermionLineG5.";

TrG5=Function[exp,Module[{aux,auxNoG5,auxG5,fcng5},
If[FCVersion>=9.3,
Tr[exp],
auxNoG5=Tr[FermionLineNoG5[exp]];
auxG5=Tr[ChangeTo4[FermionLineG5[exp]]];
aux=auxNoG5 + auxG5;   
fcng5=aux /. {Tr[0] -> 0}]]];
(*---------------------------------------------------------------------*)


(*---------------------------------------------------------------------*)
(* MyFADExplicit: Substitute FAD by 1/(SP[.,.]-m^2) *)
(* Created by: Jorge Romao
   Email: jorge.romao@tecnico.ulisboa.pt 
   Last Update: 03.08.2020

*)

MyFADExplicit::"usage"="MyFADExplicit[expr] substitutes the FAD by 1/(SP[.,.]-m^2). It is useful for FC-9.2 that has not the function FeynAmpDenominatorExplicit that does the same.";

MyFADExplicit = 
    Function[xamp, Module[{aux1,aux2},
    aux1 = xamp//FeynAmpDenominatorSplit//FCE; 			     
    RuleFAD = {FAD[{x_, y_}] -> 1/(SP[x, x] - y^2), FAD[x_] -> 1/SP[x, x]};
    aux2=aux1/. RuleFAD;
    aux2
]];

