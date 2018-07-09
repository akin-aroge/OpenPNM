import openpnm as op
from numpy.testing import assert_approx_equal


class ElectricalConductanceTest:
    def setup_class(self):
        self.net = op.network.Cubic(shape=[4, 4, 4])
        self.geo = op.geometry.GenericGeometry(network=self.net,
                                               pores=self.net.Ps,
                                               throats=self.net.Ts)
        self.phase = op.phases.GenericPhase(network=self.net)
        self.phase['pore.conductivity'] = 1
        self.phys = op.physics.GenericPhysics(network=self.net,
                                              phase=self.phase,
                                              geometry=self.geo)
        self.geo['pore.diameter'] = 1.0
        self.geo['pore.area'] = 1.0
        self.geo['throat.diameter'] = 1.0
        self.geo['throat.length'] = 1e-9
        self.geo['throat.area'] = 1

    def test_electrical_conductance(self):
        self.geo['throat.conduit_lengths.pore1'] = 0.2
        self.geo['throat.conduit_lengths.throat'] = 0.6
        self.geo['throat.conduit_lengths.pore2'] = 0.2
        self.geo['throat.equivalent_area.pore1'] = 0.2
        self.geo['throat.equivalent_area.throat'] = 0.2
        self.geo['throat.equivalent_area.pore2'] = 0.2
        mod = op.models.physics.electrical_conductance.series_resistors
        self.phys.add_model(propname='throat.electrical_conductance',
                            pore_conductivity='pore.conductivity',
                            model=mod)
        self.phys.regenerate_models()
        a = 0.2
        assert_approx_equal(self.phys['throat.electrical_conductance'].mean(), a)


if __name__ == '__main__':

    t = ElectricalConductanceTest()
    self = t
    t.setup_class()
    for item in t.__dir__():
        if item.startswith('test'):
            print('running test: '+item)
            t.__getattribute__(item)()