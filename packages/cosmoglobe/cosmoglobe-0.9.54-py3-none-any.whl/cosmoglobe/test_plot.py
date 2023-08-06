#%%
from re import L
from cosmoglobe.plot.plottools import standalone_colorbar, seds_from_model, symlog
from cosmoglobe.plot import plot, gnom, trace, spec
from cosmoglobe.sky import model_from_chain
from cosmoglobe.h5.chain import Chain
from cosmoglobe import get_test_chain
from astropy import constants as const
import numpy as np 
import healpy as hp 
import astropy.units as u
import matplotlib.pyplot as plt
from matplotlib.colors import colorConverter, LinearSegmentedColormap, ListedColormap
import os
from pathlib import Path
import data as data_dir
import scicm
import cmasher
import cmcrameri
cmap_path = Path(data_dir.__path__[0]) / "planck_cmap.dat"
planck_cmap = np.loadtxt(cmap_path) / 255.0
planck_cmap = ListedColormap(planck_cmap, "planck")

paperfigs='/Users/svalheim/work/BP/papers/09_leakage/figs2/'
path='/Users/svalheim/work/cosmoglobe-workdir/'
#chain='bla.h5'
dust='dust_c0001_k000200.fits'
cmb='cmb_c0001_k000200.fits'


"""
TODO:
Legg inn savefig med automatisk output-formattering i skymap som save=True

"""
"""
chain=get_test_chain()
model = model_from_chain(chain, nside=256, components=["synch", "ff", "ame", "dust", "radio"])
emission = model(70*u.GHz, fwhm=180*u.arcmin,)
hp.write_map("mask_template_n256.fits", emission)
#plot(emission, sig=1)
#plt.show()
"""

if False:
    #cmaps=["B2P", "B2T", "BgreyY", "BkG", "BkO", "BkR", "BkT", "BkY", "Blue", "Blue2080", "BwG", "BwM", "BwO", "BwR", "Cyan", "Day", "G2Y", "Garnet", "GkM", "GkP", "Green", "Green2080", "GwM", "GwP", "M2R", "Magenta", "Magenta2080", "Night", "O2Y", "OkM", "Orange", "Orange2080", "P2M", "PgreyG", "PkM", "PkO", "PkR", "PkY", "Purple", "Purple2080", "PwM", "Quartile", "R2O", "Red", "Red2080", "RgreyB", "Ripe", "RwM", "RwP", "SoftBlue", "SoftGreen", "SoftMagenta", "SoftOrange", "SoftPurple", "SoftRed", "SoftTeal", "SoftYellow", "Stone", "T2G", "Teal", "Teal2080", "TgreyM", "TkG", "TkO", "TkP", "TkR", "TkY", "Tropical", "TwG", "TwO", "TwR", "Yellow", "Yellow2080", "YkB", "YkM", "iso_1", "iso_2",]
    cmaps=[x for x in scicm.cm.cmaps if x not in scicm.cm.diverging]
    print(cmaps)
    print("Number of cmaps:",len(cmaps))
    dust = hp.read_map(path+dust, field=(0,2))
    plt.figure(figsize=(16,9))
    for i in range(len(cmaps)):
        hp.mollview(dust[0], norm="hist", min=30,max=3000,cmap=getattr(scicm.cm, cmaps[i]), sub=(7,7,1+i), cbar=False, title=cmaps[i],)
        print(i)
    plt.tight_layout()
    plt.savefig("scicm.png",dpi=300, pad_inches = 0, bbox_inches="tight")
    plt.show()
    cmaps=list((scicm.cm.diverging).keys())
    print(cmaps)
    print("Number of cmaps:",len(cmaps))
    plt.figure(figsize=(16,9))
    for i in range(len(cmaps)-1):
        hp.mollview(symlog(dust[1]), min=-np.log(10), max=np.log(10), cmap=getattr(scicm.cm, cmaps[i]), sub=(5,6,1+i), cbar=False, title=cmaps[i],)
        print(i)
    plt.tight_layout()
    plt.savefig("scicm_divirging.png",dpi=300, pad_inches = 0, bbox_inches="tight")
    plt.show()

if False:
    cmb = hp.read_map(path+cmb, field=(0,2))
    cmb = hp.smoothing(cmb[0], fwhm=40*0.000291)
    plt.figure(figsize=(16,9))
    hp.mollview(cmb, min=-300, max=300, cmap=getattr(scicm.cm, "Day"), title="Day",sub=(2,2,1), remove_dip=True)
    hp.mollview(cmb, min=-300, max=300, cmap=getattr(cmasher.cm, "fusion_r"), title="fusion",sub=(2,2,2), remove_dip=True)
    hp.mollview(cmb, min=-300, max=300, cmap=getattr(cmcrameri.cm, "roma_r"), title="roma",sub=(2,2,3), remove_dip=True)
    hp.mollview(cmb, min=-300, max=300, cmap=planck_cmap, title="planck",sub=(2,2,4), remove_dip=True)
    plt.show()

