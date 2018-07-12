import fnmatch
import sys, os

from pyms.Experiment.IO import load_expr
from pyms.Peak.List.DPA.Class import PairwiseAlignment
from pyms.Peak.List.DPA.Function import align_with_tree, exprl2alignment


def glob(glob_pattern, directoryname):
    '''
    Walks through a directory and its subdirectories looking for files matching
    the glob_pattern and returns a list=[].

    :param directoryname: Any accessible folder name on the filesystem.
    :param glob_pattern: A string like "*.txt", which would find all text files.
    :return: A list=[] of absolute filepaths matching the glob pattern.
    '''
    matches = []
    names = []
    for root, dirnames, filenames in os.walk(directoryname):
        for filename in fnmatch.filter(filenames, glob_pattern):
            absolute_filepath = os.path.join(root, filename)
            matches.append(absolute_filepath)

            name = filename.rsplit('/StrawberryExotic/')[-1]
            names.append(name)

    return matches, names


def alifeGuru(listem, folder_expr):
    # within replicates alignment parameters
    Dw=2.0 # rt modulation [s]
    Gw=0.30  # gap penalty
    # do the alignment
    trees = []

    expr_list = []
    expr_dir = folder_expr
    for gru_list in listem:
        for item in gru_list:
            print('Aligning...'+item)
            file_name = os.path.join(expr_dir, item )
            expr = load_expr(file_name)
            expr_list.append(expr)
        F1 = exprl2alignment(expr_list)
        print('F1' + '\n' )
        print(F1)
        trees.append(F1)

    for t in trees:
        T1 = PairwiseAlignment(t, Dw, Gw)
        print('T1' + '\n')
        print(T1)
        A1 = align_with_tree(T1, min_peaks=2)

        A1.write_csv('/home/cocopalacelove/Desktop/StrawberryExotic/output/Alignments/fullSpec_rt.csv', '/home/cocopalacelove/Desktop/StrawberryExotic/output/Alignments/fullSpec_area.csv')
    print(trees)


def main():
    folder_expr = '/home/cocopalacelove/Desktop/StrawberryExotic/output/area_expr'

    llamas = [ 'NA', 'Alexandria', 'Bucharica', 'Capron', 'Tortona', 'Mara', 'Mignonette', 'Strawberry', 'Viridis']
    listem = []


    for name in llamas:
        nomo = '*'+ name + '*'
        print(nomo)
        list_of_expr, names = glob(glob_pattern= nomo, directoryname=folder_expr)
        listem.append(list_of_expr)


    print(listem)
    alifeGuru(listem, folder_expr)

    # print list_of_expr , names
    #
    # alifeGuru(list_of_expr, folder_expr)
    # print('done')

if __name__ == "__main__":
    main()