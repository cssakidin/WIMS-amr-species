import csv
from xlsxwriter.workbook import Workbook
import argparse

# Initialize parser
parser = argparse.ArgumentParser()
# Adding optional argument
parser.add_argument("-o", "--Output", help="Show Output")
parser.add_argument("-i", "--Input", help="Show Input")
# Read arguments from command line
args = parser.parse_args()
amrfile = args.Input
target = args.Output

if amrfile and target:

    #name files:
    # amrfile = r"database/test/clean_amr2.tsv"
    # target = r"database/test/count_files/amr_count2.xlsx"

    # Create an XlsxWriter workbook object and add a worksheet.
    workbook = Workbook(target)
    worksheet = workbook.add_worksheet()

    #make dictionary:
    amr_dict = {}

    #read file with tab as delimiter.
    with open(amrfile) as spfile:
        count_file = csv.reader(spfile, delimiter='\t')
        for row in count_file: #use for-loop to count
            amr = row[1]
            if amr in amr_dict.keys():
                amr_dict[amr] = amr_dict[amr] + 1
            if amr not in amr_dict.keys():
                amr_dict[amr] = 1

    # #write dictionary keys and result in new file
    # with open(target, "x") as spcountfile:
    #     write_file = csv.writer(spcountfile, delimiter= "\t")
    #     for key in amr_dict.keys():
    #         listed = [key, amr_dict[key]]
    #         write_file.writerow(listed)
    #
    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    for key in amr_dict.keys():
        worksheet.write(row, col, key)
        worksheet.write(row, col + 1, amr_dict[key])
        row += 1

    workbook.close()