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

def draw_color_dist(total_color_count, genre, wood, era):
    
    labels = [ z for z in sorted(total_color_count.keys()) if total_color_count[z] != 0 ]
    y = [total_color_count[n] for n in sorted(total_color_count.keys()) if total_color_count[n] != 0 ]
    y_sum = sum(y)
    y_perc = [ z*100.0/y_sum for z in y]
    x = range(len(y))
    
    print y
    print y_sum
    print y_perc
   
    plt.title("Color Distribution for " + era + "->" + wood + "->" + genre)
    plt.ylim(0.0, 50.0)
    plt.xticks(x, labels)
    plt.bar(x, y_perc, width = 0.75, color = [norm_dict[x] for x in sorted(norm_dict.keys()) if x in labels], align= 'center')
    plt.savefig("graphs/" + era + "_" + wood + "_" + genre + ".jpg")
    plt.clf()
    plt.cla()
    plt.close()
    #plt.show()
    
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
                draw_color_dist(total_color_count, genre, wood, era)
                
if __name__ == '__main__':
    main()
