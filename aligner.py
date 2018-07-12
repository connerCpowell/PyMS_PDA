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


def alife(exprZ, folder_expr):
    # within replicates alignment parameters
    Dw=10.0 # rt modulation [s]
    Gw=0.30  # gap penalty
    # do the alignment

    expr_list = []
    expr_dir = folder_expr
    for expr_code in exprZ:
        print('Aligning...'+expr_code)
        file_name = os.path.join(expr_dir, expr_code )
        expr = load_expr(file_name)
        expr_list.append(expr)
    F1 = exprl2alignment(expr_list)
    print('F1' + '\n' )
    print(F1)
    T1 = PairwiseAlignment(F1, Dw, Gw)
    print('T1' + '\n')
    print(T1)
    A1 = align_with_tree(T1, min_peaks=2)
    A1.write_csv('/home/cocopalacelove/Desktop/StrawberryExotic/output/Alignments/Allstar10_rt.csv', '/home/cocopalacelove/Desktop/StrawberryExotic/output/Alignments/Allstar10_area.csv')



def main():
    folder_expr = '/home/cocopalacelove/Desktop/StrawberryExotic/output/area_expr'


    print("Welcome to Aligner, ")
    #input_var = input(" Select sample group, enter specific characters that represent your desired sample: ")

    list_of_expr, names = glob(glob_pattern='*cdf2*', directoryname=folder_expr)

    #print list_of_expr , names

    alife(list_of_expr, folder_expr)
    print('done')

if __name__ == "__main__":
    main()