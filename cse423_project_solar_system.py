from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random


paused=False
speed_mult= 1.0
orbital_mode= True  
cam_angle= 45.0    
cam_yheight = 600.0  
cam_r = 1200.0  

moon_cam=False         


planet_angles= [0.0] * 8
moon_angle= 0.0      

MOON_ORBIT_R= 42
MOON_SIZE= 7

random.seed(7)

STARS=[]                       

for i in range(350):               
    x=random.uniform(-2000, 2000) 
    y=random.uniform(-600, 600)   
    z=random.uniform(-2000, 2000)
    star=(x, y, z)               
    STARS.append(star)             



PLANETS =[
    ("Mercury", 160,  10,  0.72, 0.72, 0.72,  4.74),
    ("Venus",   240,  18,  0.95, 0.78, 0.30,  3.50),
    ("Earth",   330,  20,  0.20, 0.52, 0.92,  2.98),
    ("Mars",    420,  14,  0.85, 0.28, 0.10,  2.41),
    ("Jupiter", 550,  46,  0.82, 0.62, 0.42,  1.31),
    ("Saturn",  680,  38,  0.92, 0.82, 0.52,  0.97),
    ("Uranus",  790,  28,  0.48, 0.82, 0.92,  0.68),
    ("Neptune", 900,  26,  0.18, 0.28, 0.92,  0.54),
]





selfRotation_own_axis_angles = [0.0] * 8

SelfRotation_own_axis_speedss = [0.8, 0.5, 12.0, 6.0, 320.0, 250.0, 105.0, 68.0]


Asteroid_Belt_angless = 0.0
random.seed(42)
Astreroid_listss = [
    (
        random.uniform(450, 520),           
        random.uniform(0, 360),             
        random.uniform(-8, 8),             
        random.uniform(2, 5),               
        random.uniform(0.35, 0.85)          
    )
    for _ in range(350)
]


planet_tail_length= 30 
planet_tail_tracker_lists= [[] for _ in range(8)] 

comet_t  = 0.0
COMET_Ar     = 900.0
COMET_Br     = 350.0
comet_trail = []
TRAIL_MAX   = 90

blackhole_X              = -1050.0    
blackhole_Z              = -1050.0    
blackhole_Radius         = 70.0
blackhole_pulls = 15.0
blackhole_consume_area_distance = 50.0
blackhole_absorbing_counter = 0

blackhole_camera = False   

focuss_plnet = -1   
focuss_cam    = False


gametimee       = False     
gamee_over       = False     
gamescore           = 0
gamelive           = 3

spstation_angle   = 0.0       

probes          = []        
PROBE_SPEED     = 18.0
PROBE_RADIUS    = 6.0       

ships          = []        
ships_radi    = 20.0      
ships_sp     = 5.5
MAX_ships      = 15       
ships_spawntimer = 0.0     
ships_spawnrate  = 40.0    

comet2_position_  = [-600.0, 0.0, -600.0]   
comet2_speed_  = [-3.5, 0.0, -4]    

comet2_tail_tracker = []
tail2_max   = 90




def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)



def Get_planetPosition_track(idx):
    _, orb_r, _, _, _, _, _ = PLANETS[idx]
    if orbital_mode:
        rad = math.radians(planet_angles[idx])
        return orb_r * math.cos(rad), orb_r * math.sin(rad)
    else:
        return float(orb_r), 0.0


def get_moon_world_pos():

    ex, ez = Get_planetPosition_track(2)         
    mrad   = math.radians(moon_angle)
    mx = ex + MOON_ORBIT_R * math.cos(mrad)
    my = 0.0
    mz = ez + MOON_ORBIT_R * math.sin(mrad)
    return mx, my, mz

def comet_world_pos(t):
    x = COMET_Ar * math.cos(t) - (COMET_Ar - COMET_Br)
    z = COMET_Br * math.sin(t)
    return x, 0.0, z 


def draw_stars():
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(2)
    glBegin(GL_POINTS)
    for (sx, sy, sz) in STARS:
        glVertex3f(sx, sy, sz)
    glEnd()
    glPointSize(1)


