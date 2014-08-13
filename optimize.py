import sys,math,pickle,ROOT as r
from operator import itemgetter
from utils import rndAll, rnd

Lumi = 18500 # in picobarns
r.gROOT.LoadMacro("cpp/roostats_cl95.C+")
data=pickle.load(open('data/data'+sys.argv[1]+'.pkl'))
explimits=pickle.load(open('data/explimits'+sys.argv[1]+'.pkl'))
data['pdfs']=pickle.load(open('pdfs/pdfs'+('err' if sys.argv[-1] == 'err' else '')+'.pkl'))
signals = [key for key in data.keys() if 'H' in key]

def optimSig(eff, sigma):
	sig = [e[0]*sigma*Lumi for e in eff]
	bkg = [b[0] for b in data['bkg']]
	merit = [[significance(pdf,S+B),S,B,i] for i,(S,B,pdf) in enumerate(zip(sig,bkg,data['pdfs']))]
	rndAll(merit,3)
	return sorted(merit, key=itemgetter(0), reverse=True)

def significance(pdf,obs):
	pvalue = pdf.Integral(pdf.FindFixBin(obs),pdf.GetNbinsX()+1)
	return r.RooStats.PValueToSignificance(pvalue) if (pvalue>0. and pvalue<1.) else None

for signal in signals:
	sigma = 5
	bestSig = None 
	while (bestSig>5.1 or bestSig==None):
		sigma /= 1.1
		sign = optimSig(data[signal],sigma)
		bestSig = sign[0][0]

	print 'signal: ', signal,' cross-section:', rnd(sigma,3)
	for x in sign[:10]: print x

	limits = [[limit,i] for i,limit in enumerate(explimits[signal])]
	limits = rndAll(sorted(limits, key=itemgetter(0), reverse=False),3)
	print 'signal', signal, 'limits'
	for x in limits[:10]: print x
	


