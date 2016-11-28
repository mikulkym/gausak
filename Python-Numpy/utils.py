import math
import numpy as np


def update_model(model, img):
    """
    :param model: model obrazku
    :param img: obrazek
    """
    width = model.width
    height = model.height

    # print (height, width)
    for x in range(height):
        for y in range(width):
            index = count_index_2d(x, y, width)
            weight = model.weight[index]
            sigma = model.sigma[index]
            mu = model.mu[index]
            # print (x, y)
            c = img[x][y]
            # it.iternext()

            sum_gauss_mix, argmax_k, bay = sum_and_max_gauss_mixture(int(c), weight, sigma, mu, model.K)
            weight_k = weight[argmax_k]
            mu_k = mu[argmax_k]
            sigma_k = sigma[argmax_k]

            weight_k_1 = (1.0 - model.alpha) * weight_k + model.alpha * bay
            weight[argmax_k] = weight_k_1
            normalize_weight(weight, model.K)

            rho_k = (model.alpha * bay) / weight_k_1
            rho_k_1 = (1.0 - rho_k)
            mu_k_1 = rho_k_1 * mu_k + rho_k * float(c)
            sigma_k_1 = rho_k_1 * (sigma_k * sigma_k) + rho_k * (c - mu_k)*(c - mu_k)

            mu[argmax_k] = mu_k_1

            new_sigma = math.sqrt(sigma_k_1)
            if new_sigma > model.sigma_tresh:
                sigma[argmax_k] = new_sigma


def normalize_weight(weight, K):
    """
    normalizace vah (soucet vah 1)
    :param weight: pole vah pro jeden pixel
    :param K: pocet vah
    """

    sum_weight = sum(weight)
    for k in range(K):
        weight[k] /= sum_weight


def sum_and_max_gauss_mixture(pixel_val, weight, sigma, mu, K):
    """
    :param pixel_val: pixel na pozici img[x][y]
    :param weight: vaha pixelu
    :param sigma: odchylka
    :param mu: stredni hodnota
    :param K: povrch pixelu
    :return: soucet mixtury Gaussianu, povrch s nejvetsi pravdepodobnosti vyskytu, Baesuv teorem
    """

    gauss_sum = 0.0
    max_k = 0
    max_distribution = -10.0

    for k in range(K):
        weight_k = weight[k]
        mu_k = mu[k]
        sigma_k = sigma[k]

        tmp_distribution = weighted_distribution(pixel_val, weight_k, mu_k, sigma_k)
        gauss_sum += tmp_distribution

        if tmp_distribution > max_distribution:
            max_distribution = tmp_distribution
            max_k = k

    return gauss_sum, max_k, (max_distribution / gauss_sum)


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
    x_mu = x - mu

    exp_arg = -(x_mu * x_mu / (2.0 * sigma * sigma))
    e = math.exp(exp_arg)

    return (1.0 / (sigma * SQRT_2PI)) * e


def extract_fg(model, inp_img, fg_img):
    """
    vytahnuti popredi
    :param model: model obrazku
    :param inp_img: vstupni obrazek
    :param fg_img: vystupni obrazek
    """
    LAMBDA = 2.5
    b = 0
    # fg_img.fill(0)

    for x in range(model.width):
        for y in range(model.height):
            index = count_index_2d(y, x, model.width)
            weight = model.weight[index]
            sigma = model.sigma[index]
            mu = model.mu[index]

            color = inp_img[y][x]
            sum_thresh = 0.0

            for k in range(model.K):
                sum_thresh += weight[k]

                if sum_thresh > model.T:
                    b = k
                    break

            mu_k = mu[b]
            sigma_k = sigma[b]

            if math.fabs(int(color) - mu_k) > LAMBDA * sigma_k:
                fg_img[y][x] = 255
            else:
                fg_img[y][x] = 0


def count_index_2d(y, x, num_x):
    """
    Count 1D array index from 2D
    :param y: int row
    :param x: int column
    :param num_x: int number of row
    :return:
    """
    return y * num_x + x


"""
def count_index_3d(x, y, z, num_y, num_z):

    Count 1D array index from 3D
    :param x: int row
    :param y: int col
    :param z: int depth element
    :param num_y: int number of columns
    :param num_z: int number of elements (max depth)
    :return:

    return (x * num_y * num_z) + (y * num_z) + z
"""