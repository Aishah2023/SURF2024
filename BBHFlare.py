

import numpy as np
from scipy import stats
from .core import Transient

from .environments import get_hostmass_rvs
from ..tools.utils import random_radec

import matplotlib.pyplot as plt
import sncosmo

try:
    import afterglowpy
except:
    raise ImportError("could not import afterglowpy ; run pip install afterglowpy")

__all__ = ["afterglowpy"]



# plt.plot(times,fluxes)
# plt.title("Flux vs. Time ")
# plt.xlabel("Flux")
# plt.ylabel("Time")
# plt.show()


wave =  np.linspace(3600,8000,6)

tr = np.random.uniform(10,100)
td = np.random.uniform(tr,200)
t0 = np.random.uniform(58300,60500)
A = np.random.uniform(50,1000)


times = np.linspace(t0 - tr,t0 + td,50)
times = np.unique(np.concatenate(([t0],times))) #making sure t0 is in there


fluxes = np.empty(len(times))
for i, time in enumerate(times):
    if i == 0:
        fluxes[0] = 0
    elif i != 0:
        if time == t0:
            flux = A         
        elif time < t0: #rising
            flux = fluxes[i-1] + (A/tr * (times[i] - times[i-1]))
        elif time > t0: #decaying
            flux = fluxes[i-1] + (-A/td * (times[i] - times[i-1])) 

        fluxes[i] = flux
    
#This block of code is to fix the formatting of the 'fluxes' variable so that it can work in sncosmo.TimeSeriesSource()
list2 = []
for flux in fluxes:
    list1 = []
    for i in range(len(wave)): #len(wave) = number of wavelengths
        list1.append(flux)
    list2.append(list1)
fluxes = list2
fluxes = np.array(fluxes)


template = sncosmo.Model(sncosmo.TimeSeriesSource(times, wave, np.array(fluxes)))
sncosmo.plot_lc(model = template, bands = ['ztfg', 'ztfr'])


class BBH_Flux_Times( object ):

    @staticmethod
    def times(t0,tr,td):
        times = np.linspace(t0 - tr,t0 + td,1)
        times = np.unique(np.concatenate(([t0],times))) #making sure t0 is in there

        return times
    
    @staticmethod
    def flux(time,A,t0,tr,td):
        if time == t0:
            flux = A         
        elif time < t0: #rising
           flux = fluxes[i-1] + (A/tr * (times[i] - times[i-1]))
        elif time > t0: #decaying
            flux = fluxes[i-1] + (-A/td * (times[i] - times[i-1])) 

        return flux

class BBH( Transient ):

    _KIND = "afterglow"
    _TEMPLATE = template
    _RATE = 3.095 
    

    _MODEL = dict( redshift = {"kwargs":{"zmax":0.2},
                                  "as":"z"},

                   t0 = {"func": np.random.uniform,
                         "kwargs": {"low":58_300, "high":60_500} },
                    
                   
                    radec = {"func": random_radec,
                            "kwargs": {},
                            "as": ["ra","dec"]
                           },
                    # tr = {"func": np.random.uniform,
                    #      "kwargs": {"low":10, "high":100} },
                    # td = {"func": np.random.uniform,
                    #      "kwargs": {"low":"@tr", "high":200} },
                    # A = {"func": np.random.uniform,
                    #      "kwargs": {"low":50, "high":1000} },
                    # time = {"func": BBH_Flux_Times.times,
                    #      "kwargs": {"t0":"@t0", "tr":"@tr", "td":"@tr"} } #This works and ends up showing up in the data attribue
                    # flux = {"func": BBH_Flux_Times.flux,
                    #      "kwargs": {"t0":"@t0", "tr":"@tr", "td":"@tr"} } #PROBLEM: This can only work if BBH_Flux_Times.times() outputs only 1 time.
                    
                    
                    
                    
                   )









                   
# class BBHFlare(Transient):
#     _KIND = "SNIa"
#     _TEMPLATE = "salt2"
#     _RATE = 2.35 * 10**4 # REPLACE W NUMBER FROM LIGO. 17.9 Gpc−3 yr−1 and 44 Gpc−3 yr−1

#     # {'name': {func: ,'kwargs': {}, 'as': str_or_list }}
#     _MODEL = dict( redshift = {"kwargs": {"zmax":0.2}, "as":"z"},

#                    tr = {"func": np.random.uniform, 
#                          "kwargs": {"low":10, "high":100} },

#                     td = {"func": np.random.uniform, 
#                          "kwargs": {"low":"@tr", "high":200} }, 

#                    t0 = {"func": np.random.uniform, 
#                          "kwargs": {"low":58300, "high":60500} },
#                     A = {"func": np.random.uniform, 
#                          "kwargs": {"low":50, "high":1000} },
                       
#                    radec = {"func": random_radec,
#                             "kwargs": {},
#                             "as": ["ra","dec"]
#                            },
#                     )
#look for rate, clone code, and edit model...keep radec redshift
#look more into how they define other classes..kwargs....look for ways for one parameter...
#look sncosmo defining their models and format they're saved in
#look at target and transient definitions in .core
#search template, sncosmo nd see where it comes up
#move to ksysurvy
