import cPickle as pickle
import numpy as np
from sklearn import linear_model
import pandas as pd
import matplotlib.pyplot as plt

class Strikezone(object):
    def __init__(self, pitch_df, sel="", binsx=None, binsy=None, smooth=None):
        if not binsx:
            binsx = np.linspace(-1.5,1.5,41)
        if not binsy:
            binsy = np.linspace(-0.5,1.5,41)

        self.xmin = binsx[0]
        self.xmax = binsx[-1]
        self.ymin = binsy[0]
        self.ymax = binsy[-1]


        # filter out non-called pitches and pitches with no pfx data
        pitch_df = pitch_df.query("px>-900 & (strike_type=='C' | strike_type=='B')")
        # add normalized pz column
        pitch_df["pz_norm"] = (pitch_df.pz-pitch_df.sz_bot)/(pitch_df.sz_top-pitch_df.sz_bot)
        
        df_all = pitch_df.query(sel) if sel!="" else pitch_df
        strikes = df_all.query("strike_type=='C'")
        h2_all,_,_ = np.histogram2d(df_all.px, df_all.pz_norm, bins=[binsx,binsy])
        h2_str,_,_ = np.histogram2d(strikes.px, strikes.pz_norm, bins=[binsx,binsy])
        self.prob_map = np.divide(h2_str, h2_all, out=np.ones_like(h2_all)*(-np.inf), where=(h2_all>0))
        self.prob_map_smoothed = None
        if smooth:
            self.smooth(smooth)


    def smooth(self, finebin=3):
        new_sz = np.zeros((self.prob_map.shape[0]*finebin, self.prob_map.shape[1]*finebin))
        model = linear_model.LinearRegression(fit_intercept=True)
        for i in range(self.prob_map.shape[0]):
            for j in range(self.prob_map.shape[1]):
                x_vals = []
                y_vals = []
                for ix in range(i-3, i+4):
                    for iy in range(j-3, j+4):
                        if ix<0 or iy<0 or ix>=self.prob_map.shape[0] or iy>=self.prob_map.shape[1] or self.prob_map[ix,iy]==-np.inf:
                            continue
                        x_vals.append([ix, iy, ix**2, iy**2, ix*iy])
                        y_vals.append(self.prob_map[ix,iy])
                model.fit(x_vals, y_vals)
                for a in range(finebin):
                    for b in range(finebin):
                        x = i - 0.5 + 1./(2*finebin) + 1.*a/finebin
                        y = j - 0.5 + 1./(2*finebin) + 1.*b/finebin
                        pred = min(max(model.predict([[x, y, x**2, y**2, x*y]])[0],0),1)
                        new_sz[finebin*i+a, finebin*j+b] = pred
        self.prob_map_smoothed = np.copy(new_sz)

    @staticmethod
    def _plot(sz, extent, fig=None, ax=None, zlim=(0.0,1.0), sz_zbounds=None, interp='none', cb=True):
        if not fig:
            fig = plt.gcf()
        if not ax:
            ax = fig.add_subplot(111)

        im = ax.imshow(sz.T, interpolation=interp, cmap='RdBu_r', extent=extent, 
                       origin='low', aspect='auto', vmin=zlim[0], vmax=zlim[1])
        if cb:
            cb = fig.colorbar(im)
            cb.set_label("Prob(called strike)")
        mean_szbot, mean_sztop = (0,1) if not sz_zbounds else tuple(sz_zbounds)
        ax.plot([-8.5/12,8.5/12], [mean_szbot, mean_szbot], '-', color='lime', lw=2)
        ax.plot([-8.5/12,8.5/12], [mean_sztop, mean_sztop], '-', color='lime', lw=2)
        ax.plot([8.5/12,8.5/12], [mean_szbot, mean_sztop], '-', color='lime', lw=2)
        ax.plot([-8.5/12,-8.5/12], [mean_szbot, mean_sztop], '-', color='lime', lw=2)
        ax.set_xlabel("x (ft)")
        ax.set_ylabel("z ({0})".format("ft" if sz_zbounds else "norm"))

    def plot(self, fig=None, ax=None, zlim=(0.0,1.0), smoothed=False, sz_zbounds=None, interp='none', cb=True):
        if smoothed and self.prob_map_smoothed is None:
            raise Exception("must compute smoothed strikezone before plotting!")
        sz = self.prob_map if not smoothed else self.prob_map_smoothed

        extent = [self.xmin, self.xmax, self.ymin, self.ymax]
        if sz_zbounds:
            extent[2] = extent[2]*(sz_zbounds[1]-sz_zbounds[0]) + sz_zbounds[0]
            extent[3] = extent[3]*(sz_zbounds[1]-sz_zbounds[0]) + sz_zbounds[0]

        self._plot(sz, extent, fig=fig, ax=ax, zlim=zlim, sz_zbounds=sz_zbounds, interp=interp, cb=cb)

    def get_prob(self, x, z, szbot=0, sztop=1, use_smoothed=False):
        if use_smoothed and self.prob_map_smoothed is None:
            raise Exception("must compute smoothed strikezone before getting probability!")
        znorm = (z-szbot)/(sztop-szbot)
        sz = self.prob_map if not use_smoothed else self.prob_map_smoothed
        
        dx = (self.xmax-self.xmin)/(sz.shape[0]-1)
        dy = (self.ymax-self.ymin)/(sz.shape[1]-1)

        ix = int((x-self.xmin)/dx)
        iz = int((znorm-self.ymin)/dy)

        if ix<0 or (self.xmin+ix*dx > self.xmax) or \
                iz<0 or (self.ymin+iz*dy > self.ymax):
            return 0.0

        return sz[ix, iz]

class StrikezoneCollection:
    def __init__(self):
        self.szs = {}

    def add(self, name, sz):
        self.szs[name] = sz

    def get(self, name):
        if name in self.szs:
            return self.szs[name]
        raise Exception("strikezone with name {0} doesn't exist in this collection!".format(name))
              
    def plot_diff(self, name1, name2, fig=None, ax=None, smoothed=False, zlim=(-0.5,0.5), sz_zbounds=None, cb=True):
        sz1 = self.get(name1)
        sz2 = self.get(name2)

        if (sz1.xmin, sz1.xmax, sz1.ymin, sz1.ymax) != (sz2.xmin, sz2.xmax, sz2.ymin, sz2.ymax):
            raise Exception("Bounds must be the same to plot difference!")

        extent = [sz1.xmin, sz1.xmax, sz1.ymin, sz1.ymax]
        if sz_zbounds:
            extent[2] = extent[2]*(sz_zbounds[1]-sz_zbounds[0]) + sz_zbounds[0]
            extent[3] = extent[3]*(sz_zbounds[1]-sz_zbounds[0]) + sz_zbounds[0]

        if smoothed:
            diff = sz1.prob_map_smoothed - sz2.prob_map_smoothed
        else:
            diff = sz1.prob_map - sz2.prob_map
        
        Strikezone._plot(diff, extent, fig=fig, ax=ax, zlim=zlim, sz_zbounds=sz_zbounds, cb=cb)

    def to_pickle(self, outname):
        with open(outname, 'wb') as fid:
            pickle.dump(self, fid, protocol=-1)
