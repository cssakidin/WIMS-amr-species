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
  FDA_dict = {}
  output_species = open(target, "w")
  writer = csv.writer(output_species, delimiter="\t")

  with open(original) as FDA:
    for line in FDA:
      identifier = ""
      species = ""
      if ">" in line:
        if ".1 " in line: #voor .1
          split_preid = line.split(".1 ")
          split_preid1 = split_preid[0]
          split_preid2 = split_preid1.replace(">", "")
          split_id = split_preid2 + ".1"
          split_species = split_preid[1].split("\n")
          split_species1 = split_species[0].split(" ")
          split_species2 = split_species1[0] + " " + split_species1[1]
          row = [split_species2, split_id]
          writer.writerow(row)
        elif ".2 " in line: #voor .2
          split_preid = line.split(".2 ")
          split_preid1 = split_preid[0]
          split_preid2 = split_preid1.replace(">", "")
          split_id = split_preid2 + ".2"
          split_species = split_preid[1].split("\n")
          split_species1 = split_species[0].split(" ")
          split_species2 = split_species1[0] + " " + split_species1[1]
          row = [split_species2, split_id]
          writer.writerow(row)
        elif ".3 " in line: #voor .3
          split_preid = line.split(".3 ")
          split_preid1 = split_preid[0]
          split_preid2 = split_preid1.replace(">", "")
          split_id = split_preid2 + ".3"
          split_species = split_preid[1].split("\n")
          split_species1 = split_species[0].split(" ")
          split_species2 = split_species1[0] + " " + split_species1[1]
          row = [split_species2, split_id]
          writer.writerow(row)
        elif ".4 " in line: #voor .4
          split_preid = line.split(".4 ")
          split_preid1 = split_preid[0]
          split_preid2 = split_preid1.replace(">", "")
          split_id = split_preid2 + ".4"
          split_species = split_preid[1].split("\n")
          split_species1 = split_species[0].split(" ")
          split_species2 = split_species1[0] + " " + split_species1[1]
          row = [split_species2, split_id]
          writer.writerow(row)
        else: #voor .5
          split_preid = line.split(".5 ")
          split_preid1 = split_preid[0]
          split_preid2 = split_preid1.replace(">", "")
          split_id = split_preid2 + ".5"
          split_species = split_preid[1].split("\n")
          split_species1 = split_species[0].split(" ")
          split_species2 = split_species1[0] + " " + split_species1[1]
          row = [split_species2, split_id]
          writer.writerow(row)

  output_species.close()