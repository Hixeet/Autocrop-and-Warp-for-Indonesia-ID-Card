import numpy as np
import cv2

image = cv2.imread("KTP.jpg")

blurred_frame_b = cv2.GaussianBlur(image[:,:,0], (5, 5), 1)
blurred_frame_r = cv2.GaussianBlur(image[:,:,2], (5, 5), 1)

_, blue_threshold = cv2.threshold(blurred_frame_b, 255, 255,  cv2.THRESH_BINARY + cv2.THRESH_OTSU )
_, red_threshold = cv2.threshold(blurred_frame_r, 200, 255, cv2.THRESH_BINARY)
combined_threshold = cv2.subtract(blue_threshold, red_threshold)

kernel = np.ones((2, 2), np.uint8)
eroded_image = cv2.erode(combined_threshold, kernel, iterations=1)

contours, _ = cv2.findContours(eroded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest_contour = max(contours, key=cv2.contourArea)

x, y, w, h = cv2.boundingRect(largest_contour)
crop_image = image[y:y+h, x:x+w]

height, width, channels = crop_image.shape

if width < height:
    rotated_image = cv2.rotate(crop_image, cv2.ROTATE_90_CLOCKWISE)
    rotated_height, rotated_width, _ = rotated_image.shape
    print("Gambar sudah dirotasi:", rotated_height, rotated_width)
else:
    rotated_image = crop_image
    print("Tidak perlu merotasi gambar")
    
resized_image = cv2.resize(rotated_image, (900, 600))

mean_value_b = np.mean(resized_image[resized_image[:,:,0] > 0])
print("Nilai rata-rata intensitas dari channel B pada KTP:", mean_value_b)

if 150 >= mean_value_b >= 100:
    blur_frame_b = cv2.GaussianBlur(resized_image[:,:,0], (5, 5), 1)
    blur_gray = cv2.GaussianBlur(resized_image, (5, 5), 1)
elif 200 >= mean_value_b >= 150:
    blur_frame_b = cv2.GaussianBlur(resized_image[:,:,0], (5, 5), 1)
    blur_gray = cv2.GaussianBlur(resized_image, (7, 7), 3)
else:
    blur_frame_b = resized_image[:,:,0]
    blur_gray = cv2.GaussianBlur(resized_image, (5, 5), 1)

gray = cv2.cvtColor(blur_gray, cv2.COLOR_BGR2GRAY)
blur_frame_r = cv2.GaussianBlur(resized_image[:,:,2], (5, 5), 1)

# Tentukan nilai threshold untuk kanal biru berdasarkan mean value
if mean_value_b <= 95:
    threshold_value = 50
    threshold_value_r = 160
elif 96 <= mean_value_b <= 115:
    threshold_value = 105
    threshold_value_r = 170
elif 116 <= mean_value_b <= 145:
    threshold_value = 107
    threshold_value_r = 180
elif 146 <= mean_value_b <= 160:
    threshold_value = 110
    threshold_value_r = 180
else:
    threshold_value = 126
    threshold_value_r = 190

_, crop_threshold_b = cv2.threshold(blur_frame_b, threshold_value, 255, cv2.THRESH_BINARY)
_, crop_threshold_r = cv2.threshold(blur_frame_r, threshold_value_r, 255,  cv2.THRESH_BINARY )
_, threshold_gray = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
combined_threshold2 = cv2.subtract(crop_threshold_b, crop_threshold_r)

def find_nearest_coordinates(image_array):
    # Periksa ukuran gambar
    height, width = image_array.shape 

    # Inisialisasi variabel untuk menyimpan koordinat terdekat dengan nilai intensitas grayscale >= 200
    min_x_0 = width
    min_y_0 = height
    min_x_hw = width
    min_y_hw = height
    min_x_h0 = width
    min_y_h0 = 0
    min_x_0w = width
    min_y_0w = 0

    # Loop untuk mencari koordinat terdekat dengan nilai intensitas grayscale >= 200 dari (0, 0)
    x = 0
    y = 0
    while x < width and y < height:
        intensity = image_array[y, x]

        if intensity >= 255:
            if x < min_x_0:
                min_x_0 = x
                min_y_0 = y
            break
        x += 1
        y += 1

    # Loop untuk mencari koordinat terdekat dengan nilai intensitas grayscale >= 200 dari (height, width)
    x = width - 1
    y = height - 1
    while x >= 0 and y >= 0:
        intensity = image_array[y, x]

        if intensity >= 255:
            if x < min_x_hw:
                min_x_hw = x
                min_y_hw = y
            break
        x -= 1
        y -= 1

    # Loop untuk mencari koordinat terdekat dengan nilai intensitas grayscale >= 200 dari (0, width)
    x = width - 1
    y = 0
    while x >= 0 and y < height:
        intensity = image_array[y, x]

        if intensity >= 255:
            if x < min_x_0w:
                min_x_0w = x
                min_y_0w = y
            break
        x -= 1
        y += 1

    # Loop untuk mencari koordinat terdekat dengan nilai intensitas grayscale >= 200 dari (height, 0)
    x = 0
    y = height - 1
    while x < width and y >= 0:
        intensity = image_array[y, x]

        if intensity >= 255:
            if x < min_x_h0:
                min_x_h0 = x
                min_y_h0 = y
            break
        x += 1
        y -= 1

    # Mengembalikan koordinat terdekat dari semua empat sudut
    return (min_x_0, min_y_0), (min_x_hw, min_y_hw), (min_x_0w, min_y_0w), (min_x_h0, min_y_h0)
 
hasil_coordinates = find_nearest_coordinates(combined_threshold2)

# Mengakses nilai-nilai dari luar fungsi
(min_x_0, min_y_0), (min_x_hw, min_y_hw), (min_x_0w, min_y_0w), (min_x_h0, min_y_h0) = hasil_coordinates

# Loop untuk mencari koordinat terkecil yang memiliki intensitas yang sama dengan point (min_x_0, min_y_0)
image_array = combined_threshold2
height, width = image_array.shape

min_x_same_intensity = min_x_0
min_y_same_intensity = min_y_0
for x in range(min_x_0+10, 0, -1):
    for y in range(min_y_0+10, 0, -1):
        if image_array[y, x] == image_array[min_y_0, min_x_0]:
            sum_coordinates = x + y
            if sum_coordinates < min_x_same_intensity + min_y_same_intensity:
                min_x_same_intensity = x
                min_y_same_intensity = y

min_x_same_intensity_w0 = min_x_0w 
min_y_same_intensity_w0 = min_y_0w
for x in range(min_x_0w-10, width):
    for y in range(min_y_0w+10, 0, -1):
        if image_array[y, x] == image_array[min_y_0w, min_x_0w]:
            sum_coordinates = (width - x) + y
            if sum_coordinates < (width - min_x_same_intensity_w0) + min_y_same_intensity_w0:
                min_x_same_intensity_w0 = x
                min_y_same_intensity_w0 = y

min_x_same_intensity_h0 = min_x_h0 
min_y_same_intensity_h0 = min_y_h0
for x in range(min_x_h0+10, 0, -1):
    for y in range(min_y_h0-10, height):
        if image_array[y, x] == image_array[min_y_h0, min_x_h0]:
            sum_coordinates = x + (height - y)
            if sum_coordinates < min_x_same_intensity_h0 + (height - min_y_same_intensity_h0):
                min_x_same_intensity_h0 = x
                min_y_same_intensity_h0 = y

min_x_same_intensity_hw = min_x_hw 
min_y_same_intensity_hw = min_y_hw
for x in range(min_x_hw-10, width, +1):
    for y in range(min_y_hw-10, height, +1):
        if image_array[y, x] == image_array[min_y_hw, min_x_hw]:
            sum_coordinates = (width - x) + (height - y)
            if sum_coordinates < (width - min_x_same_intensity_hw) + (height - min_y_same_intensity_hw):
                min_x_same_intensity_hw = x
                min_y_same_intensity_hw = y


pointa = (min_x_same_intensity, min_y_same_intensity)
pointb = (min_x_same_intensity_w0, min_y_same_intensity_w0)
pointc = (min_x_same_intensity_h0, min_y_same_intensity_h0)
pointd = (min_x_same_intensity_hw, min_y_same_intensity_hw)

points = ['c1', 'c2', 'c3', 'c4']
min_coordinate_sums = [float("inf")] * 4
min_coordinates = [None] * 4

# Loop untuk mencari seluruh point pada threshold grey
for point_idx, point_name in enumerate(points[:4]):
    for y in range(height):
        for x in range(width):
            if threshold_gray[y, x] == 255:
                if point_name == 'c1':
                    coordinate_sum = x + y
                elif point_name == 'c2':
                    coordinate_sum = (width - x) + y
                elif point_name == 'c3':
                    coordinate_sum = x + (height - y)
                elif point_name == 'c4':
                    coordinate_sum = (width - x) + (height - y)
                else:
                    coordinate_sum = float("inf")
                
                if coordinate_sum < min_coordinate_sums[point_idx]:
                    min_coordinate_sums[point_idx] = coordinate_sum
                    min_coordinates[point_idx] = (x, y)

pointc1 = min_coordinates[0]
pointc2 = min_coordinates[1]
pointc3 = min_coordinates[2]
pointc4 = min_coordinates[3]

top_left = np.float32(pointa)
top_right = np.float32(pointb)
bottom_left = np.float32(pointc)
bottom_right = np.float32(pointd)

"""print("\nsudut kiri atas KTP berada pada pixel (x, y)  :", top_left)
print("sudut kanan atas KTP berada pada pixel (x, y) :", top_right)
print("sudut kiri bawah KTP berada pada pixel (x, y) :", bottom_left)
print("sudut kanan bawah KTP berada pada pixel (x, y):", bottom_right)

print("\nsudut kiri atas pantulan cahaya di KTP berada pada pixel (x, y)  :", pointc1)
print("sudut kanan atas pantulan cahaya di KTP berada pada pixel (x, y) :", pointc2)
print("sudut kiri bawah pantulan cahaya di KTP berada pada pixel (x, y) :", pointc3)
print("sudut kanan bawah pantulan cahaya di KTP berada pada pixel (x, y):", pointc4)
"""
# Mnemapilkan hasil dari setiap point
for point_name, coordinate in zip(points, min_coordinates):
    if coordinate is not None:
        x, y = coordinate
        if point_name == 'c1' and x < 85 and y < 85:
            top_left = np.float32(pointc1)
        elif point_name == 'c2' and x > 815 and y < 85:
            top_right = np.float32(pointc2)
        elif point_name == 'c3' and x < 50 and y > 515:
            bottom_left = np.float32(pointc3)
        elif point_name == 'c4' and x > 815 and y > 515:
            bottom_right = np.float32(pointc4)

pts = np.float32([[0, 0], [900, 0], [0, 600], [900, 600]])
pts2 = np.float32([top_left, top_right, bottom_left, bottom_right])
matrix = cv2.getPerspectiveTransform(pts2,pts)
final = cv2.warpPerspective(resized_image, matrix, (900, 600))

test_coordinates = find_nearest_coordinates(blue_threshold)
(min_x_0, min_y_0), (min_x_hw, min_y_hw), (min_x_0w, min_y_0w), (min_x_h0, min_y_h0) = test_coordinates

height2, width2, channel = image.shape

if (
    min_x_0 <= 1 and (min_y_0) <= 1 and
    (width2 - min_x_hw )<= 1 and (height2 - min_y_hw) <= 1 and
    (width2 - min_x_hw )<= 1 and (min_y_0) <= 1 and
    min_x_0 <= 1 and (height2 - min_y_hw) <= 1
):
    akhir = image  
else:
    akhir = final

cv2.imshow('akhir',akhir)
cv2.waitKey(0)
cv2.destroyAllWindows

