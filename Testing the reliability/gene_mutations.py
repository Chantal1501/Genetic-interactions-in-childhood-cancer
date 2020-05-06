import os


def get_mutations(gene, file):
    """
    :param gene: For which gene is looked what different mutations are available in the maffiles.
    :param file: Through which maffile the function will loop.
    This function loops through a maffile to see which mutations of a specified gene are available. Those mutations
    are written to the list mutations. Only mutations that are of a mutation type present in the list mutationlist
    will be taken into account.
    :return mutations: List with in it the mutations of a certain gene present in this maffile.
    """
    mutations = []
    mutationlist = ["Frame_Shift_Del", "Frame_Shift_Ins", "In_Frame_Del", "In_Frame_Ins", "Missense_Mutation",
                    "Nonsense_Mutation", "Nonstop_Mutation"]
    filename = "D:/Chantal/Data/Maffiles/" + file
    with open(filename) as maffile:
        maffile.readline()
        for line in maffile:
            genename = line.split("\t")[0]
            mutationtype = line.split("\t")[8]
            if genename == gene and mutationtype in mutationlist:
                mutation = (line.split("\t")[35])
                mutations.append(mutation)
    return mutations


def update_mutation_dic(mutation_dictionary, mutations):
    """
    :param mutation_dictionary: Dictionary with in it all the mutations of a certain gene and a count how often this
    mutation occurs.
    :param mutations: List with in it the mutations of a certain gene present in this maffile.
    This function updates the mutation_dictionary with the list of mutations of a certain maffile. 
    """
    for mutation in mutations:
        if mutation in mutation_dictionary:
            mutation_dictionary[mutation] += 1
        else:
            mutation_dictionary[mutation] = 1


def main():
    if os.path.exists("D:/Chantal/Data/mutation_counts.txt"):
        os.remove("D:/Chantal/Data/mutation_counts.txt")
    mutation_dictionary = {}
    gene = input("For which gene do you want to know the mutations? ")
    maffiles = os.listdir("D:/Chantal/Data/Maffiles")
    for file in maffiles:
        mutations = get_mutations(gene.upper(), file)
        print(mutations)
        update_mutation_dic(mutation_dictionary, mutations)
    print(mutation_dictionary)
    sorted_dic = sorted(mutation_dictionary.items(), key=lambda x: x[1], reverse=True)
    mutation_counts_file = open("D:/Chantal/Data/mutation_counts.txt", "a")
    for mutation in sorted_dic:
        mutation_counts_file.write(mutation[0] + ": " + str(mutation[1]) + "\n")
    mutation_counts_file.close()


main()
