import csv
import argparse

# Initialize parser
parser = argparse.ArgumentParser()
# Adding optional argument
parser.add_argument("-o", "--Output", help="Show Output")
parser.add_argument("-i1", "--Input_species", help="Show Input species")
parser.add_argument("-i2", "--Input_amr", help="Show Input AMR")
# Read arguments from command line
args = parser.parse_args()

# original_species = r'database/test/clean_species.tsv'
# original_amr = r'database/test/aln_amr.tsv'
# target = r'database/test/join_test10.tsv'

if args.Input_species and args.Input_amr and args.Output:
    #readid_other_dict = {}
    other_readid_dict = {}

    #readid_other_amr_dict = {}
    other_readid_amr_dict = {}

    with open(args.Input_species) as tsvfile:  # file met accessions en species
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
            #except:
                #print("list index out of range sp?")

    with open(args.Input_amr) as tsvfile1:  # file met accessions en species
        amr_file = csv.reader(tsvfile1, delimiter="\t")
        for row1 in amr_file:
            # try:
            read_id_amr = row1[0]  # kolom met read_id
            other_amr = row1[1:]  # kolommen met de rest van de gegevens
            if read_id_amr not in other_readid_amr_dict.keys():
                other_readid_amr_dict[read_id_amr] = other_amr  # wanneer readid nog niet aanwezig is
            if read_id_amr in other_readid_amr_dict.keys() and other_amr[0] in other_readid_amr_dict[read_id_amr] and other_amr[-2] > other_readid_amr_dict[read_id_amr][-2]:
                other_readid_amr_dict[read_id_amr] = other_amr #check of readid aanwezig is en dubbele amr naam en e-scoree hoger dan de vorige is
            if read_id_amr in other_readid_amr_dict.keys() and other_amr[0] not in other_readid_amr_dict[read_id_amr] and other_amr[-2] > other_readid_amr_dict[read_id_amr][-2]:
                other_readid_amr_dict[read_id_amr] = other_amr #voor het geval dat een amr gen aanwezig is met een betere e-score
            # except TypeError:
            #     if read_id_amr in other_readid_amr_dict.keys() and other_amr[0] in other_readid_amr_dict[read_id_amr] and other_amr[-2] > other_readid_amr_dict[read_id_amr][-2]:
            #         other_readid_amr_dict[read_id_amr] = other_amr #check of readid aanwezig is en dubbele amr naam en e-scoree hoger dan de vorige is

    # for key, value in other_readid_dict.items():
    #     print(key, value)
    #for key, value in other_readid_amr_dict():
        #print(key, value)

    with open(args.Output, "x") as jfile:
        join_file = csv.writer(jfile, delimiter="\t")
        header = ["read id", "amr gene", "seq identity", "", "", "", ""]
        join_file.writerow(header)
        for key in other_readid_amr_dict.keys():
            try:
                other_readid_amr_dict[key].insert(0, key)
                other_readid_amr_dict[key].append(other_readid_dict[key][0])
                other_readid_amr_dict[key].append(other_readid_dict[key][1])
                other_readid_amr_dict[key].append(other_readid_dict[key][2])
                other_readid_amr_dict[key].append(other_readid_dict[key][3])
                other_readid_amr_dict[key].append(other_readid_dict[key][4])
                other_readid_amr_dict[key].append(other_readid_dict[key][5])
                other_readid_amr_dict[key].append(other_readid_dict[key][6])
                other_readid_amr_dict[key].append(other_readid_dict[key][7])
                other_readid_amr_dict[key].append(other_readid_dict[key][8])
                other_readid_amr_dict[key].append(other_readid_dict[key][9])
                other_readid_amr_dict[key].append(other_readid_dict[key][10])
                join_file.writerow(other_readid_amr_dict[key]) #toevoegen van nieuwe row (species gegevens achter amr gegevens)
            except KeyError: #wanneer bij readid geen species is toegewezen, dan wordt species unknown toegevoegd
                other_readid_amr_dict[key].append("Species unknown")
                join_file.writerow(other_readid_amr_dict[key])