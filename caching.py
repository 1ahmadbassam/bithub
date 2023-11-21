import os

CACHE_DIRECTIVE = "cache/"


def handle_cache_object(web_url: str, filename: str, obj: bytes):
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
