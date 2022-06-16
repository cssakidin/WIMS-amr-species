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

# original = r'database/test/combine_species_and_amr2.tsv'
# target = r'database/test/count_files/count_match2.xlsx'

if args.Input and args.Output:
    amr_spec_dict = {}

    # Create an XlsxWriter workbook object and add a worksheet.
    workbook = Workbook(args.Output)
    worksheet = workbook.add_worksheet()

    with open(args.Input) as amr_spec_file:
        join_file = csv.reader(amr_spec_file, delimiter="\t")
        next(join_file)
        for row1 in join_file:
            try:
                amr = row1[1]
                species = row1[12]
                #match counter
                if (amr + " + " + species) in amr_spec_dict.keys():
                    amr_spec_dict[(amr + " + " + species)] = amr_spec_dict[(amr + " + " + species)] + 1 #+1 bij counter wanneer een match is gevonden
                if (amr + " + " + species) not in amr_spec_dict.keys():
                    amr_spec_dict[(amr + " + " + species)] = 1 #nieuwe waarde aan value toevoegen (de counter)
            except IndexError:
                print("something went wrong in the joined amr-species file? (index error)")
            # print(amr_spec_dict)
            # print(amr_count_dict)
            # print(species_count_dict)

    # with open("database/test/count_match.tsv", "x") as cf:
    #     count_file = csv.writer(cf, delimiter="\t")
    #     for key in amr_spec_dict.keys(): #schrijven van match counts
    #         row = [key, amr_spec_dict[key]]
    #         count_file.writerow(row)

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    for key in amr_spec_dict.keys():  # schrijven van match counts
        worksheet.write(row, col, key)
        worksheet.write(row, col + 1, amr_spec_dict[key])
        row += 1

    workbook.close()