def draw_sun():
    glPushMatrix()
    glColor3f(1.0, 0.92, 0.10)
    gluSphere(gluNewQuadric(), 68, 28, 28)
    glColor3f(1.0, 0.42, 0.00)  
    gluSphere(gluNewQuadric(), 74, 18, 18)
    glPopMatrix()


def draw_orbit_ring(orb_r):
    glColor3f(0.55, 0.55, 0.55)
    glPointSize(1)
    glBegin(GL_POINTS)
    steps = 5000
    for i in range(steps):
        a = 2.0 * math.pi * i / steps
        glVertex3f(orb_r * math.cos(a), 0.0, orb_r * math.sin(a))
    glEnd()

def draw_orbit_trails():
    glPointSize(1)
    steps = 200 
    for (name, orb_r, size, r, g, b, _) in PLANETS:
        glColor3f(r * 0.4, g * 0.4, b * 0.4)
        glBegin(GL_POINTS)
        for i in range(steps):
            a = 2.0 * math.pi * i / steps
            glVertex3f(orb_r * math.cos(a), 0.0, orb_r * math.sin(a))
        glEnd()


def draw_planet(idx):
    name, orb_r, size, r, g, b, _ = PLANETS[idx]
    px, pz = Get_planetPosition_track(idx)

    glPushMatrix()
    glTranslatef(px, 0.0, pz)

    glColor3f(r, g, b)
    gluSphere(gluNewQuadric(), size, 22, 22)

    glPushMatrix()
    glRotatef(selfRotation_own_axis_angles[idx], 0.0, 1.0, 0.0)

    glPushMatrix()
    glRotatef(27.0, 1.0, 0.0, 0.0)
    glRotatef(90.0, 1.0, 0.0, 0.0)
    equitorial_Band_heightt = size * 0.18
    equitorial_Band_radius = size * 1.01
    glColor3f(
        min(r * 1.4, 1.0),
        min(g * 1.4, 1.0),
        min(b * 1.4, 1.0)
    )
    glTranslatef(0.0, 0.0, -equitorial_Band_heightt / 2)
    gluCylinder(gluNewQuadric(), equitorial_Band_radius, equitorial_Band_radius, equitorial_Band_heightt, 28, 1)
    glPopMatrix()

    if idx == 5:
        glPushMatrix()
        glRotatef(27.0, 1.0, 0.0, 0.0) 

        inner_r = size * 1.25
        outer_r = size * 1.75
        steps   = 60

        for ringLayer in range(4):
            t0 = ringLayer / 4
            t1 = (ringLayer + 1) / 4
            r0 = inner_r + (outer_r - inner_r) * t0
            r1 = inner_r + (outer_r - inner_r) * t0 + (outer_r - inner_r) * 0.12

            if ringLayer % 2 == 0:
                glColor3f(0.85, 0.78, 0.55) 
            else:
                glColor3f(0.65, 0.58, 0.38) 

            glBegin(GL_QUADS)
            for i in range(steps):
                a0 = 2.0 * math.pi * i / steps
                a1 = 2.0 * math.pi * (i + 1) / steps

                glVertex3f(r0 * math.cos(a0), 0.0, r0 * math.sin(a0))
                glVertex3f(r1 * math.cos(a0), 0.0, r1 * math.sin(a0))
                glVertex3f(r1 * math.cos(a1), 0.0, r1 * math.sin(a1))
                glVertex3f(r0 * math.cos(a1), 0.0, r0 * math.sin(a1))
            glEnd()

        glPopMatrix() 
    glPopMatrix() 

    if idx == 2:
        glPushMatrix()
        mrad = math.radians(moon_angle)
        glTranslatef(
            MOON_ORBIT_R * math.cos(mrad),
            0.0,
            MOON_ORBIT_R * math.sin(mrad)
        )
        glColor3f(0.85, 0.85, 0.85)
        gluSphere(gluNewQuadric(), MOON_SIZE, 12, 12)
        glPopMatrix()

    glPopMatrix() 

    
