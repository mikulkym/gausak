# cython: profile=True
# cython: linetrace=True


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
        self.pm = [[generatePixelModel(K, sigma, weight_init) for j in range(width)] for i in range(height)]
