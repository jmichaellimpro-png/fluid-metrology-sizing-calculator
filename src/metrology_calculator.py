import math
import numpy as np
from typing import Dict, Union

class FluidMetrologyCalculator:
    """
    Advanced transit-time and Doppler ultrasonic flow meter sizing calculator.
    Handles velocity verification, Reynolds profile correction, and scale factor optimization.
    """

    def __init__(self, pipe_diameter_m: float, fluid_speed_of_sound_ms: float = 1480.0, kinematic_viscosity_m2s: float = 1.004e-6):
        """
        :param pipe_diameter_m: Internal pipe diameter in meters.
        :param fluid_speed_of_sound_ms: Speed of sound in medium (default ~1480 m/s for water at 20°C).
        :param kinematic_viscosity_m2s: Kinematic viscosity in m^2/s (default water at 20°C).
        """
        if pipe_diameter_m <= 0:
            raise ValueError("Pipe diameter must be greater than zero.")
        self.d = pipe_diameter_m
        self.c = fluid_speed_of_sound_ms
        self.nu = kinematic_viscosity_m2s

    def transit_time_velocity(self, delta_t_ns: float, acoustic_path_length_m: float, path_angle_deg: float) -> float:
        """
        Calculates fluid velocity (v) using transit-time differential equation:
        v = (c^2 * delta_t) / (2 * L * cos(theta))
        """
        delta_t_sec = delta_t_ns * 1e-9
        theta_rad = math.radians(path_angle_deg)
        cos_theta = math.cos(theta_rad)

        if cos_theta == 0:
            raise ValueError("Path angle cannot be 90 degrees (orthogonal to flow).")

        v = (self.c**2 * delta_t_sec) / (2 * acoustic_path_length_m * cos_theta)
        return float(v)

    def doppler_velocity(self, doppler_shift_hz: float, transmit_frequency_hz: float, transducer_angle_deg: float) -> float:
        """
        Calculates fluid velocity (v) using Doppler frequency shift equation:
        v = (f_d * c) / (2 * f_0 * cos(theta))
        """
        theta_rad = math.radians(transducer_angle_deg)
        cos_theta = math.cos(theta_rad)

        if cos_theta == 0:
            raise ValueError("Transducer angle cannot be 90 degrees.")

        v = (doppler_shift_hz * self.c) / (2 * transmit_frequency_hz * cos_theta)
        return float(v)

    def reynolds_profile_correction(self, raw_velocity_ms: float) -> float:
        """
        Computes hydraulic profile factor (K_h) based on Reynolds Number (Re)
        to convert line-average velocity to area-average velocity.
        """
        abs_v = abs(raw_velocity_ms)
        if abs_v == 0:
            return 0.0

        reynolds = (abs_v * self.d) / self.nu

        # Laminar flow (Re < 2000): K_h = 0.75
        if reynolds < 2000:
            k_h = 0.75
        # Turbulent flow (Re >= 4000): Power law approximation K_h = 1 / (1 + 0.19 * Re^-0.1)
        elif reynolds >= 4000:
            k_h = 1.0 / (1.0 + 0.19 * (reynolds ** -0.1))
        # Transitional region
        else:
            k_h = 0.75 + (0.2 * (reynolds - 2000) / 2000)

        return float(raw_velocity_ms * k_h)

    def compute_volumetric_flow_rate(self, corrected_velocity_ms: float) -> Dict[str, float]:
        """Calculates volumetric flow rate (Q) in m^3/h and Liters/sec."""
        area = math.pi * ((self.d / 2.0) ** 2)
        q_m3s = area * corrected_velocity_ms
        q_m3h = q_m3s * 3600.0
        q_lps = q_m3s * 1000.0

        return {
            "velocity_m_s": corrected_velocity_ms,
            "flow_rate_m3_h": q_m3h,
            "flow_rate_l_s": q_lps
        }

    def optimize_scale_factor(self, measured_velocities: np.ndarray, reference_velocities: np.ndarray) -> float:
        """
        Determines optimal scale factor (K-factor) via linear least-squares regression.
        """
        scale_factor, _, _, _ = np.linalg.lstsq(measured_velocities[:, np.newaxis], reference_velocities, rcond=None)
        return float(scale_factor[0])
