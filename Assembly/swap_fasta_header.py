#!/usr/bin/env python3

import argparse
from Bio import SeqIO


def parse_arguments():
    parser = argparse.ArgumentParser(description="Swap fasta header name with a prefix and number them. Output is printed to stdout")

    parser.add_argument('prefix', metavar='PREFIX', help='the prefix in the fasta header contig/scaffold/chr/..')
    parser.add_argument('fasta', metavar='FASTA', help='Fasta to swap')


    return parser.parse_args()


args = parse_arguments()

count = 1
for record in SeqIO.parse(args.fasta, 'fasta'):
    print(f">{args.prefix}{count}")
    print(record.seq)

    count += 1
