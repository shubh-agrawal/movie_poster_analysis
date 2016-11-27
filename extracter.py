import color_clustering as cc
import argparse
import cv2
import os
import re
import unicodedata
import urllib

def process_poster(poster, k, path_to_write):
   
    #Read image and perform k-means clustering
    img = cv2.imread(poster)
    clustered, labels, centers = cc.kmeans_color_quant(img, k)

    #Get density histogram and draw color bar from histogram
    hist = cc.get_histogram(labels)
    bar = cc.draw_color_bar(hist, centers)

    #Write color quantized poster and color bar
    cv2.imwrite(path_to_write + '/qp_dir/' + poster.split('/')[-1], clustered)
    cv2.imwrite(path_to_write + '/br_dir/' + poster.split('/')[-1], bar)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--clusters', required=True, type=int, 
                        help='Number of cluters')
    args = vars(parser.parse_args())

    k = args['clusters']
    
    print k
    eras = os.listdir('posters')
    eras = [x for x in eras if os.path.isdir(os.path.join('posters', x))]
    print eras
    for era in eras:
        woods = os.listdir(os.path.join('posters', era))
        woods = [x for x in woods if os.path.isdir(os.path.join('posters', era, x))]
        print woods
            
        for wood in woods:
            genres = os.listdir(os.path.join('posters', era, wood))
            genres = [x for x in genres if os.path.isdir(os.path.join('posters', era, wood, x))]
            print genres
            for genre in genres:
                img_names = os.listdir(os.path.join('posters', era, wood, genre))
                for indx, img_name in enumerate(img_names):
                    img_path = os.path.join('posters', era, wood, genre, img_name)
                    path_to_write = os.path.join('output', era, wood, genre)
                    process_poster(img_path, k, path_to_write)
                    print img_path

if __name__ == '__main__':
    main()
