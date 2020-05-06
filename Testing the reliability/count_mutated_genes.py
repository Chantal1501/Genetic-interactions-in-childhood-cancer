import os


def get_genedict(file):
    """
    :param file: The file in which will be looked in how many samples a certain gene is mutated.
    This function loops through a mutation list file. Every line represents a gene and behind the gene is written an
    index of which samples this gene is mutated in. For every gene is looked how many indexes are behind the gene, or in
    other words in how many samples this gene is mutated. This is written to a dictionary.
    :return gene_dict: Dictionary with for every gene in how many different samples it is mutated.
    """
    gene_dict = {}
    with open(file) as genes_mutated:
        for line in genes_mutated:
            splitlist = line.split("\t")
            if len(splitlist) == 2 and line.split("\t")[0] != "samples":
                gene = line.split("\t")[0]
                mutated_count = len(line.split("\t")[1].rstrip("\n").split(","))
                gene_dict[gene] = mutated_count
    return gene_dict


def update_dict(gene_dict_total, gene_dict_dataset, listposition):
    """
    :param gene_dict_total: The dictionary with in it all the genes that are mutated in CBTTC and in how many samples
    these genes are mutated. These numbers will be updated for the other datasets as well.
    :param gene_dict_dataset: A dicitionary with in it for every gene in the dataset in how many samples this gene is
    mutated.
    :param listposition: The position of the specific dataset in the list with the amount of mutated samples.
    This function counts for every gene that is present in the CBTTC dataset in how many samples this gene is mutated
    in TARGET and DKFZ.
    :return gene_dict_total: The dictionary with in it all the genes that are mutated in CBTTC and in how many samples
    these genes are mutated. These numbers are updated for the another dataset in this function.
    """
    for gene in gene_dict_total:
        if gene in gene_dict_dataset:
            gene_dict_total[gene][listposition] = gene_dict_dataset[gene]
    return gene_dict_total


def get_genelist(file):
    """
    :param file: The file with the smgs of a certain dataset.
    This function makes a list of all the significantly mutated genes of a specific dataset.
    :return smgs: List with in it all the smgs of this dataset.
    """
    smgs = []
    with open(file) as smg_file:
        for line in smg_file:
            gene = line.rstrip("\n")
            if gene != "GENE":
                smgs.append(gene)
    return smgs


def in_genelist(gene, genelist):
    """
    :param gene: A gene for which will be checked whether it is present in a certain genelist or not.
    :param genelist: The list in which is checked if a certain gene is present.
    This function checks whether a certain gene is present in a genelist.
    :return: Yes if it is present in the genelist and no if it is not present.
    """
    if gene in genelist:
        return "Yes"
    else:
        return "No"


def main():
    if os.path.exists("D:/Chantal/Data/Counts_mutated_genes.txt"):
        os.remove("D:/Chantal/Data/Counts_mutated_genes.txt")
    gene_dict_cbttc = get_genedict("D:/Chantal/Data/Mutationlists/PAN/PAN_smut_list.txt")
    gene_dict_dkfz = get_genedict("D:/Chantal/Data/PAN cancer mutlists/DKFZ/PAN/PAN_smut_list.txt")
    gene_dict_target = get_genedict("D:/Chantal/Data/PAN cancer mutlists/TARGET/PAN/PAN_smut_list.txt")
    gene_dict_total = {}
    for gene in gene_dict_cbttc:
        gene_dict_total[gene] = [gene_dict_cbttc[gene], 0, 0]
    gene_dict_total = update_dict(gene_dict_total, gene_dict_dkfz, 1)
    gene_dict_total = update_dict(gene_dict_total, gene_dict_target, 2)
    sorted_dic = sorted(gene_dict_total.items(), key=lambda x: x[1], reverse=True)
    smg_dkfz = get_genelist("D:/Chantal/Data/DkfzSMGs.txt")
    smg_target = get_genelist("D:/Chantal/Data/StJudeSMGs.txt")
    mutated_genes_file = open("D:/Chantal/Data/Counts_mutated_genes.txt", "a")
    mutated_genes_file.write("Gene\tCount\tSMG DKFZ\tCount DKFZ\tSMG TARGET\tCount TARGET\n")
    for mutated_gene in sorted_dic:
        dkfz = in_genelist(mutated_gene[0], smg_dkfz)
        target = in_genelist(mutated_gene[0], smg_target)
        mutated_genes_file.write(mutated_gene[0] + "\t" + str(mutated_gene[1][0]) + "/650 ("
                                 + str(round(((mutated_gene[1][0] / 650) * 100), 1)) + "%)\t" + dkfz + "\t" +
                                 str(mutated_gene[1][1]) + "/843 (" + str(round(((mutated_gene[1][1] / 843) * 100), 1))
                                 + "%)\t" + target + "\t" + str(mutated_gene[1][2]) + "/1632 (" +
                                 str(round(((mutated_gene[1][2] / 1632) * 100), 1)) + "%)\n")
    mutated_genes_file.close()


main()
