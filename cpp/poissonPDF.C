#include"TH1D.h"
#include"TRandom2.h"
#include"TMath.h"
#include<stdio.h>

TH1D* poisPDFerr(double b,double be,int Ntoys){
	// prepare a histogram
	char name[20];
	sprintf(name,"%.2f +- %.2f",b,be);
	int nbins = int(max(b+20*sqrt(b),15.));
	TH1D *h = new TH1D(name,name,nbins,-0.5,nbins-0.5);
	// generate 
	TRandom2 *rand = new TRandom2();
	int counter = 0;
	while (counter < Ntoys){
		double mu = rand->Gaus(b,be);
		if (mu<0.) continue; 
		h->Fill(rand->Poisson(mu),TMath::Gaus(mu,b,be,true));
		counter++;
	}
	// normalize
	h->Scale(1./h->Integral());
	return h;
}

TH1D* poisPDF(double b,int Ntoys){
	// prepare a histogram
	char name[20];
	sprintf(name,"%.2f",b);
	int nbins = int(max(b+20*sqrt(b),15.));
	TH1D *h = new TH1D(name,name,nbins,-0.5,nbins-0.5);
	// generate 
	TRandom2 *rand = new TRandom2();
	int counter = 0;
	while (counter < Ntoys){
		h->Fill(rand->Poisson(b));
		counter++;
	}
	// normalize
	h->Scale(1./h->Integral());
	return h;
}
