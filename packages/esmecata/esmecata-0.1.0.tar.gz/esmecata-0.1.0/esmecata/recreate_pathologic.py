import csv
import os
from esmecata.annotation import create_pathologic

annotated_protein_to_keeps = {}

output = 'pathologic'
if not os.path.exists(output):
    os.mkdir(output)
for annot_file in os.listdir('2_annotaiton/annotation_reference'):
    with open('2_annotaiton/annotation_reference/'+annot_file) as input_file:
        csvreader = csv.reader(input_file, delimiter='\t')
        next(csvreader)
        for line in csvreader:
            protein_id = line[0]
            protein_name = line[1]
            gene_name = line[2]
            gos = [go for go in line[3].split(',') if go != '']
            ecs = [ec for ec in line[4].split(',') if ec != '']
            annotated_protein_to_keeps[protein_id] = [protein_name, gos, ecs, gene_name]

    if not os.path.exists(output+'/'+annot_file.replace('.tsv', '.pf')):
        base_filename = os.path.splitext(annot_file)[0]
        if not os.path.exists(output+'/'+base_filename):
            os.mkdir(output+'/'+base_filename)
        create_pathologic(base_filename, annotated_protein_to_keeps, output+'/'+base_filename+'/'+annot_file.replace('.tsv', '.pf'))