import math
import numpy as np
import cv2 as cv


def thresholding_adaptative(original, umbral):
    return np.where(original > umbral, 255, 0)


def get_average(image1, max_x, max_y, windows_size1):
    g = np.copy(image1)
    for pos_x in range(max_x):
        for pos_y in range(max_y):
            left = windows_size1 // 2
            right = windows_size1 - left - 1
            p_range_x = pos_x - left
            s_range_x = pos_x + right + 1
            p_range_y = pos_y - left
            s_range_y = pos_y + right + 1
            if p_range_x < 0:
                p_range_x = 0
            if p_range_y < 0:
                p_range_y = 0
            if s_range_x > max_x + 1:
                s_range_x = max_x + 1
            if s_range_y > max_y + 1:
                s_range_y = max_y + 1
            g[pos_x][pos_y] = np.mean(image1[p_range_x:s_range_x, p_range_y:s_range_y])
    return g


def solve_thresholding_adaptative(image_original, windows_s, constant_s):
    values = image_original.shape
    g = np.uint8(get_average(image_original, values[0], values[1], windows_s) - constant_s)
    g = np.uint8(thresholding_adaptative(image_original, g))
    return g


def histogram_equalization(img, data):
    return np.where(img, data[img], 0)


def contrast_stretching_operator(image_con, values, limit_inf=0, limit_sup=255):
    for i in range(3):
        diference = values[i][1]-values[i][0]
        image_con[:, :, i] = (image_con[:, :, i] - values[i][0]) * ((limit_sup-limit_inf)/diference) + limit_inf
    return image_con


def raise_power_operator(constant, second_constant, data_pixel):
    return constant * np.power(data_pixel, second_constant)


def exponential_operator(constant, second_constant, data_pixel):
    return constant * (np.power(second_constant, data_pixel) - 1)


def logarithm_operator(constant, data_pixel):
    return constant * np.log10(1 + data_pixel)


def square_root_operator(constant, data_pixel):
    return constant * np.power(data_pixel, 0.5)


def thresholding_operator(img, r1, r2):
    return np.where((r1 <= img) & (img <= r2), 255, 0)


def add_pixel(img1, img2):
    return img1 + img2


def difference_pixel(img1, img2):
    return np.abs(img1 - img2)


def dot_images(img1, img2):
    return img1 * img2


def division_image(img1, img2):
    return img1/img2


def blinding_image(img1, img2, var_x):
    return (var_x*img1) + ((1-var_x)*img2)


def and_operator(img1, img2):
    return np.bitwise_and(img1, img2)


def or_operator(img1, img2):
    return np.bitwise_or(img1, img2)


def xor_operator(img1, img2):
    return np.bitwise_xor(img1, img2)


def not_operator(img1):
    return np.bitwise_not(img1)


def get_values(matrix):
    rows, columns = matrix.shape
    minimo = 260
    maximo = 0
    for i in range(rows):
        for j in range(columns):
            if i == j:
                continue
            if matrix[i, j] < minimo:
                minimo = matrix[i, j]

            if matrix[i, j] > maximo:
                maximo = matrix[i, j]
    return minimo, maximo


def filtro_conservating(imagen):
    img = np.copy(imagen)
    rows, columns = img.shape
    for i in range(1, rows-1):
        for j in range(1, columns-1):
            minimo, maximo = get_values(imagen[i-1:i+2, j-1:j+2])
            if img[i, j] < minimo:
                img[i, j] = minimo
            elif img[i, j] > maximo:
                img[i, j] = maximo
    return img


