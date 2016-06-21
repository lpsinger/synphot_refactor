# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test integrator.py module."""
from __future__ import absolute_import, division, print_function

# THIRD-PARTY
from astropy.modeling.models import Polynomial1D
from numpy.testing import assert_allclose

# LOCAL
from ..integrator import trapezoid_integrator
from ..models import Box1D
from ..spectrum import SourceSpectrum


# TODO: Replace this with model with actual analytic integral when it
#       exists in Astropy.
class DummyModel(Box1D):
    """Fake source with its own analytic integral."""
    @property
    def integral(self):
        return Polynomial1D(1, c1=1)  # f(x) = x


# TODO: Update test when Astropy models have integral.
def test_analytic_source():
    """Test integration using built-in analytic integral."""
    sp = SourceSpectrum(DummyModel)
    assert_allclose(sp.integrate([1000, 1010, 1020]).value, 20)


# TODO: Replace model with one that is without analytic integral when
#       integral is in Astropy.
def test_trapz_spec():
    sp = SourceSpectrum(Box1D, amplitude=1, x_0=5000, width=10)
    assert_allclose(sp.integrate().value, 10)


def test_trapz_box1d():
    m = Box1D(amplitude=1, x_0=5000, width=10)
    x = m.sampleset()

    # Ascending.
    assert_allclose(trapezoid_integrator(x, m(x)), 10)

    # Descending.
    x2 = x[::-1]
    assert_allclose(trapezoid_integrator(x2, m(x2)), 10)
