import multiprocessing,sys,pickle,ROOT as r

def poisPDF_(b): return r.poisPDF(b[0],pow(10,int(sys.argv[1])))
def poisPDFerr_(b): return r.poisPDFerr(b[0],b[1],pow(10,int(sys.argv[1])))

data = pickle.load(open('data/dataLow.pkl','r'))
r.gROOT.LoadMacro("cpp/poissonPDF.C+")
p = multiprocessing.Pool(18)
pickle.dump(p.map(poisPDF_,data['bkg']),open('pdfs/tmp_pdfs.pkl','w'))
pickle.dump(p.map(poisPDFerr_,data['bkg']),open('pdfs/tmp_pdfserr.pkl','w'))