def detect_advance(img, punto, superior, lado):
    best_point = np.array(punto, dtype=int)
    print(best_point)
    while img[best_point[1], best_point[0]]:
        if superior == 0 and lado == 0:
            if img[best_point[1] - 1, best_point[0]] == 255:
                best_point[1] = best_point[1] - 1
            elif img[best_point[1], best_point[0]-1] == 255:
                best_point[0] = best_point[0]-1
            else:
                break
        if superior == 1 and lado == 0:
            if img[best_point[1] - 1, best_point[0]] == 255:
                best_point[1] = best_point[1] - 1
            elif img[best_point[1], best_point[0]+1] == 255:
                best_point[0] = best_point[0]+1
            else:
                break

        if superior == 0 and lado == 1:
            if img[best_point[1] + 1, best_point[0]] == 255:
                best_point[1] = best_point[1] + 1
            elif img[best_point[1], best_point[0]-1] == 255:
                best_point[0] = best_point[0]-1
            else:
                break

        if superior == 1 and lado == 1:
            if img[best_point[1] + 1, best_point[0]] == 255:
                best_point[1] = best_point[1] + 1
            elif img[best_point[1], best_point[0]+1] == 255:
                best_point[0] = best_point[0]+1
            else:
                break

    return best_point


def help_detect_corners(img, corners):
    another_corners = np.zeros((4, 2), dtype=np.float32)
    helper = corners[corners[:, 0].argsort()]
    if helper[0, 1] < helper[1, 1]:
        another_corners[0] = detect_advance(img, helper[0, :], 0, 0)
        another_corners[1] = detect_advance(img, helper[1, :], 0, 1)
    else:
        another_corners[0] = detect_advance(img, helper[1, :], 0, 0)
        another_corners[1] = detect_advance(img, helper[0, :], 0, 1)
    if helper[2, 1] < helper[3, 1]:
        another_corners[2] = detect_advance(img, helper[2, :], 1, 0)
        another_corners[3] = detect_advance(img, helper[3, :], 1, 1)
    else:
        another_corners[2] = detect_advance(img, helper[3, :], 1, 0)
        another_corners[3] = detect_advance(img, helper[2, :], 1, 1)

    return another_corners