def draw_comet():
    n = len(comet_trail)
    glPointSize(3)
    glBegin(GL_POINTS)
    for i, (tx, ty, tz) in enumerate(comet_trail):
        b = (i + 1) / max(n, 1)
        glColor3f(b, b, b * 0.55)
        glVertex3f(tx, ty, tz)
    glEnd()
    glPointSize(1)

    cx, cy, cz = comet_world_pos(comet_t)
    glPushMatrix()
    glTranslatef(cx, cy, cz)
    glColor3f(1.0, 1.0, 0.7)
    gluSphere(gluNewQuadric(), 14, 14, 14)
    glColor3f(1.0, 1.0, 1.0)
    gluSphere(gluNewQuadric(), 7, 10, 10)
    glPopMatrix()

def comet2_drawing():
    n = len(comet2_tail_tracker)
    glPointSize(3)
    glBegin(GL_POINTS)
    for i, (tx, ty, tz) in enumerate(comet2_tail_tracker):
        b = (i + 1) / max(n, 1)
        glColor3f(b, b * 0.3, 0.0)  
        glVertex3f(tx, ty, tz)
    glEnd()
    glPointSize(1)

    glPushMatrix()
    glTranslatef(comet2_position_[0], comet2_position_[1], comet2_position_[2])
    glColor3f(1.0, 0.5, 0.2)        
    gluSphere(gluNewQuadric(), 12, 14, 14)
    glColor3f(1.0, 0.8, 0.6)        
    gluSphere(gluNewQuadric(), 6, 10, 10)
    glPopMatrix()

def draw_comet_orbit_guide():
    glColor3f(0.38, 0.38, 0.25)
    glPointSize(1)
    glBegin(GL_POINTS)
    steps = 800
    for i in range(steps):
        t  = 2.0 * math.pi * i / steps
        cx = COMET_Ar * math.cos(t) - (COMET_Ar - COMET_Br)
        cz = COMET_Br * math.sin(t)
        glVertex3f(cx, 0.0, cz)
    glEnd()

def asteroid_belt_drawing():
    glPushMatrix()
    glRotatef(Asteroid_Belt_angless, 0.0, -1.0, 0.0)

    for (orb_r, start_angle, y_offset, ast_size, shade) in Astreroid_listss:
        glPushMatrix()

        radian = math.radians(start_angle)
        ax  = orb_r * math.cos(radian)
        az  = orb_r * math.sin(radian)

        glTranslatef(ax, y_offset, az)
        glColor3f(shade, shade, shade)     
        glutSolidCube(ast_size)

        glPopMatrix()

    glPopMatrix()

def Planet_tail_drawing():
    glPointSize(5)
    for i in range(8):
        trail = planet_tail_tracker_lists[i]
        n = len(trail)
        if n < 2:
            continue
        glBegin(GL_POINTS)
        for j, (tx, tz) in enumerate(trail):
            if j < 7:
                continue
            if j % 2 == 0:
                continue

            alpha = (j + 1) / n

            if alpha < 0.5:
                r = alpha * 2.0
                g = alpha * 1.0
                b = 0.0
            else:
                r = 1.0
                g = min(alpha * 1.4, 1.0)
                b = min((alpha - 0.5) * 0.6, 1.0)

            glColor3f(r, g, b)
            glVertex3f(tx, 0.0, tz)
        glEnd()
    glPointSize(1)


def ships_spawning():
    ex, ez = Get_planetPosition_track(2)

    angle  = random.uniform(0, 2 * math.pi)
    dist   = random.uniform(280.0, 380.0)   

    ax = ex + dist * math.cos(angle)
    az = ez + dist * math.sin(angle)

    dx = ex - ax
    dz = ez - az
    mag = math.sqrt(dx * dx + dz * dz) + 0.001
    vx = (dx / mag) * ships_sp
    vz = (dz / mag) * ships_sp

    ships.append([ax, 0.0, az, vx, vz])



