import csv
import argparse

# Initialize parser
parser = argparse.ArgumentParser()
# Adding optional argument
parser.add_argument("-o", "--Output", help="Show Output")
parser.add_argument("-i", "--Input", help="Show Input")
# Read arguments from command line
args = parser.parse_args()

if args.Output and args.Input:

    # original = r'database/test/aln_amr_test.tsv'
    # target = r'database/test/clean_amr2.tsv'

    with open(args.Output, "x") as alnfile:  # kopie file waar accession wordt vervangen voor species naam
        output_amr_aln = csv.writer(alnfile, delimiter="\t")
        read_original_file = csv.reader(open(args.Input), delimiter="\t") #originele file met volledige notatie
        for row in read_original_file:
            amr_col = row[1] #kolom waar naam van amr gene etc staat
            split_amr_col = amr_col.split("Name:")  # vervang overige info voor amr naam
            split1_amr_col = split_amr_col[1].split("|NCBI")
            amr_name = split1_amr_col[0]
            if "confer" not in amr_name:
                row[1] = amr_name #Alles gesplits zodat alleen de naam overblijft
                output_amr_aln.writerow(row) #vervang de kolom naar alleen de naam