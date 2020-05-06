import os


def get_cancertypes():
    """
    This function starts with obtaining the samples that aren't hypermutators. This are the samples that has less than
    225 mutations. After that it opens the file patientfiles.txt and gets all cancertypes from this file. This are only
    the cancertypes of the samples that aren't hypermutators. The cancertypes in this case refers to the abbrevations
    of the cancertypes. All the cancertypes are put in a list. By using a set, there is also a list that only contains
    the unique cancertypes.
    :return unique_types: Set with in it the unique cancertypes of the dataset.
    :return types: All of the cancertypes that are available in the dataset. The cancertypes can occur more than
    one time.
    :return sample_list: List with in it all the samples that aren't hypermutators.
    """
    sample_list = filter_hypermutators()
    types = []
    with open("D:/Chantal/Data/patientfiles.txt") as patientfiledata:
        for x in patientfiledata:
            biospecimen = (x.split("\t")[1])
            if biospecimen in sample_list:
                types.append(x.split("\t")[5].rstrip("\n"))
    unique_types = set(types)
    return unique_types, types, sample_list


def filter_hypermutators():
    """
    This function opens the file mutation_rates_silent.txt. This is a file with in it the mutationrate of each sample.
    The mutationrate is how often there is a proteincoding gene mutated in this patient. This are all the coding
    mutations including also the silent mutations. When the sample has less than 225 mutations, the biospecimen
    identifier is added to the sample_list.
    :return sample_list: List with in it all the biospecimen identifiers that aren't hypermutators.
    """
    sample_list = []
    with open("D:/Chantal/Data/mutation_rates_silent.txt") as mutationrates_silent:
        for line in mutationrates_silent:
            if line.split("\t")[0] != "sampleID":
                mutationrate = int(line.split("\t")[2].rstrip("\n"))
                if mutationrate < 225:
                    sample_list.append(line.split("\t")[0])
    return sample_list


def get_highfrequent_ctypes(unique_types, types):
    """
    :param unique_types: Set with in it the unique cancertypes of the dataset.
    :param types: All of the cancertypes that are available in the dataset. The cancertypes can occur more than
    one time.
    This function loops through the list with unique_types. For every type, it checks how often this type occurs in the
    types list. This is a list with in it the cancertypes of all the not hypermutator samples. If the cancertype
    occurs more than 5 times in the dataset, this cancertype is added to the highfrequentlist and to the file
    cantypes.txt.
    :return highfrequentlist: A list with in it all of the cancertypes that occur more than 5 times in the dataset.
    """
    if os.path.exists("D:/Chantal/Data/cantypes.txt"):
        os.remove("D:/Chantal/Data/cantypes.txt")
    cantype_file = open("D:/Chantal/Data/cantypes.txt", "a")
    highfrequentlist = []
    for ctype in unique_types:
        if types.count(ctype) > 5:
            highfrequentlist.append(ctype)
    for cancer in sorted(highfrequentlist):
        cantype_file.write(cancer + "\n")
    cantype_file.close()
    return highfrequentlist


def get_filtered_participants(sample_list, highfrequentlist):
    """
    :param sample_list: List with in it all the samples that aren't hypermutators.
    :param highfrequentlist: A list with in it all of the cancertypes that occur more than 5 times in the dataset.
    This function opens the file patientfiles.txt. It loops through this file. For every line in this file it is
    checked whether this patient is present in the sample_list and if it has a cancertype that is present in the
    highfrequentlist. If this is both the case, this biospecimenidentifier is added to the filtered_participantlist.
    :return filtered_participantlist: A list with in it the participants that aren't hypermutators and that have a
    cancertype that occurs more than 5 times in the dataset.
    """
    filtered_participantlist = []
    biospecimen_ctype_dic = {}
    with open("D:/Chantal/Data/patientfiles.txt") as patientfiledata:
        for patient in patientfiledata:
            biospecimen = patient.split("\t")[1]
            cancertype = patient.split("\t")[5].rstrip("\n")
            if biospecimen in sample_list and cancertype in highfrequentlist:
                filtered_participantlist.append(biospecimen)
                biospecimen_ctype_dic[biospecimen] = cancertype
    return filtered_participantlist, biospecimen_ctype_dic


