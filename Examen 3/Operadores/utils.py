import os
import shutil
from CG_Operadores.settings import MEDIA_ROOT
from matplotlib import pyplot as plt
from .algoritmos import *
from django.core.files.storage import FileSystemStorage
import json
from json import JSONEncoder
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils



class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def solve_exponential(path, name, constant, second_constant):
    image = cv.imread(path + "/" + name)
    message_failed = "Didn't create file"
    if image is None:
        return False, message_failed
    col=['r','g','b']
    for i in range(len(image[0][0])):
        h=cv2.calcHist([image], [i], None, [256], [0, 256])
    
    #nueva imagen
    out=np.zeros(shape=image.shape,dtype=np.uint8)
    #aplicamos el Histogram equalization en los 3 canales
    for i in range(len(image[0][0])):
        for j in range(image.shape[0]):
            for k in range(image.shape[1]):
                #vtmp = c*((b**image[j][k][i])-1)
                g = np.uint8(exponential_operator(constant, second_constant, image[j][k][i]))
                if g>255:
                    g=255
                if g<0:
                    g=0
                out[j][k][i]=g

    name_to_archive = "exponential_of_"+name+"_"+str(constant)+"_"+str(second_constant)+".png"
    ubication_final = MEDIA_ROOT + "/" + name_to_archive
    check_folder(ubication_final)
    cv.imwrite(ubication_final+"/"+name_to_archive, out)
    return True, name_to_archive, ubication_final


def solve_logarithm(path, name, constant):
    image = cv.imread(path + "/" + name)
    message_failed = "Didn't create file"
    if image is None:
        return False, message_failed
    g = np.uint8(logarithm_operator(constant, image))
    name_to_archive = "logarithm_of_"+name+"_"+str(constant)+".png"
    ubication_final = MEDIA_ROOT + "/" + name_to_archive
    check_folder(ubication_final)
    cv.imwrite(ubication_final + "/" + name_to_archive, g)
    return True, name_to_archive, ubication_final


def solve_raise_power(path, name, constant, second_constant):
    image = cv.imread(path + "/" + name)
    message_failed = "Didn't create file"
    if image is None:
        return False, message_failed
    g = np.uint8(raise_power_operator(constant, second_constant, image))
    name_to_archive = "raise_power_of_"+name+"_"+str(constant)+"_"+str(second_constant)+".png"
    ubication_final = MEDIA_ROOT + "/" + name_to_archive
    check_folder(ubication_final)
    cv.imwrite(ubication_final + "/" + name_to_archive, g)
    return True, name_to_archive, ubication_final


def solve_square_root(path, name, constant):
    image = cv.imread(path + "/" + name)
    message_failed = "Didn't create file"
    if image is None:
        return False, message_failed
    g = np.uint8(square_root_operator(constant, image))
    name_to_archive = "square_root_of_"+name+"_"+str(constant)+".png"
    ubication_final = MEDIA_ROOT + "/" + name_to_archive
    check_folder(ubication_final)
    cv.imwrite(ubication_final + "/" + name_to_archive, g)
    return True, name_to_archive, ubication_final


def solve_thresholding(path, name, constant, constant1):
    original = cv.imread(path + "/" + name)
    message_failed = "Didn't create file"
    if original is None:
        return False, message_failed

    image = cv.cvtColor(original, cv.COLOR_BGR2GRAY)
    g = np.uint8(thresholding_operator(image, constant, constant1))
    name_to_archive = "thresholding_of_"+name+"_"+str(constant)+"_"+str(constant1)+".png"
    ubication_final = MEDIA_ROOT + "/" + name_to_archive
    check_folder(ubication_final)
    cv.imwrite(ubication_final + "/" + name_to_archive, g)
    return True, name_to_archive, ubication_final


# suma y  resta de imagenes

def rescale(img, img1, value):
    first_image = cv.resize(img, value)
    second_image = cv.resize(img1, value)
    return first_image, second_image


