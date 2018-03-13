# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, unicode_literals

import subprocess
import numpy as np

class testCmdAACGMV2:
    def setup(self):
        """Runs before every method to create a clean testing setup"""
        self.output = "tests/test_data/output.txt"
        self.convert = "tests/test_data/test_convert.txt"
        self.single = 'tests/test_data/test_convert_single_line.txt'
        self.mlt = 'tests/test_data/test_convert_mlt.txt'
        self.mlt_single = 'tests/test_data/test_convert_mlt_single_line.txt'

    def teardown(self):
        """Runs after every method to clean up previous testing"""
        import os

        if os.path.isfile(self.output):
            os.remove(self.output)

        del self.output, self.convert, self.single, self.mlt, self.mlt_single

    def test_module_invocation(self):
        p = subprocess.Popen(['python', '-m', 'aacgmv2', 'convert', '-i',
                              'tests/test_convert.txt', '-d', '20150224',
                              '-o', self.output])
        p.communicate()
        p.wait()
        data = np.loadtxt(self.output)
        np.testing.assert_allclose(data, [[57.4761, 93.5572],
                                          [58.5332, 93.9607],
                                          [59.5852, 94.3897]], rtol=1e-4)

    def test_convert_g2a(self):
        p = subprocess.Popen(['aacgmv2', 'convert', '-i', self.convert, '-d',
                              '20150224', '-o', self.output])
        p.communicate()
        p.wait()
        data = np.loadtxt(self.output)
        np.testing.assert_allclose(data, [[57.4761, 93.5572],
                                          [58.5332, 93.9607],
                                          [59.5852, 94.3897]], rtol=1e-4)

    def test_convert_a2g(self):
        p = subprocess.Popen(['aacgmv2', 'convert', '-i', self.convert,
                              '-d', '20150224', '-o', self.output, '-v'])
        p.communicate()
        p.wait()
        data = np.loadtxt(self.output)
        np.testing.assert_allclose(data, [[51.6547, -66.6601],
                                          [52.6725, -66.7555],
                                          [53.6914, -66.8552]], rtol=1e-4)

    def test_convert_trace_g2a(self):
        p = subprocess.Popen(['aacgmv2', 'convert', '-i', self.convert, '-d',
                              '20150224', '-o', self.output, '-t'])
        p.communicate()
        p.wait()
        data = np.loadtxt(self.output)
        np.testing.assert_allclose(data, [[57.4736, 93.5676],
                                          [58.5305, 93.9716],
                                          [59.5825, 94.4009]], rtol=1e-4)

    def test_convert_trace_a2g(self):
        p = subprocess.Popen(['aacgmv2', 'convert', '-i', self.convert, '-d',
                              '20150224', '-o', self.output, '-t', '-v'])
        p.communicate()
        p.wait()
        data = np.loadtxt(self.output)
        np.testing.assert_allclose(data, [[51.6454, -66.6444],
                                          [52.6671, -66.7432],
                                          [53.6899, -66.8469]], rtol=1e-4)

    def test_convert_geocentric(self):
        p = subprocess.Popen(['aacgmv2', 'convert', '-i', self.convert, '-d',
                              '20150224', '-o', self.output, '-g'])
        p.communicate()
        p.wait()
        data = np.loadtxt(self.output)
        np.testing.assert_allclose(data, [[57.6697, 93.6319],
                                          [58.7223, 94.0385],
                                          [59.7695, 94.4708]], rtol=1e-4)

    def test_convert_today(self):
        p = subprocess.Popen(['aacgmv2', 'convert', '-i', self.convert])
        p.communicate()
        p.wait()

    def test_convert_single_line(self):
        p = subprocess.Popen(['aacgmv2', 'convert', '-i', self.single, '-d',
                              '20150224', '-o', self.output])
        p.communicate()
        p.wait()
        data = np.loadtxt(self.output)
        np.testing.assert_allclose(data, [57.4761, 93.5572], rtol=1e-4)

    def test_convert_stdin_stdout(self):
        p = subprocess.Popen('echo 60 15 300 | aacgmv2 convert -d 20150224',
                             shell=True, stdout=subprocess.PIPE)
        stdout, _ = p.communicate()
        p.wait()
        assert b'57.47612194 93.55719875' in stdout

    def test_convert_mlt_a2m(self):
        p = subprocess.Popen(['aacgmv2', 'convert_mlt', '-i', self.mlt,
                              '20150224140015', '-o', self.output])
        p.communicate()
        p.wait()
        data = np.loadtxt(self.output)
        np.testing.assert_allclose(data, [9.056476, 9.78981, 10.523143],
                                   rtol=1e-6)

    def test_convert_mlt_m2a(self):
        p = subprocess.Popen(['aacgmv2', 'convert_mlt', '-i', self.mlt,
                              '20150224140015', '-o', self.output, '-v'])
        p.communicate()
        p.wait()
        data = np.loadtxt(self.output)
        np.testing.assert_allclose(data, [240.152854, 45.152854, 210.152854],
                                   rtol=1e-6)

    def test_convert_mlt_single_line(self):
        p = subprocess.Popen(['aacgmv2', 'convert_mlt', '-i', self.mlt_single,
                              '20150224140015', '-o', self.output])
        p.communicate()
        p.wait()
        data = np.loadtxt(self.output)
        np.testing.assert_allclose(data, 9.0564764, rtol=1e-6)

    def test_convert_mlt_stdin_stdout(self):
        p = subprocess.Popen('echo 12 | aacgmv2 convert_mlt -v 20150224140015',
                             shell=True, stdout=subprocess.PIPE)
        stdout, _ = p.communicate()
        p.wait()
        assert b'45.15285362' in stdout

    def test_convert_mlt_stdin_stdout_order(self):
        p = subprocess.Popen('echo 12 | aacgmv2 convert_mlt 20150224140015 -v',
                             shell=True, stdout=subprocess.PIPE)
        stdout, _ = p.communicate()
        p.wait()
        assert b'45.15285362' in stdout
