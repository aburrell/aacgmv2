import subprocess
import numpy as np
import os
import pytest

import aacgmv2


@pytest.mark.xfail
class TestCmdAACGMV2:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.test_dir = os.path.join(aacgmv2.__path__[0], 'tests', 'test_data')
        self.output = os.path.join(self.test_dir, "output.txt")
        self.convert = os.path.join(self.test_dir, "test_convert.txt")
        self.single = os.path.join(self.test_dir,
                                   'test_convert_single_line.txt')
        self.mlt = os.path.join(self.test_dir, 'test_convert_mlt.txt')
        self.mlt_single = os.path.join(self.test_dir,
                                       'test_convert_mlt_single_line.txt')
        self.rtol = 1.0e-4

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        if os.path.isfile(self.output):
            os.remove(self.output)

        del self.test_dir, self.output, self.convert, self.single, self.mlt
        del self.mlt_single, self.rtol

    @pytest.mark.parametrize('pin,ref',
                             [([], [[57.4810, 93.5290, 1.04566],
                                    [58.5380, 93.9324, 1.0456],
                                    [59.5900, 94.3614, 1.04556]]),
                              (['-v'], [[51.6616, -66.6338, 306.1783],
                                        [52.6792, -66.7291, 306.5470],
                                        [53.6980, -66.8286, 306.91265]]),
                              (['-g'], [[57.6746, 93.6036, 1.0471],
                                        [58.7271, 94.0102, 1.0471],
                                        [59.7743, 94.4425, 1.0471]]),
                              (['-t'], [[57.4785, 93.5398, 1.04566],
                                        [58.5354, 93.9438, 1.04561],
                                        [59.5873, 94.3731, 1.04556]]),
                              (['-t', '-v'], [[51.6524, -66.6180, 306.1750],
                                              [52.6738, -66.7167, 306.5451],
                                              [53.6964, -66.8202, 306.9121]])])
    def test_convert_command_line(self, pin, ref):
        """ Test the output from the command line routine"""
        p_commands = ['python', '-m', 'aacgmv2', 'convert', '-i',
                      self.convert, '-d', '20150224', '-o',
                      self.output]
        p_commands.extend(pin)
        p = subprocess.Popen(p_commands)
        p.communicate()
        p.wait()
        assert os.path.isfile(self.output)
        data = np.loadtxt(self.output)
        np.testing.assert_allclose(data, ref, rtol=self.rtol)

    def test_convert_today(self):
        """ Test the shape of the output for today's date """
        p = subprocess.Popen(['python', '-m', 'aacgmv2', 'convert', '-i',
                              self.convert, '-o', self.output])
        p.communicate()
        p.wait()
        assert os.path.isfile(self.output)
        data = np.loadtxt(self.output)
        assert data.shape == (3, 3)

    def test_convert_single_line(self):
        """ Test the command line with a single line as input """
        p = subprocess.Popen(['python', '-m', 'aacgmv2', 'convert', '-i',
                              self.single, '-d', '20150224', '-o', self.output])
        p.communicate()
        p.wait()
        assert os.path.isfile(self.output)
        data = np.loadtxt(self.output)
        np.testing.assert_allclose(data, [57.4810, 93.5290, 1.04566],
                                   rtol=self.rtol)

    def test_main_help(self):
        p = subprocess.Popen('python -m aacgmv2 -h', shell=True,
                             stdout=subprocess.PIPE)
        stdout, _ = p.communicate()
        p.wait()
        assert b'usage' in stdout

    def test_convert_stdin_stdout(self):
        p = subprocess.Popen(
            'echo 60 15 300 | python -m aacgmv2 convert -d 20150224',
            shell=True, stdout=subprocess.PIPE)
        stdout, _ = p.communicate()
        p.wait()
        assert b'57.48099198 93.52895314' in stdout

    @pytest.mark.parametrize('pin,ref',
                             [([], [9.0912, 9.8246, 10.5579]),
                              (['-v'], [-120.3687, 44.6313, -150.3687])])
    def test_convert_mlt_command_line(self, pin, ref):
        """ Test the command line MLT conversion options"""
        p_command = ['python', '-m', 'aacgmv2', 'convert_mlt', '-i',
                     self.mlt, '20150224140015', '-o', self.output]
        p_command.extend(pin)
        p = subprocess.Popen(p_command)
        p.communicate()
        p.wait()
        assert os.path.isfile(self.output)
        data = np.loadtxt(self.output)
        np.testing.assert_allclose(data, ref, rtol=self.rtol)

    def test_convert_mlt_single_line(self):
        p = subprocess.Popen(['python', '-m', 'aacgmv2', 'convert_mlt', '-i',
                              self.mlt_single, '20150224140015', '-o',
                              self.output])
        p.communicate()
        p.wait()
        assert os.path.isfile(self.output)
        data = np.loadtxt(self.output)
        np.testing.assert_allclose(data, 9.0912, rtol=self.rtol)

    @pytest.mark.parametrize('echo_command',
                             [('echo 12 | python -m aacgmv2 convert_mlt -v 20150224140015'),
                              ('echo 12 | python -m aacgmv2 convert_mlt 20150224140015 -v')])
    def test_convert_mlt_stdin_stdout(self, echo_command):
        p = subprocess.Popen(echo_command, shell=True, stdout=subprocess.PIPE)
        stdout, _ = p.communicate()
        p.wait()
        assert b'44.63126817' in stdout
