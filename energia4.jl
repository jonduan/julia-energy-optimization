##minor change
using Convex, Mosek, PyPlot

eh=readdlm("../e_high.csv")
em=readdlm("../e_med.csv")
el=readdlm("../e_low.csv")
d=readdlm("../demanda.csv")

delta_t = 5/60; #(5 min)
T=collect(5/60:delta_t:24*7)
n=size(T)[1];
T2=[0;T]

#cargo los vectores en kWh (multiplico por delta_t)
d=[d;d;d;d;d;d;d]*delta_t;
e=[eh;em;el;el;em;eh;em]*delta_t;

#Capacidad del Banco
B_max = 308.2;
#Potencia maxima del banco
p_bmax = 36*delta_t;
#Potencia maxima generador
p_dmax = 40*delta_t;
#Potencia maxima solar
p_emax = 52*delta_t;

#Construyo el modelo usando Convex
solver=MosekSolver(MSK_DPAR_MIO_TOL_REL_GAP=0.02);
set_default_solver(solver);

#Defino el modelo
x=Variable(n+1);
y=Variable(n);
u=Variable(n, :Bin);

#Defino el problema
p=minimize(sum(u) + sum(abs(u[2:end]-u[1:end-1])));

#agrego restricciones
p.constraints += x>=0;						#bateria positiva
p.constraints += x<=B_max;					#capacidad del banco
p.constraints += y>=0;						#generacion solar positiva
p.constraints += u>=0;
p.constraints += u<=1;						#generacion diesel On-OFF
p.constraints += x[2:end]-x[1:end-1] == y+p_dmax*u-d;		#carga de bateria
p.constraints += x[end] == x[1];		                #bateria final igual a inicial
p.constraints += y<=e;						#y=uso de la energia solar posible
p.constraints += x[2:end]-x[1:end-1]<= p_bmax;			#maxima carga de bateria
p.constraints += x[2:end]-x[1:end-1]>= -p_bmax		   	#maxima descarga de bateria

#resuelvo
solve!(p)
println("****************************")
println(p.status)

println("Objective value: ", p.optval)
uast = u.value;
yast = y.value;

writedlm("u.csv",[T uast]," ")
writedlm("e.csv",[T e]," ")
writedlm("y.csv",[T yast]," ")
writedlm("d.csv",[T d]," ")


xast = x.value
writedlm("x.csv",[T2 xast]," ")

plot(T,e)
plot(T,d)
plot(T,p_dmax*uast)
