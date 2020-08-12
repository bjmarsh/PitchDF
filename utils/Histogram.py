import matplotlib.pyplot as plt
import numpy as np

class Histogram1D(object):
    def __init__(self, name, bins, xlow=None, xhigh=None, title=""):
        if type(bins)==int:
            if xlow is None or xhigh is None:
                raise Exception("If bins is an integer (# of bins), must specify xlow and xhigh")
            self.bin_edges = np.linspace(xlow, xhigh, bins+1)
        elif type(bins) in [list, np.ndarray]:
            self.bin_edges = np.array(bins)
        else:
            raise Exception("bins must either be integer number of bins or array of bin edges")

        self.name = name
        self.title = title
        self.nentries = 0
        self.nbins = self.bin_edges.size-1
        self.contents = np.zeros(self.nbins+2)
        self.sumw2 = np.zeros(self.nbins+2)
        self.sumx = 0.0
        self.sumx2 = 0.0

        self.bin_centers = 0.5*(self.bin_edges[:-1] + self.bin_edges[1:])
        self.bin_widths = self.bin_edges[1:] - self.bin_edges[:-1]

    def FindBin(self, x):
        if x >= self.bin_edges[-1]:
            return self.nbins + 1
        else:
            return np.argmax(self.bin_edges>x)

    def Fill(self, x, w=1.0):
        ibin = self.FindBin(x)
        self.contents[ibin] += w
        self.sumw2[ibin] += w**2
        self.sumx += w*x
        self.sumx2 += w*x**2
        self.nentries += 1

    def GetContents(self, ibin):
        return self.contents[ibin]

    def GetError(self, ibin):
        return np.sqrt(self.sumw2[ibin])

    def Scale(self, a):
        self.contents *= a
        self.sumw2 *= a**2
        self.sumx *= a
        self.sumx2 *= a

    def Normalize(self):
        N = np.sum(self.contents)
        if N != 0:
            self.Scale(1.0/N)

    def mean(self):
        N = np.sum(self.contents)
        if N==0:
            return None
        return self.sumx / N

    def rms(self):
        N = np.sum(self.contents)
        if N==0:
            return None
        return (self.sumx2 - self.sumx**2)/N

    def Draw(self, fig=None, ax=None, opt="HIST", **kwargs):
        if not fig:
            fig = plt.gcf()
        if not ax:
            ax = fig.add_subplot(111)
        
        didplot = False
        if "HIST" in opt:
            plt.hist(self.bin_centers, bins=self.bin_edges, weights=self.contents[1:-1], histtype="step", 
                     **kwargs)
            didplot = True
        if didplot:
            kwargs['label'] = None
        if "ERR" in opt:
            errors = np.sqrt(self.sumw2)
            xerr = None if "YERR" in opt else self.bin_widths/2
            plt.errorbar(self.bin_centers, self.contents[1:-1], xerr=xerr, yerr=errors[1:-1], 
                         fmt=',', capsize=0, **kwargs)
