import csv
import gzip
import json
import math
import os
import pandas as pd
import random
import requests
import shutil
import sys
import time

from collections import OrderedDict

from Bio import __version__ as biopython_version
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from ete3 import __version__ as ete3_version
from ete3 import NCBITaxa, is_taxadb_up_to_date

from SPARQLWrapper import __version__ as sparqlwrapper_version

from esmecata.utils import get_rest_uniprot_release, get_sparql_uniprot_release, is_valid_file, is_valid_dir, send_uniprot_sparql_query
from esmecata import __version__ as esmecata_version

REQUESTS_HEADERS = {'User-Agent': 'EsMeCaTa proteomes v' + esmecata_version + ', request by requests package v' + requests.__version__ }


def associate_taxon_to_taxon_id(taxonomies, ncbi):
    tax_id_names = {}
    clusters_dicts = {}
    json_cluster_taxons = {}

    if taxonomies == {}:
        print('Empty taxonomy dictionary.')
        return

    # For each taxonomy find the taxonomy ID corresponding to each taxon.
    for cluster in taxonomies:
        if isinstance(taxonomies[cluster], str):
            taxons = [taxon for taxon in taxonomies[cluster].split(';')]
            names = ncbi.get_name_translator(taxons)
            taxon_ids = OrderedDict()
            for taxon in taxons:
                taxon_translations = ncbi.get_name_translator([taxon])
                if taxon_translations == {}:
                    print('For {0}, no taxon ID has been found associated to the taxon "{1}" in the NCBI taxonomy of ete3.'.format(cluster, taxon))
                    taxon_translations = {taxon: ['not_found']}
                taxon_ids.update(taxon_translations)
            invert_names = {v: k for k, vs in names.items() for v in vs }
            tax_id_names.update(invert_names)
            clusters_dicts[cluster] = [names[tax_name] for tax_name in taxonomies[cluster].split(';') if tax_name in names]
            json_cluster_taxons[cluster] = taxon_ids

    return tax_id_names, json_cluster_taxons

def filter_taxon(json_cluster_taxons, ncbi):
    # If there is multiple taxon ID for a taxon, use the taxonomy to find the most relevant taxon.
    # The most relevant taxon is the one with the most overlapping lineage with the taxonomy.
    taxon_to_modify = {}

    for cluster in json_cluster_taxons:
        cluster_taxons = list(json_cluster_taxons[cluster].values())

        for index, taxon in enumerate(json_cluster_taxons[cluster]):
            taxon_ids = json_cluster_taxons[cluster][taxon]
            # If a taxon name is associated to more than one taxon ID, search for the one matching with the other taxon in the taxonomy.
            if len(taxon_ids) > 1:
                taxon_shared_ids = {}
                for taxon_id in taxon_ids:
                    # Extract the other taxon present in the taxonomy.
                    data_lineage = [tax_id for tax_id_lists in cluster_taxons[0:index] for tax_id in tax_id_lists]
                    # Extract the known taxonomy corresponding to one of the taxon ID.
                    lineage = ncbi.get_lineage(taxon_id)
                    # Computes the shared taxon ID between the known taxonomy and the taxonomy associated to the taxon.
                    nb_shared_ids = len(set(data_lineage).intersection(set(lineage)))
                    taxon_shared_ids[taxon_id] = nb_shared_ids

                # If there is no match in the taxonomy for all the multiple taxon ID, it is not possible to decipher, stop esmecata.
                if all(shared_id==0 for shared_id in taxon_shared_ids.values()):
                    taxids = ','.join([str(taxid) for taxid in list(taxon_shared_ids.keys())])
                    print('It is not possible to find the taxon ID for the taxon named "{0}" (associated to "{1}") as there is multiple taxID possible ({2}), please add taxonomy to help finding the correct one.'.format(taxon, cluster, taxids))
                    sys.exit()
                # If there is some matches, take the taxon ID with the most match and it will be the "correct one".
                else:
                    previous_nb_shared_ids = 0
                    for taxon_id in taxon_shared_ids:
                        if taxon_shared_ids[taxon_id] > previous_nb_shared_ids:
                            relevant_taxon = taxon_id
                            taxon_to_modify[cluster] = {}
                            taxon_to_modify[cluster][taxon] = [relevant_taxon]
                        previous_nb_shared_ids = nb_shared_ids

    for cluster in taxon_to_modify:
        for taxon in taxon_to_modify[cluster]:
            json_cluster_taxons[cluster][taxon] = taxon_to_modify[cluster][taxon]

    return json_cluster_taxons

