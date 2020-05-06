import os


def make_length_dictionary():
    """
    This function makes a dictionary of all the genes that are present in the biomartfile. For every gene, the highest
    gene length that is present in the biomartfile is assigned.
    :return gene_length_dic: The dictionary with for every gene the belonging length.
    """
    gene_length_dic = {}
    with open("D:/Chantal/Data/mart_export.txt") as biomartfile:
        biomartfile.readline()
        for line in biomartfile:
            gene = line.split("\t")[2].rstrip("\n")
            length = line.split("\t")[1]
            if len(gene) > 0:
                if gene not in gene_length_dic:
                    gene_length_dic[gene] = length
                else:
                    if int(length) > int(gene_length_dic[gene]):
                        gene_length_dic[gene] = length
    return gene_length_dic


def make_gene_length_file(gene_length_dic):
    """
    :param gene_length_dic: The dictionary with for every gene the belonging length.
    This function loops through the file with the counts of the mutated genes. For every gene in this list, the length
    is assigned to it in this function. The count and the length are written to the file gene_count_length.txt.
    """
    if os.path.exists("D:/Chantal/Data/gene_counts_length.txt"):
        os.remove("D:/Chantal/Data/gene_counts_length.txt")
    gene_lengthfile = open("D:/Chantal/Data/gene_counts_length.txt", "a")
    gene_lengthfile.write("Gene\tCount\tLength\n")
    with open("D:/Chantal/Data/Counts_mutated_genes.txt") as countfile:
        countfile.readline()
        for line in countfile:
            gene = line.split("\t")[0]
            samples_mutated = line.split("\t")[1]
            if gene in gene_length_dic:
                gene_lengthfile.write(gene + "\t" + samples_mutated + "\t" + gene_length_dic[gene] + "\n")
    gene_lengthfile.close()


def main():
    gene_length_dic = make_length_dictionary()
    make_gene_length_file(gene_length_dic)


main()
