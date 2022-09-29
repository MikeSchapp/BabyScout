import uos as os


def walk_directories(initial_directory="/"):
    if not initial_directory.startswith("/"):
        initial_directory = f"/{initial_directory}"
    directories = [initial_directory]
    paths = {}
    while directories:
        for directory in directories:
            new_directories, files = recursive_walk(directory)
            paths[directory] = files
            directories = new_directories
    return paths

def recursive_walk(initial_directory):
    files = []
    directories = []
    unprocessed_directory = os.ilistdir(initial_directory)
    if unprocessed_directory:
        for item in unprocessed_directory:
            if item[1] == 16384:
                if initial_directory == "/":
                    initial_directory = ""
                directories.append(f"{initial_directory}/{item[0]}")
            else:
                files.append(item[0])
    return (directories, files)
