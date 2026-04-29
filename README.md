# Solar_System_and_Probe_Firing_Game_OpenGL3D

Member 1 - (AIVEE AKTAR 23301568)

1.  Planets orbiting the Sun:  sun+ 8 planets. each planet revolves at different speeds and distances 

2. Pause/Resume + Speed control: spacebar freezes all motion; +/- keys multiply orbital speed up to 5x, letting you watch centuries pass in seconds

3.  Moon orbiting Earth — a small sphere independently orbits Earth using nested transformations inside Earth's push/pop matrix

4. Camera orbit + height control — arrow keys let you swing the camera 360° around the entire system and raise/lower it for dramatic top-down or ground-level views with arrow keys.

5. Static vs Orbital toggle — S key snaps all planets into a neat lineup for comparison, then back to orbiting, like a textbook diagram coming to life

6. Comet with a tail — a small sphere moving in an elliptical orbit with a stretched trail of GL_POINTS fading behind it









MEMBER 2 - ( TANHA TASNIM LOHONA 23201120)

1. Planet rotation on own axis + equitorial band:  Each planet spins on its own axis. A tilted equatorial cylinder band drawn around each planet's middle to make the rotation clearly visible.

2. Saturn's ring system : 4 layered flat rings around Saturn using, alternating between light and dark golden colors It rotates like the equatorial band as the planet moves on its own axis.

3.Asteroid belt :  a band of small randomly-placed spheres between Mars and Jupiter that slowly rotates as a group and are colors of different shades of grey.

4.Planet orbit trail path:Each planet's last 30 world positions are recorded every frame and drew them as dotted GL_POINTS behind each planet, skipping the first 7 positions to create a gap.  An orange-to-yellow gradient that fades toward the tail to create a glowing effect showing each planet's speed and direction. 


5.Blackhole:  A dark sphere placed at the edge of the solar system surrounded by 3 spiral GL_POINTS arms offset 120 degrees apart creating a cyclone swirl effect, with a flat purple disc ring drawn using GL_QUADS around the core.  It lowly pulls the comet 2 towards it.

6.Comet2 (Blackhole comet) : A second orange comet with real position and velocity physics that gets pulled by black hole gravity, curves toward it naturally. disappears on absorption and resets.  An absorption counter shown on the screen. The comet also has a gradient tail like the planet.


7..Black Hole Camera: We added a special camera mode toggled by the B key that positions the camera above and beside the black hole and tracks comet2's position every frame using gluLookAt, so the viewer watches the orange comet get pulled in and absorbed from the black hole's perspective. 

Member 3 - ( MD. MOTAHAR ALI 23201167)


1. Planet focus mode: press 1–8 to snap the camera to follow a specific planet as it orbits, Tracking camera that follows a moving planet's world-space coordinates each frame


Mini Game (Alien Destroyer) — triggered by G key:
Alien spawning — aliens spawn from random directions around Earth 
Alien movement — aliens continuously home toward Earth, recalculating direction every frame
Space station rotation — station orbits around Earth automatically
Probe firing — press F to shoot a probe from the station toward where camera is aimed
Probe movement — fired probes travel forward each frame
Probe vs alien collision detection — probes destroy aliens on contact, awards score
Alien reaches Earth — alien hitting Earth removes it and deducts a life
Score tracking — increments by 1 per alien destroyed
Lives system — starts at 3, decrements when alien reaches Earth
Game over state — triggers when lives hit 0, freezes spawning and movement
Game reset — R key resets score, lives, clears all aliens and probes
Camera orbit around Earth — arrow keys rotate camera around Earth during game mode
Game over screen — displays final score and restart/exit instructions

