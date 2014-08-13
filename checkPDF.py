import sys,pickle,ROOT as r

pdfs = pickle.load(open(sys.argv[1],'r'))
c=r.TCanvas('pdf & significance','',600,800)
c.Divide(1,2)

for pdf in reversed(pdfs):
	sig = pdf.Clone()
	for i in range(1,pdf.GetNbinsX()):
		pvalue = pdf.Integral(i,pdf.GetNbinsX()+1)
		z = r.RooStats.PValueToSignificance(pvalue)
	   	sig.SetBinContent(i,z if (pvalue>0. and pvalue<1.) else 0.)
	c.cd(1)
	r.gPad.SetLogy()
	pdf.Draw()
	c.cd(2)
	sig.Draw()
	c.Update()
	raw_input("Press Enter to get next PDF...")
