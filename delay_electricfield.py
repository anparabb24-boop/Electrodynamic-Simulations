import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib import cm
from matplotlib.colors import LightSource
ls = LightSource(azdeg=315, altdeg=65)

#lines 6 to 34 define the axes and the size.

plt.rcParams['figure.facecolor'] = "#121111"
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor("#121111")
ax.set_axis_off()

#define all constants
x_l = 30
y_l = 30
z_l = 30
freq = 1/4
q = 2
k = 9000000000
R = 5
c = 0.4


# 1. Define the Origin
origin = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

# 3. Draw the Axes as solid lines spanning the frame
# We draw each axis from -50 to 50 to match your set_xlim/ylim/zlim
ax.plot([-x_l, x_l], [0, 0], [0, 0], color="#337BA4", linewidth=2) # X-axis
ax.plot([0, 0], [-y_l, y_l], [0, 0], color='#337BA4', linewidth=2) # Y-axis
ax.plot([0, 0], [0, 0], [-z_l, z_l], color='#337BA4', linewidth=2) # Z-axis

# 5. Add text labels for the axes
ax.text(x_l, 0, 0, "X", color='white', fontsize=12)
ax.text(0, y_l, 0, "Y", color='white', fontsize=12)
ax.text(0, 0, z_l, "Z", color='white', fontsize=12)

# Set limits so the arrows aren't cut off
ax.set_xlim([-x_l/2, x_l/2])
ax.set_ylim([-y_l/2, y_l/2])
ax.set_zlim([-z_l/2, z_l/2])

#the code for geomtry begins here

# Create a grid of points on the XY plane
x = np.linspace(-x_l, x_l, 40)
y = np.linspace(-y_l, y_l, 40)
X, Y = np.meshgrid(x, y)

# Set the Z-level (e.g., the "floor" of your simulation)
Z = np.zeros_like(X)

#cmap = cm.get_cmap('jet')
colors = "#337BA4"

p = [ax.scatter(0,0,0,color="#C32828",s=300)]

def update(frame):
    x_pos = 0
    y_pos = 0
    z_pos = R * np.sin(freq * frame)
    norm = plt.Normalize(vmin=0, vmax=30)


    # 1. Remove the old point from the previous frame
    p[0].remove()
    p[0] = ax.scatter(x_pos,y_pos,z_pos,color="#C32828",s=300)

    # 2. Calculate distance from EVERY grid point to the ORIGIN 
    # (or wherever the charge orbits) to estimate the delay
    dist_to_center = np.sqrt(X**2 + Y**2 + Z**2)
    
    # 3. Calculate the delay 
    delay = dist_to_center / c
    delayed_frame = frame - delay
    
    # 4. Calculate where the charge WAS when it "sent" the signal to that point
    x_del  = R * np.cos(freq * delayed_frame)
    y_del = R * np.cos(freq * delayed_frame)
    #z_del = R * np.sin(freq * delayed_frame)
    
    # 5. Field vectors point away 
    dx = X - 0
    dy = Y - 0
    dz = Z - x_del
    
    
    r2 = dx**2 + dy**2 + dz**2 + 0.01
    r = np.sqrt(r2)
    
    # E = k / r^2. 
    U = k*q*dx / (r**2)
    V = k*q*dy / (r**2)
    W = k*q*dz / (r**2)

    # Normalize the vectors so they don't look messy
    mag = np.sqrt(U**2 + V**2 + W**2)
    #colors = cmap(norm(mag.flatten()))
    U, V, W = U/mag, V/mag, W/mag
    
    # Plot the field
    # We use a list 'field' to manage removal just like 'V' and 'P'
    global field
    if 'field' in globals(): field.remove()
    
    field = ax.quiver(X, Y, Z, U, V, W, length=3, color=colors, alpha=0.5)
   
    
    # 4. Handle camera rotation
    ax.view_init(elev=15+np.sin(frame/63)*21, azim=45+frame/2)
    
    return []


ani = FuncAnimation(fig, update, frames=256, interval=50, blit=False)

plt.tight_layout()
#plt.show()

writer = FFMpegWriter(fps=24, bitrate=2000)
ani.save("Circular polarization.mp4", writer=writer)

print("Export Complete")