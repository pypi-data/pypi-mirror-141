import cv2
import os
import numpy as np
import time
from tqdm import tqdm
from threading import Thread
from sidd import siddcompares, siddcolors


dupe_list = []
'''A list of duplicate images.'''
prob_threshold = .1
'''Delta threshold to use when performing probablistic matching.'''
#list_of_colors = [[255,0,0],[150,33,77],[75,99,23],[45,88,250],[250,0,255]]
list_of_colors = [[2,63,165],[125,135,185],[190,193,212],[214,188,192],[187,119,132],[142,6,59],[74,111,227],[133,149,225],[181,187,227],[230,175,185],[224,123,145],[211,63,106],[17,198,56],[141,213,147],[198,222,199],[234,211,198],[240,185,141],[239,151,8],[15,207,192],[156,222,214],[213,234,231],[243,225,235],[246,196,225],[247,156,212]]
'''Common colors used to create buckets during bucketed comparison.'''



def DedupeImageDir(directory, t_count=10, compMethod = siddcompares.CompareImageProbability):
    '''
    Function to deduplicate entire directories. This moves through one image at a time. Can be slower but more accurate than grouping deduper.
    \r\n
    Parameters
    ------------------------
    directory : str
        The directory to de-duplicate.
    t_count : int
        The number of threads to use (10 by default)
    comp_method:
        Use CompareImageProbability (default) or CompareImageExact

    \r\n
    Returns
    ------------------------ \r\n
    str[]
        Returns an array of images in the directory that are duplicates. \r\n
    '''
    dupe_list.clear()
    dir_list = [os.path.join(directory,x) for x in os.listdir(directory)]
    dir_list_len = len(dir_list)
    if t_count > dir_list_len: 
        tqdm.write("Collection to small, just using 1 thread per file.", end='.\n')
        t_count = dir_list_len
    i = 1
    for current in dir_list:
        if current in dupe_list:
            tqdm.write(f"Skipping, this is a duplicate ..  {current} .. {i}/{dir_list_len - len(dupe_list)}", end='.\n')
        else:
            tqdm.write(f"\r\nProcessing: {current} .. {i}/{dir_list_len - len(dupe_list)}", end='.\n')
            threads = []
            others_list = list(set(dir_list) - set([current]))
            others_list_filtered = list(set(others_list) - set(dupe_list))
            others_list_chunks = np.array_split(others_list_filtered, t_count)
            for chunk in others_list_chunks:
                threads.append(Thread(target=CompareWorker, args=(current, chunk, compMethod)))
            for t in threads: t.start()
            for t in threads: t.join()
        i=i+1
    return dupe_list


def DedupeImageDirWithBuckets(directory, t_count=10, comp_method = siddcompares.CompareImageProbability, resize=[256,256]):
    '''
    Function to deduplicate entire directories. This moves through one image at a time. Can be slower but more accurate than grouping deduper.
    \r\n
    Parameters
    ------------------------
    directory : str
        The directory to de-duplicate.
    t_count : int
        The number of threads to use (10 by default)
    comp_method: method
        Use CompareImageProbability (default) or CompareImageExact from siddcompares
    resize: [int,int]
        Image resolution. All images are resized because this is an expensive operation. Don't want a resize? Let me know on github.

    \r\n
    Returns
    ------------------------ \r\n
    str[]
        Returns an array of images in the directory that are duplicates. \r\n
    '''
    start_time = time.time()
    
    global color_buckets 
    color_buckets = [{'color':c, 'images':[]} for c in list_of_colors]
    tqdm.write(f"Created {len(color_buckets)} buckets...", end='.\r\n')
    
    dupe_list.clear()
    dir_list = [os.path.join(directory,x) for x in os.listdir(directory)]
    dir_list_len = len(dir_list)
    
    chunks_t_count = t_count
    if chunks_t_count > dir_list_len: 
        tqdm.write("Collection to small, just using 1 thread per file.", end='.\r\n')
        chunks_t_count = dir_list_len
    
    # Creates Buckets of Images Based On Most Frequent Color
    chunks = np.array_split(dir_list, chunks_t_count)
    tqdm.write(f"Created {len(chunks)} chunks of images to process...", end='.\r\n')
    threads_chunks = []
    for chunk in chunks:
        threads_chunks.append(Thread(target=BucketByColorWorker, args=(chunk, resize, t_count)))
    for t in threads_chunks: t.start()
    for t in threads_chunks: t.join()
    
    stop_time = time.time()
    tqdm.write(f"Time Lapsed (seconds): {str(stop_time - start_time)}")
    
    return dupe_list
    

def CompareWorker(current, chunk, comp_method=siddcompares.CompareImageProbability, with_progress=True):
    '''
    Worker thread. Don't use this unless you know what you're doing.
    Set with_progress false t disable tqpm progress bar (buggy with nested operations)
    '''
    collection = []
    if with_progress == True:
        collection = tqdm(chunk)
    else:
        collection = chunk
    for suspect in collection:
        result = siddcompares.CompareImage(current, suspect, comp_method)
        if result == True:
            dupe_list.append(suspect)        
            
            
def BucketByColorWorker(chunk, resize, t_count):
    '''
    Worker thread. Don't use this unless you know what you're doing.
    '''
    for suspect in tqdm(chunk):
        img = cv2.imread(suspect)
        img_resized = cv2.resize(img, resize)
        frequent_color = siddcolors.FrequentColor(img_resized)
        closest_color = siddcolors.ClosestColor(frequent_color, list_of_colors)
        
        # Append to bucket before doing anything
        [x for x in color_buckets if (np.array(x['color']) == np.array(closest_color)).all()][0]['images'] \
            .append(suspect)
        
        # Divid bucket into chunks and begin comparison
        current_bucket = [x for x in color_buckets if (np.array(x['color']) == np.array(closest_color)).all()][0]
        current_bucket_images_others = [x for x in current_bucket['images'] if (x != suspect)]
        
        chunk_t_count = t_count
        
        if len(current_bucket_images_others) < chunk_t_count:
            chunk_t_count = len(current_bucket_images_others)
        
        if(len(current_bucket_images_others)) > 0:
            bucket_chunks = np.array_split(current_bucket_images_others, chunk_t_count)
            for bucket_chunk in bucket_chunks:
                for current in bucket_chunk:
                    if suspect not in dupe_list:
                        if siddcompares.CompareImage(current, suspect) == True:
                            dupe_list.append(suspect)