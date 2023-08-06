import softpotato as sp

# CV
wf = sp.technique.Sweep(Eini=0.5, Efin=-0.5, sr=0.01)
twf = wf.t
Ewf = wf.E
e = sp.simulate.E(cRb=0, cOb=1e-6)
tgrid = sp.simulate.TGrid(twf, Ewf)
xgrid = sp.simulate.XGrid([e], tgrid)
simE = sp.simulate.Simulate([e], 'E', tgrid, xgrid)
simE.sim()
e = sp.simulate.E(cRb=0, cOb=1e-6)
c = sp.simulate.C(kc=1e-1)
xgrid = sp.simulate.XGrid([e,c], tgrid)
simEC = sp.simulate.Simulate([e,c], 'EC', tgrid, xgrid)
simEC.sim()
plot(Ewf, [simE.i, simEC.i], xlab='$E$ / V', ylab='$i$ / A', 
     legend=['E', 'EC'], fig=1, show=0)

# CA
wf = sp.technique.Step(Es=-0.4, dt=0.002)
twf = wf.t
Ewf = wf.E
tgrid = sp.simulate.TGrid(twf, Ewf)
e = sp.simulate.E(cRb=0, cOb=1e-6)
xgrid = sp.simulate.XGrid([e], tgrid)
simE = sp.simulate.Simulate([e], 'E', tgrid, xgrid)
simE.sim()
e = sp.simulate.E(cRb=0, cOb=1e-6)
c = sp.simulate.C(kc=1e-1)
xgrid = sp.simulate.XGrid([e,c], tgrid)
simEC = sp.simulate.Simulate([e,c], 'EC', tgrid, xgrid)
simEC.sim()

# Cottrell
macro = sp.calculate.Macro()
i_cott = macro.Cottrell(twf)

legend = ['E', 'EC', 'Cottrell']
mark = ['-o', 'o', '--']
plot(1/np.sqrt(twf[1:]), [simE.i[1:], simEC.i[1:], i_cott[1:]], 
     xlab='$t^{-1/2}$ / s$^{-1/2}$', ylab='$i$ / A', 
     legend=legend, mark=mark, fig=2, show=0)
plot(twf[1:], [simE.i[1:]/i_cott[1:], simEC.i[1:]/i_cott[1:]],
     xlab='$t$ / s', ylab='$i$ / $i_{cott}$',
     legend=legend, mark=mark, fig=3, show=1)
