import csv
import argparse

# Initialize parser
parser = argparse.ArgumentParser()
# Adding optional argument
parser.add_argument("-o", "--Output", help="Show Output")
parser.add_argument("-i1", "--Input_species", help="Show Input species")
parser.add_argument("-i2", "--Input_acc_species", help="Show Input accession number + species file")
# Read arguments from command line
args = parser.parse_args()
acc_species = args.Input_acc_species
original_species = args.Input_species
target = args.Output

if acc_species and original_species and target:

    # original = r'database/test/aln_test.tsv'
    # original_species = r'database/test/acc_to_species.tsv'
    # target = r'database/test/acc_to_species.tsv'

    spec_acc_dict = {}
    other_readid_dict = {}
    # acc_spec_dict = {}

    with open(acc_species) as tsvfile:  # file met accessions en species
        species_file = csv.reader(tsvfile, delimiter="\t")
        for row in species_file:
            species = row[0]  # kolom met naam van species
            accession = row[1]  # kolom met accession nummers
            spec_acc_dict[accession] = species
            # if species not in acc_spec_dict.keys():
            #     acc_spec_dict[species] = [accession]
            # else:
            #     acc_spec_dict[species].append(accession)
        #print(spec_acc_dict)

    with open(target, "x") as alnfile:  # kopie file waar accession wordt vervangen voor species naam
        output_acc_to_species = csv.writer(alnfile, delimiter="\t")
        read_org_file = csv.reader(open(original_species), delimiter="\t") #orginele file met accession numbers
        #print(f"in open with copy file: {spec_acc_dict}")
        for row2 in read_org_file:
            #print(f"in open with copy file: {spec_acc_dict}")
            acc_number = row2[1]
            row2[1] = (spec_acc_dict[acc_number]) #accession number wordt gelijk gesteld met de corresponderende naam
            #print(row2)
            output_acc_to_species.writerow(row2) #heel de rij wordt geschreven