import os,sys,multiprocessing,pickle,ROOT as r

Lumi = 18500 # in picobarns
r.gROOT.LoadMacro("cpp/roostats_cl95.C+")
data=pickle.load(open('data/data'+sys.argv[1]+'.pkl'))
signals = [key for key in data.keys() if 'H' in key]
limits = {}

def wrapLim(obj):
	# obj[0],obj[1] is eff, seff; obj[2],obj[3] is b,sb
	dirName='tmp/'+str(obj[1])+str(obj[2])
	os.mkdir(dirName); os.chdir(dirName)
	limit = r.roostats_cl95(Lumi,0.026*Lumi,obj[0],obj[1],obj[2],obj[3],int(obj[2]),1,0,'cls','',0)
	#limit = obj[2]	
	os.system('rm ws.root')
	os.chdir('../../')
	os.rmdir(dirName)
	return limit


def optimLim(eff):
	p = multiprocessing.Pool(18)
	return p.map(wrapLim, [(e[0],e[1],b[0],b[1]) for e,b in zip(eff,data['bkg'])])


for signal in signals:
	limits[signal] = optimLim(data[signal])

pickle.dump(limits,open('data/explimits'+sys.argv[1]+'.pkl','w'))