def detect_corners(img):
    esquinas = np.zeros((4, 2), dtype=np.float32)
    rows, columns = img.shape
    columna = 0
    fila = 0
    contador = 0
    rango_valido = 50
    # detectar primeras esquinas empezando por izquierda, pasando por columnas
    for i in range(columns):
        estado = False
        for j in range(rows):
            if img[j, i] == 255:
                fila = j
                columna = i
                estado = True
                break
        if estado:
            break

    for i in range(rows-1, 0, -1):
        if img[i, columna] == 255:
            if abs(i - fila) < rango_valido:
                esquinas[contador, 0] = columna
                esquinas[contador, 1] = (fila + i) // 2
                contador = contador + 1
            else:
                esquinas[contador, 0] = columna
                esquinas[contador, 1] = fila
                contador = contador + 1
                esquinas[contador, 0] = columna
                esquinas[contador, 1] = i
                contador = contador + 1
            break

    # detectar esquinas Empezando por derecha, pasando por columnas
    for i in range(columns-1, 0, -1):
        estado = False
        for j in range(rows):
            if img[j, i] == 255:
                fila = j
                columna = i
                estado = True
                break
        if estado:
            break

    for i in range(rows-1, 0, -1):
        if img[i, columna] == 255:
            if abs(i - fila) < rango_valido:
                esquinas[contador, 0] = columna
                esquinas[contador, 1] = (fila + i) // 2
                contador = contador + 1
            else:
                esquinas[contador, 0] = columna
                esquinas[contador, 1] = fila
                contador = contador + 1
                esquinas[contador, 0] = columna
                esquinas[contador, 1] = i
                contador = contador + 1
            break

    if contador == 4:
        return esquinas
    else:
        # detectar esquinas empezando por arriba, pasando por filas
        for i in range(rows):
            estado = False
            for j in range(columns):
                if img[i, j] == 255:
                    fila = i
                    columna = j
                    estado = True
                    break
            if estado:
                break

        for i in range(columns - 1, 0, -1):
            if img[fila, i] == 255:

                if abs(i - columna) < rango_valido:
                    flag = False
                    for k in range(contador):
                        if abs(esquinas[k, 0] - columna) < rango_valido and abs(esquinas[k, 1] - fila) < rango_valido:
                            flag = True
                            break
                    if not flag:
                        esquinas[contador, 0] = columna
                        esquinas[contador, 1] = fila

                        contador = contador + 1
                else:
                    flag = False
                    for k in range(contador):
                        if abs(esquinas[k, 0] - columna) < rango_valido and abs(esquinas[k, 1] - fila) < rango_valido:
                            flag = True
                            break
                    if not flag:
                        esquinas[contador, 0] = columna
                        esquinas[contador, 1] = fila
                        contador = contador + 1

                    flag = False
                    for k in range(contador):
                        if abs(esquinas[k, 0] - columna) < rango_valido and abs(esquinas[k, 1] - fila) < rango_valido:
                            flag = True
                            break
                    if not flag:
                        esquinas[contador, 0] = i
                        esquinas[contador, 1] = fila
                        contador = contador + 1
                break

        if contador == 4:
            return esquinas

        # detectar esquinas empezando por abajo, pasando por filas
        for i in range(rows - 1, 0, -1):
            estado = False
            for j in range(columns):
                if img[i, j] == 255:
                    fila = i
                    columna = j
                    estado = True
                    break
            if estado:
                break

        for i in range(columns - 1, 0, -1):
            if img[fila, i] == 255:
                if abs(i - columna) < rango_valido:
                    flag = False
                    for k in range(contador):
                        if abs(esquinas[k, 0] - columna) < rango_valido and abs(esquinas[k, 1] - fila) < rango_valido:
                            flag = True
                            break
                    if not flag:
                        esquinas[contador, 0] = columna
                        esquinas[contador, 1] = fila
                        contador = contador + 1
                else:
                    flag = False
                    for k in range(contador):
                        if abs(esquinas[k, 0] - columna) < rango_valido and abs(esquinas[k, 1] - fila) < rango_valido:
                            flag = True
                            break
                    if not flag:
                        esquinas[contador, 0] = columna
                        esquinas[contador, 1] = fila
                        contador = contador + 1
                    flag = False
                    for k in range(contador):
                        if abs(esquinas[k, 0] - columna) < rango_valido and abs(esquinas[k, 1] - fila) < rango_valido:
                            flag = True
                            break
                    if not flag:
                        esquinas[contador, 0] = i
                        esquinas[contador, 1] = fila
                        contador = contador + 1
                break

    if contador == 4:
        return esquinas

    punto_referencia = np.array([0, 0])
    helper = np.sort(esquinas[:3, 0])
    helper1 = np.sort(esquinas[:3, 1])
    # 0 -> conviene que se lo mas pequeño posible y 1-> lo mas alto
    eje_x = -1
    eje_y = -1
    if helper[1] - helper[0] > helper[2] - helper[1]:
        punto_referencia[0] = helper[0]
        eje_x = 1
    else:
        punto_referencia[0] = helper[2]

    if helper1[1] - helper1[0] > helper1[2] - helper1[1]:
        punto_referencia[1] = helper1[0]
        eje_y = 1
    else:
        punto_referencia[1] = helper1[2]

    while img[punto_referencia[1], punto_referencia[0]] != 255:
        punto_referencia[0] = punto_referencia[0] + eje_x
        punto_referencia[1] = punto_referencia[1] + eje_y

    esquinas[contador, 0] = punto_referencia[0]
    esquinas[contador, 1] = punto_referencia[1]
    esquinas = help_detect_corners(img, esquinas)
    return esquinas


