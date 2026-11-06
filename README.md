# Rocket Roll Lab

An interactive 3D tool that shows why the **roll rate a rocket's IMU gyro measures** is not the same thing as the **roll angle measured against the world** (the Euler roll φ), and why a world-referenced "zero-roll" direction breaks down at certain orientations.

It is a single self-contained HTML file with no install, no server and no network access needed.

## Run it

- **Locally:** download `index.html` and open it in any modern browser.
- **GitHub Pages:** go to Settings → Pages, set the source to the `main` branch at `/ (root)`, and open the URL it gives you.

## What's inside

### Tab 1: Gyro vs world roll

A rocket flies under body rates you control (p, q, r in °/s). The tool shows, side by side:

| IMU (body frame) | World (Euler angles) |
|---|---|
| Gyro rates p, q, r | Roll φ, pitch θ, yaw ψ |
| Each rate added up over time (∫p, ∫q, ∫r) | Rate of change of each angle |

The 3D view shows the body axes, the world axes, the amber **zero-roll fin direction** with the roll arc φ, and a trail of where the nose has pointed. A 20 s plot compares φ with ∫p. A live readout breaks the world roll rate into the part from p and the part leaking in from q and r:

```
φ̇ = p + (q·sin φ + r·cos φ)·tan θ
```

**Scenarios**

1. **Level flight, pure roll:** world roll and ∫p match.
2. **Tilted 60°, pure roll:** they still match, because q = r = 0.
3. **Tilted, body yaw only (p = 0):** world roll swings ±50° while the roll gyro reads 0.
4. **Coning wobble (p = 0):** world roll climbs about 8° per cycle, by the solid angle the nose's circle encloses.
5. **On the pad, pure roll:** horizon-referenced roll is undefined at θ = 90°, so the spin shows up as yaw.
6. **3° off vertical, tiny yaw rate:** small body rates become large world roll and yaw rates.
7. **Free fly:** your own rates and start attitude.

**Convention toggle:** horizon-referenced (aircraft ZYX, undefined with the nose straight up) or vertical-referenced (launch frame, undefined with the nose along North/South, the crossrange axis).

### Tab 2: Amber line builder

This tab breaks the zero-roll direction into the conditions that define it:

1. At 90° to the nose
2. At 90° to a world reference axis (Up, North, East or custom)
3. Unit length (normalized)
4. A sign rule that picks one of the two opposite candidates

Switch the conditions on and off to see the allowed fin directions narrow from the whole sphere, to a circle, to two opposite lines, to one line. It also shows:

- **Raw cross product view (condition 3 off):** the arrow's length is sin(angle to axis), so normalizing magnifies sideways nose motion by 1 / sin(angle).
- **Nose motion modes:** manual, a circle (that does or doesn't enclose the axis) and a pass-by with adjustable miss distance.
- **Field view:** the amber line drawn for about 420 nose directions at once. The two points where it can't be defined are visible, and they can be moved but not removed.
- **Measured vs predicted:** how fast the amber line actually turns compared with the 1 / sin limit, plotted over 12 s.

## Conventions used

- **World frame:** North-East-Down (NED). The tool labels Up explicitly.
- **Body frame:** x = nose (roll, p), y = green fin (pitch, q), z = blue fin (yaw, r).
- **Attitude:** a quaternion integrated from body rates at 240 Hz.
- **Euler angles:** ZYX (yaw → pitch → roll). The vertical-referenced variant applies the same decomposition in an Up-East-North frame.
- **At the singularity** (|cos θ| ≈ 0), φ is set to 0 and the rotation is assigned to ψ.

## Key takeaways for flight software

- Treat the gyro p as "rotation about the nose right now", never as "roll angle so far".
- Integrate attitude as a quaternion (with coning compensation at high wobble rates). Adding up each axis separately loses rotation that comes from the order of the motions.
- Use Euler angles only for display, logging and control targets.
- Pick a convention whose singularity is outside the flight envelope: vertical-referenced during boost, with its singular axis set crossrange.

## Repository layout

```
index.html        built, self-contained app (open this)
src/app.html      app source with a /*THREE*/ placeholder
vendor/           three.js r128 (MIT) and its license
build.py          inlines vendor/three.min.js into src/app.html -> index.html
```

To rebuild after editing `src/app.html`:

```
python3 build.py
```

## Credits

- 3D rendering: [three.js](https://threejs.org) r128, MIT License (see `vendor/three.LICENSE`).
