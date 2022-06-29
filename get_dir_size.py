import os
import matplotlib.pyplot as plt

def get_size_format(b, factor=1024, suffix="B"):
    
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def get_directory_size(directory):
    """Returns the `directory` size in bytes."""
    total = 0
    try:
        for entry in os.scandir(directory):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                try:
                    total += get_directory_size(entry.path)
                except FileNotFoundError:
                    pass
    except NotADirectoryError:
        # if `directory` isn't a directory, get the file size then
        return os.path.getsize(directory)
    except PermissionError:
        return 0
    return total

def plot_pie(sizes, name):
    plt.pie(sizes, labels=names, autopct=lambda pct: f"{pct:.2f}%")
    plt.title("Different sub-directory sizes in bytes")
    plt.show()

if __name__ == "__main__":
    import sys
    folder_path = sys.argv[1]

    directory_sizes = []
    names = []
    
    for directory in os.listdir(folder_path):
        directory = os.path.join(folder_path, directory)
        # get the size of this directory (folder)
        directory_size = get_directory_size(directory)
        if directory_size == 0:
            continue
        directory_sizes.append(directory_size)
        names.append(os.path.basename(directory) + ": " + get_size_format(directory_size))

    print("[+] Total directory size:", get_size_format(sum(directory_sizes)))
    plot_pie(directory_sizes, names)
