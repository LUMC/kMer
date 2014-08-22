"""
Tests for the `k_mer.metrics` module.
"""


from StringIO import StringIO

import numpy as np

from k_mer import kdifflib, klib, metrics

import utils


class TestKDiffLib():
    def test_distance_matrix_one(self):
        counts = utils.counts(utils.SEQUENCES, 8)

        profiles = [klib.kMer(utils.as_array(counts, 8), 'a')]

        k_diff = kdifflib.kMerDiff()
        out = StringIO()
        kdifflib.distance_matrix(profiles, out, 2, k_diff)

        assert out.getvalue().strip().split('\n') == ['1', 'a']

    def test_distance_matrix_two(self):
        counts_left = utils.counts(utils.SEQUENCES_LEFT, 8)
        counts_right = utils.counts(utils.SEQUENCES_RIGHT, 8)

        profiles = [klib.kMer(utils.as_array(counts_left, 8), 'a'),
                    klib.kMer(utils.as_array(counts_right, 8), 'b')]

        k_diff = kdifflib.kMerDiff()
        out = StringIO()
        kdifflib.distance_matrix(profiles, out, 2, k_diff)

        assert out.getvalue().strip().split('\n') == ['2', 'a', 'b', '0.46']

    def test_distance_matrix_three(self):
        counts_left = utils.counts(utils.SEQUENCES_LEFT, 8)
        counts_right = utils.counts(utils.SEQUENCES_RIGHT, 8)

        profiles = [klib.kMer(utils.as_array(counts_left, 8), 'a'),
                    klib.kMer(utils.as_array(counts_right, 8), 'b'),
                    klib.kMer(utils.as_array(counts_left, 8), 'c')]

        k_diff = kdifflib.kMerDiff()
        out = StringIO()
        kdifflib.distance_matrix(profiles, out, 2, k_diff)

        assert out.getvalue().strip().split('\n') == ['3', 'a', 'b', 'c', '0.46', '0.00 0.46']

    def test_kmerdiff_dynamic_smooth(self):
        # If we use function=min and threshold=0, we should get the following
        # transformation:
        #
        #           | before           | after
        # ----------+------------------+-----------------
        #           | 0111111111111011 | 3000111111113000
        # profile A | ACGTACGTACGTACGT | ACGTACGTACGTACGT
        #           | AAAACCCCGGGGTTTT | AAAACCCCGGGGTTTT
        # ----------+------------------+-----------------
        #           | 0101111111111111 | 2000111111114000
        # profile B | ACGTACGTACGTACGT | ACGTACGTACGTACGT
        #           | AAAACCCCGGGGTTTT | AAAACCCCGGGGTTTT
        counts_a = utils.Counter(['AC', 'AG', 'AT', 'CA', 'CC', 'CG', 'CT', 'GA', 'GC', 'GG', 'GT', 'TA', 'TG', 'TT'])
        counts_b = utils.Counter(['AC', 'AT', 'CA', 'CC', 'CG', 'CT', 'GA', 'GC', 'GG', 'GT', 'TA', 'TC', 'TG', 'TT'])

        profile_a = klib.kMer(utils.as_array(counts_a, 2))
        profile_b = klib.kMer(utils.as_array(counts_b, 2))

        k_diff = kdifflib.kMerDiff()
        k_diff.dynamic_smooth(profile_a, profile_b)

        counts_a = utils.Counter(['AA', 'AA', 'AA', 'CA', 'CC', 'CG', 'CT', 'GA', 'GC', 'GG', 'GT', 'TA', 'TA', 'TA'])
        counts_b = utils.Counter(['AA', 'AA', 'CA', 'CC', 'CG', 'CT', 'GA', 'GC', 'GG', 'GT', 'TA', 'TA', 'TA', 'TA'])

        np.testing.assert_array_equal(profile_a.counts, utils.as_array(counts_a, 2))
        np.testing.assert_array_equal(profile_b.counts, utils.as_array(counts_b, 2))

    def test_kmerdiff_distance(self):
        counts_a = utils.Counter(['AC', 'AG', 'AT', 'CA', 'CC', 'CG', 'CT', 'GA', 'GC', 'GG', 'GT', 'TA', 'TG', 'TT'])
        counts_b = utils.Counter(['AC', 'AT', 'CA', 'CC', 'CG', 'CT', 'GA', 'GC', 'GG', 'GT', 'TA', 'TC', 'TG', 'TT'])

        profile_a = klib.kMer(utils.as_array(counts_a, 2))
        profile_b = klib.kMer(utils.as_array(counts_b, 2))

        k_diff = kdifflib.kMerDiff()
        assert k_diff.distance(profile_a, profile_b) == 0.0625

    def test_kmerdiff_distance_k8(self):
        counts_a = utils.counts(utils.SEQUENCES_LEFT, 8)
        counts_b = utils.counts(utils.SEQUENCES_RIGHT, 8)

        profile_a = klib.kMer(utils.as_array(counts_a, 8))
        profile_b = klib.kMer(utils.as_array(counts_b, 8))

        k_diff = kdifflib.kMerDiff()
        np.testing.assert_almost_equal(k_diff.distance(profile_a, profile_b), 0.4626209322)
