import datetime, os, time, pickle
from min_heap import MinHeap, Pair

# need to check if caching is allowed

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
    global cache_size, cache_min_heap, cache_dictionary
    if (os.path.exists(CACHE_SIZE_FILE)
            and os.path.exists(CACHE_MIN_HEAP_FILE)
            and os.path.exists(CACHE_DICTIONARY_FILE)):
        with open(CACHE_SIZE_FILE, "rb") as file:
            cache_size = pickle.loads(file.read())
        with open(CACHE_MIN_HEAP_FILE, "rb") as file:
            cache_min_heap = pickle.loads(file.read())
        with open(CACHE_DICTIONARY_FILE, "rb") as file:
            cache_dictionary = pickle.loads(file.read())
        print("[INFO] Cache loaded.")
    else:
        print("[WARNING] Cache not found. This is normal if you are running the script for the first time.")
        os.makedirs(CACHE_DIRECTIVE, exist_ok=True)
        with open(CACHE_SIZE_FILE, "wb") as file:
            file.write(pickle.dumps(cache_size))
        with open(CACHE_MIN_HEAP_FILE, "wb") as file:
            file.write(pickle.dumps(cache_min_heap))
        with open(CACHE_DICTIONARY_FILE, "wb") as file:
            file.write(pickle.dumps(cache_dictionary))


def save_globals():
    os.makedirs(CACHE_DIRECTIVE, exist_ok=True)
    with open(CACHE_SIZE_FILE, "wb") as file:
        file.write(pickle.dumps(cache_size))
    with open(CACHE_MIN_HEAP_FILE, "wb") as file:
        file.write(pickle.dumps(cache_min_heap))
    with open(CACHE_DICTIONARY_FILE, "wb") as file:
        file.write(pickle.dumps(cache_dictionary))
    print("[INFO] Cache properties saved to disk.")


def get_current_time() -> int:
    return int(time.time())


def get_path_from_url(url: str, filename: str) -> str:
    path = url.removeprefix("http://")
    if path.endswith(filename):
        return path
    else:
        if path.endswith('/'):
            return path + filename
        else:
            return path + '/' + filename


def add_to_cache(path: str, filename: str, obj: bytes, modified: datetime.datetime) -> None:
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
    if path in cache_dictionary:
        access_time = get_current_time()
        new_position = cache_min_heap.increase_key(cache_dictionary[path][1], access_time)
        cache_dictionary[path] = access_time, new_position
        obj = get_cache_object(path)
        modified = datetime.datetime.fromtimestamp(get_file_modified_date(path))
        return obj, modified
    else:
        return None, None


def update_times(path: str, access_time: int, modified: datetime.datetime):
    path = CACHE_DIRECTIVE + path
    if not modified:
        os.utime(path, (access_time, access_time))
    else:
        os.utime(path, (access_time, modified.timestamp()))


def delete_oldest_file() -> None:
    global cache_size, cache_min_heap, cache_dictionary
    oldest_file = cache_min_heap.extract()
    cache_size -= get_file_size(oldest_file.value)
    delete_object_from_disk(oldest_file.value)
    del cache_dictionary[oldest_file.value]
    print(f"[INFO] Deleted {oldest_file.value} from cache.")


def save_object_to_disk(web_url: str, filename: str, obj: bytes) -> None:
    path = CACHE_DIRECTIVE + web_url.removeprefix("http://")
    os.makedirs(path.removesuffix(filename), exist_ok=True)
    with open(path, "wb") as file:
        file.write(obj)


def delete_object_from_disk(path: str):
    path = CACHE_DIRECTIVE + path
    os.remove(path)
    path = get_previous_directory(path)
    while os.path.exists(path) and len(os.listdir(path)) == 0:
        os.rmdir(path)
        path = get_previous_directory(path)


def get_previous_directory(path: str):
    path = path[::-1]
    path = path.split("/", 1)
    if len(path) > 1:
        path = path[1]
    else:
        path = path[0]
    return path[::-1]


def get_cache_object(path: str) -> bytes:
    path = CACHE_DIRECTIVE + path
    with open(path, "rb") as file:
        return file.read()


def get_file_modified_date(path: str):
    path = CACHE_DIRECTIVE + path
    return os.path.getmtime(path)


def get_file_size(path: str):
    path = CACHE_DIRECTIVE + path
    return os.stat(path).st_size

# add a size variable for the cache and when it reaches a certain size, delete the oldest file
# use os.remove(path) to remove the file
# use os.stat(path).st_size to get the size of the file
# use os.listdir(path) to get a list of all the files in the directory
# use os.path.getmtime(path) to get the time the file was last modified
# use os.path.join(path, filename) to get the path of the file
# use os.path.getctime(path) to get the creation time of the file
# use os.path.getatime(path) to get the last access time of the file
# use os.path.getmtime(path) to get the last modification time of the file