def probes_drawing():
    for (px, py, pz, vx, vy, vz) in probes:
        glPushMatrix()
        glTranslatef(px, py, pz)

        glColor3f(1.0, 0.9, 0.2)
        gluSphere(gluNewQuadric(), PROBE_RADIUS, 10, 10)

        glColor3f(1.0, 0.5, 0.0)
        gluSphere(gluNewQuadric(), PROBE_RADIUS * 1.4, 8, 8)

        glPopMatrix()

def ships_drawing():
    for (ax, ay, az, vx, vz) in ships:
        glPushMatrix()
        glTranslatef(ax, ay, az)

        glColor3f(0.2, 0.9, 0.3)    
        steps = 36
        inner_r = 8.0
        outer_r = ships_radi

        glBegin(GL_QUADS)
        for i in range(steps):
            a0 = 2.0 * math.pi * i       / steps
            a1 = 2.0 * math.pi * (i + 1) / steps
            glVertex3f(inner_r * math.cos(a0), 0.0, inner_r * math.sin(a0))
            glVertex3f(outer_r * math.cos(a0), 0.0, outer_r * math.sin(a0))
            glVertex3f(outer_r * math.cos(a1), 0.0, outer_r * math.sin(a1))
            glVertex3f(inner_r * math.cos(a1), 0.0, inner_r * math.sin(a1))
        glEnd()

        glColor3f(0.5, 1.0, 0.5)
        gluSphere(gluNewQuadric(), inner_r, 12, 12)

        glColor3f(0.0, 1.0, 0.2)
        glPointSize(3)
        glBegin(GL_POINTS)
        for i in range(steps):
            a = 2.0 * math.pi * i / steps
            glVertex3f(outer_r * math.cos(a), 0.0, outer_r * math.sin(a))
        glEnd()
        glPointSize(1)

        glPopMatrix()

def spstation_drawing():
    ex, ez = Get_planetPosition_track(2)   

    glPushMatrix()
    glTranslatef(ex, 0.0, ez)         
    glRotatef(spstation_angle, 0.0, 1.0, 0.0)  

    spstation_ORBIT = 55.0  

    arm_angles = [0, 90, 180, 270]
    for a in arm_angles:
        glPushMatrix()
        glRotatef(a, 0.0, 1.0, 0.0)
        glTranslatef(spstation_ORBIT, 0.0, 0.0)
        glColor3f(0.6, 0.6, 0.7)
        gluSphere(gluNewQuadric(), 5, 10, 10)  
        glPopMatrix()

    glColor3f(0.5, 0.5, 0.6)
    glPointSize(3)
    glBegin(GL_POINTS)
    steps = 120
    for i in range(steps):
        a = 2.0 * math.pi * i / steps
        glVertex3f(
            spstation_ORBIT * math.cos(a),
            0.0,
            spstation_ORBIT * math.sin(a)
        )
    glEnd()
    glPointSize(1)

    glColor3f(0.8, 0.8, 0.9)
    gluSphere(gluNewQuadric(), 8, 12, 12)

    glPopMatrix()

def Blackhole_drawing():
    glPushMatrix()
    glTranslatef(blackhole_X, 0.0, blackhole_Z)

    glColor3f(0.0, 0.0, 0.0)
    gluSphere(gluNewQuadric(), blackhole_Radius, 28, 28)

    glColor3f(0.04, 0.0, 0.06)
    gluSphere(gluNewQuadric(), blackhole_Radius * 1.12, 20, 20)

    glPointSize(3)
    num_arms   = 3
    arm_points = 120
    max_radius = blackhole_Radius * 3.2

    for arm in range(num_arms):
        arm_offset = (360.0 / num_arms) * arm
        glBegin(GL_POINTS)
        for k in range(arm_points):
            t      = k / arm_points
            angle  = math.radians(arm_offset + t * 420.0)
            radius = blackhole_Radius * 1.1 + (max_radius - blackhole_Radius * 1.1) * t
            sx     = radius * math.cos(angle)
            sz     = radius * math.sin(angle)
            brightness = 1.0 - t
            glColor3f(
                brightness * 0.5,
                brightness * 0.0,
                brightness * 0.8
            )
            glVertex3f(sx, 0.0, sz)
        glEnd()

    glPushMatrix()
    glRotatef(90, 1.0, 0.0, 0.0)
    inner_r = blackhole_Radius * 1.05
    outer_r = blackhole_Radius * 1.5
    steps   = 60
    glColor3f(0.18, 0.0, 0.28)
    glBegin(GL_QUADS)
    for i in range(steps):
        a0 = 2.0 * math.pi * i / steps
        a1 = 2.0 * math.pi * (i + 1) / steps
        glVertex3f(inner_r * math.cos(a0), inner_r * math.sin(a0), 0.0)
        glVertex3f(outer_r * math.cos(a0), outer_r * math.sin(a0), 0.0)
        glVertex3f(outer_r * math.cos(a1), outer_r * math.sin(a1), 0.0)
        glVertex3f(inner_r * math.cos(a1), inner_r * math.sin(a1), 0.0)
    glEnd()
    glPopMatrix()

    glPointSize(1)
    glPopMatrix()


