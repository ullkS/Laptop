import colorsys

def rgb_to_lab(r, g, b):
    var_R = r / 255
    var_G = g / 255
    var_B = b / 255

    if var_R > 0.04045:
        var_R = ((var_R + 0.055) / 1.055) ** 2.4
    else:
        var_R = var_R / 12.92
    if var_G > 0.04045:
        var_G = ((var_G + 0.055) / 1.055) ** 2.4
    else:
        var_G = var_G / 12.92
    if var_B > 0.04045:
        var_B = ((var_B + 0.055) / 1.055) ** 2.4
    else:
        var_B = var_B / 12.92

    var_R = var_R * 100
    var_G = var_G * 100
    var_B = var_B * 100

    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505

    var_X = X / 95.047
    var_Y = Y / 100.000
    var_Z = Z / 108.883

    if var_X > 0.008856:
        var_X = var_X ** (1/3)
    else:
        var_X = (var_X * 903.3 + 16) / 116
    if var_Y > 0.008856:
        var_Y = var_Y ** (1/3)
    else:
        var_Y = (var_Y * 903.3 + 16) / 116
    if var_Z > 0.008856:
        var_Z = var_Z ** (1/3)
    else:
        var_Z = (var_Z * 903.3 + 16) / 116

    L = (116 * var_Y) - 16
    a = 500 * (var_X - var_Y)
    b = 200 * (var_Y - var_Z)

    return L, a, b

def lab_to_rgb(L, a, b):
    var_Y = (L + 16) / 116
    var_X = a / 500 + var_Y
    var_Z = var_Y - b / 200

    if var_Y ** 3 > 0.008856:
        var_Y = var_Y ** 3
    else:
        var_Y = (var_Y - 16 / 116) / 7.787
    if var_X ** 3 > 0.008856:
        var_X = var_X ** 3
    else:
        var_X = (var_X - 16 / 116) / 7.787
    if var_Z ** 3 > 0.008856:
        var_Z = var_Z ** 3
    else:
        var_Z = (var_Z - 16 / 116) / 7.787

    X = var_X * 95.047
    Y = var_Y * 100.000
    Z = var_Z * 108.883

    var_X = X / 100
    var_Y = Y / 100
    var_Z = Z / 100

    var_R = var_X *  3.2406 + var_Y * -1.5372 + var_Z * -0.4986
    var_G = var_X * -0.9689 + var_Y *  1.8758 + var_Z *  0.0415
    var_B = var_X *  0.0557 + var_Y * -0.2040 + var_Z *  1.0570

    if var_R > 0.0031308:
        var_R = 1.055 * (var_R ** (1 / 2.4)) - 0.055
    else:
        var_R = 12.92 * var_R
    if var_G > 0.0031308:
        var_G = 1.055 * (var_G ** (1 / 2.4)) - 0.055
    else:
        var_G = 12.92 * var_G
    if var_B > 0.0031308:
        var_B = 1.055 * (var_B ** (1 / 2.4)) - 0.055
    else:
        var_B = 12.92 * var_B

    r = int(var_R * 255)
    g = int(var_G * 255)
    b = int(var_B * 255)

    return r, g, b

def rgb_to_hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return int(h * 360), int(s * 100), int(v * 100)

def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
    return int(r * 255), int(g * 255), int(b * 255)

def rgb_to_ycbcr(r, g, b):
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cb = 0.564 * (b - y)
    cr = 0.713 * (r - y)
    return y, cb, cr

def ycbcr_to_rgb(y, cb, cr):
    r = y + 1.403 * cr
    g = y - 0.714 * cr - 0.344 * cb
    b = y + 1.773 * cb
    return int(r), int(g), int(b)

# Пример использования функций
r, g, b = 255, 0, 0
L, a, b = rgb_to_lab(r, g, b)
print(f"RGB: ({r}, {g}, {b}) -> LAB: ({L}, {a}, {b})")

h, s, v = rgb_to_hsv(r, g, b)
print(f"RGB: ({r}, {g}, {b}) -> HSV: ({h}, {s}, {v})")

y, cb, cr = rgb_to_ycbcr(r, g, b)
print(f"RGB: ({r}, {g}, {b}) -> YCbCr: ({y}, {cb}, {cr})")