SAMPLES="barcode07_test4"

rule all:
  input:
    expand("results/trimmed_reads/{sample}/{sample}_trimmed.fq", sample=SAMPLES),
    expand("results/filtered_reads/{sample}/{sample}_filtered.fq", sample=SAMPLES),
    expand("results/nanoplot/nanoplot_raw/{sample}/", sample=SAMPLES),
    expand("results/nanoqc/nanoqc_raw/{sample}/", sample=SAMPLES),
    expand("results/nanoplot/nanoplot_trimmed/{sample}/", sample=SAMPLES),
    expand("results/nanoqc/nanoqc_trimmed/{sample}/", sample=SAMPLES),
    expand("results/nanoplot/nanoplot_filtered/{sample}/", sample=SAMPLES),
    expand("results/nanoqc/nanoqc_filtered/{sample}/", sample=SAMPLES),
    expand("results/output/{sample}/results.xlsx", sample=SAMPLES)

rule RawNanoPlot:
  input:
    "dataset_nanopore/{sample}.fastq.gz"
  output:
    directory("results/nanoplot/nanoplot_raw/{sample}/")
  conda:
    "workflow/envs/NanoPlot.yaml"
  shell:
    "NanoPlot -t 6 --fastq {input} -o {output}"

rule RawNanoQC:
  input:
     "dataset_nanopore/{sample}.fastq.gz"
  output:
    directory("results/nanoqc/nanoqc_raw/{sample}/")
  conda:
     "workflow/envs/NanoQC.yaml"
  shell:
     "nanoQC {input} -o {output}"

rule Trimming:
  input:
    "dataset_nanopore/{sample}.fastq.gz"
  output:
    "results/trimmed_reads/{sample}/{sample}_trimmed.fq"
  conda:
    "workflow/envs/NanoFilt.yaml"
  shell:
    "gunzip -c {input} | NanoFilt -q 10 -l 500 > {output}"

rule TrimmedNanoPlot:
  input:
    "results/trimmed_reads/{sample}/{sample}_trimmed.fq"
  output:
    directory("results/nanoplot/nanoplot_trimmed/{sample}/")
  conda:
    "workflow/envs/NanoPlot.yaml"
  shell:
    "NanoPlot -t 6 --fastq {input} -o {output}"

rule TrimmedNanoQC:
  input:
    "results/trimmed_reads/{sample}/{sample}_trimmed.fq"
  output:
    directory("results/nanoqc/nanoqc_trimmed/{sample}/")
  conda:
     "workflow/envs/NanoQC.yaml"
  shell:
    "nanoQC {input} -o {output}"

rule Filtering:
  input:
    "results/trimmed_reads/{sample}/{sample}_trimmed.fq"
  output:
    "results/filtered_reads/{sample}/{sample}_filtered.fq"
  conda:
    "workflow/envs/NanoLyse.yaml"
  shell:
    "cat {input} | NanoLyse -r database/human_genome/GRCh38_latest_genomic.fna > {output}"

rule FilteredNanoPlot:
  input:
    "results/filtered_reads/{sample}/{sample}_filtered.fq"
  output:
    directory("results/nanoplot/nanoplot_filtered/{sample}/")
  conda:
    "workflow/envs/NanoPlot.yaml"
  shell:
    "NanoPlot -t 6 --fastq {input} -o {output}"

rule FilteredNanoQC:
  input:
    "results/filtered_reads/{sample}/{sample}_filtered.fq"
  output:
    directory("results/nanoqc/nanoqc_filtered/{sample}/")
  conda:
    "workflow/envs/NanoQC.yaml"
  shell:
     "nanoQC {input} -o {output}"

########################################################################################################################################################################################################################################################################################################################################
######################################################################    PART 2    ####################################################################################################################################################################################################################################################
########################################################################################################################################################################################################################################################################################################################################

rule Fastq_to_Fasta:
  input:
    "results/filtered_reads/{sample}/{sample}_filtered.fq"
  output:
    "results/filtered_reads/{sample}/{sample}_filtered.fasta"
  conda:
    "workflow/envs/seqtk.yaml"
  shell:
    "seqtk seq -A {input} > {output}"

