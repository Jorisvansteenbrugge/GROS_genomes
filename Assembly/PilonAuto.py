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
    p.add_argument("-pb", dest='pacbioread', help="Raw pacbio reads. Concatenate multiple samples before running", required = True)
    p.add_argument('-it', dest='iterations', help="Numer of iterations (default:5)",default=5,type=int)
    p.add_argument("--pilon", dest='pilonjar', help="Jar file containing the pilon program",required=True)
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
        call = check_call("java -h 2> /dev/null", shell = True)
    except CalledProcessError as e:
        print(f"Please install a java runtime environment (retcode: {e.returncode})")
        all_ins = False

    if not all_ins:
        exit()
    logger.debug("Dependencies satisfied")

def run(genome, reads, threads, mem, outdir, roundnum, pilonjar):
    rundir = f"{outdir}/round{roundnum}/"
    mkdir(rundir)
    logger.info(f"Starting ROUND {roundnum}")


    # Map
    if threads >= 4:
        samthreads = 4
    else:
        samthreads = threads
    cmd = f"minimap2 -ax map-pb -t {threads} -K 1000M {genome} {reads} | samtools view -hF 256 - | samtools sort -@ {samthreads} -m 10G -o {rundir}/aligned.bam; cd {rundir}; samtools index aligned.bam"
    logger.info("Aligning reads with minimap2")
    logger.debug(cmd)
    check_call(cmd, shell = True)

    logger.info("Running Pilon")
    # Pilon
    cmd = f"java -Xmx100G -jar {pilonjar} --genome {genome} --pacbio {rundir}/aligned.bam --changes --vcf --diploid --threads {threads} --output {rundir}/pilon_run{roundnum}"
    try:
        check_call(cmd, shell = True)
    except:
        pass

    return f"{rundir}/pilon_run{roundnum}.fasta"

if __name__ =="__main__":
    args = get_args()
    check_deps()

    genome = args.genome

    
    for i in range(args.iterations):
        genome = run(genome, args.pacbioread, args.threads, args.memory, args.outdir, i, args.pilonjar)