if False:
    comps=["synch", "ff", "ame",]
    components=["cmb","dust"]
    chain=get_test_chain()
    ico=False
    for i in range(5):
        model = model_from_chain(chain, nside=64,components=components)
        spec(model,long=False,include_co=ico)
        plt.savefig(f"spectrum_{i}.png", bbox_inches='tight',  pad_inches=0.02, transparent=True, dpi=300)
        if i==3:
            ico=True
        else:
            components.append(comps[i])

if False:
    chain=get_test_chain()
    model = model_from_chain(chain, components=["synch", "cmb"], nside=64)
    spec(model,pol=True,)
    plt.savefig(f"spectrum_synch.png", bbox_inches='tight',  pad_inches=0.02, transparent=True, dpi=300)

if False:
    model = model_from_chain(path+chain, components=["dust"], nside=16)
    nu  = np.logspace(np.log10(0.1),np.log10(5000),1000)
    seds = seds_from_model(nu, model, nside=64)
    plt.loglog(seds["dust"][0][0])
    plt.show()

if False:
    plot(path+dust, comp="dust", cbar=True, cb_orientation="vertical",)
    plt.show()
    #plot(path+chain, comp="dust", nside=16, )
    #plt.show()

if False:
    plot(path+dust, comp="dust",  sig="U", interactive=True) 
    plt.show()

if False:
    plot(path+dust, width="m", sig="Q", ticks=[0, np.pi, None], norm="log", 
        unit=u.uK, nside=512, cmap="chroma", left_label="Left", 
        right_label="Right", title="Cool figure", graticule=True, 
        projection_type="hammer", mask=path+"mask_common_dx12_n0512_TQU.fits", 
        maskfill="pink", graticule_color="white", xtick_label_color="white", 
        ytick_label_color="white",)#fwhm=14*u.arcmin, darkmode=True)
    plt.show()

# m 4.7 = 0.07
# l 7   = 0.04
#0.07=4.7*(0.07-0.04)/(4.7-7)



#ratio = ratio_l*width/width_l
#ratio = 0.04*width/7

#0.04x = 0.07
#7     = 4.7   

#ratio_y = l
#ratio = width/7*0.04

if True:
    plot(path+dust, width="m", sig="Q",comp="dust",norm="log")
    plt.show()
    #plt.savefig("testm.png", dpi=600, pad_inches = 0, bbox_inches="tight")
    #plot(path+dust, width="s", sig="Q",comp="dust", title="title")
    #plt.savefig("tests.png", dpi=600)

if False:
    plot(path+dust, interactive=True, sig="Q", ticks=[0, np.pi, None], norm="log", unit=u.uK, fwhm=14*u.arcmin, nside=512, cmap="chroma", left_label="Left", right_label="Right", title="Cool figure", width=7, graticule=True, projection_type="hammer", mask=path+"mask_common_dx12_n0512_TQU.fits", maskfill="pink", graticule_color="white", xtick_label_color="white", ytick_label_color="white",)# darkmode=True)
    plt.show()

if False:
    plot(path+dust, comp="cmb", sig="Q", ticks=[0, np.pi, None], norm="log", unit=u.uK, fwhm=14*u.arcmin, nside=512, cmap="chroma", left_label="Left", right_label="Right", title="Cool figure", width=7, graticule=True, projection_type="hammer", mask=path+"mask_common_dx12_n0512_TQU.fits", maskfill="pink", graticule_color="white", xtick_label_color="white", ytick_label_color="white",)# darkmode=True)
    plt.show()

if False:
    m = hp.read_map(path+dust, field=1,)
    plot(m, comp="dust",  sig="U",cbar=True, width="s")
    plt.show()

if False:
    gnom(path+dust, comp="dust", subplot=(2,2,1), cbar_pad=0.0, cbar_shrink=0.7)
    gnom(path+dust, comp="dust", subplot=(2,2,2), cbar_pad=0.0, cbar_shrink=0.8)
    gnom(path+dust, comp="dust", subplot=(2,2,3), cbar_pad=0.0, cbar_shrink=0.9)
    gnom(path+dust, comp="dust", subplot=(2,2,4), cbar_pad=0.0, cbar_shrink=1)
    plt.show()

if False:
    #os.system(f'cosmoglobe plot {path}{dust} -comp freqmap -range 0.5 -freq 70 -show')
    #os.system(f'cosmoglobe plot {path}030_diff_filt.fits -sig 0 -right_label "\Delta A_{{30}}" -left_label "\Delta I" -range 10 -unit "\mu\mathrm{{K}}"')
    os.system(f'cosmoglobe plot {path}030_diff_filt.fits -comp freqmap -right_label "$\Delta A_{30}$" -left_label "$\Delta I$" -freq 30 ')

    #os.system(f'cosmoglobe gnom {path}{dust} -lon 30 -lat 70 -comp freqmap -ticks auto -freq 70 -show')
    #os.system(f'cosmoglobe trace {path}{chain} -labels "1 2 3 4" -dataset synch/beta_pixreg_val -show')

