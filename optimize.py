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

def plotRoot(sign,lim):
	hs,hsl,hl,hls = r.TGraph(len(cuts)),r.TGraph(len(cuts)),r.TGraph(len(cuts)),r.TGraph(len(cuts))
	hsl.SetFillColor(2); hls.SetFillColor(4), hs.SetFillColor(0)
	topsigidxs = [s[1] for s in sign[:5]]
	toplimidxs = [l[1] for l in lim[:5]]
	for i,(s,l) in enumerate(zip(sign,lim)):
		hs.SetPoint(hs.GetN(),i,s[0]) 
		if s[1] in toplimidxs: hsl.SetPoint(hsl.GetN(),i,s[0])
		hl.SetPoint(hl.GetN(),i,l[0]) 
		if l[1] in topsigidxs: hls.SetPoint(hls.GetN(),i,l[0])
		#hsl.GetXaxis().SetBinLabel(i+1,s[2])
		#hls.GetXaxis().SetBinLabel(i+1,l[2])
	return hs, hsl, hl, hls
	
def plot(sign,lim):
	sign,lim = np.array(sign),np.array(lim)
	_,hl,_=plt.hist(np[:,1])
	plt.plot(hl)
		

c=r.TCanvas('c','c',600,800);c.Divide(1,2)
for name in data.keys():
	if 'H' not in name: continue
	sigmaSig, sign = optimizeSignificance(name)
	sigmaLim, lim = optimizeLimit(name)

	print 'signal: ', name,' cross-section:', sigmaSig
	for x in sign[:10]: print x
	print 'signal', name, 'best limit:', sigmaLim
	for x in lim[:10]: print x

	plot(sign,lim)
	raw_input()
