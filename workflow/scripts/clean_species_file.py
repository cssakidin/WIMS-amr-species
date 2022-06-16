import csv
import argparse

# Initialize parser
parser = argparse.ArgumentParser()
# Adding optional argument
parser.add_argument("-o", "--Output", help="Show Output")
parser.add_argument("-i", "--Input", help="Show Input")
# Read arguments from command line
args = parser.parse_args()
original = args.Input
target = args.Output

if original and target:
    # original = r'database/test/acc_to_species.tsv'
    # target = r'database/test/clean_species.tsv'

    other_readid_dict = {}

    with open(original) as tsvfile:  # file met accessions en species
        species_file = csv.reader(tsvfile, delimiter="\t")
        for row in species_file:
            #try:
            read_id = row[0]  # kolom met read_id
            other = row[1:]  # kolommen met de rest van de gegevens
            # print(other)
                #readid_other_dict[read_id] = other
            if read_id not in other_readid_dict.keys():
                    other_readid_dict[read_id] = other
            if read_id in other_readid_dict.keys() and other[0] in other_readid_dict[read_id] and other[-2][-2:] > other_readid_dict[read_id][-2][-2:]:
                    other_readid_dict[read_id] = other #check of readid aanwezig is en dubbele species naam en e-scoree hoger dan de vorige is
            if read_id in other_readid_dict.keys() and other[0] not in other_readid_dict[read_id] and other[-2][-2:] > other_readid_dict[read_id][-2][-2:]:
                    other_readid_dict[read_id] = other #voor het geval dat een species aanwezig is die een hogere e-score heeft

    with open(target, "x") as cleansp:
        clean_species = csv.writer(cleansp, delimiter="\t")
        for key in other_readid_dict.keys():
            other_readid_dict[key].insert(0, key)
            clean_species.writerow(other_readid_dict[key])