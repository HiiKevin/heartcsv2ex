import os
import sys
import argparse

import pandas as pd

from heartcsv2ex.csvpoints import CSVPoint
from heartcsv2ex.csv2ex import write_ex


GROUPS = {'Epi': 'epicardium',
          'LVendo': 'endocardium of left ventricle',
          'RV_freewall': 'endocardium of right ventricle',
          'RV_septum': 'endocardium of right ventricle',
          'AV': 'root of aorta',
          'MV': 'root of mitral valve',
          'TV': 'root of triscupid valve',
          'PV': 'root of pulmonary valve'}


class ProgramArguments(object):
    def __init__(self):
        self.input_csvs = None
        self.output_ex = None


def read_csv(files_path):
    csv_data = {}
    for file in os.listdir(files_path):
        file_name = file.split('.')[0]
        points = []
        if file_name in GROUPS.keys():
            data = pd.read_csv(os.path.join(files_path, file), sep=',')
            for pts in data.values:
                points.append(_create_csv_point(pts))
            csv_data[GROUPS[file_name]] = points
    return csv_data


def _create_csv_point(pts):
    return CSVPoint(float(pts[0]),
                    float(pts[1]),
                    float(pts[2]))


def main():
    args = parse_args()
    if os.path.exists(args.input_csvs):
        if args.output_ex is None:
            output_ex = os.path.join(args.input_csvs, 'combined.ex')
        else:
            output_ex = args.output_ex
        contents = read_csv(args.input_csvs)
        if contents is None:
            sys.exit(-2)
        else:
            write_ex(output_ex, contents)
    else:
        sys.exit(-1)


def parse_args():
    parser = argparse.ArgumentParser(description="Transform CMI surface data files to ex format.")
    parser.add_argument("input_csvs", help="Location of the input csv files.")
    parser.add_argument("--output-ex", help="Location of the output ex file. "
                                            "[defaults to the location of the input file if not set.]")

    program_arguments = ProgramArguments()
    parser.parse_args(namespace=program_arguments)

    return program_arguments


if __name__ == "__main__":
    main()