def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, 1.25, 1.0, 6000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if moon_cam:
        mx, my, mz = get_moon_world_pos()
        ex, ez     = Get_planetPosition_track(2)

        dx  = mx - ex
        dz  = mz - ez
        mag = math.sqrt(dx * dx + dz * dz) + 0.001
        ux, uz = dx / mag, dz / mag

        offset = MOON_SIZE * 3 + 10
        cam_x  = mx + ux * offset
        cam_y  = my + MOON_SIZE * 2
        cam_z  = mz + uz * offset

        gluLookAt(
            cam_x, cam_y, cam_z,
            ex,    0.0,   ez,
            0.0,   1.0,   0.0
        )

    elif gametimee:
        ex, ez = Get_planetPosition_track(2)
        rad    = math.radians(cam_angle)
        cam_x  = ex + 350.0 * math.sin(rad)
        cam_z  = ez + 350.0 * math.cos(rad)
        gluLookAt(
            cam_x, 180.0, cam_z,  
            ex,      0.0, ez,      
            0.0,     1.0,  0.0
        )

    elif focuss_cam:
        px, pz = Get_planetPosition_track(focuss_plnet)
        _, orb_r, size, _, _, _, _ = PLANETS[focuss_plnet]

        cam_x = px * 1.15
        cam_y = size * 6.0 + 80.0
        cam_z = pz * 1.15

        gluLookAt(
            cam_x, cam_y, cam_z,  
            px,    0.0,   pz,      
            0.0,   1.0,   0.0      
        )

    elif blackhole_camera:
        cam_x = blackhole_X + 80.0
        cam_y = 200.0
        cam_z = blackhole_Z + 80.0

        target_x = comet2_position_[0]
        target_y = comet2_position_[1]
        target_z = comet2_position_[2]

        gluLookAt(
            cam_x,    cam_y,    cam_z,
            target_x, target_y, target_z,
            0.0,      1.0,      0.0
        )

    else:
        rad   = math.radians(cam_angle)
        cam_x = cam_r * math.sin(rad)
        cam_z = cam_r * math.cos(rad)
        cam_y = cam_yheight

        gluLookAt(
            cam_x, cam_y, cam_z,
            0.0,   0.0,   0.0,
            0.0,   1.0,   0.0
        )


