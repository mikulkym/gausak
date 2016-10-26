import numpy

def generatePixelModel(K, sigma, weight_init):
    """
    :param K: pocet povrchu pixelu
    :param sigma: odchylka
    :param weight_init: vaha pixelu, (1/pocet povrchu), (celkovy soucet vah je 1)
    :return: pixel model
    """
    # pm = [[weight], [mu], [sigma]]
    pm = [[], [], []]
    for k in range(K):
        pm[0].append(weight_init)
        pm[1].append(k*(255/K) + (255/K)/2)
        pm[2].append(sigma)
    return pm


class Model:
    def __init__(self, width, height, K, sigma, alpha, sigma_thresh, T):
        self.K = K
        self.T = T
        self.alpha = alpha
        self.sigma_tresh = sigma_thresh
        self.width = width
        self.height = height
        weight_init = 1.0 / K
        # generator v generatoru
        # self.pm = [[generatePixelModel(K, sigma, weight_init) for j in range(width)] for i in range(height)]
        self.pm = numpy.empty((height, width), numpy.object)
        # print self.pm

        initial_mu = numpy.zeros((K,), numpy.float)
        for k in range(K):
            initial_mu[k] = (k * (255 / K) + (255 / K) / 2)

        initial_sigma = numpy.zeros((K,), numpy.float)
        initial_sigma.fill(sigma)

        initial_weight = numpy.zeros((K,), numpy.float)
        initial_weight.fill(weight_init)
        #
        # for x in numpy.nditer(self.pm, op_flags=['readwrite'], flags = ['REFS_OK']):
        #     x[...] = numpy.array([numpy.copy(initial_weight), numpy.copy(initial_mu), numpy.copy(initial_sigma)])
        for i in xrange(height):
            for j in xrange(width):
                self.pm[i][j] = numpy.array([numpy.copy(initial_weight), numpy.copy(initial_mu), numpy.copy(initial_sigma)])

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

        # prepare initial
        # vypocitam si hodnoty(jeden pixel)
        mu_init = numpy.zeros((K,), numpy.float)
        for k in xrange(0, K):
            mu_init[k] = (k * (255 / K) + (255 / K) / 2)

        # prekopiruju
        tmp_mu = numpy.empty((num_pixels, K), numpy.float)
        for pixel in xrange(0, num_pixels):
            for i in xrange(0, K):
                tmp_mu[pixel][i] = mu_init[i]

        self.mu = tmp_mu