def get_max_values(img, img1):
    rows1 = max(img.shape[0], img1.shape[0])
    columns1 = max(img.shape[1], img1.shape[1])
    # return rows1, columns1
    return columns1, rows1


def solve_addition(path, name, variable1):
    image = cv.imread(path + "/" + name)
    message_failed = "Didn't create file"
    image1 = variable1
    if type(variable1) != str:
        if image is None:
            return False, message_failed
    else:
        image1 = cv.imread(path + "/" + variable1)
        if image is None or image1 is None:
            return False, message_failed

        max_ranges = get_max_values(image, image1)
        image, image1 = rescale(image, image1, max_ranges)

    g = np.uint8(add_pixel(image, image1))
    name_to_archive = "Addition_of_"+name+"_"+str(variable1)+".png"
    ubication_final = MEDIA_ROOT + "/" + name_to_archive
    check_folder(ubication_final)
    cv.imwrite(ubication_final + "/" + name_to_archive, g)
    return True, name_to_archive, ubication_final


def solve_difference(path, name, variable1):
    image = cv.imread(path + "/" + name)
    message_failed = "Didn't create file"
    image1 = variable1
    if type(variable1) != str:
        if image is None:
            return False, message_failed
    else:
        image1 = cv.imread(path + "/" + variable1)
        if image is None or image1 is None:
            return False, message_failed

        max_ranges = get_max_values(image, image1)
        image, image1 = rescale(image, image1, max_ranges)

    g = np.uint8(difference_pixel(image, image1))
    name_to_archive = "Difference_of_"+name+"_"+str(variable1)+".png"
    ubication_final = MEDIA_ROOT + "/" + name_to_archive
    check_folder(ubication_final)
    cv.imwrite(ubication_final + "/" + name_to_archive, g)
    return True, name_to_archive, ubication_final


# multiplicación, division, blinding

def solve_dot(path, name, variable1):
    image = cv.imread(path + "/" + name)
    message_failed = "Didn't create file"
    image1 = variable1
    if type(variable1) != str:
        if image is None:
            return False, message_failed
    else:
        image1 = cv.imread(path + "/" + variable1)
        if image is None or image1 is None:
            return False, message_failed

        max_ranges = get_max_values(image, image1)
        image, image1 = rescale(image, image1, max_ranges)

    g = np.uint8(dot_images(image, image1))
    name_to_archive = "Dot_of_" + name + "_" + str(variable1) + ".png"
    ubication_final = MEDIA_ROOT + "/" + name_to_archive
    check_folder(ubication_final)
    cv.imwrite(ubication_final + "/" + name_to_archive, g)
    return True, name_to_archive, ubication_final


def solve_division(path, name, variable1):
    image = cv.imread(path + "/" + name)
    message_failed = "Didn't create file"
    image1 = variable1
    if type(variable1) != str:
        if image is None:
            return False, message_failed
    else:
        image1 = cv.imread(path + "/" + variable1)
        if image is None or image1 is None:
            return False, message_failed

        max_ranges = get_max_values(image, image1)
        image, image1 = rescale(image, image1, max_ranges)

    g = np.uint8(division_image(image, image1))
    m_in = np.min(g)
    m_ax = np.max(g)
    d_max = 255
    d_min = 0
    g = np.uint8((g - m_in) * ((d_max - d_min) / (m_ax - m_in)) + d_min)
    name_to_archive = "Division_of_" + name + "_" + str(variable1) + ".png"
    ubication_final = MEDIA_ROOT + "/" + name_to_archive
    check_folder(ubication_final)
    cv.imwrite(ubication_final + "/" + name_to_archive, g)
    return True, name_to_archive, ubication_final