rule MakeDirectories:
  run:
    shell("mkdir results/mmseq2/{sample}")
    shell("mkdir results/mmseq2/{sample}/species")
    shell("mkdir results/mmseq2/{sample}/amr")
    shell("mkdir results/output/{sample}")
    shell("mkdir results/output/{sample}/count_files")

rule Setup:
  run:
    import sys
    import subprocess
    import pkg_resources
    
    required  = {'xlsxwriter', 'openpyxl'} 
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing   = required - installed
    
    if missing:
        # implement pip as a subprocess:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])

rule Align_Species:
  input:
    "results/filtered_reads/{sample}/{sample}_filtered.fasta"
  output:
    "results/mmseq2/{sample}/species/aln{sample}.tsv"
  conda:
    "workflow/envs/mmseqs2.yaml"
  shell:
    "mmseqs easy-search {input} /mnt/studentfiles/2022/2022MBI_11/database/FDA/FDA_ARGOS.fasta {output} tmp --search-type 4 --alignment-mode 3  --min-seq-id 0.95 --threads 8" #min-seq-id aanpassen naar e value of andere waarde

rule Align_AMR:
  input:
    "results/filtered_reads/{sample}/{sample}_filtered.fasta"
  output:
    "results/mmseq2/{sample}/amr/aln{sample}.tsv"
  conda:
    "workflow/envs/mmseqs2.yaml"
  shell:
    "mmseqs easy-search {input} database/card/card_database_v3.2.0.fasta {output} tmp --search-type 4 --alignment-mode 3 --min-seq-id 0.9 --threads 8 --min-aln-len 200"

rule Accession_number_to_species_name:
  input:
    i1 = "results/mmseq2/{sample}/species/aln{sample}.tsv",
    i2 = "database/FDA/output_species_final_2words.tsv"
  output:
    "results/mmseq2/{sample}/species/acc_to_species_{sample}.tsv"
  shell:
    "python workflow/scripts/acc_to_species.py -i1 {input.i1} -i2 {input.i2} -o {output}"

rule Filter_species:
  input:
    "results/mmseq2/{sample}/species/acc_to_species_{sample}.tsv"
  output:
      "results/mmseq2/{sample}/species/clean_{sample}.tsv"
  shell:
    "python workflow/scripts/clean_species_file.py -i {input} -o {output}"

rule Count_species:
  input:
    "results/mmseq2/{sample}/species/clean_{sample}.tsv"
  output:
    "results/output/{sample}/count_files/species_count.xlsx"
  shell:
    "python workflow/scripts/species_count.py -i {input} -o {output}"

rule Clean_AMR_alignment_file:
  input:
    "results/mmseq2/{sample}/amr/aln{sample}.tsv"
  output:
    "results/mmseq2/{sample}/amr/clean_{sample}.tsv"
  shell:
    "python workflow/scripts/clean_amr2.py -i {input} -o {output}"

rule Count_amr:
  input:
    "results/mmseq2/{sample}/amr/clean_{sample}.tsv"
  output:
    "results/output/{sample}/count_files/amr_count.xlsx"
  shell:
    "python workflow/scripts/amr_count.py -i {input} -o {output}"

rule Combine_AMR_and_Species:
  input:
    input1 = "results/mmseq2/{sample}/species/clean_{sample}.tsv",
    input2 = "results/mmseq2/{sample}/amr/clean_{sample}.tsv"
  output:
    "results/mmseq2/{sample}/combined_{sample}.tsv"
  shell:
    "python workflow/scripts/combine_files.py -i1 {input.input1} -i2 {input.input2} -o {output}"

rule Count_AMR_species_match:
  input:
    "results/mmseq2/{sample}/combined_{sample}.tsv"
  output:
    "results/output/{sample}/count_files/count_match.xlsx"
  shell:
    "python workflow/scripts/counting_amr_species.py -i {input} -o {output}"

rule Create_output:
  input:
    i1 = "results/output/{sample}/count_files/species_count.xlsx",
    i2 = "results/output/{sample}/count_files/amr_count.xlsx",
    i3 = "results/output/{sample}/count_files/count_match.xlsx"
  output:
    "results/output/{sample}/results.xlsx"
  shell:
    "python workflow/scripts/combine_count_files.py -i1 {input.i1} -i2 {input.i2} -i3 {input.i3} -o {output}"