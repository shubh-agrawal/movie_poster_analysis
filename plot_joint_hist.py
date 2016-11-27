import color_clustering as cc
import argparse
import cv2
import os
import re
import unicodedata
import urllib
import math
from matplotlib import pyplot as plt

color_dict = {'black':[0,0,0], 'gray':[128,128,128], 'white':[255,255,255], 'maroon':[128,0,0], 'red':[255,0,0], 'olive':[128,128,0], 'yellow':[255,255,0], 'green':[0,128,0], 'teal':[0,128,128], 'aqua':[0,255,255], 'blue':[0,0,255], 'orange':[255,165,0], 'purple':[128,0,128], 'fuchsia':[255,0,255], 'brown':[139,69,19] }

norm_dict = {'black':[0,0,0], 'gray':[128/255.0,128/255.0,128/255.0], 'white':[255/255.0,255/255.0,255/255.0], 'maroon':[128/255.0,0/255.0,0/255.0], 'red':[255/255.0,0/255.0,0/255.0], 'olive':[128/255.0,128/255.0,0/255.0], 'yellow':[255/255.0,255/255.0,0/255.0], 'green':[0/255.0,128/255.0,0/255.0], 'teal':[0/255.0,128/255.0,128/255.0], 'aqua':[0/255.0,255/255.0,255/255.0], 'blue':[0,0,255/255.0], 'orange':[255/255.0,165/255.0,0], 'purple':[128/255.0,0,128/255.0], 'fuchsia':[255/255.0,0,255/255.0], 'brown':[139/255.0,69/255.0,19/255.0] }

all_data_dict = {}

thershold_distance = 50.00

def dist_between_colors(list1, list2):
    dist = math.sqrt(math.pow((list1[0]-list2[0])*0.3,2) + math.pow((list1[1]-list2[1])*0.59,2) + math.pow((list1[2]-list2[2])*0.11,2))
    return dist

def process_poster(poster, k, path_to_write):
   
    #Read image and perform k-means clustering
    img = cv2.imread(poster)
    clustered, labels, centers = cc.kmeans_color_quant(img, k)
    clst_clr_list = []

    for center in centers:          # Put a threshold for dist. If greater than that, then dont consider the color
        min_dist = 195075.00
        center_clr = center.astype('uint8').tolist()
        for color, code in color_dict.items():
            if dist_between_colors(center, code) <= min_dist:
                min_dist = dist_between_colors(center_clr, code)
                closest_clr = color
            else:
                min_dist = min_dist
        if min_dist < thershold_distance :
            clst_clr_list.append(closest_clr)

    return clst_clr_list


def draw_joint_hist(all_data_dict):
    labels = [ z for z in sorted(color_dict.keys())]
    times = ['1990s', '2000s', '2010s']
    cultures = ['bollywood', 'hollywood']
    genres = ['action', 'comedy', 'romance', 'horror']
    rect_list = []

    for culture in cultures:
        for genre in genres:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.set_ylim(0, 50)
            ax.set_title(culture + "_" + genre)
            for time in times:
                y = [ all_data_dict[time+"_"+culture+"_"+genre][z] for z in sorted(all_data_dict[time+"_"+culture+"_"+genre].keys())]
                print y, time
                x = range(len(y))
                plt.xticks(x, labels)
                y_sum = sum(y)
                y_perc = [z*100.0/y_sum for z in y]
                rect_list.append(ax.hist(x, y_perc, width = 0.75, stacked = False, color= [norm_dict[x] for x in sorted(norm_dict.keys())]))    
            plt.show()
    

    
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
                total_color_count = {'black':0, 'gray':0, 'white':0, 'maroon':0, 'red':0, 'olive':0, 'yellow':0, 'green':0, 'teal':0, 'aqua':0, 'blue':0, 'orange':0, 'purple':0, 'fuchsia':0, 'brown':0 }
                img_names = os.listdir(os.path.join('posters', era, wood, genre))  
                for indx, img_name in enumerate(img_names):
                    img_path = os.path.join('posters', era, wood, genre, img_name)
                    path_to_write = os.path.join('output', era, wood, genre)
                    clst_clr_list = process_poster(img_path, k, path_to_write)  
                    for key, value in total_color_count.items():
                        if key in clst_clr_list:
                            total_color_count[key] += 1
                    #print img_path
                print total_color_count
                all_data_dict[era + "_" + wood + "_" + genre] = total_color_count
                #draw_color_dist(total_color_count, genre, wood, era)
                
