import os
from datetime import time
from min_heap import MinHeap, Pair

CACHE_DIRECTIVE = "cache/"

cache_size = 0
max_cache_size = 104857600 # 100 MB
cache_min_heap = MinHeap(max_cache_size)
cache_dictionary = {}

def get_current_time():
    return int(time.time()*1000)

def add_to_cache(path, size, filename, obj):
	global cache_size, cache_min_heap, cache_dictionary
	if path not in cache_dictionary:
		while cache_size + size > max_cache_size:
			delete_oldest_file()
		cache_size += size
		time = get_current_time()
		position = cache_min_heap.insert(Pair(time, path))
		cache_dictionary[path] = time, position
		save_object_on_disk(path, filename, obj)
	else:
		time = get_current_time()
		new_position = cache_min_heap.increase_key(Pair(time, path))
		cache_dictionary[path] = time, new_position
		save_object_to_disk(path, filename, obj)

def delete_oldest_file():
	global cache_size, cache_min_heap, cache_dictionary
	oldest_file = cache_min_heap.extract()
	cache_size -= os.stat(oldest_file).st_size
	del cache_dictionary[oldest_file]
      

def save_object_to_disk(web_url: str, filename: str, obj: bytes):
	path = CACHE_DIRECTIVE + web_url.removeprefix("http://")
	os.makedirs(path.removesuffix(filename), exist_ok=True)
	with open(path, "wb") as file:
		file.write(obj)
		
def get_cache_object(web_url: str, filename: str):
    path = CACHE_DIRECTIVE + web_url.removeprefix("http://")
    return get_object(path)

def get_object(path):
    with open(path, "rb") as file:
         return file.read()



def save_object_on_disk(web_url: str, filename: str, obj: bytes):
    path = CACHE_DIRECTIVE + web_url.removeprefix("http://")
    os.makedirs(path.removesuffix(filename), exist_ok=True)
    cache_object(path, obj)


def cache_object(path, obj):
    with open(path, "wb") as file:
        file.write(obj)

# add a size variable for the cahce and when it reaches a certain size, delete the oldest file
# use os.remove(path) to remove the file
# use os.stat(path).st_size to get the size of the file
# use os.listdir(path) to get a list of all the files in the directory
# use os.path.getmtime(path) to get the time the file was last modified
# use os.path.join(path, filename) to get the path of the file
# use os.path.getctime(path) to get the creation time of the file
# use os.path.getatime(path) to get the last access time of the file
# use os.path.getmtime(path) to get the last modification time of the file