def filter_rank_limit(json_cluster_taxons, ncbi, rank_limit):
    """
    Using teh rank_limit specificied, remove the taxon associated ot this rank.
    For example, if rank_limit == 'superkingdom', Bacteria will be removed.
    """
    # Rank level from Supplementary Table S3 of https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7408187/
    rank_level = {'superkingdom': 1, 'kingdom': 2, 'subkingdom': 3, 'superphylum': 4,
                    'phylum': 5, 'subphylum': 6, 'infraphylum': 7, 'superclass': 8,
                    'class': 9, 'subclass': 10, 'infraclass': 11, 'cohort': 12, 'subcohort': 13,
                    'superorder': 14, 'order': 15, 'suborder': 16, 'infraorder': 17, 'parvorder': 18,
                    'superfamily': 19, 'family': 20, 'subfamily': 21, 'tribe': 22, 'subtribe': 23,
                    'genus': 24, 'subgenus': 25, 'section': 26, 'subsection': 27, 'series': 28,
                    'subseries': 29, 'species group': 30, 'species subgroup': 31, 'species': 32,
                    'forma specialis': 33, 'subspecies': 34, 'varietas': 35, 'subvariety': 36,
                    'forma': 37, 'serogroup': 38, 'serotype': 39, 'strain': 40, 'isolate': 41}
    unclassified_rank = ['unclassified '+rank for rank in rank_level]
    non_hierarchical_ranks = ['clade', 'environmental samples', 'incertae sedis', 'no rank'] + unclassified_rank

    rank_limit_level = rank_level[rank_limit]
    rank_to_keeps = [rank for rank in rank_level if rank_level[rank] > rank_limit_level]

    for cluster in json_cluster_taxons:
        cluster_taxons = json_cluster_taxons[cluster]
        tax_keep = []
        tax_ranks = {}
        tax_names = {}
        tax_rank_position = {}
        tax_ids = []
        for index, tax_name in enumerate(cluster_taxons):
            tax_id = cluster_taxons[tax_name][0]
            tax_ids.append(tax_id)
            if tax_id != 'not_found':
                tax_rank = ncbi.get_rank([tax_id])[tax_id]
                tax_rank_position[tax_rank] = index
                if tax_rank in rank_to_keeps:
                    tax_ranks[tax_rank] = tax_id
                tax_names[tax_id] = tax_name
                # If the rank is below the rank to remove keep it.
                if tax_rank in rank_to_keeps:
                    tax_keep.append(True)
                elif tax_rank in non_hierarchical_ranks:
                    # If a nonhierarchical rank is below a rank that has been checked as being below the rank to remove, keep it.
                    if any(tax_keep):
                        tax_keep.append(True)
                    # If not remove it.
                    else:
                        tax_keep.append(False)
                else:
                    tax_keep.append(False)
            else:
                tax_keep.append(False)

        # If the rank to remove is in the tax_ranks, keep all the rank below this rank.
        if rank_limit in tax_ranks:
            tax_rank_max_index = tax_rank_position[rank_limit]
            keep_tax_ids = [tax_id[0] for tax_name, tax_id in list(cluster_taxons.items())[tax_rank_max_index+1:]]
        # If not find all the rank below this rank (by using rank_level and rank_to_keeps) in the list and keep them.
        # Use the tax_keep to keep non_hierarchical_ranks below the rank to remove.
        # But they need to be below a hierarchical rank that has been checked as being below the rank to remove.
        else:
            keep_tax_ids = [tax_ids[tax_index] for tax_index, bool_choice in enumerate(tax_keep) if bool_choice is True]

        tax_ids_wo_not_found = [tax_id for tax_id in tax_ids if tax_id != 'not_found']
        tax_id_to_deletes = set(tax_ids_wo_not_found) - set(keep_tax_ids)

        # Delete the remvoed rank and all its superior.
        for tax_id in tax_id_to_deletes:
            tax_name = tax_names[tax_id]
            del json_cluster_taxons[cluster][tax_name]

    return json_cluster_taxons

from ete3 import NCBITaxa
ncbi = NCBITaxa()
taxonomies = {}
taxonomies['clsuter_1']='Bacteria;Cloacimonetes;Cloacimonadia;Cloacimonadales;Cloacimonadaceae;W5;unknown species'
taxonomies['alveolate']='cellular organisms;Eukaryota;Sar;Alveolata;Colponemida;Acavomonidia;Acavomonas'
tax_id_names, json_cluster_taxons = associate_taxon_to_taxon_id(taxonomies, ncbi)

json_cluster_taxons = filter_taxon(json_cluster_taxons, ncbi)
json_cluster_taxons = filter_rank_limit(json_cluster_taxons, ncbi, 'family')
print(json_cluster_taxons)