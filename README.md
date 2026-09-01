# fluid-metrology-sizing-calculator
Advanced  transit-time/Doppler calculations, liquid velocity verification, and scale  factor optimization
Here is the complete setup for **`fluid-metrology-sizing-calculator`**.

This repository modernizes fluid metrology computations for acoustic flow meters. It packages transit-time and Doppler ultrasonic velocity equations, scale factor calibrations, and Reynolds-number-based hydraulic corrections into a modular Python engine with full unit testing.

# Fluid Metrology Sizing Calculator

A fluid metrology library for sizing acoustic flow meters, verifying liquid velocities, and applying hydrodynamic profile corrections.

Designed for field verification and industrial telemetry systems (e.g., Transit-Time and Doppler ultrasonic metering setups).

## Features

* **Transit-Time Differential Math:** High-resolution fluid velocity estimation derived from nanosecond-level delta-t ($\Delta t$) pulse measurements.
* **Doppler Shift Velocity Analysis:** Frequency-shift velocity extraction for suspended solids and aerated liquid streams.
* **Hydrodynamic Reynolds Corrections:** Automatically adjusts raw line-average velocities to volumetric area-average velocities across Laminar, Transitional, and Turbulent flow regimes.
* **K-Factor Optimization:** Least-squares linear regression routine to calculate optimal meter scale factors against reference calibration standards.

---

## Architecture & Layout

```text
fluid-metrology-sizing-calculator/
├── .github/
│   └── workflows/
│       └── run_tests.yml              # CI test runner
├── src/
│   ├── __init__.py
│   └── metrology_calculator.py        # Core metrology engine
├── tests/
│   └── test_metrology_calculator.py   # Unit test suite
├── .gitignore
├── README.md
└── requirements.txt

```

---

## Quickstart

### Installation

```bash
git clone [https://github.com/your-username/fluid-metrology-sizing-calculator.git](https://github.com/your-username/fluid-metrology-sizing-calculator.git)
cd fluid-metrology-sizing-calculator
pip install -r requirements.txt

```

### Basic Usage

```python
from src.metrology_calculator import FluidMetrologyCalculator

# Initialize calculator for a 0.3m (12-inch) pipe
calc = FluidMetrologyCalculator(pipe_diameter_m=0.3)

# 1. Calculate raw velocity via Transit-Time delta-t (in nanoseconds)
raw_v = calc.transit_time_velocity(delta_t_ns=180.0, acoustic_path_length_m=0.45, path_angle_deg=45.0)

# 2. Apply Reynolds Number profile correction factor (K_h)
corrected_v = calc.reynolds_profile_correction(raw_velocity_ms=raw_v)

# 3. Compute Volumetric Flow Rate (Q)
flow_data = calc.compute_volumetric_flow_rate(corrected_velocity_ms=corrected_v)

print(f"Corrected Velocity: {flow_data['velocity_m_s']:.3f} m/s")
print(f"Flow Rate: {flow_data['flow_rate_m3_h']:.2f} m³/h ({flow_data['flow_rate_l_s']:.2f} L/s)")

```

---

## Unit Testing

Run the test suite using `unittest`:

```bash
python -m unittest discover -s tests

```

---

## License

MIT License. Free for industrial metrology adaptation.

```

```
