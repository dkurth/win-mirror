'''Given a file or directory underneath main_root,
   this script will mirror that file/directory within
   mirror_root by creating directories within mirror_root
   containing hard links to each file.

   I use this to maintain a subset of my music collection
   that is family-friendly so I can point my music player
   to that directory.
'''

import sys
import os
import os.path

main_root = r'''E:\\music'''
mirror_root = r'E:\\music\\family'

def link_directory(d):
    for root, dirs, files in os.walk(d):
        path = os.path.relpath(root, main_root)

        mirror_dir = os.path.join(mirror_root, path)
        main_dir = os.path.join(main_root, path)

        for file in files:
            mirror_file = os.path.join(mirror_dir, file)
            main_file = os.path.join(main_dir, file)
            link_file(main_file, mirror_file)

'''Takes two full file paths, and creates a hard link from the first to the second.'''
def link_file(f_main, f_mirror):

    path_parts = os.path.split(f_mirror)
    
    if not os.path.exists(path_parts[0]):
        os.makedirs(path_parts[0])

    cmd = 'mklink /H "{}" "{}'.format(f_mirror, f_main)
    os.system(cmd)


def is_within(d, parent):
    rel = os.path.relpath(d, parent) # the path to d from parent should not include going up any directories
    return rel.find('..') != 0

if __name__ == "__main__":
    
    argc = len(sys.argv)

    if argc < 2 or not os.path.exists(sys.argv[1]):
        print("Please pass a file or directory.")
        sys.exit()

    for i in range(1, argc):

        f = sys.argv[i]

        if not is_within(f, main_root):
            print("Failed because {} is not within {}".format(f, main_root))
            sys.exit()

        if os.path.isdir(f):
            link_directory(f)
        else:
            rel = os.path.relpath(f, main_root)
            main_file = os.path.join(main_root, rel)
            mirror_file = os.path.join(mirror_root, rel)
            link_file(main_file, mirror_file)
