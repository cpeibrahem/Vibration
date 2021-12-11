#Flags for different features
random_velocity_on = False      #Determines whether particles start with an initial random velocity
scale_off = False               #If true, the scale is not shown on the scatterplot of particles
avg_velocity_on = True          #Show the plot of Average Particle Velocity vs Elapsed steps
CoM_on = True                   #Show the plot of Center of Mass position vs Elapsed steps

#Simulation parameters
dt = 1.0          #Timestep to use for simulation (seconds), lower numbers result in smoother movement
num_ticks = 500 #Number of timesteps to run the simulation for. total simulated time = dt * num_ticks
n = 100         #Number of particles to simulate

#Particle Generation parameters
low_pos = -100 #Minimum value of x,y,z for generated particles 
high_pos = 100 #Maximum value of x,y,z for generated particles 
pos_scale = 10 ** -3 #Magnitude of high and low pos. treated as low_pos (meters) * pos_scale

low_mass = 1.0  #Minimum mass for generated particles
high_mass = 10.0#Maximum mass for generated particles
mass_scale = 1  #Magnitude of mass. treated as mass(kg) * mass_scale

particle_radius = 0.0035 #Radius of generated particles in meters

#These only have an effect if on = True
low_v = -5.0 #Minimum initial component velocity of generated particles
high_v = 5.0 #Maximum initial component velocity of generated particles
velocity_scale = 10 ** -5 #Magnitude of velocity. treated as valocity (m/s) * velocity_scale

#--END PARAMS--#######################################################################################
######################################################################################################









# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
x, y, z, m, vx, vy, vz, px, py, pz, fx, fy, fz, v_avg, ts = [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

#store timestep^2 for future use
dt2 = dt ** 2
#Set gravitational constant
G = 6.67408 * 10 ** -11

#Generate random particles
for i in range(0,n):
    #position
    x.append(np.random.randint(low_pos,high_pos)*pos_scale)
    y.append(np.random.randint(low_pos,high_pos)*pos_scale)
    z.append(np.random.randint(low_pos,high_pos)*pos_scale)
    #mass
    m.append(np.random.randint(low_mass,high_mass)*mass_scale)
    #velocity
    vx.append(np.random.randint(low_v,high_v) * velocity_scale * random_velocity_on)
    vy.append(np.random.randint(low_v,high_v) * velocity_scale * random_velocity_on)
    vz.append(np.random.randint(low_v,high_v) * velocity_scale * random_velocity_on)
    #momentum
    px.append(vx[i] * m[i])
    py.append(vy[i] * m[i])
    pz.append(vz[i] * m[i])
    #forces
    fx.append(0)
    fy.append(0)
    fz.append(0)

    
#This function is run each time the animation steps. It takes the current frame, and updates all particles' properties
def update_particles(int):
    #calculate forces w/out interactions
    for i in range(0,n):
        fx[i] = 0
        fy[i] = 0
        fz[i] = 0
        for j in range(0,n):
            f = 0
            if i != j:
                #find distance
                dx = x[j] - x[i]
                dy = y[j] - y[i]
                dz = z[j] - z[i]
                r = (dx**2 + dy**2 + dz**2)**0.5
                #if they aren't inside eachother
                if r > particle_radius * 2:
                    #F = G*m1*m2 / r^2
                    f = (G * m[i] * m[j]) / (r **2)
                else:
                    #Approximate a force that keeps them from phasing through eachother
                    f = -(G * m[i] * m[j]) / (r **2)
                #find component vectors of force
                cosa = dx / r
                cosb = dy / r
                cosg = dz / r
                #update them
                fx[i] += f * cosa
                fy[i] += f * cosb
                fz[i] += f * cosg

    #account for interactions
    for i in range(0,n):
        for j in range(0,n):
            if i != j:
                dx = x[j] - x[i]
                dy = y[j] - y[i]
                dz = z[j] - z[i]
                r = (dx**2 + dy**2 + dz**2)**0.5
                if r <= particle_radius * 2: #in contact -- collision => (m1 * v1 + m2 * v2)(m1 + m2) = vf => (p1 + p2)/(m1 + m2) = vf
                    #x-dir
                    new_vx = (px[i] + px[j])/(m[i] + m[j])
                    px[i] = new_vx * m[i]
                    px[j] = new_vx * m[j]
                    vx[i] = new_vx
                    vx[j] = new_vx
                    #y-dir
                    new_vy = (py[i] + py[j])/(m[i] + m[j])
                    py[i] = new_vy * m[i]
                    py[j] = new_vy * m[j]
                    vy[i] = new_vy
                    vy[j] = new_vy
                    #z-dir
                    new_vz = (pz[i] + pz[j])/(m[i] + m[j])
                    pz[i] = new_vz * m[i]
                    pz[j] = new_vz * m[j]
                    vz[i] = new_vz
                    vz[j] = new_vz 
        
        
    for i in range(0,n):
        #a = F/m
        ax = fx[i] / m[i]
        ay = fy[i] / m[i]
        az = fz[i] / m[i]

        #x = x0 + v0t + 0.5 at^2
        x[i] = x[i] + vx[i] * dt + 0.5 * ax * dt2
        y[i] = y[i] + vy[i] * dt + 0.5 * ay * dt2
        z[i] = z[i] + vz[i] * dt + 0.5 * az * dt2
        #v = v0 + at
        vx[i] = vx[i] + ax * dt
        vy[i] = vy[i] + ay * dt
        vz[i] = vz[i] + az * dt
        #p = m * v
        px[i] = m[i] * vx[i]
        py[i] = m[i] * vy[i]
        pz[i] = m[i] * vz[i]

        
    #calc avg speed
    if(avg_velocity_on == True):
        v_tot = 0
        for i in range(0,n):
            v_tot += (vx[i]**2 + vy[i]**2 + vz[i]**2)**0.5
        v_avg.append(v_tot / n)
        ts.append(int)
        
    #calc CoM (x,y)
    if(CoM_on == True):
        CoM_x = 0
        CoM_y = 0
        m_tot = 0
        for i in range(0,n):
            CoM_x += x[i] * m[i]
            CoM_y += y[i] * m[i]
            m_tot += m[i]
        CoM_x /= m_tot
        CoM_y /= m_tot
        
    #print iteration number
    #print(int)
    #clear scatter and  reset axis
    axis.cla()
    axis.set_xlim(left = low_pos*pos_scale, right = high_pos*pos_scale)
    axis.set_ylim(bottom = low_pos*pos_scale, top = high_pos*pos_scale)
    axis.set_zlim(bottom = low_pos*pos_scale, top = high_pos*pos_scale)
    axis.set_title("t = " + str(int * dt) + " s")
    if(scale_off == True):
        axis.set_axis_off()
    if(avg_velocity_on == True):
        spd.plot(ts, v_avg, c = "red")
    if(CoM_on == True):
        CoM.scatter(CoM_x, CoM_y, c = "red", s = 0.02)
    
    if int == num_ticks - 1:
        if(avg_velocity_on == True):
            spd.set_visible(True)
        if(CoM_on == True):
            CoM.set_visible(True)
    
    return axis.scatter(x, y, z)

#Create the plots and set their initial conditions
fig = plt.figure(0)
axis = fig.add_subplot(111, projection='3d')
spd = fig.add_subplot(331, label = "speed", title = "Average speed (m/s)")
CoM = fig.add_subplot(333, label = "CoM", title = "Center of Mass (X,Y)")
spd.set_visible(False)
CoM.set_visible(False)

#Run the animation
anim = animation.FuncAnimation(fig, update_particles, num_ticks, interval = 1, blit = False, repeat = False)
plt.show()