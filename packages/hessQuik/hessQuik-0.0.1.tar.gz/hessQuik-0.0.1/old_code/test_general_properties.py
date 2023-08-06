import unittest
import torch
import hessQuik.activations as act
import hessQuik.layers as lay
import hessQuik.networks as net
from utils import run_all_tests


class TestInputOutputDimensions(unittest.TestCase):

    @staticmethod
    def run_test(f, m, n):

        # check input and output dimensions
        assert f.dim_input() == m
        assert f.dim_output() == n

    def test_singleLayer(self):
        m = 3
        n = 4
        f = lay.singleLayer(m, n)

        print(self)
        self.run_test(f, m, n)

    def test_resnetLayer(self):
        m = 3
        d = 4
        f = lay.singleLayer(m, d)

        print(self)
        self.run_test(f, m, m)


if __name__ == '__main__':
    torch.set_default_dtype(torch.float64)
    unittest.main()
