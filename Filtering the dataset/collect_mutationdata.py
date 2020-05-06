import os

def make_genelist():
    """
    This function opens the file GeneBaseGenes.txt. This is a file that includes all of the protien coding genes of the
    human genome. These proteins are filtered from the file and are put in the genelist. This genelist is returned
    by this function.
    :return genelist: List with in it all of the protein coding genes of the human genome.
    """
    genelist = []
    with open("D:/Chantal/Data/GeneBaseGenes.txt") as genefile:
        for line in genefile:
            if line.split("\t")[0] != "EntrezID":
                gene = line.split("\t")[1].rstrip("\n")
                genelist.append(gene)
    return genelist

def main():
    """
    This script collects all of the interesting mutations that are available in the file merged_maffiles.txt.
    The script takes the frame shift deletions/insertions, in frame insertions/deletions and the
    missense/nonsense/nonstop mutations. It writes it to the file mutation_file.txt. It takes also the silent mutations
    and writes it to the file mutation_file_with_silent.txt. It writes the filename, the cancertype and the gene name to
    both of the files. The script takes only the mutations of genes that are in the genelist. This is a list of all
    the protein coding genes in the dataset.
    """
    if os.path.exists("D:/Chantal/Data/mutation_file.txt"):
        os.remove("D:/Chantal/Data/mutation_file.txt")
    if os.path.exists("D:/Chantal/Data/mutation_file_with_silent.txt"):
        os.remove("D:/Chantal/Data/mutation_file_with_silent.txt")
    genelist = make_genelist()
    mutationlist = ["Frame_Shift_Del", "Frame_Shift_Ins", "In_Frame_Del", "In_Frame_Ins", "Missense_Mutation",
                    "Nonsense_Mutation", "Nonstop_Mutation", "Silent"]
    mutationlist_extra = ["Silent"]
    mutationfile = open("D:/Chantal/Data/mutation_file.txt", "a")
    mutationfilesilent = open("D:/Chantal/Data/mutation_file_with_silent.txt", "a")
    with open("D:/Chantal/Data/merged_maffiles.txt") as mergedfile:
        for line in mergedfile:
            list = line.split("\t")
            if(list[10]) in mutationlist and list[5] in genelist:
                mutationfilesilent.write(list[1] + "\t" + list[2] + "\t" + list[3] + "\t" + list[4] + "\t" + list[5] + "\n")
                if list[10] not in mutationlist_extra:
                    mutationfile.write(list[1] + "\t" + list[2] + "\t" + list[3] + "\t" + list[4] + "\t" + list[5] + "\n")
    mutationfile.close()
    mutationfilesilent.close()
main()