if False:
    #c = Chain(path+chain)
    #print(c["000001/tod/023-WMAP_K/chisq"])
    trace(path+chain, figsize=(10,2), sig=0, labels=["Reg1","Reg2","Reg3","Reg4"], dataset="synch/beta_pixreg_val", subplot=(3,1,1), ylabel=r"$\beta_s^T$")
    trace(path+chain, sig=1, labels=["Reg1","Reg2","Reg3","Reg4"], dataset="synch/beta_pixreg_val", subplot=(3,1,2), ylabel=r"$\beta_s^P$")
    trace(path+chain, dataset="tod/023-WMAP_K/bp_delta", subplot=(3,1,3), ylabel=r"$\Delta_{bp}$")
    #trace(path+chain, dataset="tod/023-WMAP_K/chisq", subplot=(5,1,4), ylabel=r"$\chi^2$")
    #trace(path+chain, dataset="tod/023-WMAP_K/gain", subplot=(5,1,5), ylabel="gain", xlabel="Gibbs sample")
    plt.show()

if False:    
    standalone_colorbar("planck", ticks=[-0.2,0,0.2], unit=r"$S/\sigma_S$",)
    plt.savefig(paperfigs+"colorbar_planck_pm0.2smap.pdf", pad_inches = 0, dpi=300)

    standalone_colorbar("planck", ticks=[-0.2,0,0.2], unit=u.uK,)
    plt.savefig(paperfigs+"colorbar_planck_pm0.2.pdf", pad_inches = 0, dpi=300)
    standalone_colorbar("planck", ticks=[-0.1,0,0.1], unit=u.uK,)
    plt.savefig(paperfigs+"colorbar_planck_pm0.1.pdf", pad_inches = 0, dpi=300)
    
    standalone_colorbar("planck", ticks=[-5,0,5], unit=u.uK,)
    plt.savefig(paperfigs+"colorbar_planck_pm5.pdf",  pad_inches = 0, dpi=300)

    standalone_colorbar("planck", ticks=[-3,0,3], unit=u.uK,)
    plt.savefig(paperfigs+"colorbar_planck_pm3.pdf", pad_inches = 0, dpi=300)

    standalone_colorbar("planck", ticks=[-1,0,1], unit=u.uK,)
    plt.savefig(paperfigs+"colorbar_planck_pm1.pdf", pad_inches = 0, dpi=300)

    standalone_colorbar("planck", ticks=[-10,0,10], unit=u.uK,)
    plt.savefig(paperfigs+"colorbar_planck_pm10.pdf", pad_inches = 0, dpi=300)



def transform(m):
    y = m/100
    y[y > 1] = np.log10(y[y>1]) + 1
    return y

def f(nu):
    return 1/(const.c.value**2 / 2. / const.k_B.value / (nu * 1e9) **2 * 1e-26 * 1e6)

def f2(nu):
    return (nu/22)**-3

if False:
    chain=get_test_chain()
    cmb = model_from_chain(chain, nside=64, components=["cmb"])
    sky = model_from_chain(chain, nside=64, components=["synch", "ff", "ame", "dust",])
    nus=np.logspace(np.log10(10),np.log10(800),num=50,dtype=int)
    for i, freq in enumerate(nus): #enumerate(nus): #enumerate([200,]): #enumerate([353,]):
        #outname = f'{str(int(freq)).zfill(4)}GHz.png'
        if freq > 180:
            s = f(freq)*1e-3
        elif freq < 20:
            s = f2(freq)
        else:
            s=1

        #s = 1/(f(freq)*1e-3) if freq > 180 else 1
        if freq < 353:
            if freq > 250:
                r = ((353-freq)/(353-250))*67
            else:
                r = 67

        else:
            r = 0

        fsky = hp.remove_dipole(sky(freq*u.GHz,)[0].value, gal_cut=30, copy=True)
        fcmb = hp.remove_dipole(cmb(freq*u.GHz,)[0].value, gal_cut=30, copy=True)
        ftot = fcmb + fsky*s

        #plot(fsky, ticks=[-1e3, -100, 0, 100, 1e3, 1e7], cmap="planck_log", title=f'{freq:.0f} GHz', remove_mono=True, cbar=False, width=1)
        plot(fsky, ticks=[10, 100], norm="log", cmap="binary", remove_mono=True, cbar=False, width=1)
        #plot(ftot, ticks=[-1e3, -100, 0, 100, 1e3, 1e7], cmap="planck_log", remove_mono=True, cbar=False, width=1,fwhm=120*u.arcmin)
        plt.savefig(f"/Users/svalheim/work/thesis/figures/gifs/smallgif_{i+1}.png", bbox_inches='tight',  pad_inches=0.02, transparent=True, dpi=300)
        plt.show()

# %%


# %%
