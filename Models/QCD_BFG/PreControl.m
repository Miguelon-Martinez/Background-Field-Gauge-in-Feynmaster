FMversion = "2.0.2"; 
 
FMdate = "September 28, 2021"; 
 
osswitch = "Linux"; 
 
antimap = {ubar->u, cbar->c, tbar->t, ghGbar->ghG}; 
 
PrMassFL = False; 
 
GaugeWithGold = {}; 
 
renps = {gs -> gs + dgs,Muq -> Muq + dMuq,mu -> mu + dmu,mc -> mc + dmc,mt -> mt + dmt}; 
 
CTcor = {dgs,dMuq,dmu,dmc,dmt}; 
 
renconscar = {dgs,dmu,dmc,dmt,dG,dZghG}; 
 
renconsadd = {dgs,dmu,dmc,dmt,dG,dZghG,dMuq,dZuq}; 
 
LArenconsadd = {"\\delta g_s","\\delta m_u","\\delta m_c","\\delta m_t","\\delta G","\\delta Z_{gh}","","\\delta Z^{uq}"}; 
 
renconslist = {dgs,dmu,dmc,dmt,dG,dZghG,dMuq[1,1],dMuq[1,2],dMuq[1,3],dMuq[2,1],dMuq[2,2],dMuq[2,3],dMuq[3,1],dMuq[3,2],dMuq[3,3],dZuq[1,1],Conjugate[dZuq[1,1]],dZuq[1,2],Conjugate[dZuq[1,2]],dZuq[1,3],Conjugate[dZuq[1,3]],dZuq[2,1],Conjugate[dZuq[2,1]],dZuq[2,2],Conjugate[dZuq[2,2]],dZuq[2,3],Conjugate[dZuq[2,3]],dZuq[3,1],Conjugate[dZuq[3,1]],dZuq[3,2],Conjugate[dZuq[3,2]],dZuq[3,3],Conjugate[dZuq[3,3]]}; 
 
GFreno = True; 
 
RenoLogic = False; 
 
renorrules = {gs -> gs + dgs,Muq -> Muq + dMuq,mu -> mu + dmu,mc -> mc + dmc,mt -> mt + dmt,ghG[aa_] -> ghG[aa] + 1/2 dZghG ghG[aa],ghGbar[aa_] -> ghGbar[aa] + 1/2 Conjugate[dZghG] ghGbar[aa],uq -> uq + 1/2 dZuq.uq,uqbar -> uqbar + 1/2 uqbar.HC[dZuq]}; 
 
