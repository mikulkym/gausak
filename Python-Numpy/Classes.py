import numpy


class Model1D:
    def __init__(self, width, height, K, sigma, alpha, sigma_thresh, T):
        self.K = K
        self.T = T
        self.alpha = alpha
        self.sigma_tresh = sigma_thresh
        self.width = width
        self.height = height

        num_pixels = width * height

        # weight
        self.weight = numpy.empty((num_pixels, K), numpy.float)
        for i in xrange(0, num_pixels):
            self.weight[i].fill(1.0 / K)

        # sigma
        self.sigma = numpy.empty((num_pixels, K), numpy.float)
        for i in xrange(0, num_pixels):
            self.sigma[i].fill(sigma)

        # mu
        # prepare initial, vypocet hodnot pro jeden pixel
        mu_init = numpy.zeros((K,), numpy.float)
        for k in xrange(0, K):
            mu_init[k] = (k * (255 / K) + (255 / K) / 2)

        tmp_mu = numpy.empty((num_pixels, K), numpy.float)
        for pixel in xrange(0, num_pixels):
            for i in xrange(0, K):
                tmp_mu[pixel][i] = mu_init[i]

        self.mu = tmp_mu