def make_oncogene_list():
    """
    This functions makes an list of all the oncogenes that are present in the file Oncogene_list.txt.
    :return oncogene_list: List with in it all the oncogenes of the file Oncogene_list.txt.
    """
    oncogene_list = []
    with open("D:/Chantal/Data/Oncogene_list.txt") as oncogene:
        for line in oncogene:
            oncogene_list.append(line.rstrip("\n"))
    return oncogene_list


def make_filtered_mutation_file(filtered_participantlist, biospecimen_ctype_dic, cancergenes):
    """
    :param filtered_participantlist: A list with in it the participants that aren't hypermutators and that have a
    cancertype that occurs more than 5 times in the dataset.
    :param biospecimen_ctype_dic: Dictionary with in it the cancertype of a certain biospecimen.
    :param cancergenes: Input whether the mutationlist files are made for only known cancergenes or not.
    This function loops through the file mutation_file.txt. This is a file that includes all of the coding mutations in
    the dataset. If the biospecimen of a specific mutation is present in the filtered_participantlist, this mutation
    will be written to the file mutation_file_filtered.txt. When the input of cancergenes is yes, only the cancergenes
    present in the oncogenelist will be written to the file. Only biospecimen that have mutations in the cancergenes
    are written to the list new_filtered_participantlist.
    :return new_filtered_participantlist: Biospecimen with mutations in cancergenes.
    """
    oncogene_list = make_oncogene_list()
    if cancergenes.lower() == "yes":
        new_filtered_participantlist = []
    else:
        new_filtered_participantlist = filtered_participantlist
    if os.path.exists("D:/Chantal/Data/mutation_file_filtered.txt"):
        os.remove("D:/Chantal/Data/mutation_file_filtered.txt")
    filtered_mutationfile = open("D:/Chantal/Data/mutation_file_filtered.txt", "a")
    with open("D:/Chantal/Data/mutation_file.txt") as mutationfile:
        for line in mutationfile:
            biospecimen = (line.split("\t")[0])
            gene = line.split("\t")[4].rstrip("\n")
            if cancergenes.lower() == "yes":
                if biospecimen in filtered_participantlist and gene in oncogene_list:
                    filtered_mutationfile.write(line.rstrip("\n") + "\t" + biospecimen_ctype_dic[biospecimen] + "\n")
                    if biospecimen not in new_filtered_participantlist:
                        new_filtered_participantlist.append(biospecimen)
            else:
                if biospecimen in filtered_participantlist:
                    filtered_mutationfile.write(line.rstrip("\n") + "\t" + biospecimen_ctype_dic[biospecimen] + "\n")
    filtered_mutationfile.close()
    return new_filtered_participantlist


def make_directories(unique_types):
    """
    :param unique_types: Set with in it the unique cancertypes.
    This function makes directories for every cancertype. It also makes a mainfolder in which the folders will be
    placed. If a folder already exists, a notification is printed to the screen.
    """
    mainfolder = "D:/Chantal/Data/Mutationlists"
    try:
        os.mkdir(mainfolder)
    except OSError:
        print("Creation of the directory %s failed" % mainfolder)
    else:
        print("Successfully created the directory %s " % mainfolder)
    for cancertype in unique_types:
        path = "D:/Chantal/Data/Mutationlists/" + cancertype
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)
    panfolder = "D:/Chantal/Data/Mutationlists/PAN"
    try:
        os.mkdir(panfolder)
    except OSError:
        print("Creation of the directory %s failed" % panfolder)
    else:
        print("Successfully created the directory %s " % panfolder)


