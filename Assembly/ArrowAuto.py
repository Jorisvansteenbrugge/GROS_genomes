#!/usr/bin/env python3

import logging
import argparse
from subprocess import check_call, CalledProcessError
from sys import exit
from os import mkdir, path


logger =logging.getLogger("Arrow Iterator")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

def get_args():
    p = argparse.ArgumentParser()
    p.add_argument("-g", dest='genome',help="Genome assembly in fasta format", required=True)
    p.add_argument("-m", dest='memory', help="The available memory to allocate in GigaByte, mainly for sorting bamfiles (m*t will be used)", required=True,type=int)
    p.add_argument("-t",dest="threads", help="CPU threads to use (default:4)", default = 4, type=int)
    p.add_argument("-pb", dest='pacbioreads', help="Raw pacbio reads in bam format. Multiple files may be provided in a space separated list.", required = True, nargs = '+')
    p.add_argument('-it', dest='iterations', help="Numer of iterations (default:3)",default=35,type=int)
    p.add_argument('-o', dest ='outdir', help ="output directory", required=True)
    return p.parse_args()


def check_deps():
    logger.debug("Checking dependencies")
    all_ins = True
    try:
        call = check_call("minimap2 -h 1> /dev/null", shell =True)
    except CalledProcessError as e:
        print(f"Please install minimap2 (retcode: {e.returncode})")

        all_ins = False
    try:
        call = check_call("which samtools  1> /dev/null", shell = True)
    except CalledProcessError as e:
        print(f"Please install samtools (retcode: {e.returncode})")
        all_ins = False
    try:
        call = check_call("pbindex -h > /dev/null", shell = True)
    except CalledProcessError as e:
        print(f"Please install pbbam (from bioconda)  (retcode: {e.returncode})")
        all_ins = False

    try:
        call = check_call("blasr -h > /dev/null", shell = True)
    except CalledProcessError as e:
        print("Please install blasr (from bioconda) (retcode: {e.returncode})")
        all_ins = False

    if not all_ins:
        exit()
    logger.debug("Dependencies satisfied")

def run(genome, args, roundnum):
    rundir = f"{args.outdir}/round{roundnum}/"
    mkdir(rundir)
    logger.info(f"Starting ROUND {roundnum}")

    # Map
    if args.threads >= 4:
        samthreads = 4
    else:
        samthreads = threads

    for idx, bam_reads in enumerate(args.pacbioreads):
        cmd_map = f"blasr {bam_reads} {genome} --out /tmp/bam.{idx}.bam --bam --bestn 10 --minMatch 12 --maxMatch 30 --nproc {args.threads} --minSubreadLength 50 --minAlnLength 50 --minPctSimilarity 70 --minPctAccuracy 70 --hitPolicy randombest --randomSeed 1"
        cmd_sort = f"samtools sort -@ {samthreads} -m {args.memory}G /tmp/bam.{idx}.bam -o /tmp/bam.{idx}_sorted.bam"


        if path.exists(f"/tmp/bam.{idx}_sorted.bam"):
            continue
        else:
            check_call(cmd_map,  shell = True)
            check_call(cmd_sort, shell = True)

    sorted_bams = " ".join([f"/tmp/bam.{idx}_sorted.bam" for idx in range(len(args.pacbioreads))])

    #Merge bam files
    cmd_merge = f"samtools merge /tmp/sorted_merged.bam {sorted_bams} -@ {samthreads} -f"
    cmd_pbindex = "cd /tmp/; pbindex sorted_merged.bam"

    check_call(cmd_merge, shell = True)
    check_call(cmd_pbindex, shell = True)


    #Index genome
    cmd_faindex = f"samtools faidx {genome}"
    check_call(cmd_faindex, shell = True)

    # Arrow
    cmd_arrow = f"arrow /tmp/sorted_merged.bam -j {args.threads} --referenceFilename {genome} -o {rundir}/arrow.{roundnum}.fasta -o {rundir}/arrow.{roundnum}.gff -o {rundir}/arrow.{roundnum}.fastq"
    check_call(cmd_arrow, shell = True)

    # Cleanup
    check_call(f"rm {sorted_bams}", shell = True)
    

    return f"{rundir}/arrow.{roundnum}.fasta"

if __name__ =="__main__":
    check_deps()

    args = get_args()
    genome = args.genome

    
    for i in range(args.iterations):
        genome = run(genome, args, i)