def keyboardListener(key, x, y):
    global paused, speed_mult, orbital_mode, moon_cam, blackhole_camera
    global planet_angles, moon_angle, comet_t, comet_trail
    global comet2_position_, comet2_speed_, comet2_tail_tracker
    global gametimee, gamee_over, gamescore, gamelive
    global probes, ships, ships_spawntimer, spstation_angle

    if key == b' ':
        paused = not paused

    elif key in (b'+', b'='):
        speed_mult = min(speed_mult + 0.2, 5.0)

    elif key in (b'-', b'_'):
        speed_mult = max(speed_mult - 0.2, 0.2)

    elif key == b's':
        orbital_mode = not orbital_mode

    elif key == b'm':
        moon_cam = not moon_cam
        blackhole_camera   = False   

    elif key == b'b':
        blackhole_camera   = not blackhole_camera
        moon_cam = False   

    elif key in (b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8'):
        global focuss_plnet, focuss_cam
        idx = int(key.decode()) - 1
        if focuss_cam and focuss_plnet == idx:
            focuss_cam    = False
            focuss_plnet = -1
        else:
            focuss_plnet = idx
            focuss_cam    = True
            moon_cam     = False
            blackhole_camera       = False

    elif key == b'f':
        if gametimee and not gamee_over:
            global probes, spstation_angle

            ex, ez        = Get_planetPosition_track(2)
            spstation_ORBIT = 55.0

            rad   = math.radians(cam_angle)
            cam_x = ex + 350.0 * math.sin(rad)
            cam_z = ez + 350.0 * math.cos(rad)

            dx = ex - cam_x
            dz = ez - cam_z
            mag = math.sqrt(dx * dx + dz * dz) + 0.001
            dx /= mag
            dz /= mag

            sx = ex + spstation_ORBIT * dx
            sy = 0.0
            sz = ez + spstation_ORBIT * dz

            vx = dx * PROBE_SPEED
            vz = dz * PROBE_SPEED

            probes.append([sx, sy, sz, vx, 0.0, vz])

    elif key == b'g':
        
        
        gametimee = not gametimee
        if gametimee:
            gamee_over         = False
            gamescore             = 0
            gamelive             = 3
            probes            = []
            ships            = []
            ships_spawntimer = 0.0
            spstation_angle     = 0.0
            moon_cam    = False
            blackhole_camera      = False
            focuss_cam   = False
            focuss_plnet = -1


    elif key == b'r':
        if gametimee:
            gamee_over         = False
            gamescore             = 0
            gamelive             = 3
            probes            = []
            ships            = []
            ships_spawntimer = 0.0
            spstation_angle     = 0.0
        else:
            planet_angles = [0.0] * 8
            moon_angle    = 0.0
            comet_t       = 0.0
            comet_trail.clear()
            comet2_position_[0] = -600.0
            comet2_position_[1] = 0.0
            comet2_position_[2] = -600.0
            comet2_speed_[0] = -3.5
            comet2_speed_[1] = 0.0
            comet2_speed_[2] = -4.0
            comet2_tail_tracker.clear()
            moon_cam      = False
            blackhole_camera        = False
            speed_mult= 1.0


    glutPostRedisplay()


def specialKeyListener(key, x, y):

    global cam_angle, cam_yheight

    if not moon_cam and not gametimee:
        if key == GLUT_KEY_LEFT:
            cam_angle -= 3.0
        if key == GLUT_KEY_RIGHT:
            cam_angle += 3.0
        if key == GLUT_KEY_UP:
            cam_yheight = min(cam_yheight + 35.0, 1800.0)
        if key == GLUT_KEY_DOWN:
            cam_yheight = max(cam_yheight - 35.0, 20.0)

    if gametimee:
        if key == GLUT_KEY_LEFT:
            cam_angle -= 3.0
        if key == GLUT_KEY_RIGHT:
            cam_angle += 3.0

    glutPostRedisplay()






def idle():
    global planet_angles, moon_angle, comet_t, comet_trail
    global selfRotation_own_axis_angles, Asteroid_Belt_angless, planet_tail_tracker_lists
    global comet2_position_, comet2_speed_, comet2_tail_tracker, blackhole_absorbing_counter
    global spstation_angle, probes
    global gamelive, gamee_over, ships, ships_spawntimer, gamescore

    if not paused:
        dt = 0.31 * speed_mult

        for i, (name, orb_r, size, r, g, b, spd) in enumerate(PLANETS):
            planet_angles[i] = (planet_angles[i] + spd * dt) % 360.0

        for i in range(8):
            px, pz = Get_planetPosition_track(i)
            planet_tail_tracker_lists[i].append((px, pz))
            if len(planet_tail_tracker_lists[i]) > planet_tail_length:
                planet_tail_tracker_lists[i].pop(0)

        for i in range(8):
            selfRotation_own_axis_angles[i] = (selfRotation_own_axis_angles[i] + SelfRotation_own_axis_speedss[i] * 0.05 * speed_mult) % 360.0

        moon_angle = (moon_angle + 9.0 * dt) % 360.0

        cx, _, cz   = comet_world_pos(comet_t)
        dist        = math.sqrt(cx * cx + cz * cz) + 40.0
        comet_speed = 700.0 / dist * dt
        comet_t     = (comet_t + comet_speed) % (2.0 * math.pi)
        pos = comet_world_pos(comet_t)
        comet_trail.append(pos)
        if len(comet_trail) > TRAIL_MAX:
            comet_trail.pop(0)

        sun_dx   = -comet2_position_[0]
        sun_dz   = -comet2_position_[2]
        sun_distance = math.sqrt(sun_dx * sun_dx + sun_dz * sun_dz) + 1.0
        sun_pull = 60.0 / (sun_distance * sun_distance) * dt
        comet2_speed_[0] += sun_dx / sun_distance * sun_pull
        comet2_speed_[2] += sun_dz / sun_distance * sun_pull

        bh_dx   = blackhole_X - comet2_position_[0]
        bh_dz   = blackhole_Z - comet2_position_[2]
        bh_distance = math.sqrt(bh_dx * bh_dx + bh_dz * bh_dz) + 1.0
        Blackhole_pulls = blackhole_pulls * (1000.0 / (bh_distance * bh_distance)) * dt
        comet2_speed_[0] += bh_dx / bh_distance * Blackhole_pulls
        comet2_speed_[2] += bh_dz / bh_distance * Blackhole_pulls

        comet2_position_[0] += comet2_speed_[0] * dt
        comet2_position_[2] += comet2_speed_[2] * dt

        bh_dx_new   = blackhole_X - comet2_position_[0]
        bh_dz_new   = blackhole_Z - comet2_position_[2]
        bh_distance_new = math.sqrt(bh_dx_new * bh_dx_new + bh_dz_new * bh_dz_new)

        if bh_distance_new < blackhole_consume_area_distance:
            comet2_position_[0] = -600.0
            comet2_position_[1] = 0.0
            comet2_position_[2] = -600.0
            comet2_speed_[0] = -3.5
            comet2_speed_[1] = 0.0
            comet2_speed_[2] = -4.0
            comet2_tail_tracker.clear()
            blackhole_absorbing_counter += 1

        if abs(comet2_position_[0]) > 2500 or abs(comet2_position_[2]) > 2500:
            comet2_position_[0] = -600.0
            comet2_position_[1] = 0.0
            comet2_position_[2] = -600.0
            comet2_speed_[0] = -3.5
            comet2_speed_[1] = 0.0
            comet2_speed_[2] = -4.0
            comet2_tail_tracker.clear()

        comet2_tail_tracker.append((comet2_position_[0], comet2_position_[1], comet2_position_[2]))
        if len(comet2_tail_tracker) > tail2_max:
            comet2_tail_tracker.pop(0)

        Asteroid_Belt_angless    = (Asteroid_Belt_angless    + 0.08 * speed_mult) % 360.0
        spstation_angle = (spstation_angle + 1.5  * speed_mult) % 360.0

        if gametimee and not gamee_over:

            ships_spawntimer += 1.0
            if ships_spawntimer >= ships_spawnrate and len(ships) < MAX_ships:
                ships_spawning()
                ships_spawntimer = 0.0

            ex, ez = Get_planetPosition_track(2)

            for probe in probes:
                probe[0] += probe[3]  
                probe[1] += probe[4]  
                probe[2] += probe[5]   

            probes[:] = [
                p for p in probes
                if abs(p[0] - ex) < 500 and abs(p[2] - ez) < 500
            ]

            for alien in ships:
                dx  = ex - alien[0]
                dz  = ez - alien[2]
                mag = math.sqrt(dx * dx + dz * dz) + 0.001
                alien[3] = (dx / mag) * ships_sp
                alien[4] = (dz / mag) * ships_sp
                alien[0] += alien[3]
                alien[2] += alien[4]

            hits_probes = set()
            hits_ships = set()
            for pi, probe in enumerate(probes):
                for ai, alien in enumerate(ships):
                    dx   = probe[0] - alien[0]
                    dz   = probe[2] - alien[2]
                    dist = math.sqrt(dx * dx + dz * dz)
                    if dist < (PROBE_RADIUS + ships_radi):
                        hits_probes.add(pi)
                        hits_ships.add(ai)
                        gamescore += 1

            probes[:] = [p for i, p in enumerate(probes) if i not in hits_probes]
            ships[:] = [a for i, a in enumerate(ships) if i not in hits_ships]

            earth_r       = PLANETS[2][2]
            hit_threshold = earth_r + ships_radi
            for alien in ships[:]:
                dx   = alien[0] - ex
                dz   = alien[2] - ez
                dist = math.sqrt(dx * dx + dz * dz)
                if dist < hit_threshold:
                    ships.remove(alien)
                    gamelive -= 1
                    if gamelive <= 0:
                        gamelive     = 0
                        gamee_over = True

    glutPostRedisplay()




def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    glEnable(GL_DEPTH_TEST)

    setupCamera()

    draw_stars()
    draw_orbit_trails()
    if orbital_mode:
        for (_, orb_r, *__) in PLANETS:
            draw_orbit_ring(orb_r)
        draw_comet_orbit_guide()

    draw_sun()
    Planet_tail_drawing()
    asteroid_belt_drawing()
    for i in range(8):
        draw_planet(i)

    draw_comet()
    comet2_drawing()
    Blackhole_drawing()
    if gametimee:
        spstation_drawing()
        ships_drawing()
        probes_drawing()



    if gametimee:
        draw_text(10, 670, f"gamescore: {gamescore}        gamelive: {gamelive}")
        draw_text(10, 640, "[F] Fire Probe   [G] Exit Game")

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 800)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glPointSize(14)
        glBegin(GL_POINTS)
        for i in range(gamelive):
            if gamelive == 3:
                glColor3f(0.0, 1.0, 0.0)  
            elif gamelive == 2:
                glColor3f(1.0, 0.8, 0.0)   
            else:
                glColor3f(1.0, 0.1, 0.1)  
            glVertex3f(200 + i * 28, 670, 0)
        glEnd()
        glPointSize(1)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        if gamee_over:
            draw_text(340, 380, "GAME  OVER", GLUT_BITMAP_TIMES_ROMAN_24)
            draw_text(300, 340, f"Final gamescore: {gamescore}", GLUT_BITMAP_TIMES_ROMAN_24)
            draw_text(270, 300, "[R] Play Again   [G] Exit Game", GLUT_BITMAP_HELVETICA_18)


    mode_str  = "ORBITAL"  if orbital_mode else "LINED-UP"
    state_str = "PAUSED"   if paused       else "RUNNING"
    if focuss_cam:
        cam_str = f"FOCUS: {PLANETS[focuss_plnet][0]}"
    elif moon_cam:
        cam_str = "MOON-CAM"
    elif blackhole_camera:
        cam_str = "BH-CAM"
    else:
        cam_str = "FREE-CAM"

    if not gametimee:
        draw_text(10, 705, f"Mode: {mode_str}    Status: {state_str}    Speed: {speed_mult:.1f}x")
        draw_text(10, 726, f"Black Hole Absorptions: {blackhole_absorbing_counter}")
        draw_text(10, 684,  "[SPACE] Pause   [S] Lined-Up/Orbital   [+/-] Speed   [R] Reset")
        draw_text(10, 662,  "[M] Moon Cam   [B] BH Cam   [1-8] Focus Planet   Arrows: orbit/raise camera")

    glutSwapBuffers()




def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Solar Sytem")

    glClearColor(0.0, 0.0, 0.02, 1.0)

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutIdleFunc(idle)

    glutMainLoop()


if __name__ == "__main__":
    main()