def matrix_get_affine(pts1, pts2):
    answer = np.zeros((2, 3), dtype=np.float64)
    matrix_a = np.zeros((3, 3), dtype=np.float64)
    matrix_b = np.zeros((3, 1), dtype=np.float64)
    for i in range(len(pts1)):
        matrix_a[i, :] = np.array([pts1[i][0], pts1[i][1], 1], dtype=np.float64)
        matrix_b[i, 0] = pts2[i][0]
    value = cv.solve(matrix_a, matrix_b)[1]
    answer[0, :] = np.transpose(value)

    for i in range(len(pts1)):
        matrix_b[i, 0] = pts2[i][1]
    value = cv.solve(matrix_a, matrix_b)[1]
    answer[1, :] = np.transpose(value)
    return answer


def affine_copy(image, matrix, dim_out):
    image_original = np.float32(image)
    image_blank = np.zeros([dim_out[1], dim_out[0], 3], dtype=np.float32)
    rows1, columns1 = (dim_out[0], dim_out[1])
    matrix_a = matrix[:2, :2]
    matrix_b = matrix[:, 2:]
    answer = np.array([[0], [0]], dtype=np.float32)
    for u in range(rows1):
        for v in range(columns1):
            value_y = np.array([[u], [v]], dtype=np.float32) - matrix_b
            cv.solve(matrix_a, value_y, answer)
            valor_x = int(round(answer[0, 0]))
            valor_y = int(round(answer[1, 0]))
            # image_blank[v, u] = image[valor_y, valor_x]
            if 0 <= valor_x < image_original.shape[0] and 0 <= valor_y < image_original.shape[1]:
                image_blank[v, u] = image_original[valor_y, valor_x]

    return np.uint8(image_blank)


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def get_points_limits(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1],[0, maxHeight - 1]], dtype="float32")
    return rect, dst, maxWidth, maxHeight

# --------------------------------------
# Función Perspective transform
# --------------------------------------


