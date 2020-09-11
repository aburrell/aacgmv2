import datetime as dt
import warnings

import aacgmv2


class TestFutureDepWarning:
    def setup(self):
        # Initialize the routine to be tested
        self.test_routine = None
        self.test_args = []
        self.test_kwargs = {}

    def teardown(self):
        del self.test_routine, self.test_args, self.test_kwargs

    def test_future_dep_warning(self):
        """Test the implementation of FutureWarning for dupicate routines"""
        if self.test_routine is None:
            assert True
        else:
            with warnings.catch_warnings(record=True) as wout:
                # Cause all warnings to always be triggered.
                warnings.simplefilter("always")

                # Trigger a warning.
                self.test_routine(*self.test_args, **self.test_kwargs)

                # Verify some things
                assert len(wout) == 1
                assert issubclass(wout[-1].category, FutureWarning)
                assert "Duplicate routine" in str(wout[-1].message)


class TestDepAACGMV2Warning(TestFutureDepWarning):
    def setup(self):
        self.dtime = dt.datetime(2015, 1, 1, 0, 0, 0)
        self.test_routine = None
        self.test_args = []
        self.test_kwargs = {}

    def teardown(self):
        del self.dtime, self.test_routine, self.test_args, self.test_kwargs

    def test_igrf_dipole_axis_warning(self):
        """Test future deprecation warning for igrf_dipole_axis"""

        self.test_routine = aacgmv2.deprecated.igrf_dipole_axis
        self.test_args = [self.dtime]
        self.test_future_dep_warning()

    def test_subsol_warning(self):
        """Test future deprecation warning for subsol"""

        self.test_routine = aacgmv2.deprecated.subsol
        self.test_args = [self.dtime.year, 1, 1.0]
        self.test_future_dep_warning()

    def test_gc2gd_lat(self):
        """Test future deprecation warning for gc2gd_lat"""

        self.test_routine = aacgmv2.deprecated.gc2gd_lat
        self.test_args = [45.0]
        self.test_future_dep_warning()
