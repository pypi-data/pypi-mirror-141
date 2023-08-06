from numpy import isin
import autograd.numpy as np  # Thinly-wrapped numpy
from autograd import grad
from autograd.extend import primitive, defvjp
import pandas as pd
import os.path
from scipy.interpolate import UnivariateSpline
try:
    from pyees.unitSystem import unit as unitConversion
except ModuleNotFoundError:
    from unitSystem import unit as unitConversion
try:
    from pyees.pyees import variable, System
except ModuleNotFoundError:
    from pyees import variable, System


def _read(fileName, names, sheetNr=1):
    """Function to read datasheets from excel files files"""

    fileExtension = os.path.splitext(fileName)[1]
    knownFileExtensions = ['.xlsx']
    if fileExtension not in knownFileExtensions:
        raise ValueError(f'The file extension {fileExtension} is unkown. The known file extensions are {knownFileExtensions}')

    elif fileExtension == '.xlsx':
        xlFile = pd.ExcelFile(fileName, engine='openpyxl')
        df = pd.read_excel(xlFile, sheetNr - 1)

    # get all measurements
    measurements = []
    for name in names:
        measurements.append(df[name])

    # get the units for all measurements
    # remove the unit from the measurement
    units = []
    for i, meas in enumerate(measurements):
        units.append(meas[0])
        measurements[i] = list(meas[1:])

    # remove all rows where some of the measurements are nan
    measurements = np.array(measurements).transpose()
    reducedMeasurements = []
    for row in measurements:
        if not any(np.isnan(row)):
            reducedMeasurements.append(list(row))
    measurements = np.array(reducedMeasurements).transpose()

    # convert all measurements to SI
    U = unitConversion()
    scales = [U.convertToSI(1, unit)[0] for unit in units]
    for i, (scale, meas) in enumerate(zip(scales, measurements)):
        measurements[i] = [elem * scale for elem in meas]

    return measurements


class Pipe(System):
    def __init__(self, d, L, epsilon):
        self.unitConversion = unitConversion()

        self.d = self._getParameter(d, 'm')
        self.L = self._getParameter(L, 'm')
        self.epsilon = self._getParameter(epsilon, '1')

        self.area = np.pi / 4 * self.d**2
        super().__init__()

    def _getParameter(self, par, expectedUnit):
        if isinstance(par, variable):
            if par.unit != expectedUnit:
                raise ValueError(f'The unit of the input was {par.unit} but an input with a unit of {expectedUnit} was expected')
            return par.value
        else:
            return par

    def curve(self, flow, rho, mu):

        flow = self._getParameter(flow, 'm3/s')
        rho = self._getParameter(rho, 'kg/m3')
        mu = self._getParameter(mu, 'kg/m-s')

        v = flow / self.area
        Re = np.max([rho * v * self.d / mu, 1e-8])

        if Re <= 3000:
            # Laminar
            f = 64 / Re

        else:
            # turbulent
            # solve the friction factor using the Churchill equation
            # this is the same function as EES
            # https://powderprocess.net/Tools_html/Piping/Churchill.html

            B = (37530 / Re)**16
            innerA = 1 / ((7 / Re)**0.9 + 0.27 * self.epsilon)
            A = (2.457 * np.log(innerA))**16
            f = 8 * ((8 / Re)**12 + 1 / ((A + B)**1.5))**(1 / 12)

        # hL = f * L/D * v**2 /(2*g)
        # dP = rho * g * hL
        dP = rho * f * self.L / self.d * v**2 / 2
        return variable(dP, 'Pa')


class Pump(System):

    def __init__(self, datasheet, flowName, pressureName, sheetNr=1, order=1):
        Q, dP = _read(datasheet, [flowName, pressureName], sheetNr)
        self.inter = UnivariateSpline(Q, dP, k=order, ext=0)
        self.diff = self.inter.derivative(n=1)
        super().__init__()
        defvjp(Pump._curve, Pump.curve_g, argnums=[1, 2])

    def curve(self, flow):
        if isinstance(flow, variable):
            flow = flow.value
        dP = self._curve(flow)
        return variable(dP, 'Pa')

    @primitive
    def _curve(self, flow):
        dP = self.inter(flow)
        return dP

    def curve_g(ans, self, flow):
        diff = self.diff(flow)
        return lambda g: g * diff


class Valve(System):

    def __init__(self, dP, dPUnit, flow, flowUnit):
        U = unitConversion()
        dp, _ = U.convertToSI(dP, dPUnit)
        flow, _ = U.convertToSI(flow, flowUnit)
        self.kv = dp / flow ** 2
        super().__init__()

    def curve(self, flow, opening=100):
        if isinstance(opening, variable):
            opening = opening.value
        if isinstance(flow, variable):
            flow = flow.value
        opening /= 100
        dP = (self.kv * opening + (1 - opening) * 100 * self.kv) * flow ** 2
        return variable(dP, 'Pa')


def main():

    pump = Pump('pump.xlsx', 'Q', 'dP')
    valve = Valve(1, 'bar', 100, 'L/min')
    pipe = Pipe(d=variable(30, 'mm'), L=variable(1, 'm'), epsilon=0.25 / 30)

    def f(x):
        flow = variable(x[0], 'L/min')
        cost = pump.curve(flow)
        # cost = pump.curve(x[0])
        # cost = flow ** 2
        if isinstance(cost, variable):
            cost = cost.value
        # print(cost)
        # exit()
        return cost

    def FD(func, x0):
        dx = 0.001
        f1 = func(x0)
        f2 = func(x0 + dx)
        df = (f2 - f1) / dx
        return df

    x0 = np.array([500], dtype=float)
    g = grad(f)
    print('grad', g(x0))
    print('fd', FD(f, x0))


if __name__ == "__main__":
    main()
