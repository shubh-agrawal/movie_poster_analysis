import numpy as np
import argparse
import cv2

def kmeans_color_quant(img, k):
   
    #Reshape into list of pixels
    Z = np.float32(img.reshape((-1, 3)))
    
    #Define criteria and perform clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, label, center = cv2.kmeans(Z, k, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    #Convert back into uint8 and reshape to shape of original image
    center = np.uint8(center)
    clustered = center[label.flatten()].reshape((img.shape))
    return (clustered, label, center)

def get_histogram(label):
    
    n_labels = np.arange(0, len(np.unique(label)) + 1)
    hist, _ = np.histogram(label, bins=n_labels, density=True)
    return hist

def draw_color_bar(hist, center):
   
    #Initialize a 150x600 pixel color bar
    bar = np.zeros((600, 150, 3), dtype='uint8')
    start = 0

    #Plot color bar, loopping over each percentage and color
    for (percentage, color) in zip(hist, center):
        end = start + (percentage * 600)
        cv2.rectangle(bar, (0, int(start)), (150, int(end)), 
                      color.astype('uint8').tolist(), -1)
        start = end
    return bar

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--img', required=True, help='Image path')
    parser.add_argument('-k', '--clusters', required=True, type=int, help='Number of cluters')
    args = vars(parser.parse_args())

    img = cv2.imread(args['img'])
    clustered, labels, centers = kmeans_color_quant(img, args['clusters'])

    hist = get_histogram(labels)
    bar = draw_color_bar(hist, centers)

    cv2.imwrite('out.png', bar)

if __name__ == '__main__':
    main()
