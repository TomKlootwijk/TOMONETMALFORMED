"""New independent calculations for PM 1.0; no hardware or source executables."""
from pathlib import Path
from fractions import Fraction as F
import math, json, hashlib, platform
ROOT=Path(__file__).resolve().parent
checks=[]
def check(name,truth):
    if not truth: raise AssertionError(name)
    checks.append(name)
def det(a):
    a=[[F(x) for x in row] for row in a]; ans=F(1)
    for i in range(len(a)):
        pivot=next(j for j in range(i,len(a)) if a[j][i])
        if pivot!=i:a[i],a[pivot]=a[pivot],a[i];ans=-ans
        val=a[i][i];ans*=val
        for j in range(i+1,len(a)):
            factor=a[j][i]/val
            for k in range(i,len(a)):a[j][k]-=factor*a[i][k]
    return ans
B=[[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]]
H=[[F(v,2) for v in row] for row in B]
check('H4 exact orthogonality',all(sum(H[i][k]*H[j][k] for k in range(4))==int(i==j) for i in range(4) for j in range(4)))
check('H4 determinant',det(H)==1)
phi=(1+math.sqrt(5))/2
D=[phi,1/phi,1,-1]
A=[[D[i]*float(H[i][j]) for j in range(4)] for i in range(4)]
v=[float(H[0][j]) for j in range(4)]
Av=[sum(A[i][j]*v[j] for j in range(4)) for i in range(4)]
gain=math.sqrt(sum(t*t for t in Av))
check('Unscaled pinion has passive-gain counterexample',math.isclose(gain,phi,rel_tol=1e-14) and gain>1)
sv=[abs(x)/phi for x in D]
check('Scaled pinion has contractive singular values',all(x<=1 for x in sv))
for occupancy in (0,1):
    g0={((r&2047)^(occupancy<<10))&2047 for r in range(2048)}
    z0={(((r&2047)^occupancy)<<10)&2047 for r in range(2048)}
    check(f'OTAN2 profile image difference O={occupancy}',len(g0)==2048 and z0=={0,1024})
def asa(x,ma,mn,boundary,valid=255):
    a=x&ma&valid;n=a&mn;h=(n&boundary).bit_count()
    return (a,n,h,0 if h else n)
check('Whole-word sink example',asa(255,255,255,128)==(255,255,1,0))
check('Mask-narrowing nonmonotonic counterexample',asa(3,3,3,2)[3]==0 and asa(3,1,3,2)[3]==1)
check('JK truth table from old state',all(((J&(1-q))|((1-K)&q))==({(0,0):q,(1,0):1,(0,1):0,(1,1):1-q}[(J,K)]) for q in (0,1) for J in (0,1) for K in (0,1)))
C,G,P,Ta,Tup,Tdown=.02,.005,.1,293.15,304.15,301.15
tau=C/G;Tinf=Ta+P/G
tfirst=-tau*math.log1p(-G*(Tup-Ta)/P)
Ein=P*tfirst;stored=C*(Tup-Ta)
# Independent integration of the analytical loss rate G*(P/G)*(1-exp(-t/tau)).
loss=P*(tfirst-tau*(1-math.exp(-tfirst/tau)))
check('Thermal example energy residual',abs(Ein-stored-loss)<1e-14)
ton=tau*math.log((P/G-(Tdown-Ta))/(P/G-(Tup-Ta)))
toff=tau*math.log((Tup-Ta)/(Tdown-Ta))
check('Thermal times and period reproduce source rounding',round(tfirst,5)==3.19403 and round(ton+toff,5)==2.42454)
def thermal(T,u,dt):return Ta+P*u/G+(T-Ta-P*u/G)*math.exp(-dt/tau)
temperatures=[]
for seq in ([1,0,0,1],[1,1,0,0]):
    temp=Ta
    for u in seq:temp=thermal(temp,u,.5)
    temperatures.append(temp)
check('Equal pulse counts retain modeled timing information',abs(temperatures[0]-temperatures[1])>.1)
# Four-node scalar consensus with one weight per undirected edge.
x=[0.,1.,3.,2.];edges=[(0,1),(1,2),(2,3)];xdot=[0.]*4
for i,j in edges:xdot[i]-=x[i]-x[j];xdot[j]-=x[j]-x[i]
average=sum(x)/4
vdot=sum((x[i]-average)*xdot[i] for i in range(4))
check('Consensus energy identity and mean preservation',sum(xdot)==0 and vdot==-sum((x[i]-x[j])**2 for i,j in edges))
depletion=40-(6-1)-4-0+5+0
check('Illustrative crop-water depletion balance',depletion==36)
check('Finite reserve runtime bound',360000/2/3600==50)
result={'status':'passed','scope':'new finite mathematical and model calculations only','checks_passed':len(checks),'checks':checks,'python':platform.python_version(),'platform':platform.platform(),'thermal':{'tau_s':tau,'equilibrium_K':Tinf,'first_passage_s':tfirst,'input_J':Ein,'stored_J':stored,'loss_J':loss,'residual_J':Ein-stored-loss,'oscillator_period_s':ton+toff,'two_equal_count_sequences_final_K':temperatures},'wave':{'phi':phi,'unscaled_amplitude_gain':gain,'unscaled_power_gain':gain**2,'scaled_singular_values':sv},'consensus':{'mean':average,'mean_rate':sum(xdot)/4,'Vdot':vdot},'illustrative_water_depletion_mm':depletion,'reference_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(ROOT/'formal_checks_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