def get_mutationlist(unique_types, filtered_participantlist):
    """
    :param unique_types: Set with in it the unique cancertypes.
    :param filtered_participantlist: A list with in it the participants that aren't hypermutators and that have a
    cancertype that occurs more than 5 times in the dataset.
    This function makes a mutationlist file for every individual cancertype. It makes a gene dictionary with in it
    all the genes of the specific cancer type. The value of these keys are a list with in it the position of the
    biospecimen in the header of the file. The keys and the values of the dictionary are written to the mutationlistfile
    of the specific cancertype. It also makes this for all the mutations together. This is done when the cancertype
    equals PAN.
    """
    mutationfile = open("D:/Chantal/Data/mutation_file_filtered.txt", "r")
    unique_types.append("PAN")
    for cancertype in unique_types:
        print(cancertype)
        gene_dict = {}
        header, biospecimen = get_header(cancertype, filtered_participantlist)
        for mutation in mutationfile:
            bs_mutation = mutation.split("\t")[0]
            if bs_mutation in biospecimen:
                gene = mutation.split("\t")[4].rstrip("\n")
                if gene in gene_dict:
                    if biospecimen.index(bs_mutation) not in gene_dict[gene]:
                        gene_dict[gene].append(biospecimen.index(bs_mutation))
                else:
                    gene_dict[gene] = [biospecimen.index(bs_mutation)]
        mutationfile.seek(0)
        write_to_mutlistfile(cancertype, gene_dict, header)
    mutationfile.close()


def get_header(cancertype, filtered_participantlist):
    """
    :param cancertype: cancertype for which the header will be made
    :param filtered_participantlist: A list with in it the participants that aren't hypermutators and that have a
    cancertype that occurs more than 5 times in the dataset.
    This functions makes a header for a specific cancer type. The header consists of the word samples. Behind this word
    the biospecimen of the samples that has this cancer type are printed. It also makes a list of the biospecimen.
    It loops through the patientfile and looks whether the cancertype is equal to the cancer type given to the function.
    It also looks whether the specific biospecimen identifier is present in the filtered_participantlist. The header and
    the biospecimen list are given to the make mutlist function. If the cancertype equals PAN, then it takes all the
    biospecimen of the file patientfiles.txt and puts this together in the list and header.
    :return header: This header contains the word sample with behind it all the biospecimen.
    :return biospecimenlist: A list with in it all the biospecimen that has this particular cancertype.
    """
    patientfile = open("D:/Chantal/Data/patientfiles.txt", "r")
    header = "samples "
    biospecimenlist = []
    for sample in patientfile:
        diseasetype = sample.split("\t")[5].rstrip("\n")
        if diseasetype == cancertype or cancertype == "PAN":
            biospecimen = (sample.split("\t")[1])
            if biospecimen in filtered_participantlist:
                header = header + biospecimen + ","
                biospecimenlist.append(biospecimen)
    header = header.rstrip(",") + "\n"
    patientfile.seek(0)
    return header, biospecimenlist


def write_to_mutlistfile(cancertype, gene_dict, header):
    """
    :param cancertype: Cancertype of which the genes will be written to a file.
    :param gene_dict: Gene dictionary with the gene as key and as a value the positions of the biospecimen in the header
    that has this specific gene mutated.
    :param header: This header contains the word samples with behind it all the biospecimen.
    This function writes the content of the gene_dict to the mutlistfile. It writes first the header to this file. Then
    it adds to each gene the positions of the biospecimen that has a mutation in this specific gene. It concludes with
    writing this line to a file.
    """
    filename = "D:/Chantal/Data/Mutationlists/" + cancertype + "/" + cancertype + "_smut_list.txt"
    if os.path.exists(filename):
        os.remove(filename)
    mutlistfile = open(filename, "a")
    mutlistfile.write(header)
    for item in sorted(gene_dict.keys()):
        samples = ""
        sample_positions = gene_dict[item]
        for position in sample_positions:
            samples = samples + str(position) + ","
        mutlistfile.write(item + "\t" + samples.rstrip(",") + "\n")
    mutlistfile.close()


def main():
    unique_types, types, sample_list = get_cancertypes()
    highfrequentlist = get_highfrequent_ctypes(unique_types, types)
    filtered_participantlist, biospecimen_ctype_dic = get_filtered_participants(sample_list, highfrequentlist)
    cancergenes = input("Do you only want to use the cancer genes? (yes/no) ")
    filtered_participantlist = make_filtered_mutation_file(filtered_participantlist, biospecimen_ctype_dic, cancergenes)
    make_directories(highfrequentlist)
    get_mutationlist(highfrequentlist, filtered_participantlist)


main()
