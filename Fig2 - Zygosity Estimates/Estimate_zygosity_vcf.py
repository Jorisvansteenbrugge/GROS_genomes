from sys import argv


hom_counts = 0
het_counts = 0
o_counts   = 0

with open(argv[1]) as vcf_file:
    for line in vcf_file:
        if line.startswith('#'):
            continue

        if "1/1" in line:
            hom_counts+=1

        elif "0/0" in line:
            hom_counts +=1
        elif "0/1" in line or "1/0" in line or "./1" in line or "1/."  in line:
            het_counts +=1


print(f"Hom counts {hom_counts}")
print(f"Het counts {het_counts}")
print(f"Other counts {o_counts}")

print(f"Total counts{(hom_counts+het_counts+o_counts)}")