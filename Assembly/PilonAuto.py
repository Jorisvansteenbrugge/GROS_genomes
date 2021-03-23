#!/usr/bin/env python3

import logging
import argparse
from subprocess import check_call, CalledProcessError
from sys import exit
from os import mkdir


logger =logging.getLogger("Pilon Iterator")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

def get_args():
    p = argparse.ArgumentParser()
    p.add_argument("-g", dest='genome',help="Genome assembly in fasta format", required=True)
    p.add_argument("-m", dest='memory', help="The available memory to allocate in GigaByte. Pilon prefers 1G per megabase in the assembly", required=True,type=int)
    p.add_argument("-t",dest="threads", help="CPU threads to use (default:4)", default = 4, type=int)
    p.add_argument("-1", dest='read_left', help="Raw pacbio reads. Concatenate multiple samples before running", required = True, nargs='+')
    p.add_argument("-2", dest='read_right', help="Raw pacbio reads. Concatenate multiple samples before running", required = True, nargs='+')
    p.add_argument('-it', dest='iterations', help="Numer of iterations (default:5)",default=5,type=int)
    p.add_argument("--pilon", dest='pilonjar', help="Jar file containing the pilon program",required=True)
    p.add_argument('-o', dest ='outdir', help ="output directory", required=True)
    return p.parse_args()


def check_deps():
    logger.debug("Checking dependencies")
    all_ins = True
    # try:
    #     call = check_call("minimap2 -h 1> /dev/null", shell =True)
    # except CalledProcessError as e:
    #     print(f"Please install minimap2 (retcode: {e.returncode})")

    #     all_ins = False
    try:
        call = check_call("which samtools  1> /dev/null", shell = True)
    except CalledProcessError as e:
        print(f"Please install samtools (retcode: {e.returncode})")
        all_ins = False
    try:
        call = check_call("java -h 2> /dev/null", shell = True)
    except CalledProcessError as e:
        print(f"Please install a java runtime environment (retcode: {e.returncode})")
        all_ins = False

    if not all_ins:
        exit()
    logger.debug("Dependencies satisfied")

def run(genome, read_left, read_right, threads, mem, outdir, roundnum, pilonjar):
    rundir = f"{outdir}/round{roundnum}/"
    mkdir(rundir)
    logger.info(f"Starting ROUND {roundnum}")

    samthreads = 2

    idx_cmd = f"/home/joris/tools/bwa-mem2-2.0_x64-linux/bwa-mem2 index -p /tmp/genome_idx {genome}"
    check_call(idx_cmd, shell=True)


    map_cmd = f"/home/joris/tools/bwa-mem2-2.0_x64-linux/bwa-mem2 mem -t {threads} /tmp/genome_idx {read_left[0]} {read_right[0]} | samtools sort -m 30G -o {rundir}/Lane1.bam"
    logger.info("Aligning reads with bwa")
    check_call(map_cmd, shell = True)


    idx_cmd = f'samtools index {rundir}/Lane1.bam'
    check_call(idx_cmd, shell = True)

    #map_cmd = f"/home/joris/tools/bwa-mem2-2.0_x64-linux/bwa-mem2 mem -t {threads} /tmp/genome_idx {read_left[1]} {read_right[1]} | samtools sort -m 30G -o {rundir}/Lane2.bam"
    #logger.info("Aligning reads with bwa")
    
    #check_call(map_cmd, shell = True)

    logger.info("Running Pilon")
    # Pilon
    cmd = f"java -Xmx100G -jar {pilonjar} --genome {genome} --frags {rundir}/Lane1.bam  --changes --vcf --diploid --threads {threads} --output {rundir}/pilon_run{roundnum}"
    try:
        check_call(cmd, shell = True)
    except:
        pass

    cleanup_cmd = f'rm {rundir}/Lane1.bam '
    check_call(cleanup_cmd, shell=True)

    return f"{rundir}/pilon_run{roundnum}.fasta"

if __name__ =="__main__":
    args = get_args()
    check_deps()

    genome = args.genome

    
    for i in range(args.iterations):
        genome = run(genome, args.read_left, args.read_right, args.threads, args.memory, args.outdir, i, args.pilonjar)