def solve_blinding(path, name, name1, variable1):
    image = cv.imread(path + "/" + name)
    message_failed = "Didn't create file"
    image1 = cv.imread(path + "/" + name1)
    if image is None or image1 is None:
        return False, message_failed

    max_ranges = get_max_values(image, image1)
    image, image1 = rescale(image, image1, max_ranges)

    g = np.uint8(blinding_image(image, image1, float(variable1)))
    name_to_archive = "blinding_of_" + name + "_" + name1 + ".png"
    ubication_final = MEDIA_ROOT + "/" + name_to_archive
    check_folder(ubication_final)
    cv.imwrite(ubication_final + "/" + name_to_archive, g)
    return True, name_to_archive, ubication_final


def solve_and(path, name, name1):
    image = cv.imread(path + "/" + name)
    image1 = cv.imread(path + "/" + name1)
    message_failed = "Didn't create file"
    if image is None or image1 is None:
        return False, message_failed

    max_ranges = get_max_values(image, image1)
    img1, img2 = rescale(image, image1, max_ranges)
    g = np.uint8(and_operator(img1, img2))
    name_to_archive = "And_of_"+name+"_"+str(name1)+".png"
    ubication_final = MEDIA_ROOT + "/" + name_to_archive
    check_folder(ubication_final)
    cv.imwrite(ubication_final + "/" + name_to_archive, g)
    return True, name_to_archive, ubication_final


def solve_or(path, name, name1):
    image = cv.imread(path + "/" + name)
    image1 = cv.imread(path + "/" + name1)
    message_failed = "Didn't create file"
    if image is None or image1 is None:
        return False, message_failed

    max_ranges = get_max_values(image, image1)
    img1, img2 = rescale(image, image1, max_ranges)
    g = np.uint8(or_operator(img1, img2))
    name_to_archive = "OR_of_"+name+"_"+str(name1)+".png"
    ubication_final = MEDIA_ROOT + "/" + name_to_archive
    check_folder(ubication_final)
    cv.imwrite(ubication_final + "/" + name_to_archive, g)
    return True, name_to_archive, ubication_final


def solve_xor(path, name, name1):
    image = cv.imread(path + "/" + name)
    image1 = cv.imread(path + "/" + name1)
    message_failed = "Didn't create file"
    if image is None or image1 is None:
        return False, message_failed

    max_ranges = get_max_values(image, image1)
    img1, img2 = rescale(image, image1, max_ranges)
    g = np.uint8(xor_operator(img1, img2))
    name_to_archive = "XOR_of_"+name+"_"+str(name1)+".png"
    ubication_final = MEDIA_ROOT + "/" + name_to_archive
    check_folder(ubication_final)
    cv.imwrite(ubication_final + "/" + name_to_archive, g)
    return True, name_to_archive, ubication_final


# ----------------------------------------
# Funciones para la solucion de corners
# ----------------------------------------
def solve_corners(path, name):
    image = cv.imread(path + "/" + name)
    altura, ancho, colores = image.shape
    val = 1
    if ancho > 500 or altura > 500:
        val = 500 / max(ancho, altura)
    image = cv.resize(image, (int(ancho*val), int(altura*val)))
    gris = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gris = cv.bilateralFilter(gris, 9, 75, 75)
    gris = cv.adaptiveThreshold(gris, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 115, 4)
    gris = cv.medianBlur(gris, 11)
    gris = cv.copyMakeBorder(gris, 5, 5, 5, 5, cv.BORDER_CONSTANT, value=[0, 0, 0])
    edges = cv.Canny(gris, 200, 250)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # Finding contour of biggest rectangle
    # Otherwise return corners of original image
    # Don't forget on our 5px border!
    height = edges.shape[0]
    width = edges.shape[1]
    MAX_COUNTOUR_AREA = (width - 10) * (height - 10)
    # Page fill at least half of image, then saving max area found
    maxAreaFound = MAX_COUNTOUR_AREA * 0.5
    # Saving page contour
    pageContour = np.array([[5, 5], [5, height-5], [width-5, height-5], [width-5, 5]])
    # Go through all contours
    for cnt in contours:
        # Simplify contour
        perimeter = cv.arcLength(cnt, True)
        approx = cv.approxPolyDP(cnt, 0.03 * perimeter, True)
        if len(approx) == 4 and cv.isContourConvex(approx) and maxAreaFound < cv.contourArea(approx) < MAX_COUNTOUR_AREA:
            maxAreaFound = cv.contourArea(approx)
            pageContour = approx
    answer = pageContour
    answer2 = []
    for value in answer:
        for data in value:
            answer2.append(data)
    print(answer2)
    temp = answer2[2]
    answer2[2] = answer2[3]
    answer2[3] = temp
    print(answer2)
    return True, answer2

