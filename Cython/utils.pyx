# cython: profile=True
# cython: linetrace=True
import math
# from libc.stdint cimport uintptr_t

cdef void update_model(model, img):
    """
    :param model: model obrazku
    :param img: obrazek
    """
    cdef int width = model.width
    cdef int height = model.height
    pm = model.pm

    cdef int x, y

    # print (height, width)
    for x in range(height):
        for y in range(width):
            # print (x, y)
            c = img.getpixel((y, x))
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


def sum_and_max_gauss_mixture(int pixel_val, pm_xy, int K):
    """
    :param pixel_val: barva pixelu
    :param pm_xy: pixel model na pozici [x][y], 3 prvky [[weight], [mu], [sigma]]
    :param K: povrch pixelu
    :return: soucet mixtury Gaussianu, povrch s nejvetsi pravdepodobnosti vyskytu, Baesuv teorem
    """
    cdef float gauss_sum = 0.0
    cdef int max_k = 0
    cdef float max_distribution = -10.0
    cdef float weight_k
    cdef float mu_k
    cdef float sigma_k
    cdef float tmp_distribution

    weights = pm_xy[0]
    mus = pm_xy[1]
    sigmas = pm_xy[2]

    for k in range(K):
        weight_k = weights[k]
        mu_k = mus[k]
        sigma_k = sigmas[k]

        tmp_distribution = weighted_distribution(pixel_val, weight_k, mu_k, sigma_k)
        gauss_sum += tmp_distribution

        if tmp_distribution > max_distribution:
            max_distribution = tmp_distribution
            max_k = k

    return (gauss_sum, max_k, (max_distribution / gauss_sum))


cdef float weighted_distribution(int pixel, float weight, float mu, float sigma):
    """
    :param pixel: barva pixelu
    :param weight: vaha pixelu
    :param mu: stredni hodnota
    :param sigma: odchylka
    :return: vazena distribuce
    """
    return weight * gauss_pdf(pixel, mu, sigma)


cdef float SQRT_2PI = math.sqrt(2.0 * math.pi)


cdef float gauss_pdf(int x, float mu, float sigma):
    """
    Funkce hustoty pravdepodobnosti pro jeden pixel (Probability Density Function)
    :param x: pixel
    :param mu: stredni hodnota
    :param sigma: odchylka
    :return: hustota pravdepodobnosti (hodnota normalniho rozdeleni pro dany pixel)
    """
    # exponent argumentu
    cdef float x_mu = x - mu
    cdef float exp_arg = -((x_mu*x_mu) / 2.0 * sigma * sigma)
    # cdef float e = math.pow(math.e, exp_arg)
    cdef float e = pow(math.e, exp_arg)

    return (1.0 / (sigma * SQRT_2PI)) * e


cdef void extract_fg(model, inp_img, fg_img):
    """
    vytahnuti popredi
    :param model: model obrazku
    :param inp_img: vstupni obrazek
    :param fg_img: vystupni obrazek
    """
    cdef float LAMBDA = 2.5
    pm = model.pm
    cdef unsigned int b = 0
    # fg_img.fill(0)
    cdef float sum_thresh
    cdef int x, y, k
    for x in range(model.height):
        for y in range(model.width):
            color = inp_img.getpixel((y, x))
            sum_thresh = 0.0

            for k in range(model.K):
                sum_thresh += pm[x][y][0][k]

                if sum_thresh > model.T:
                    b = k
                    break

            mu_k = pm[x][y][1][b]
            sigma_k = pm[x][y][2][b]

            if math.fabs(int(color) - mu_k) > LAMBDA * sigma_k:
                fg_img.putpixel((y, x), 255)
            else:
                fg_img.putpixel((y, x), 0)
