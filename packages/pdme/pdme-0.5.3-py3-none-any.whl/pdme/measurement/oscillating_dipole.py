from dataclasses import dataclass
import numpy
import numpy.typing
from typing import Sequence, List, Tuple
from pdme.measurement.dot_measure import DotMeasurement, DotRangeMeasurement


DotInput = Tuple[numpy.typing.ArrayLike, float]


@dataclass
class OscillatingDipole():
	'''
	Representation of an oscillating dipole, either known or guessed.

	Parameters
	----------
	p : numpy.ndarray
		The oscillating dipole moment, with overall sign arbitrary.
	s : numpy.ndarray
		The position of the dipole.
	w : float
		The oscillation frequency.
	'''
	p: numpy.ndarray
	s: numpy.ndarray
	w: float

	def __post_init__(self) -> None:
		'''
		Coerce the inputs into numpy arrays.
		'''
		self.p = numpy.array(self.p)
		self.s = numpy.array(self.s)

	def s_at_position(self, r: numpy.ndarray, f: float) -> float:
		'''
		Returns the noise potential at a point r, at some frequency f.

		Parameters
		----------
		r : numpy.ndarray
			The position of the dot.
		f : float
			The dot frequency to sample.
		'''
		return (self._alpha(r))**2 * self._b(f)

	def _alpha(self, r: numpy.ndarray) -> float:
		diff = r - self.s
		return self.p.dot(diff) / (numpy.linalg.norm(diff)**3)

	def _b(self, f: float) -> float:
		return (1 / numpy.pi) * (self.w / (f**2 + self.w**2))


def dot_inputs_to_array(dot_inputs: Sequence[DotInput]) -> numpy.ndarray:
	return numpy.array([numpy.append(numpy.array(input[0]), input[1]) for input in dot_inputs])


def dot_range_measurements_low_high_arrays(dot_range_measurements: Sequence[DotRangeMeasurement]) -> Tuple[numpy.ndarray, numpy.ndarray]:
	lows = [measurement.v_low for measurement in dot_range_measurements]
	highs = [measurement.v_high for measurement in dot_range_measurements]
	return (numpy.array(lows), numpy.array(highs))


class OscillatingDipoleArrangement():
	'''
	A collection of oscillating dipoles, which we are interested in being able to characterise.

	Parameters
	--------
	dipoles : Sequence[OscillatingDipole]
	'''
	def __init__(self, dipoles: Sequence[OscillatingDipole]):
		self.dipoles = dipoles

	def get_dot_measurement(self, dot_input: DotInput) -> DotMeasurement:
		r = numpy.array(dot_input[0])
		f = dot_input[1]
		return DotMeasurement(sum([dipole.s_at_position(r, f) for dipole in self.dipoles]), r, f)

	def get_dot_measurements(self, dot_inputs: Sequence[DotInput]) -> List[DotMeasurement]:
		'''
		For a series of points, each with three coordinates and a frequency, return a list of the corresponding DotMeasurements.
		'''
		return [self.get_dot_measurement(dot_input) for dot_input in dot_inputs]

	def get_percent_range_dot_measurement(self, dot_input: DotInput, low_percent: float, high_percent: float) -> DotRangeMeasurement:
		r = numpy.array(dot_input[0])
		f = dot_input[1]
		return DotRangeMeasurement(low_percent * sum([dipole.s_at_position(r, f) for dipole in self.dipoles]), high_percent * sum([dipole.s_at_position(r, f) for dipole in self.dipoles]), r, f)

	def get_percent_range_dot_measurements(self, dot_inputs: Sequence[DotInput], low_percent: float, high_percent: float) -> List[DotRangeMeasurement]:
		'''
		For a series of points, each with three coordinates and a frequency, and also a lower error range and upper error range, return a list of the corresponding DotRangeMeasurements.
		'''
		return [self.get_percent_range_dot_measurement(dot_input, low_percent, high_percent) for dot_input in dot_inputs]