def fourCornersSort(pts):
    """ Sort corners: top-left, bot-left, bot-right, top-right """
    # Difference and sum of x and y value
    diff = np.diff(pts, axis=1)
    summ = pts.sum(axis=1)
    # Top-left point has smallest sum...
    # np.argmin() returns INDEX of min
    return np.array([pts[np.argmin(summ)], pts[np.argmax(diff)], pts[np.argmax(summ)], pts[np.argmin(diff)]])


def contourOffset(cnt, offset):
    """ Offset contour, by 5px border """
    # Matrix addition
    cnt += offset
    # if value < 0 => replace it by 0
    cnt[cnt < 0] = 0
    return cnt


def get_image_perspective(path, name, points_corners):
    image = cv.imread(path + "/" + name)
    altura, ancho, colores = image.shape
    val = 1
    if ancho > 500 or altura > 500:
        val = 500 / max(ancho, altura)
    image = cv.resize(image, (int(ancho * val), int(altura * val)))

    points_corners = points_corners.split(",")
    points_corners = list(map(float, points_corners))
    for i in range(len(points_corners)):
        points_corners[i] = int(round(points_corners[i]))
    corners = np.zeros((4, 2), dtype=np.float32)
    helper = ""
    for i in range(0, len(points_corners), 2):
        corners[i // 2, 0] = points_corners[i]
        corners[i // 2, 1] = points_corners[i+1]
        helper = helper + "_" + str(corners[i // 2, 0]) + "_" + str(corners[i // 2, 1])

    final_image = solve_scanner_perspective(image, corners)
    name_to_archive = "Solution_perspective" + helper
    cv.imwrite(path + "/" + name_to_archive + "_c.png", final_image)
    gray = cv.cvtColor(np.uint8(final_image), cv.COLOR_BGR2GRAY)
    cv.imwrite(path + "/" + name_to_archive + "_g.png", gray)
    blanco_negro = filtro_gaussiano(gray, 2)
    blanco_negro = filtro_conservating(blanco_negro)
    blanco_negro = solve_thresholding_adaptative(blanco_negro, 7, 10)
    cv.imwrite(path + "/" + name_to_archive + "_b.png", blanco_negro)

    camino_color = "/media" + "/" + erase_extension(name) + "/" + name_to_archive+ "_c.png"
    camino_gris = "/media" + "/" + erase_extension(name) + "/" + name_to_archive + "_g.png"
    camino_blanco_negro = "/media" + "/" + erase_extension(name) + "/" + name_to_archive + "_b.png"
    return True, camino_color, camino_gris, camino_blanco_negro

# ----------------------------------------
# ----------------------------------------

#Funciones Contrast_Streching
# ----------------------------------------


def get_ranges(list_colors):
    least_value = 0
    most_value = 0
    global_state = True
    for b in range(len(list_colors)):
        if global_state:
            if list_colors[b] != 0:
                least_value = b
                global_state = False
        else:
            if list_colors[b] != 0:
                most_value = b
    return least_value, most_value


def get_histogram(img):
    data = []
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv.calcHist([img], [i], None, [256], [0, 256])
        data += [get_ranges(histr)]
    return data


def get_ranges_limits(values, l1, l2):
    nvalues = []
    for i in range(len(values)):
        amount = values[i][1] - values[i][0]
        individual_value = amount / 100
        nvalues += [(int(values[i][0] + l1*individual_value), int(values[i][1] - (100-l2) * individual_value))]
    return nvalues


def solve_contrast_streching(path, name, constant, constant1):
    image = cv.imread(path + "/" + name)
    message_failed = "Didn't create file"
    if image is None:
        return False, message_failed

    val = get_ranges_limits(get_histogram(image), constant, constant1)
    g = np.uint8(contrast_stretching_operator(image, val))
    name_to_archive = "Contrast_Streching_of_"+name+"_"+str(constant)+"_"+str(constant1)+".png"
    ubication_final = MEDIA_ROOT + "/" + name_to_archive
    check_folder(ubication_final)
    cv.imwrite(ubication_final + "/" + name_to_archive, g)
    return True, name_to_archive, ubication_final


def get_histogram_amount(img):
    f = plt.hist(img.ravel(), 256, [0, 256])
    return f[0]


def get_new_intensities(img, amount_bits=8):
    values = get_histogram_amount(img)
    cols, rows = img.shape
    length_pixels = 2**amount_bits
    probabilities = values / (cols*rows)
    intensities = np.array([0]*len(probabilities))
    accumulate = 0
    for i in range(len(probabilities)):
        accumulate += probabilities[i]
        intensities[i] = int((length_pixels - 1) * accumulate)
    return intensities


def solve_extra(img, sub_image=False, p_start1=None, p_end1=None):
    data = []
    if sub_image:
        blank_image = np.copy(img[p_start1[0]:p_end1[0] + 1, p_start1[1]:p_end1[1] + 1])
        data = get_new_intensities(blank_image)
    else:
        data = get_new_intensities(img)

    g = histogram_equalization(np.copy(img), data)
    return g


def solve_histogram_equalization(path, name, constant, constant1):
    image = cv.imread(path + "/" + name)
    message_failed = "Didn't create file"
    if image is None:
        return False, message_failed

    g = np.copy(image)
    indicator1 = True
    if constant == (0, 0) and constant1 == (0, 0):
        indicator1 = False

    for i in range(3):
        if indicator1:
            g[:, :, i] = solve_extra(g[:, :, i], indicator1, constant, constant1)
        else:
            g[:, :, i] = solve_extra(g[:, :, i])

    name_to_archive = "Histogram_equalization_of_"+name+"_"+str(constant)+"_"+str(constant1)+".png"
    ubication_final = MEDIA_ROOT + "/" + name_to_archive
    check_folder(ubication_final)
    cv.imwrite(ubication_final + "/" + name_to_archive, g)
    return True, name_to_archive, ubication_final


def get_original_file_extra(path, name):
    for obj in os.listdir(path):
        if os.path.isfile(path + "/" + obj):
            if os.path.splitext(obj)[0] == name:
                return obj


def check_folder(ubication_final):
    if os.path.isdir(ubication_final):
        shutil.rmtree(ubication_final)
    os.mkdir(ubication_final)


def up_image(my_file, name):
    ubication_image = MEDIA_ROOT + "/" + name
    fs = FileSystemStorage(location=ubication_image)
    filename = fs.save(my_file.name, my_file)
    return my_file.name


def erase_extension(nombre):
    return (nombre.split("."))[0]


def order_points(pts):

	rect = np.zeros((4, 2), dtype="float32")

	s = pts.sum(axis=1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]


	diff = np.diff(pts, axis=1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]

	return rect


def transformFourPoints(image, pts):

	rect = order_points(pts)
	(tl, tr, br, bl) = rect


	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))


	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))


	dst = np.array([[0, 0],	[maxWidth - 1, 0],	[maxWidth - 1, maxHeight - 1],	[0, maxHeight - 1]], dtype="float32")


	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

	return warped

def recorte(image):
    image = cv2.imread(image)
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height = 500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
    for c in cnts:

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    warped = transformFourPoints(orig, screenCnt.reshape(4, 2) * ratio)

    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset = 10, method = "gaussian")
    warped = (warped > T).astype("uint8") * 255

    return warped