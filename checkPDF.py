import sys,pickle,ROOT as r

pdfs = pickle.load(open(sys.argv[1],'r'))
c=r.TCanvas('pdf & significance','',600,800)
c.Divide(1,2)

for n,pdf in enumerate(pdfs):
	# add significance histogram
	sig = pdf.Clone()
	sig.SetBinContent(1,0)
	for i in range(2,pdf.GetNbinsX()):
		pvalue = pdf.Integral(i,pdf.GetNbinsX()+1)
		z = r.RooStats.PValueToSignificance(pvalue)
	   	sig.SetBinContent(i,z if pvalue>0. else 0.)
	# plot
	c.cd(1);r.gPad.SetLogy();pdf.Draw()
	c.cd(2);sig.Draw()
	c.Update()
	raw_input("This is "+str(n)+" pdf, press Enter to get next PDF...")
