import datetime, os, time, pickle
from min_heap import MinHeap, Pair


# constants: the maximum size of the cache in bytes, the maximum size of the heap, the cache directive 
# use pickle library to encode and decode data onto disk
# implement LRU algorithm using a min heap and a dictionary

CACHE_DIRECTIVE = "cache/"
HEAP_MAX_SIZE = 10000
DISK_MAX_SIZE = 104857600
CACHE_SIZE_FILE = CACHE_DIRECTIVE + "cache_size.dat"
CACHE_MIN_HEAP_FILE = CACHE_DIRECTIVE + "cache_min_heap.dat"
CACHE_DICTIONARY_FILE = CACHE_DIRECTIVE + "cache_dictionary.dat"

cache_size = 0
cache_min_heap = MinHeap(HEAP_MAX_SIZE)
cache_dictionary = {}


def load_globals():
    '''
        Load the cache properties from disk.
    '''
    global cache_size, cache_min_heap, cache_dictionary
    if (os.path.exists(CACHE_SIZE_FILE) 
            and os.path.exists(CACHE_MIN_HEAP_FILE)
            and os.path.exists(CACHE_DICTIONARY_FILE)): # check if the files exist
        with open(CACHE_SIZE_FILE, "rb") as file:
            cache_size = pickle.loads(file.read())
        with open(CACHE_MIN_HEAP_FILE, "rb") as file:
            cache_min_heap = pickle.loads(file.read())
        with open(CACHE_DICTIONARY_FILE, "rb") as file:
            cache_dictionary = pickle.loads(file.read())
        print("[INFO] Cache loaded.")
    else: # if the files don't exist
        print("[WARNING] Cache not found. This is normal if you are running the script for the first time.")
        os.makedirs(CACHE_DIRECTIVE, exist_ok=True)
        with open(CACHE_SIZE_FILE, "wb") as file:
            file.write(pickle.dumps(cache_size))
        with open(CACHE_MIN_HEAP_FILE, "wb") as file:
            file.write(pickle.dumps(cache_min_heap))
        with open(CACHE_DICTIONARY_FILE, "wb") as file:
            file.write(pickle.dumps(cache_dictionary))


def save_globals():
    '''
        Save the cache properties to disk.
    ''' 
    os.makedirs(CACHE_DIRECTIVE, exist_ok=True) # create the cache directory if it doesn't exist
    with open(CACHE_SIZE_FILE, "wb") as file:
        file.write(pickle.dumps(cache_size))
    with open(CACHE_MIN_HEAP_FILE, "wb") as file:
        file.write(pickle.dumps(cache_min_heap))
    with open(CACHE_DICTIONARY_FILE, "wb") as file:
        file.write(pickle.dumps(cache_dictionary))
    print("[INFO] Cache properties saved to disk.")


def get_current_time() -> int:
    '''
        Get the current time in seconds.
    '''
    return int(time.time())


def get_path_from_url(url: str, filename: str) -> str:
    '''
        Get the path of the file from the URL.
    '''
    path = url.removeprefix("http://")
    if path.endswith(filename):
        return path
    else:
        if path.endswith('/'):
            return path + filename
        else:
            return path + '/' + filename


def add_to_cache(path: str, filename: str, obj: bytes, modified: datetime.datetime) -> None:
    '''
        Add the object to the cache.
    '''
    global cache_size, cache_min_heap, cache_dictionary
    size = len(obj)
    if path not in cache_dictionary:
        while cache_size + size > DISK_MAX_SIZE or cache_min_heap.size == cache_min_heap.maxsize:
            delete_oldest_file()
        cache_size += size
        access_time = get_current_time()
        position = cache_min_heap.insert(Pair(access_time, path))
        cache_dictionary[path] = access_time, position
        save_object_to_disk(path, filename, obj)
    else:
        access_time = get_current_time()
        new_position = cache_min_heap.increase_key(cache_dictionary[path][1], access_time)
        cache_dictionary[path] = access_time, new_position
        save_object_to_disk(path, filename, obj)
    update_times(path, access_time, modified)


def retrieve_from_cache(path: str):
    '''
        Retrieve the object from the cache.
    '''
    global cache_size, cache_min_heap, cache_dictionary
    if path in cache_dictionary:
        access_time = get_current_time()
        new_position = cache_min_heap.increase_key(cache_dictionary[path][1], access_time) # increase the key of the file
        cache_dictionary[path] = access_time, new_position # update the access time of the file
        obj = get_cache_object(path) # get the object from the cache
        modified = datetime.datetime.fromtimestamp(get_file_modified_date(path)) # get the modified date of the file
        return obj, modified # return the object and the modified date
    else:
        return None, None


def update_times(path: str, access_time: int, modified: datetime.datetime):
    '''
        Update the access time and modified time of the file on disk.
    '''
    path = CACHE_DIRECTIVE + path
    if not modified: 
        os.utime(path, (access_time, access_time)) # update the access time and modified time of the file
    else:
        os.utime(path, (access_time, modified.timestamp())) # update the access time and modified time of the file


def delete_oldest_file() -> None:
    '''
        Delete the oldest file from the cache.
    '''
    global cache_size, cache_min_heap, cache_dictionary
    oldest_file = cache_min_heap.extract() # extract the oldest file from the heap efficiently in logn time
    cache_size -= get_file_size(oldest_file.value) # decrease the cache size by the size of the file
    delete_object_from_disk(oldest_file.value) # delete the file from disk
    del cache_dictionary[oldest_file.value] # delete the file from the dictionary
    print(f"[INFO] Deleted {oldest_file.value} from cache.") # print a message to inform


def save_object_to_disk(web_url: str, filename: str, obj: bytes) -> None:
    '''
        Save the object to disk.
    '''
    path = CACHE_DIRECTIVE + web_url.removeprefix("http://") # get the path of the file
    os.makedirs(path.removesuffix(filename), exist_ok=True) # create the directory if it doesn't exist
    with open(path, "wb") as file: 
        file.write(obj)


def delete_object_from_disk(path: str):
    '''
        Delete the object from disk.
    '''
    path = CACHE_DIRECTIVE + path
    os.remove(path) # remove the file from disk
    path = get_previous_directory(path) # get the previous directory using function
    while os.path.exists(path) and len(os.listdir(path)) == 0: # while the directory exists and is empty, keep on deleting directories
        os.rmdir(path)
        path = get_previous_directory(path)


def get_previous_directory(path: str):
    '''
        Get the previous directory by reversing, splitting, then reversing back.
    '''
    path = path[::-1]
    path = path.split("/", 1)
    if len(path) > 1:
        path = path[1]
    else:
        path = path[0]
    return path[::-1]


def get_cache_object(path: str) -> bytes:
    '''
        Get the object from the cache.
    '''
    path = CACHE_DIRECTIVE + path
    with open(path, "rb") as file:
        return file.read()


def get_file_modified_date(path: str):
    '''
        Get the modified date of the file.
    '''
    path = CACHE_DIRECTIVE + path
    return os.path.getmtime(path)


def get_file_size(path: str):
    '''
        Get the size of the file.
    '''
    path = CACHE_DIRECTIVE + path
    return os.stat(path).st_size
