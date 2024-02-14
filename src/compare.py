#!/usr/bin/env python
import cv2 as cv
import numpy as np
import math
from common import reference_enum, file_format

KERNEL_EROSION = np.ones((5, 5), np.uint8)
BINS = 8
IMAGES = 1

class ImageProcessor():
    def __init__(self):
        self.params = cv.SimpleBlobDetector_Params()
        self.init_params()
        self.params.minArea = 700
        self.detector = cv.SimpleBlobDetector_create(self.params)
        pass

    def init_params(self):
        self.params.filterByColor = False
        self.params.filterByCircularity = False
        self.params.filterByInertia = False
        self.params.filterByConvexity = False

    def find_mask(self, sct_img):
        """Get the mask removing the background of the provided screenshot image."""
        # Read in grayscale
        img = np.array(sct_img)[:,:,:3]
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        _, thresh = cv.threshold(img_gray, 25, 255, cv.THRESH_BINARY_INV)
        
        # Dilate image for cleaner blob detection
        img_dilation = cv.erode(thresh, KERNEL_EROSION, iterations=2)

        return img_dilation, cv.bitwise_and(img, img, mask=cv.bitwise_not(img_dilation))

    def find_keypoints(self, threshold_image, image):
        """Find keypoints in the given binary image."""
        keypoints = self.detector.detect(threshold_image)
        assert len(keypoints) == 1, "Thresholding error. Found " + str(len(keypoints)) + " keypoints in image. Should only find one."
        im_with_keypoints = cv.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        return keypoints, im_with_keypoints

    def crop_to_icon(self, image, keypoints):
        """Crop the given image to the icon based on the keypoint location."""
        img = image[:,:,:3]
        mask_r = math.trunc(keypoints[0].size/2) - 1
        mask_x = math.trunc(keypoints[0].pt[0])
        mask_y = math.trunc(keypoints[0].pt[1])

        cropped_image = np.zeros((mask_r, mask_r, 3),np.uint8)
        cropped_image[:mask_r, :mask_r] = img[mask_y:mask_y + mask_r, mask_x:mask_x + mask_r]

        # cropped_mask = np.zeros((mask_r, mask_r),np.uint8)
        # cropped_mask[:mask_r, :mask_r] = img_dilation[mask_y:mask_y + mask_r, mask_x:mask_x + mask_r]

        return cropped_image #, cv.bitwise_not(cropped_mask)

    def generate_histogram(self, image):
        """Generate a histogram for an image."""
        ar = np.ndarray(shape=(BINS,0), dtype=float, order='C')
        pix = image.shape[0] * image.shape[1]
        for i, col in enumerate(('b','g','r')):
            histr = cv.calcHist([image],[i],None,[BINS],[0,255])
            ar = np.hstack((ar, histr))
        ar = ar / pix
        return ar.astype(np.float32)

    def generate_data_csv(self):
        """Generate csv storing all histogram data of all stored images."""
        all_data =  np.array([], dtype=np.float32).reshape(0,BINS * 3)
        for i, name in enumerate(reference_enum):
            image = cv.imread(file_format.format(dname=name))
            histogram = self.generate_histogram(image)
            flat = histogram.flatten().astype(np.float32)
            all_data = np.vstack((all_data, flat))
            print(all_data.shape)
        np.savetxt("resources/histogram_icons_3.csv", all_data, delimiter=",")

    def read_single_histogram(self, index):
        """Read in a single histogram from file of an item in the reference enum"""
        local_data = None
        with np.loadtxt("resources/histogram_icons_3.csv", dtype=float, delimiter=",") as read_in:
            local_data = read_in[index,:].reshape(BINS, 3)
        return local_data

    def compare_histograms(self, hist_1, hist_2):
        """Compare the two histograms. Lower is better."""
        return cv.compareHist(hist_1, hist_2, cv.HISTCMP_CHISQR)

    def find_best_match(self, image):
        """Find the best match in the reference enum of a preproccessed, cropped, input image."""
        read_in = np.loadtxt("resources/histogram_icons_3.csv", dtype=float, delimiter=",").astype(np.float32)
        generated = self.generate_histogram(image)
        best_index_so_far = -1
        best_score_so_far = math.inf
        for i, name in enumerate(reference_enum):
            nextHist = read_in[i,:].reshape(BINS,3)
            score = self.compare_histograms(generated, nextHist)
            if (score < best_score_so_far):
                best_score_so_far = score
                best_index_so_far = i
        print("Best is " + reference_enum[best_index_so_far] + " with score " + str(best_score_so_far))
        return best_index_so_far

    def classify_raw_image(self, raw):
        """Classify an unprocessed image. Returns the index of the closest match in the reference enum."""

        threshold, combined_mask = self.find_mask(raw)
        keypoints, combined_keypoints = self.find_keypoints(threshold, raw)
        trimmed = self.crop_to_icon(raw, keypoints)
        return self.find_best_match(trimmed)
