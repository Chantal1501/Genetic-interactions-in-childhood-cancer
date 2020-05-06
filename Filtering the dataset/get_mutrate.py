import os


def get_mutationdictionary(mutfile, patientfile_boolean):
    """
    :param mutfile: The file with all the mutations of the dataset
    :param patientfile_boolean: Whether the patientfile must be opened or not to obtain the cancer type.
    This function makes a dictionary. The keys in this dictionary are the different filenames. The values of these keys
    are lists with 8 zeros in it and the cancer type. The zeros represent the counts of the patients, frameshift
    deletions, frameshift insertions, inframe deletions, inframe insertions, missense mutations, nonsense mutations,
    nonstop mutations
    :return patients: List with in it all the filenames from all mutation lines (so the same patient could occur more
    than once in this list)
    :return patientdict: Dictionary with in it the values of the mutations. In this function all these values are still
    zero.
    """
    patients = []
    patientdict = {}
    with open(mutfile) as mutationfile:
        for x in mutationfile:
            patient = x.split("\t")[0]
            if patient != "sampleID":
                patients.append(patient)
    for filename in set(patients):
        patientdict[filename] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if patientfile_boolean:
        patientfile = open("D:/Chantal/Data/patientfiles.txt", "r")
        for line in patientfile:
            abbreviation = line.split("\t")[5].rstrip("\n")
            patientdict[line.split("\t")[1]].append(abbreviation)
        patientfile.close()
    else:
        with open(mutfile) as mutationfile:
            mutationfile.readline()
            for line in mutationfile:
                patient = line.split("\t")[0]
                if len(patientdict[patient]) == 10:
                    ctype = line.split("\t")[4].rstrip("\n")
                    patientdict[patient].append(ctype)
    return patients, patientdict


def count_patient(patientdict, mutfile, mutfile_silent):
    """
    :param patientdict: Dictionary with in it the values of the mutations and how often a patient occurs in the dataset
    :param mutfile: The file with all the mutations of the dataset
    :param mutfile_silent: The file with all the mutations of the dataset inclusive the silent mutations.
    This function counts how often a certain patient is available in the dataset. This value is assigned to the patient
    in a dictionary.
    :return patientdict: Dictionary with in it the values of how often a certain patient is present in the dataset.
    It also contains information about how often a certain mutations occurs at a certain patient. But in this function
    these values are still zero.
    """
    if mutfile != False:
        with open(mutfile) as mutationfile:
            for x in mutationfile:
                filename = (x.split("\t")[0])
                patientdict[filename][1] += 1
    with open(mutfile_silent) as mutationfile_silent:
        for x in mutationfile_silent:
            filename = (x.split("\t")[0])
            if filename != "sampleID":
                patientdict[filename][0] += 1
    return patientdict


def count_mutationtype_patient(patientdict):
    """
    :param patientdict: Dictionary with in it the values of how often a certain patient is present in the dataset and
    how often a certain mutation occurs at this patient.
    This function counts how often a certain mutation type occurs in a certain patient. The function changes the values
    of the patientdict.
    """
    with open("D:/Chantal/Data/merged_mutation_file_silent.txt") as mergedfile:
        for line in mergedfile:
            filename = (line.split("\t")[1])
            mutationtype = (line.split("\t")[10])
            if mutationtype == "Silent":
                patientdict[filename][2] += 1
            if mutationtype == "Frame_Shift_Del":
                patientdict[filename][3] += 1
            if mutationtype == "Frame_Shift_Ins":
                patientdict[filename][4] += 1
            if mutationtype == "In_Frame_Del":
                patientdict[filename][5] += 1
            if mutationtype == "In_Frame_Ins":
                patientdict[filename][6] += 1
            if mutationtype == "Missense_Mutation":
                patientdict[filename][7] += 1
            if mutationtype == "Nonsense_Mutation":
                patientdict[filename][8] += 1
            if mutationtype == "Nonstop_Mutation":
                patientdict[filename][9] += 1


def get_files_most_mutations(patientdict, mutrates_file, mutrates_file_silent):
    """
    :param patientdict: Dictionary with in it the values of how often a certain patient is present in the dataset and
    how often a certain mutation occurs at this patient.
    :param mutrates_file: The mutation rates file to write how many mutations are present in  a certain sample.
    :param mutrates_file_silent: The mutation rates file to write how many mutations are present in a certain sample
    including the silent mutations.
    This function prints how often a certain patient occurs in the dataset and how many of each mutation type this
    patient has. It is printed in a descending order.
    :return:
    """
    if mutrates_file != False:
        if os.path.exists(mutrates_file):
            os.remove(mutrates_file)
        mutationratefile = open(mutrates_file, "a")
        mutationratefile.write("sampleID" + "\t" + "ct" + "\t" + "mutcount" + "\n")
        for key, value in sorted(patientdict.items(), key=lambda item:item[1], reverse = True):
            mutationratefile.write(key + "\t" + value[10] + "\t" + str(value[1]) + "\n")
        mutationratefile.close()
    if os.path.exists(mutrates_file_silent):
        os.remove(mutrates_file_silent)
    mutationratefile_silent = open(mutrates_file_silent, "a")
    mutationratefile_silent.write("sampleID" + "\t" + "ct" + "\t" + "mutcount" + "\n")
    for key, value in sorted(patientdict.items(), key=lambda item:item[1], reverse = True):
        mutationratefile_silent.write(key + "\t" + value[10] + "\t" + str(value[0]) + "\n")
    mutationratefile_silent.close()


