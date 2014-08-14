import sys,itertools,pickle,ROOT as r, matplotlib.pyplot as plt, numpy as np
from operator import itemgetter
from utils import *

### data
data=pickle.load(open('data/data'+sys.argv[1]+'.pkl'))
explimits=pickle.load(open('data/lim'+sys.argv[1]+('err' if sys.argv[-1] == 'err' else '')+'.pkl'))
data['pdfs']=pickle.load(open('pdfs/pdfs'+('err' if sys.argv[-1] == 'err' else '')+'.pkl'))
### cuts
nprompt = [2,1,0]; promptE = [0.15,0.13,0.11,0.9,0.7,0.5]; disc = [0.7,0.8,0.9,0.95]
cuts = {i:str(a) for i,a in enumerate(itertools.product(nprompt,promptE,disc))}

def sortedSignificance(eff, sigma):
	S = [eps[0]*sigma*18500 for eps in eff]
	B = [bkg[0] for bkg in data['bkg']]
	merit = rndAll([[z_score(pdf,s+b),i,cuts[i],s,b] for i,(s,b,pdf) in enumerate(zip(S,B,data['pdfs']))],3)
	return sorted(merit, key=itemgetter(0), reverse=True)

def z_score(pdf,obs):
	pvalue = pdf.Integral(pdf.FindFixBin(obs),pdf.GetNbinsX()+1)
	return r.RooStats.PValueToSignificance(pvalue) if (pvalue>0. and pvalue<1.) else None

def optimizeSignificance(name, sigma=10):
	maxSignificance = None
	while (maxSignificance>5. or maxSignificance == None):
		sigma /= 1.1
		maxSignificance = sortedSignificance(data[name],sigma)[0][0]
	return rnd(sigma,3), sortedSignificance(data[name],sigma)

def optimizeLimit(name):
	limits = [[lim,i,cuts[i]] for i,lim in enumerate(explimits[name])]
	limits = rndAll(sorted(limits, key=itemgetter(0), reverse=False),3)
	return rnd(limits[0][0],3), limits

def makePlotHistos(sign,lim):
	[hs,hsl,hl,hls] = [r.TH1F('','',len(cuts),-0.5,len(cuts)-0.5) for i in range(4)]
	topsigidxs = [s[1] for s in sign[:5]]
	toplimidxs = [l[1] for l in lim[:5]]
	for i,(s,l) in enumerate(zip(sign,lim)):
		hs.SetBinContent(i,s[0]) 
		if s[1] in toplimidxs: hsl.SetBinContent(i,s[0])
		hl.SetBinContent(i,l[0]) 
		if l[1] in topsigidxs: hls.SetBinContent(i,l[0])
	return hs,hsl,hl,hls
	
c=r.TCanvas('c','c',700,800);c.Divide(1,2)
r.gStyle.SetOptStat(0)
for name in data.keys():
	if 'H' not in name: continue
	sigmaSig, sign = optimizeSignificance(name)
	sigmaLim, lim = optimizeLimit(name)

	print 'signal: ', name,' cross-section:', sigmaSig
	for x in sign[:10]: print x
	print 'signal', name, 'best limit:', sigmaLim
	for x in lim[:10]: print x

	hs,hsl,hl,hls = makePlotHistos(sign,lim)
	hs.SetName(name+' significance'); hs.GetYaxis().SetTitle('exp. significance')
	hl.SetName(name+' expected limits'); hl.GetYaxis().SetTitle('exp. limit [pb]')
	hs.GetXaxis().SetTitle('ordered selections'); hl.GetXaxis().SetTitle('ordered selctions') 
	hsl.SetFillColor(2); hls.SetFillColor(4)
	lat=r.TLatex(); lat.SetTextSize(0.04)
	c.cd(1);hs.Draw();hsl.Draw("Bsame")
	lat.DrawLatexNDC(0.15,0.9,name+" exp. significance for #sigma=%fpb"%sigmaSig)
	c.cd(2);hl.Draw();hls.Draw("Bsame")
	lat.DrawLatexNDC(0.15,0.9,name+" exp. limit")
	c.Update()
	raw_input()
