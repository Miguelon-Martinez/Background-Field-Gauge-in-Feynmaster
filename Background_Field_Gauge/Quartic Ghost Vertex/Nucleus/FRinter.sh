cd /home/miguelon/Escritorio/Software/FeynMaster/Models/QCD_BFG/ 
math -noprompt -script Execute.m 
rm -f Execute.m 
mkdir -p /home/miguelon/Escritorio/Software/QGRAF/Models/
mv built-model /home/miguelon/Escritorio/Software/QGRAF/Models/ 
cd /home/miguelon/Escritorio/Software/QGRAF/Models/ 
rm -f QCD_BFG 
mv built-model QCD_BFG 
cd /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/ 
rm -f PrePropagators.m 
rm -f PreRulesv3Higgs.m 
rm -f PreRulesv4Higgs.m 
rm -f PreRulesv3Gauge.m 
rm -f PreRulesv4Gauge.m 
rm -f PreRulesv3Fermions.m 
rm -f PreRulesv3Yukawa.m 
rm -f PreRulesv3Ghosts.m 
rm -f PreRulesv4Ghosts.m 
rm -f PreRulesv3Beaks.m 
rm -f PreRulesv4Beaks.m 
rm -f PrePrintPropagators.m 
rm -f PrePrintRulesv3Higgs.m 
rm -f PrePrintRulesv4Higgs.m 
rm -f PrePrintRulesv3Gauge.m 
rm -f PrePrintRulesv4Gauge.m 
rm -f PrePrintRulesv3Fermions.m 
rm -f PrePrintRulesv3Yukawa.m 
rm -f PrePrintRulesv3Ghosts.m 
rm -f PrePrintRulesv4Ghosts.m 
rm -f PrePrintRulesv3Beaks.m 
rm -f PrePrintRulesv4Beaks.m 
rm -f PrePrintCTRulesv1Tads.m 
rm -f PrePrintCTRulesv2Props.m 
rm -f PrePrintCTRulesv3Higgs.m 
rm -f PrePrintCTRulesv4Higgs.m 
rm -f PrePrintCTRulesv3Gauge.m 
rm -f PrePrintCTRulesv4Gauge.m 
rm -f PrePrintCTRulesv3Fermions.m 
rm -f PrePrintCTRulesv3Yukawa.m 
rm -f PrePrintCTRulesv3Ghosts.m 
rm -f PrePrintCTRulesv4Ghosts.m 
rm -f IndicesList.m 
rm -f FRtoTeX.m 
rm -f Extras.m 
rm -f ParamsValues.m 
rm -f Matrixind.m 
rm -f Nclist.m 
mkdir -p /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/
mkdir -p /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/Processes/
mkdir -p /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/
mkdir -p /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/Counterterms/
python3 FRExtract.py 
mv Extras.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/ 
mv ParamsValues.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/ 
mv Matrixind.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/ 
mv Nclist.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/ 
cd /home/miguelon/Escritorio/Software/FeynMaster/Models/QCD_BFG/ 
mv Feynman-Rules-Main.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/ 
if [ -f ./PrePropagators.m ]; then mv PrePropagators.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PreRulesv3Higgs.m ]; then mv PreRulesv3Higgs.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PreRulesv4Higgs.m ]; then mv PreRulesv4Higgs.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PreRulesv3Gauge.m ]; then mv PreRulesv3Gauge.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PreRulesv4Gauge.m ]; then mv PreRulesv4Gauge.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PreRulesv3Fermions.m ]; then mv PreRulesv3Fermions.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PreRulesv3Yukawa.m ]; then mv PreRulesv3Yukawa.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PreRulesv3Ghosts.m ]; then mv PreRulesv3Ghosts.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PreRulesv4Ghosts.m ]; then mv PreRulesv4Ghosts.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PreRulesv3Beaks.m ]; then mv PreRulesv3Beaks.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PreRulesv4Beaks.m ]; then mv PreRulesv4Beaks.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PrePrintPropagators.m ]; then mv PrePrintPropagators.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PrePrintRulesv3Higgs.m ]; then mv PrePrintRulesv3Higgs.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PrePrintRulesv4Higgs.m ]; then mv PrePrintRulesv4Higgs.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PrePrintRulesv3Gauge.m ]; then mv PrePrintRulesv3Gauge.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PrePrintRulesv4Gauge.m ]; then mv PrePrintRulesv4Gauge.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PrePrintRulesv3Fermions.m ]; then mv PrePrintRulesv3Fermions.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PrePrintRulesv3Yukawa.m ]; then mv PrePrintRulesv3Yukawa.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PrePrintRulesv3Ghosts.m ]; then mv PrePrintRulesv3Ghosts.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PrePrintRulesv4Ghosts.m ]; then mv PrePrintRulesv4Ghosts.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PrePrintRulesv3Beaks.m ]; then mv PrePrintRulesv3Beaks.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
if [ -f ./PrePrintRulesv4Beaks.m ]; then mv PrePrintRulesv4Beaks.m /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/; fi 
cd /home/miguelon/Escritorio/Software/FeynMaster/Nucleus/ 
python3 Converter.py 
if [ -f ./Propagators.m ]; then mv Propagators.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/; fi 
if [ -f ./Rulesv3Higgs.m ]; then mv Rulesv3Higgs.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/; fi 
if [ -f ./Rulesv4Higgs.m ]; then mv Rulesv4Higgs.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/; fi 
if [ -f ./Rulesv3Gauge.m ]; then mv Rulesv3Gauge.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/; fi 
if [ -f ./Rulesv4Gauge.m ]; then mv Rulesv4Gauge.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/; fi 
if [ -f ./Rulesv3Fermions.m ]; then mv Rulesv3Fermions.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/; fi 
if [ -f ./Rulesv3Yukawa.m ]; then mv Rulesv3Yukawa.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/; fi 
if [ -f ./Rulesv3Ghosts.m ]; then mv Rulesv3Ghosts.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/; fi 
if [ -f ./Rulesv4Ghosts.m ]; then mv Rulesv4Ghosts.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/; fi 
if [ -f ./Rulesv3Beaks.m ]; then mv Rulesv3Beaks.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/; fi 
if [ -f ./Rulesv4Beaks.m ]; then mv Rulesv4Beaks.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/; fi 
rm -f CTpre.m 
if [ -f ./CTini.m ]; then mv CTini.m /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/Counterterms/; fi 
python3 Printer.py 
mkdir -p /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/TeXs-drawing/ 
mv DrawRules.tex /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/TeXs-drawing/ 
mkdir -p /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/Counterterms/TeXs-drawing/ 
mv DrawCTRules.tex /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/Counterterms/TeXs-drawing/ 
cd /home/miguelon/Escritorio/Software/FM-output/QCD_BFG/FeynmanRules/TeXs-drawing/ 
pdflatex -interaction=nonstopmode --shell-escape DrawRules.tex 
pdflatex -interaction=nonstopmode --shell-escape DrawRules.tex 
evince DrawRules.pdf & 
