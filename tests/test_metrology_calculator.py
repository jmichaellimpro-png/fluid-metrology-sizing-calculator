import unittest
import numpy as np
from src.metrology_calculator import FluidMetrologyCalculator

class TestFluidMetrologyCalculator(unittest.TestCase):

    def setUp(self):
        # 0.3m (12-inch) pipe diameter, standard water speed of sound
        self.calc = FluidMetrologyCalculator(pipe_diameter_m=0.3)

    def test_transit_time_velocity(self):
        # Test known delta-t and path length
        velocity = self.calc.transit_time_velocity(
            delta_t_ns=150.0, 
            acoustic_path_length_m=0.4, 
            path_angle_deg=45.0
        )
        self.assertGreater(velocity, 0)

    def test_doppler_velocity(self):
        velocity = self.calc.doppler_velocity(
            doppler_shift_hz=500.0, 
            transmit_frequency_hz=1e6, 
            transducer_angle_deg=60.0
        )
        self.assertAlmostEqual(velocity, 0.74, places=2)

    def test_reynolds_correction_turbulent(self):
        # High velocity guarantees turbulent flow (Re > 4000)
        corrected_v = self.calc.reynolds_profile_correction(raw_velocity_ms=2.5)
        self.assertLess(corrected_v, 2.5)
        self.assertGreater(corrected_v, 2.0)

    def test_scale_factor_optimization(self):
        measured = np.array([1.0, 2.0, 3.0, 4.0])
        reference = np.array([1.05, 2.10, 3.15, 4.20])
        k_factor = self.calc.optimize_scale_factor(measured, reference)
        self.assertAlmostEqual(k_factor, 1.05, places=4)

if __name__ == "__main__":
    unittest.main()
