

import os
import errno
from os import path
from glob import glob

import cv2
import numpy as np
import poisson

IMG_EXTENSIONS = ["png", "jpeg", "jpg", "gif", "tiff", "tif", "raw", "bmp"]
SRC_FOLDER = "input"
OUT_FOLDER = "output"

def collect_files(prefix, extension_list):
    filenames = sum(map(glob, [prefix + ext for ext in extension_list]), [])
    return filenames

subfolders = os.walk(SRC_FOLDER)
subfolders.__next__()

for dirpath, dirnames, fnames in subfolders:
    image_dir = os.path.split(dirpath)[-1]
    output_dir = os.path.join(OUT_FOLDER, image_dir)
    print("Processing input {i}...".format(i=image_dir))

    # Search for images to process
    source_names = collect_files(os.path.join(dirpath, '*source.'),IMG_EXTENSIONS)
    target_names = collect_files(os.path.join(dirpath, '*target.'),IMG_EXTENSIONS)
    mask_names = collect_files(os.path.join(dirpath, '*mask.'),IMG_EXTENSIONS)

    if not len(source_names) == len(target_names) == len(mask_names) == 1:
        print("There must be one source, one target, and one mask per input.")
        continue

    # 读图像
    source_img = cv2.imread(source_names[0], cv2.IMREAD_COLOR)
    target_img = cv2.imread(target_names[0], cv2.IMREAD_COLOR)
    mask_img = cv2.imread(mask_names[0], cv2.IMREAD_GRAYSCALE)

    mask = np.atleast_3d(mask_img).astype(np.float) / 255.
    # mask二值化处理
    mask[mask != 1] = 0
    # print(mask)
    # 取mask一个通道上的数据即可
    mask = mask[:,:,0]
    channels = source_img.shape[-1]
    # 对每个通道都做poisson image editing
    result_stack = [poisson.process(source_img[:,:,i], target_img[:,:,i], mask) for i in range(channels)]
    # 将所有通道merge回图片
    result = cv2.merge(result_stack)
    # 创建结果目录
    try:
        os.makedirs(output_dir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    # 写结果
    cv2.imwrite(path.join(output_dir, 'result.png'), result)
    print("Finished processing input {i}.".format(i=image_dir))
