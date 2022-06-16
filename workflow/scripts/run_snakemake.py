import argparse
import subprocess

# Initialize parser
parser = argparse.ArgumentParser()
# Adding optional argument
parser.add_argument("-i", "--Input", help="Show Input")
# Read arguments from command line
args = parser.parse_args()

if args.Input:
    with open(Snakefile, "w") as snake:
        for line in snake:
            if "SAMPLE=" in line:
              line = "SAMPLE=" + str(args.Input)
        subprocess.run("conda activate snakemake", shell=True)
        subprocess.run("snakemake -c 8 --use-conda", shell=True)