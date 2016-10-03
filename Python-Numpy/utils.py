import math
import numpy as np
def update_model(model, img):
    """
    :param model: model obrazku
    :param img: obrazek
    """
    width = model.width
    height = model.height
    pm = model.pm

    print (height, width)
    # for x in range(height):
    #     for y in range(width):
    # iterator
    it = np.nditer(img, flags = ['multi_index'])
    while not it.finished:
        x, y = it.multi_index
        # print (x, y)
        c = it[0]
        it.iternext()
        pm_xy = pm[x][y]
        #cython, nativni pole, array python. numpy a araay ukladani cisel, pro pixel 3 pole, struktura poli,
        #  pole R, pole G, pole B, pole separatne pro mu, theta
        sum_gauss_mix, argmax_k, bay = sum_and_max_gauss_mixture(int(c), pm_xy, model.K)
        weight_k = pm_xy[0][argmax_k]
        mu_k = pm_xy[1][argmax_k]
        sigma_k = pm_xy[2][argmax_k]

        weight_k_1 = (1.0 - model.alpha) * weight_k + model.alpha * bay
        pm_xy[0][argmax_k] = weight_k_1
        normalize_weight(model, x, y)

        rho_k = (model.alpha * bay) / weight_k_1
        rho_k_1 = (1.0 - rho_k)
        mu_k_1 = rho_k_1 * mu_k + rho_k * float(c)
        sigma_k_1 = rho_k_1 * pow(sigma_k, 2) + rho_k * pow(c - mu_k, 2)

        pm_xy[1][argmax_k] = mu_k_1

        new_sigma = math.sqrt(sigma_k_1)
        if new_sigma > model.sigma_tresh:
            pm_xy[2][argmax_k] = new_sigma


def normalize_weight(model, x, y):
    """
    normalizace vah (soucet vah 1)
    :param model: model obrazku
    :param x: pozice x
    :param y: pozice y
    """
    sum_weight = sum(model.pm[x][y][0])
    for k in range(model.K):
        model.pm[x][y][0][k] /= sum_weight


def sum_and_max_gauss_mixture(pixel_val, pm_xy, K):
    """
    :param pixel_val: barva pixelu
    :param pm_xy: pixel model na pozici [x][y]
    :param K: povrch pixelu
    :return: soucet mixtury Gaussianu, povrch s nejvetsi pravdepodobnosti vyskytu, Baesuv teorem
    """
    gauss_sum = 0.0
    max_k = 0
    max_distribution = -10.0

    for k in range(K):
        weight_k = pm_xy[0][k]
        mu_k = pm_xy[1][k]
        sigma_k = pm_xy[2][k]

        tmp_distribution = weighted_distribution(pixel_val, weight_k, mu_k, sigma_k)
        gauss_sum += tmp_distribution

        if tmp_distribution > max_distribution:
            max_distribution = tmp_distribution
            max_k = k

    return (gauss_sum, max_k, (max_distribution / gauss_sum))


def weighted_distribution(pixel, weight, mu, sigma):
    """
    :param pixel: barva pixelu
    :param weight: vaha pixelu
    :param mu: stredni hodnota
    :param sigma: odchylka
    :return: vazena distribuce
    """
    return weight * gauss_pdf(pixel, mu, sigma)


SQRT_2PI = math.sqrt(2.0 * math.pi)


def gauss_pdf(x, mu, sigma):
    """
    Funkce hustoty pravdepodobnosti pro jeden pixel (Probability Density Function)
    :param x: pixel
    :param mu: stredni hodnota
    :param sigma: odchylka
    :return: hustota pravdepodobnosti (hodnota normalniho rozdeleni pro dany pixel)
    """
    # exponent argumentu
    exp_arg = -(pow(x - mu, 2) / (2.0 * pow(sigma, 2)))
    e = math.pow(math.e, exp_arg)

    return (1.0 / (sigma * SQRT_2PI)) * e


def extract_fg(model, inp_img, fg_img):
    """
    vytahnuti popredi
    :param model: model obrazku
    :param inp_img: vstupni obrazek
    :param fg_img: vystupni obrazek
    """
    LAMBDA = 2.5
    pm = model.pm
    b = 0
    # fg_img.fill(0)

    for x in range(model.height):
        for y in range(model.width):
            color = inp_img[x][y]
            sum_thresh = 0.0

            for k in range(model.K):
                sum_thresh += pm[x][y][0][k]

                if sum_thresh > model.T:
                    b = k
                    break

            mu_k = pm[x][y][1][b]
            sigma_k = pm[x][y][2][b]

            if math.fabs(int(color) - mu_k) > LAMBDA * sigma_k:
                fg_img[x][y] = 255
            else:
                fg_img[x][y] = 0