def count_genes(patients, mutationfile, mutationfile_silent, patientdict):
    """
    :param patients: From which patients there are mutations available in the mutationfile
    :param mutationfile: File with in it all the coding mutations that are present in the maffiles
    :param mutationfile_silent: File with in it all the mutations that are interesting and present in the maffiles
    :param patientdict: Dictionary with after each patient the number of mutations etc.
    This function counts for every patient how many different genes there are mutated. This is done by making a list
    with all of the unique genes per patient. These lists are put in the dictionary patientdict. From these list a len
    is taken and the len of each unique gene list is written to a file together with the biospecimen identifier and
    the cancertype.
    """
    if os.path.exists("D:/Chantal/Data/gene_counts.txt"):
        os.remove("D:/Chantal/Data/gene_counts.txt")
    if os.path.exists("D:/Chantal/Data/gene_counts_silent.txt"):
        os.remove("D:/Chantal/Data/gene_counts_silent.txt")
    gen_ratefile = open("D:/Chantal/Data/gene_counts.txt", "a")
    gen_ratefile_silent = open("D:/Chantal/Data/gene_counts_silent.txt", "a")
    gen_ratefile.write("sampleID" + "\t" + "ct" + "\t" + "genecount" + "\n")
    gen_ratefile_silent.write("sampleID" + "\t" + "ct" + "\t" + "genecount" + "\n")
    genedict = {}
    genedict_silent = {}
    for filename in set(patients):
        genedict[filename] = []
        genedict_silent[filename] = []
    mutationfile.seek(0)
    mutationfile_silent.seek(0)
    print("Count genes")
    genedict = loop_through_mutationfile(mutationfile, genedict)
    print("Count genes including silent")
    genedict_silent = loop_through_mutationfile(mutationfile_silent, genedict_silent)
    print("Make file gene counts")
    for x in genedict:
        gen_ratefile.write(x + "\t" + patientdict[x][10] + "\t" + str(len(genedict[x])) + "\n")
    print("Make file gene counts including silent")
    for x in genedict_silent:
        gen_ratefile_silent.write(x + "\t" + patientdict[x][10] + "\t" + str(len(genedict_silent[x])) + "\n")
    gen_ratefile.close()
    gen_ratefile_silent.close()


def loop_through_mutationfile(mutationfile, genedict):
    """
    :param mutationfile: The file with in it all the mutations in the dataset. That could be a file including all the
    noncoding mutations or excluding these mutations.
    :param genedict: A dictionary that starts with an empty list for every biospecimen identifier. In this list all of
    the unique genes of this sample are added.
    This function makes a list with unique genes for every sample. This is done by filling the genedict dictionary.
    In this dictionary at first every biospecimen identifier has a empty list assigned. This list is filled with
    unique genes for this sample.
    :return genedict: A dictionary with for every biospecimen a list with the unique genes in which this sample has
    mutations.
    """
    for line in mutationfile:
        participant = line.split("\t")[0]
        gene = line.split("\t")[4].rstrip("\n")
        if gene not in genedict[participant]:
            genedict[participant].append(gene)
    return genedict


def main():
    mutationfile = "D:/Chantal/Data/mutation_file.txt"
    mutationfile_silent = "D:/Chantal/Data/mutation_file_with_silent.txt"
    patients, patientdict = get_mutationdictionary(mutationfile, True)
    patientdict = count_patient(patientdict, mutationfile, mutationfile_silent)
    count_mutationtype_patient(patientdict)
    get_files_most_mutations(patientdict, "D:/Chantal/Data/mutation_rates.txt",
                             "D:/Chantal/Data/mutation_rates_silent.txt")
    mutationfile = open("D:/Chantal/Data/mutation_file.txt", "r")
    mutationfile_silent = open("D:/Chantal/Data/mutation_file_with_silent.txt", "r")
    count_genes(patients, mutationfile, mutationfile_silent, patientdict)
    muts_file_dkfz = "D:/Chantal/Data/muts/dkfz_muts.txt"
    patients, patientdict = get_mutationdictionary(muts_file_dkfz, False)
    patientdict = count_patient(patientdict, False, muts_file_dkfz)
    get_files_most_mutations(patientdict, False, "D:/Chantal/Data/mutation_rates_dkfz.txt")


main()