if __name__ == '__main__':
    #main()
    all_data_dict = {'2010s_hollywood_comedy': {'brown': 36, 'fuchsia': 0, 'yellow': 0, 'maroon': 0, 'olive': 3, 'blue': 7, 'gray': 41, 'purple': 1, 'aqua': 5, 'black': 41, 'teal': 9, 'orange': 23, 'green': 0, 'white': 41, 'red': 0}, '2000s_bollywood_action': {'brown': 32, 'fuchsia': 0, 'yellow': 0, 'maroon': 0, 'olive': 2, 'blue': 13, 'gray': 35, 'purple': 0, 'aqua': 3, 'black': 35, 'teal': 13, 'orange': 11, 'green': 0, 'white': 33, 'red': 0}, '2010s_hollywood_romance': {'brown': 22, 'fuchsia': 0, 'yellow': 0, 'maroon': 0, 'olive': 1, 'blue': 3, 'gray': 25, 'purple': 0, 'aqua': 2, 'black': 23, 'teal': 5, 'orange': 13, 'green': 0, 'white': 22, 'red': 0}, '2010s_bollywood_comedy': {'brown': 19, 'fuchsia': 0, 'yellow': 0, 'maroon': 0, 'olive': 3, 'blue': 5, 'gray': 21, 'purple': 1, 'aqua': 3, 'black': 19, 'teal': 6, 'orange': 8, 'green': 0, 'white': 21, 'red': 0}, '2010s_hollywood_action': {'brown': 62, 'fuchsia': 0, 'yellow': 0, 'maroon': 0, 'olive': 4, 'blue': 13, 'gray': 62, 'purple': 0, 'aqua': 2, 'black': 59, 'teal': 11, 'orange': 31, 'green': 0, 'white': 52, 'red': 0}, '2010s_hollywood_horror': {'brown': 33, 'fuchsia': 0, 'yellow': 0, 'maroon': 1, 'olive': 3, 'blue': 6, 'gray': 34, 'purple': 0, 'aqua': 0, 'black': 34, 'teal': 3, 'orange': 18, 'green': 0, 'white': 22, 'red': 0}, '1990s_hollywood_action': {'brown': 39, 'fuchsia': 0, 'yellow': 0, 'maroon': 2, 'olive': 2, 'blue': 15, 'gray': 44, 'purple': 0, 'aqua': 4, 'black': 45, 'teal': 20, 'orange': 25, 'green': 0, 'white': 38, 'red': 0}, '2000s_bollywood_horror': {'brown': 22, 'fuchsia': 0, 'yellow': 0, 'maroon': 1, 'olive': 2, 'blue': 0, 'gray': 24, 'purple': 0, 'aqua': 1, 'black': 24, 'teal': 5, 'orange': 10, 'green': 1, 'white': 22, 'red': 0}, '2000s_bollywood_comedy': {'brown': 30, 'fuchsia': 0, 'yellow': 0, 'maroon': 0, 'olive': 8, 'blue': 8, 'gray': 33, 'purple': 5, 'aqua': 11, 'black': 33, 'teal': 10, 'orange': 19, 'green': 1, 'white': 30, 'red': 0}, '1990s_hollywood_romance': {'brown': 24, 'fuchsia': 0, 'yellow': 0, 'maroon': 3, 'olive': 1, 'blue': 0, 'gray': 25, 'purple': 2, 'aqua': 0, 'black': 23, 'teal': 7, 'orange': 16, 'green': 0, 'white': 19, 'red': 0}, '1990s_hollywood_horror': {'brown': 39, 'fuchsia': 0, 'yellow': 0, 'maroon': 2, 'olive': 1, 'blue': 14, 'gray': 40, 'purple': 0, 'aqua': 6, 'black': 41, 'teal': 13, 'orange': 23, 'green': 0, 'white': 27, 'red': 0}, '2000s_bollywood_romance': {'brown': 39, 'fuchsia': 1, 'yellow': 0, 'maroon': 0, 'olive': 5, 'blue': 8, 'gray': 42, 'purple': 0, 'aqua': 8, 'black': 38, 'teal': 14, 'orange': 16, 'green': 0, 'white': 40, 'red': 0}, '2000s_hollywood_action': {'brown': 54, 'fuchsia': 0, 'yellow': 0, 'maroon': 0, 'olive': 3, 'blue': 11, 'gray': 58, 'purple': 0, 'aqua': 6, 'black': 57, 'teal': 23, 'orange': 27, 'green': 0, 'white': 51, 'red': 0}, '2010s_bollywood_romance': {'brown': 25, 'fuchsia': 0, 'yellow': 0, 'maroon': 1, 'olive': 6, 'blue': 9, 'gray': 38, 'purple': 1, 'aqua': 6, 'black': 35, 'teal': 19, 'orange': 15, 'green': 1, 'white': 35, 'red': 0}, '1990s_bollywood_comedy': {'brown': 9, 'fuchsia': 0, 'yellow': 0, 'maroon': 0, 'olive': 0, 'blue': 2, 'gray': 9, 'purple': 0, 'aqua': 5, 'black': 8, 'teal': 4, 'orange': 4, 'green': 0, 'white': 8, 'red': 0}, '2000s_hollywood_comedy': {'brown': 31, 'fuchsia': 0, 'yellow': 0, 'maroon': 1, 'olive': 7, 'blue': 5, 'gray': 34, 'purple': 2, 'aqua': 7, 'black': 34, 'teal': 13, 'orange': 20, 'green': 0, 'white': 35, 'red': 0}, '2000s_hollywood_romance': {'brown': 16, 'fuchsia': 0, 'yellow': 0, 'maroon': 0, 'olive': 1, 'blue': 3, 'gray': 21, 'purple': 0, 'aqua': 1, 'black': 20, 'teal': 10, 'orange': 8, 'green': 1, 'white': 19, 'red': 0}, '2010s_bollywood_horror': {'brown': 18, 'fuchsia': 0, 'yellow': 0, 'maroon': 0, 'olive': 1, 'blue': 4, 'gray': 18, 'purple': 0, 'aqua': 0, 'black': 18, 'teal': 1, 'orange': 7, 'green': 0, 'white': 17, 'red': 0}, '1990s_bollywood_horror': {'brown': 12, 'fuchsia': 0, 'yellow': 0, 'maroon': 1, 'olive': 0, 'blue': 5, 'gray': 12, 'purple': 0, 'aqua': 1, 'black': 9, 'teal': 3, 'orange': 5, 'green': 0, 'white': 11, 'red': 0}, '2010s_bollywood_action': {'brown': 35, 'fuchsia': 0, 'yellow': 0, 'maroon': 1, 'olive': 5, 'blue': 9, 'gray': 36, 'purple': 1, 'aqua': 1, 'black': 35, 'teal': 11, 'orange': 11, 'green': 0, 'white': 31, 'red': 0}, '1990s_hollywood_comedy': {'brown': 32, 'fuchsia': 0, 'yellow': 0, 'maroon': 0, 'olive': 1, 'blue': 10, 'gray': 33, 'purple': 2, 'aqua': 5, 'black': 31, 'teal': 7, 'orange': 19, 'green': 0, 'white': 27, 'red': 0}, '1990s_bollywood_romance': {'brown': 21, 'fuchsia': 0, 'yellow': 0, 'maroon': 0, 'olive': 2, 'blue': 1, 'gray': 22, 'purple': 0, 'aqua': 3, 'black': 21, 'teal': 8, 'orange': 10, 'green': 0, 'white': 21, 'red': 0}, '1990s_bollywood_action': {'brown': 32, 'fuchsia': 0, 'yellow': 0, 'maroon': 0, 'olive': 1, 'blue': 7, 'gray': 33, 'purple': 0, 'aqua': 9, 'black': 33, 'teal': 15, 'orange': 10, 'green': 0, 'white': 30, 'red': 0}, '2000s_hollywood_horror': {'brown': 31, 'fuchsia': 0, 'yellow': 0, 'maroon': 0, 'olive': 0, 'blue': 10, 'gray': 35, 'purple': 0, 'aqua': 2, 'black': 34, 'teal': 7, 'orange': 11, 'green': 0, 'white': 25, 'red': 0}}
    draw_joint_hist(all_data_dict)

