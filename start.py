import os, shutil
from collections.abc import Iterable
import time 
SLEEP_TIMER  = 20
dir_list = []
all_files_path =[]

# log_file_path = 'C:\\Users\\johns\\Documents\\assign\\log.txt'
# origin_path = 'C:\\Users\\johns\\Documents\\assign\\Orig\\'
# copy_path = 'C:\\Users\\johns\\Documents\\assign\\Copy\\'


origin_path  = input('Inout original path with double balckslashes \\')
print(origin_path)

copy_path = input('Inout copy path with double balckslashes \\')
log_file_path = input('Inout log path with double balckslashes \\')
SLEEP_TIMER = int(input('input timer in seconds'))

#recursive function to get all files and folder in the path including the modification time
#if it's a directory there will be a list for every dir including the sub files and dirs in that dir
def dir_tree(path):
    #full_list = []
    names_and_mod = []
    files =os.scandir(path)
    for entry in files:
        if(entry.is_dir()):
            #full_list.append([[entry,os.path.getmtime(entry.path)], dir_tree(entry.path)])
            
            
            #there are different ways to check if the files is modified, like checking every line
            #in the file
            names_and_mod.append([[entry.path[len(path):]+'\\',os.path.getmtime(entry.path)], dir_tree(entry.path)])
        if(entry.is_file()):
            #full_list.append([entry,os.path.getmtime(entry.path)])
            names_and_mod.append([entry.path[len(path):],os.path.getmtime(entry.path)])
            
    return names_and_mod



def flatten(lis):
     for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:        
             yield item

                
def make_list(lis):
    lis = list(flatten(lis))
    new_list = {}
    for i in range(0,len(lis),2):
        new_list[lis[i]] = lis[i+1]
    return new_list

#a function to copy all content and overwite them to a different path
def copy_and_overwrite(dir_or_file, from_path, to_path):
    if(dir_or_file):
        if os.path.exists(to_path):
            shutil.rmtree(to_path)
        shutil.copytree(from_path, to_path)
    else:
        print(from_path,to_path)
        shutil.copyfile(from_path, to_path)        

def log(log_file, text):
    log_file.write(text + '\n')
    print(text)

    #this function is to detect changes between the two folders
def detect_change(log_file):
#     files_origin =os.scandir(path)
#     files_copy = os.scandir(copypth)
    source = make_list(dir_tree(origin_path))
    copy = make_list(dir_tree(copy_path))
    for entry in list(source.keys()):
        #if file is modified 
        if(entry in list(copy.keys())):
            #if a file is modified on the copy we dont make any change 
            if(source[entry] <= copy[entry]):
                continue 
            else :
                #if a dir 
                if(entry.endswith('\\')):
                    copy_and_overwrite(True, origin_path + entry, copy_path + entry)
                    log(log_file , 'Folder ' + entry + ' is modified PATH ' + copy_path + entry)
                    
                else:
                    copy_and_overwrite(False, origin_path + entry, copy_path + entry)
                    log(log_file , 'file ' +  entry + ' is modified PATH ' + copy_path + entry)
        #if file is added
        else:
            
            if(entry.endswith('\\')):
               
                copy_and_overwrite(True, origin_path + entry, copy_path + entry)
                log(log_file , 'Folder ' + entry +  ' is added PATH ' + copy_path + entry)
            else :
                copy_and_overwrite(False, origin_path + entry, copy_path + entry)
                log(log_file , 'file '  +  entry + ' is added PATH ' + copy_path + entry)
    #if file is deleted
    for entry in list(copy.keys()):
        if(entry not in source.keys()):
            if(entry.endswith('\\')):
                shutil.rmtree( copy_path + entry)
                log(log_file , "Folder " + entry + ' is deleted PATH ' + copy_path + entry)
                detect_change()
                break
            else:
                os.remove( copy_path + entry)
                log(log_file , "File " +  entry + ' is deleted PATH ' + copy_path + entry)
        

if(os.path.exists(log_file_path)):
    pass
else:
    f = open(log_file_path, "w")
while(True):
    f = open(log_file_path, "a")
    detect_change(f)
    time.sleep(SLEEP_TIMER)
    f.close()
