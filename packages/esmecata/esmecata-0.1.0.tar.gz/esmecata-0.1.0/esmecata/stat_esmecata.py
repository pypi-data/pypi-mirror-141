import csv
import pandas as pd
import os

proteome_folder = '0_proteomes/result'
proteome_numbers = {}
for folder in os.listdir(proteome_folder):
    number_proteome = len([proteome for proteome in os.listdir(proteome_folder+'/'+folder)])
    proteome_numbers[folder] = number_proteome

clustering_folder = '1_clustering/reference_proteins'
clustering_numbers = {}
for clustering_file in os.listdir(clustering_folder):
    num_lines = sum(1 for line in open(clustering_folder+'/'+clustering_file))
    clustering_numbers[clustering_file.replace('.tsv', '')] = num_lines

annotaiton_folder = '2_annotation/annotation_reference'
annotation_numbers = {}
for infile in os.listdir(annotaiton_folder):
    if '.tsv' in infile:
        df = pd.read_csv(annotaiton_folder+'/'+infile, sep='\t')
        go_number = set([go for gos in df['GO'] if isinstance(gos, str) for go in gos.split(',') ])
        ec_number = set([ec for ecs in df['EC'] if isinstance(ecs, str) for ec in ecs.split(',') ])
        annotation_numbers[infile.replace('.tsv','')] = (len(go_number), len(ec_number))

with open('esmecata_stats.tsv', 'w') as output_file:
    csvwriter = csv.writer(output_file, delimiter='\t')
    csvwriter.writerow(['cluster', 'Proteomes', 'Proteins', 'GOs', 'ECs'])
    for cluster in proteome_numbers:
        csvwriter.writerow([cluster, proteome_numbers[cluster], clustering_numbers[cluster], annotation_numbers[cluster][0], annotation_numbers[cluster][1]])
    
