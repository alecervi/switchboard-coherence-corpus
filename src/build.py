from operator import itemgetter
from itertools import groupby
from corpus.Switchboard.Switchboard import Switchboard
import argparse
import logging
import os
import json
import re

def group_turns(parsed_dialogue):
    """
    Returns dialogue grouped according to turn
    """
    return [list(g) for k, g in groupby(parsed_dialogue, itemgetter(3))]

def instatiate_grid(grid_id, corpus_dct):
    """
    Retrieves dialog from corpus
    """
    return corpus_dct[grid_id]

def load_corpus(corpus_path):
    """
    Load Switchboard Dialog Act corpus
    """
    corpus_loader = Switchboard(corpus_path)
    corpus_dct = corpus_loader.load_csv()
    # Group DAs according to speaker turns
    corpus_dct = {k: group_turns(v) for k,v in corpus_dct.items()}
    return corpus_dct

def load_coh_annotations(coh_anno_path, file_name = 'coh_annotations.json'):
    with open(coh_anno_path + '/' + file_name) as infile:
        loaded_infile = json.load(infile)
    return loaded_infile

def extract_text(candidate):
    return re.sub(' +', ' ', ''.join([i[1] for i in candidate]))

def format_text_speakers(context):
    return [{'speaker': turn[0][2], 'turn': re.sub(' +', ' ', ''.join(da[1] for da in turn))} for turn in context]

def augment(all_coh_annotations, swbdda_corpus_dct):
    for example_id, coh_annotations in all_coh_annotations.items():
        source_dialogue_id = coh_annotations['info']['dialog_id']
        source_dialogue = swbdda_corpus_dct[source_dialogue_id]
        candtype2text = {}

        # Extract candidates text
        for candidate in coh_annotations['info']['candidates_info']:
            if candidate['cand_type']=='original':
                original_idx = candidate['turn_idx']
                cand_txt = extract_text(source_dialogue[candidate['turn_idx']])

            elif candidate['cand_type']!='original':
                cand_source_dialogue = swbdda_corpus_dct[candidate['dialog_id']]
                cand_txt = extract_text(cand_source_dialogue[candidate['turn_idx']])
                            
            candtype2text[candidate['cand_type']] = cand_txt

        # Augment candidates with text
        for i, candidate in enumerate(all_coh_annotations[example_id]['candidates']):
            all_coh_annotations[example_id]['candidates'][i]['turn'] = candtype2text[candidate['cand_type']]
        
        # Augment with dialogue context
        all_coh_annotations[example_id]['context'] = format_text_speakers(source_dialogue[:original_idx])  

    return all_coh_annotations

def write_json(outpath, dct_to_write):
     with open(outpath + '/swbd_coh_corpus.json', 'w') as outfile:
        # Write entire dct as one json file
        to_write = json.dumps(dct_to_write)
        outfile.write(to_write)


def main(args):

    logging.basicConfig(
        level=(logging.DEBUG if args.verbose else logging.INFO),
        format='%(levelname)s %(message)s')

    # Load SWDB-DA
    logging.info(f'Switchboard Dialogue Act corpus path: {args.corpus_path}')
    logging.info(f'Loading Switchboard Dialogue Act corpus...')
    swbdda_corpus_dct = load_corpus(args.corpus_path)
    print('Size:', len(swbdda_corpus_dct))
    
    # Load SWBD-Coh src files 
    logging.info(f'SWBD-Coh annotations files path: {args.coh_anno_path}')
    logging.info(f'Loading coherence annotations...')
    coh_annotations = load_coh_annotations(args.coh_anno_path)

    # Augment models with text
    augmented_coh_annotations = augment(coh_annotations, swbdda_corpus_dct)

    # Write output files
    logging.info(f'Writing SWBD-Coh to {args.output_path} ...')
    write_json(args.output_path, augmented_coh_annotations)
    logging.info(f'Full SWBD-Coh corpus built')


def parse():
    parser = argparse.ArgumentParser(description='Corpus generator')
    parser.add_argument('-ca', '--check_annotations', action='store_true', help='Check annotated data')
    parser.add_argument('-c', '--corpus_path', default='../../../Datasets/Switchboard/data/switchboard1-release2/', help='Path to corpus')
    parser.add_argument('-s', '--coh_anno_path', default='../data', help='Path to SWBD-Coh coherence annotation file')
    parser.add_argument('-o', '--output_path', default='../data', help='Path where to save built corpus')
    parser.add_argument('-v', '--verbose', action='store_true', help='increase the verbosity level')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse()
    main(args)