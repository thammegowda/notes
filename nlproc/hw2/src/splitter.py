from perceptron import scan_data
from random import shuffle
from shutil import copy
import sys,os

def main(src, dst, percent):
    data = scan_data(src)
    paths = []
    for _, path in data:
        paths.append(path)

    tot = len(paths)
    #shuffle
    shuffle(paths)
    count = 0
    for p in paths[:int(percent * tot)]:
        dst_p = p.replace(src, dst)
        os.makedirs(dst_p[:dst_p.rindex(os.path.sep)], exist_ok=True)
        copy(p, dst_p)
        count += 1
    print("Copied %d files of %d" % (count, tot))

if __name__ == '__main__':
    src = sys.argv[1]
    dst = sys.argv[2]
    percent = float(sys.argv[3])
    assert percent > 0.0
    assert percent < 1.0
    main(src, dst, percent)
