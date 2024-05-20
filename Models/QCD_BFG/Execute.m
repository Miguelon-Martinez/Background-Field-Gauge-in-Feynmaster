$FeynRulesPath =  SetDirectory[ "/home/miguelon/Escritorio/Software/FeynRules/feynrules-current/"];
dirNuc = "/home/miguelon/Escritorio/Software/FeynMaster/Nucleus/";

Off[PacletManager`Name::shdw];
Off[FeynRules`Name::shdw]; 
Off[CloudFunction::argt]; 
Off[Syntax::stresc]; 

<< FeynRules`
dirFRmod = "/home/miguelon/Escritorio/Software/FeynMaster/Models/QCD_BFG/";
SetDirectory[dirFRmod];
LoadModel["QCD_BFG.fr"];

LoadRestriction["MyRestrictionsQCD.rst"];

<< PreControl.m
Get["Preamble.m", Path->{dirNuc}]

Get["Addendum.m", Path->{dirNuc}]
If[RenoLogic,
Get["Renapp.m", Path -> {dirNuc}]]; 
