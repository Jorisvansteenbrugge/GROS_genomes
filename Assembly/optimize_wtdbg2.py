#!/usr/bin/env python
import subprocess as subp
from os import path
import re
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reads", dest='reads',   help = 'Reads in fasta format (error correction already done by canu', required = True)
    parser.add_argument('--wd',    dest="wd",      help = "Working directory")
    parser.add_argument('-t',      dest='threads', help = 'Number of CPU threads to use')

    return parser.parse_args()



def optimize(arguments):
    """
    -L 3000 4000 5000 6000 7000
    -p 10 - 20
    -e 1 - 10
    """
    from itertools import product

    L = range(3000,8000,1000)
    p = range(15,21,1)
    e = range(2,7,1)

    combinations = product(L,p,e)
    base_cmd = "wtdbg2 -i {input} -o {wd}/{outprefix} -t {threads} -L {L} -p {p}  -e {e} 2> {wd}/{statsfile}.stdout "

    for comb in combinations:
        prefix = "Assembly_L{}p{}e{}".format(comb[0], comb[1], comb[2])

        cmd = base_cmd.format(input=arguments.reads,     outprefix=prefix,
                              wd=arguments.wd, statsfile=prefix,
                              threads=arguments.threads, L=comb[0],
                              p=comb[1],                 e=comb[2]
                              )

        if path.exists("{wd}/{statsfile}.stdout".format(wd=arguments.wd, statsfile=prefix)):
            continue
        subp.call(cmd, shell = True)

def get_stats(arguments):
    from glob import glob
    from os.path import basename, splitext

    outfile = open(arguments.wd + "/Summaryfile.csv", 'w')
    outfile.write("Run_name;GenomeSize;NContigs;Busco\n")

    for stdfile in glob(arguments.wd + "/*.stdout"):
        with open(stdfile) as stats_file:
            runname = splitext(basename(stdfile))[0]
            data = stats_file.read()
            matches = re.search(r"Estimated:\ TOT\ ([0-9]+),\ CNT\ ([0-9]+)", data)

            print(matches.group(1))
            print(matches.group(2))
            
            outfile.write(";".join([runname, matches.group(1), matches.group(2), ""])+'\n')


if __name__ == "__main__":
    arguments = get_args()
    optimize(arguments)
    get_stats(arguments)