def copy_get_perspective_transform(src, dst):
    M = np.ndarray((3, 3), dtype=float)
    A = np.ndarray((8, 8), dtype=float)
    B = np.ndarray((8, 1), dtype=float)
    X = np.ndarray((8, 1), dtype=float)
    for i in range(len(src)):
        A[i, 0] = A[i+4, 3] = src[i, 0]
        A[i, 1] = A[i + 4, 4] = src[i, 1]
        A[i, 2] = A[i + 4, 5] = 1
        A[i, 3] = A[i, 4] = A[i, 5] = A[i + 4, 0] = A[i + 4, 1] = A[i + 4, 2] = 0
        A[i, 6] = -src[i, 0] * dst[i, 0]
        A[i, 7] = -src[i, 1] * dst[i, 0]
        A[i + 4, 6] = -src[i, 0] * dst[i, 1]
        A[i + 4, 7] = -src[i, 1] * dst[i, 1]
        B[i] = dst[i, 0]
        B[i + 4] = dst[i, 1]

    cv.solve(A, B, X, cv.DECOMP_LU)
    for i in range(len(X)):
        M[i//3, i % 3] = X[i]
    M[2, 2] = 1.
    return M

# --------------------------------------
# Función Warp Perspective
# --------------------------------------


def copy_warp_perspective(image, matrix, dim_out):
    image_blank = np.ndarray((dim_out[1], dim_out[0], 3), dtype=float)

    rows1, columns1 = (dim_out[0], dim_out[1])
    for i in range(rows1):
        for j in range(columns1):
            image_blank[j, i] = (255, 255, 255)

    matrix_in = np.ndarray((2, 1), dtype=float)
    valores = np.ndarray((2, 1), dtype=float)
    for x in range(1, rows1):
        for y in range(1, columns1):
            matrix_copy = np.copy(matrix)
            matrix_copy[0, :] = matrix_copy[0, :] / float(x)
            matrix_copy[0, :2] = matrix_copy[0, :2] - matrix_copy[2, :2]
            matrix_copy[1, :] = matrix_copy[1, :] / float(y)
            matrix_copy[1, :2] = matrix_copy[1, :2] - matrix_copy[2, :2]
            matrix_in[0, 0] = matrix_copy[2, 2] - matrix_copy[0, 2]
            matrix_in[1, 0] = matrix_copy[2, 2] - matrix_copy[1, 2]

            cv.solve(matrix_copy[:2, :2], matrix_in, valores)
            valor_x = valores[0, 0]
            valor_y = valores[1, 0]
            if 0 <= valor_x < image.shape[1] and 0 <= valor_y < image.shape[0]:
                image_blank[y, x] = image[int(valor_y), int(valor_x)]

    image_blank[0, 0] = image_blank[1, 1]
    for i in range(1, rows1):
        image_blank[0, i] = image_blank[1, i]

    for i in range(1, columns1):
        image_blank[i, 0] = image_blank[i, 1]

    return image_blank


# --------------------------------------
# Erotion
# --------------------------------------
def color_get_erotion(data, color):
    for i in range(len(data)):
        if type(color) != int:
            if color[0] != data[i, 0] or color[1] != data[i, 1] or color[2] != data[i, 2]:
                return data[i]
        else:
            if color != data[i]:
                return data[i]

    return color


def erotion(imagen, tam_kernel):
    val_start = tam_kernel // 2
    image_mod = np.copy(imagen)
    comparador = 0
    if len(imagen.shape) == 3:
        comparador = (0, 0, 0)
    rows1, columns1 = imagen.shape[:2]
    for i in range(val_start, rows1):
        for j in range(columns1):
            image_mod[i, j] = color_get_erotion(imagen[i-val_start:i+val_start, j], comparador)
    return image_mod

# --------------------------------------
# Dilation
# --------------------------------------


def color_get_dilation(data, color):
    rows1, columns1 = data.shape[:2]
    for i in range(rows1):
        for j in range(columns1):
            if type(color) != int:
                if color[0] == data[i, j, 0] and color[1] == data[i, j, 1] and color[2] == data[i, j, 2]:
                    return True, color
            else:
                if color == data[i, j]:
                    return True, color
    return False, None


def dilation(imagen, tam_kernel):
    val_start = tam_kernel // 2
    image_mod = np.copy(imagen)
    comparador = 0
    if len(imagen.shape) == 3:
        comparador = (0, 0, 0)
    rows1, columns1 = imagen.shape[:2]
    for i in range(val_start, rows1):
        for j in range(val_start, columns1):
            state = color_get_dilation(imagen[i-val_start:i+val_start, j - val_start: j + val_start], comparador)
            if state[0]:
                image_mod[i, j] = state[1]
    return image_mod

# --------------------------------------
# Función closing
# --------------------------------------


def closing_fun(image, kernel_dil, kernel_erot):
    image_answer_2 = dilation(image, kernel_dil)
    answer = erotion(image_answer_2, kernel_erot)
    return answer
# --------------------------------------
# Función filtro gaussiano
# --------------------------------------


def get_matrix_gaussian(dimension, desviacion):
    matrix = np.ndarray((dimension, dimension), dtype=float)
    for i in range(dimension):
        for j in range(dimension):
            matrix[i, j] = math.e**((- j**2 + i**2) / (2 * desviacion**2)) / (2 * math.pi * desviacion**2)
    return matrix


def filtro_gaussiano(img, dim):
    image_blank = np.copy(img)
    rows, columns = img.shape
    matrix = get_matrix_gaussian(dim, 1)
    inicio = dim // 2
    for i in range(inicio, rows):
        for j in range(inicio, columns):
            image_blank[i, j] = int(round(np.sum(image_blank[i, j] * matrix)))

    return image_blank
# --------------------------------------
# Función scanner to solve
# --------------------------------------


def solve_scanner_perspective(image, points):
    rect, dst, maxWidth, maxHeight = get_points_limits(image, points)
    M = cv.getPerspectiveTransform(rect, dst)
    image_answer_2 = cv.warpPerspective(image, M, (maxWidth, maxHeight))
    # image_answer_2 = closing_fun(image_answer_2, 2, 2)
    return image_answer_2


