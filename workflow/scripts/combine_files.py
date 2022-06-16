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
# original_amr = r'database/test/clean_amr2.tsv'
# target = r'database/test/combine_species_and_amr2.tsv'
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
            other_readid_dict[read_id] = other

    with open(args.Output, "x") as jfile:
        join_file = csv.writer(jfile, delimiter="\t")
        amr_file = csv.reader(open(args.Input_amr), delimiter="\t")
        header = ["read id", "amr gene", "seq identity", "alignment length", "number of mismatches", "number of gap openings", " domain start read-id", "end-position read", "domain start amr-id", "end-position amr-id", "E-value", "bit score", "species-id", "seq identity", "alignment length", "number of mismatches", "number of gap openings", " domain start read-id", "end-position read", "domain start species-id", "end-position species-id", "E-value", "bit score"]
        join_file.writerow(header)
        for row1 in amr_file:
            readid = row1[0]
            try:
                if readid in other_readid_dict.keys():
                    combi = row1 + other_readid_dict[readid]
                    join_file.writerow(combi) #toevoegen van nieuwe row (species gegevens achter amr gegevens)
            except KeyError: #wanneer bij readid geen species is toegewezen, dan wordt species unknown toegevoegd
                idk = row1 + ["Unclassified"]
                join_file.writerow(idk)