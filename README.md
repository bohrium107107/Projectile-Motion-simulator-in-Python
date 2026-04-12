# Physics Simulator

A 2D physics sandbox built with Pygame where you fire balls from a cannon at destructible blocks. Experiment with different materials, gravity settings, and liquids to see how real physics properties affect the simulation.

---

## Features

- **5 ball types** — each with unique mass, bounce, drag, and damage values
- **5 planets** — with accurate gravity values
- **4 liquids** — with buoyancy and drag simulation
- **3 block strengths** — with cracking and shattering visuals
- **Trajectory preview** 
- **Live stats sidebar** — real-time velocity, position, weight, and material data
- **Two game modes** 
- **Fully scalable UI** — adapts to any screen resolution

---

## Requirements

- Python 3.7+
- Pygame

## Controls

| Key | Action |
|-----|--------|
| Click | Fire ball toward mouse |
| R | Reset ball to cannon |
| M | Return to menu |
| B | Cycle ball type |
| L | Cycle liquid type |
| 1-5 | Cycle through planets |
| ↑ / ↓ | Increase / decrease launch speed |
| ESC | Quit |

---

## Physics Overview

### Projectile Motion
The ball is launched at a speed set in km/h, converted to pixels per frame. Each frame applies gravity to vertical velocity and air drag to both axes:

```
ball_vy += gravity * (1/60)
ball_vx *= (1 - drag)
ball_vy *= (1 - drag)
```

### Buoyancy
When the ball enters the liquid pool, full gravity is replaced by net acceleration based on the density difference between the ball and the liquid:

```
net_accel = g * (ball_density - liquid_density) / ball_density
```

A ball denser than the liquid (e.g. iron in water) sinks but slower. A less dense ball (e.g. wood in water) floats upward.

### Block Damage
Damage dealt on collision is proportional to the ball's mass and speed at the moment of impact. Blocks display three visual states (normal → cracked → shattered) based on remaining health. Clay balls shatter on any impact and stop moving.

---

## Design Notes

- The UI is designed around a **1200×600 baseline resolution** and scaled to any screen using `sx()`, `sy()`, and `sv()` helper functions.
- The trajectory preview runs the same physics calculation forward in time before firing — it assumes vacuum (no drag) for clarity.
- Blocks respawn automatically to keep at least two on screen at all times.

---

## Built With

- [Pygame](https://www.pygame.org/)

## Built By
- Akanksha Dange 
- Ananya Bhale
- Anshika Yadav
- Riddhi Gupta
- Anibha Kumari
