import os
from random import randint
from random import seed

def make_participant_lists(participant, unique_participantlist, double_participantlist):
    """
    :param participant: participant that will be added to the unique participant list or the double participant list
    :param unique_participantlist: list with participants that only occur once in the initial and progressive samples
    :param double_participantlist: list with participants that occurs more than once in the initial and progressive samples
    This function checks whether a patient occurs once or more than once in the dataset in which there is already
     done some filter steps and adds this participant to a certain list.
    :return unique_participantlist: list with the unique participant identifiers
    :return double_participantlist: list with the double participant identifiers
    """
    if participant in unique_participantlist:
        unique_participantlist.remove(participant)
        double_participantlist.append(participant)
    elif participant in double_participantlist:
        pass
    else:
        unique_participantlist.append(participant)
    return unique_participantlist, double_participantlist

def get_filename_unique(unique_participantlist, metadata):
    """
    :param unique_participantlist: list with participants that only occur once in the initial and progressive samples
    :param metadata: all off the metadata from this dataset
    This function checks whether a specific patient is available in the unique_participantlist and looks for the
    filename of this specific patient. All of the filenames of the patients that are present in the
    unique_participantlist will be added to the files list.
    :return files: the list files with in it all of the files of the unique participants.
    """
    files = []
    metadata.seek(0)
    for x in metadata:
        if x.split(",")[6] in unique_participantlist and (x.split(",")[12] == "Initial CNS Tumor" or x.split(",")[10] == "Initial CNS Tumor" or x.split(",")[12] == "Progressive" or x.split(",")[10].lstrip(" ") == "Progressive CNS Tumor"):
            files.append(x.split(",")[1])
    return files

def multiple_participant_filters(patient, metadata):
    """
    :param patient: a patient that is present in the double_participantlist
    :param metadata: all off the metadata from this dataset
    This function makes first a list from all of the lines that are available in the metadatafile from a certain patient.
    After that it gives this list to another function that gives a list of the filenames that will be taken from this patients.
    :return files: the list files with in it all of the files of a certain patient
    """
    datalist = []
    metadata.seek(0)
    for x in metadata:
        if x.split(",")[6] == patient and (x.split(",")[12] == "Initial CNS Tumor" or x.split(",")[10] == "Initial CNS Tumor" or x.split(",")[12] == "Progressive" or x.split(",")[10].lstrip(" ") == "Progressive CNS Tumor") and ";" not in x.split(",")[9] and x.split(",")[9] != "Other":
            datalist.append(x)
    files = get_multiple_participant_files(datalist)
    return files

def get_multiple_participant_files(datalist):
    """
    :param datalist: list with all of the lines from the metadatafile of a certain patient that is multiple times in the dataset
    This function checks which files of a certain patient will be taken. At first it checks whether there are multiple
    sampleids of this specific patient. If this is not the case, a random file from this patient will be taken. If there
    are multiple sampleids of this patient, it is checked whether there are samples with different cancertypes.If this
    is the case, from this patient there will be taken multiple files from the different cancer types. If there are no
    multiple cancer types, the eldest sample will be taken of this patient.
    :return files: the list files with in it all of the files that will be taken from a certain patient
    """
    sample_ids = []
    unique_cancertypes = get_cancertypes(datalist)
    for x in datalist:
        sample_ids.append(x.split(",")[11])
    if len(set(sample_ids)) > 1:
        if len(unique_cancertypes) > 1:
            files = multiple_cancertypes(unique_cancertypes, datalist)
        else:
            files = get_lowest_age(datalist)
    else:
        files = random_file(datalist)
    return files

def get_cancertypes(datalist):
    """
    :param datalist: list with all of the lines from the metadatafile of a certain patient that is multiple times in the dataset
    This function makes a list of the unique cancer types that are available of a certain patient in the dataset.
    :return list(unique_cancertypes): list with unique cancertypes of a certain patient
    """
    cancertypes = []
    for x in datalist:
        cancertypes.append(x.split(",")[9])
    unique_cancertypes = set(cancertypes)
    return list(unique_cancertypes)

def multiple_cancertypes(unique_cancertypes, datalist):
    """
    :param unique_cancertypes: list with unique cancertypes of a certain patient
    :param datalist: list with all of the lines from the metadatafile of a certain patient that is multiple times in the dataset
    This function looks in the case that a patient has samples of multiple cancer types which files need to be taken.
    For each of the cancer types that the patient has, the eldest sample will be taken.
    :return files: list with files that need to be taken from this patient.
    """
    files = []
    for ctype in unique_cancertypes:
        file = ""
        age = 1000000
        for sample in datalist:
            if sample.split(",")[9] == ctype:
                if int(sample.split(",")[18]) < age:
                    age = int(sample.split(",")[18])
                    file = sample.split(",")[1]
        files.append(file)
    return files

def get_lowest_age(datalist):
    """
    :param datalist: list with all of the lines from the metadatafile of a certain patient that is multiple times in the dataset
    This function looks which one of the files from a certain patient is the eldest sample. This sample need to be taken.
    :return files: list with files that need to be taken from this patient.
    """
    files = []
    file = ""
    age = 1000000
    for x in datalist:
        if len(x.split(",")[18]) > 0:
            if int(x.split(",")[18]) < age:
                age = int(x.split(",")[18])
                file = x.split(",")[1]
    files.append(file)
    return files

def random_file(datalist):
    """
    :param datalist: list with all of the lines from the metadatafile of a certain patient that is multiple times in the dataset
    This function gives a random file of a patient that has multiple files that have exactly the same metadata information.
    This is done by using seed (10), so every run of the script gives the same random files.
    :return files: list with a random taken file from a certain patient.
    """
    files = []
    random_number = (randint(0, len(datalist)-1))
    file = datalist[random_number].split(",")[1]
    files.append(file)
    return files

def fill_dictionary():
    """
    This function makes a dictionary that can translate every disease type. This is done to have the same names in this
    dataset as in the DKFZ dataset. It also contains the abbreviation.
    :return: cancertype_dict: Dictionary with in it the name in the DKFZ dataset and the abbreviation.
    """
    cancertype_dict = {}
    cancertype_dict['High-grade glioma/astrocytoma (WHO grade III/IV) Other'] = ["HGG-other", "high-grade glioma - other"]
    cancertype_dict['Neurocytoma'] = ["NCT", "neurocytoma"]
    cancertype_dict['Atypical Teratoid Rhabdoid Tumor (ATRT)'] = ["ATRT", "atypical teratoid/rhabdoid tumors"]
    cancertype_dict['Hemangioblastoma'] = ["HGB", "hemangioblastoma"]
    cancertype_dict['Ganglioneuroblastoma'] = ["GNBL", "ganglioneuroblastoma"]
    cancertype_dict['Medulloblastoma SHH'] = ["MB-SHH", "medulloblastoma - SHH"]
    cancertype_dict['Choroid plexus papilloma'] = ["CPP", "choroid plexus papilloma"]
    cancertype_dict['Rhabdomyosarcoma'] = ["RMS", "rhabdomyosarcoma"]
    cancertype_dict['Langerhans Cell histiocytosis'] = ["LCH", "langerhans cell histiocytosis"]
    cancertype_dict['Choroid plexus carcinoma'] = ["CPC", "choroid plexus carcinoma"]
    cancertype_dict['Oligodendroglioma'] = ["OGDG", "oligodendroglioma"]
    cancertype_dict['Medulloblastoma WNT'] = ["MB-WNT", "medulloblastoma - WNT"]
    cancertype_dict['Brainstem glioma- Diffuse intrinsic pontine glioma'] = ["BGDIPG", "brainstem glioma- diffuse intrinsic pontine glioma"]
    cancertype_dict['Malignant peripheral nerve sheath tumor (MPNST)'] = ["MPNST", "malignant peripheral nerve sheat tumor"]
    cancertype_dict['Germinoma'] = ["GMN", "germinoma"]
    cancertype_dict['Craniopharyngioma'] = ["CPG", "craniopharyngioma"]
    cancertype_dict['Neurofibroma/Plexiform'] = ["NFPF", "neurofibroma/plexiform"]
    cancertype_dict['Dysplasia/Gliosis'] = ["DPGL", "dysplasia/gliosis"]
    cancertype_dict['Subependymal Giant Cell Astrocytoma (SEGA)'] = ["SEGA", "subependymal giant cell astrocytoma"]
    cancertype_dict['Ewings Sarcoma'] = ["EWS", "ewing's sarcoma"]
    cancertype_dict['Medulloblastoma Group3'] = ["MB-Group3", "medulloblastoma - Group3"]
    cancertype_dict['Sarcoma'] = ["SC", "sarcoma"]
    cancertype_dict['Dysembryoplastic neuroepithelial tumor (DNET)'] = ["DNET", "dysembryoplastic neuroepithelial tumor"]
    cancertype_dict['Glial-neuronal tumor NOS'] = ["GNTN", "glial-neural tumor NOS"]
    cancertype_dict['Chordoma'] = ["CDM", "chordoma"]
    cancertype_dict['Adenoma'] = ["ADN", "adenoma"]
    cancertype_dict['Schwannoma'] = ["SN", "schwannoma"]
    cancertype_dict['Meningioma'] = ["MG", "meningioma"]
    cancertype_dict['Pineoblastoma'] = ["PB", "pineoblastoma"]
    cancertype_dict['Supratentorial or Spinal Cord PNET'] = ["SSCP", "supratentorial or spinal cord PNET"]
    cancertype_dict['High-grade glioma/astrocytoma (WHO grade III/IV) K27M'] = ["HGG-K27M", "high-grade glioma - K27M"]
    cancertype_dict['Neuroblastoma'] = ["NBL", "neuroblastoma"]
    cancertype_dict['Medulloblastoma Other'] = ["MB-other", "medulloblastoma - other"]
    cancertype_dict['Gliomatosis Cerebri'] = ["GMCB", "gliomatosis cerebri"]
    cancertype_dict['Ependymoma'] = ["EDM", "ependymoma"]
    cancertype_dict['Low-grade glioma/astrocytoma (WHO grade I/II)'] = ["LGG", "low-grade glioma/astrocytoma"]
    cancertype_dict['Cavernoma'] = ["CVN", "cavernoma"]
    cancertype_dict['Metastatic secondary tumors'] = ["MST", "metastatic secondary tumors"]
    cancertype_dict['Teratoma'] = ["TT", "teratoma"]
    cancertype_dict['Ganglioglioma'] = ["GG", "ganglioglioma"]
    cancertype_dict['Medulloblastoma Group4'] = ["MB-Group4", "medulloblastoma - Group4"]
    cancertype_dict['Primary CNS lymphoma'] = ["PCL", "primary CNS lymphoma"]
    return cancertype_dict

def get_participantinformation(metadata, cbttcdata, files):
    """
    :param metadata: all of the metadata of this dataset
    :param cbttcdata: all of the data of the medulloblastoma subtypes
    :param files: all of the files that need to be taken
    This function get the participant information of the files that need to be taken. It takes the filename and the
    participant id. For Medulloblastoma and high grade glioma it also looks for the subtype. If there is no subtype,
    the overall diseasetype will be noted in this column. The disease type is translated in a way that it's the same as
    in the DKFZ dataset. The result of this function is a file with the following format:
    filename\tbiospecimen\tparticipant_id\tdisease_type\tsubtype\tabbreviation\n
    """
    cancertype_dict = fill_dictionary()
    patientfiles = open("D:/Chantal/Data/patientfiles.txt", "a")
    metadata.seek(0)
    for line in metadata:
        if line.split(",")[1] in files:
            filename = line.split(",")[1]
            biospecimen = line.split(",")[16]
            participant_id = line.split(",")[6]
            disease_type = line.split(",")[9]
            if disease_type == "Medulloblastoma":
                subtype = get_subtype_medulloblastoma(cbttcdata, participant_id)
                cancertype = "medulloblastoma"
            elif disease_type == "High-grade glioma/astrocytoma (WHO grade III/IV)":
                subtype = get_subtype_highgrade(filename)
                cancertype = "high-grade glioma"
            else:
                subtype = disease_type
                cancertype = cancertype_dict[subtype][1]
            regel = (filename + "\t" + biospecimen + "\t" + participant_id + "\t" + cancertype + "\t" +
                     cancertype_dict[subtype][1] + "\t" + cancertype_dict[subtype][0] + "\n")
            patientfiles.write(regel)
    patientfiles.close()

def get_subtype_medulloblastoma(cbttcdata, participant_id):
    """
    :param cbttcdata: all of the data of the medulloblastoma subtypes
    :param participant_id: the patient identifier of the patient for which the medulloblastoma subtype is searched
    This function looks for the subtype of Medulloblastoma in the histologies file. If this participant is not
    available in this file, than the subtype will be medulloblastoma.
    :return subtype: the subtype of medulloblastoma
    """
    subtype = "Medulloblastoma Other"
    cbttcdata.seek(0)
    for line in cbttcdata:
        if line.split("\t")[0] == participant_id:
            subtype = ("Medulloblastoma " + line.split("\t")[17])
    return subtype

def get_subtype_highgrade(filename):
    """
    :param filename: The name of a file that has cancer type high-grade glioma/astrocytoma
    This function assigns the highgrade subtype to the patient file. This is subtype K27M. It is assumed that
    every patient with this subtype has the mutation p.Lys28Met in the H3F3A gen.
    :return subtype: The subtype that is assigned to this patientfile (K27M or just high-grade glioma)
    """
    plys28met = False
    openname = "L:/gen/jdaub/extdata/cbttc/data_files/" + filename
    highgradefile = open(openname, "r")
    for line in highgradefile:
        if line.split("\t")[0] == "H3F3A" and line.split("\t")[35] == "p.Lys28Met":
            plys28met = True
            break
    if plys28met == False:
        subtype = "High-grade glioma/astrocytoma (WHO grade III/IV) Other"
    if plys28met == True:
        subtype = "High-grade glioma/astrocytoma (WHO grade III/IV) K27M"
    return subtype

def main():
    unique_participantlist = []
    double_participantlist = []
    metadata = open("C:/Users/cbon/Documents/Chantal/CBTTC metadata/CBTTC_metadata.csv")
    cbttcdata = open("C:/Users/cbon/Documents/Chantal/CBTTC metadata/cbttc-histologies2.xlsx")
    for x in metadata:
        if x.split(",")[0] != "id":
            participant = x.split(",")[6]
            if len(x.split(",")[10]) < 1:
                if (x.split(",")[12] == "Initial CNS Tumor" or x.split(",")[12] == "Progressive") and ";" not in x.split(",")[9] and x.split(",")[9] != "Other":
                    unique_participantlist, double_participantlist = make_participant_lists(participant, unique_participantlist, double_participantlist)
            else:
                if (x.split(",")[10] == "Initial CNS Tumor" or x.split(",")[10].lstrip(" ") == "Progressive CNS Tumor") and ";" not in x.split(",")[9] and x.split(",")[9] != "Other":
                    unique_participantlist, double_participantlist = make_participant_lists(participant, unique_participantlist, double_participantlist)
    seed(10)
    unique_participantlist.sort()
    double_participantlist.sort()
    files = get_filename_unique(unique_participantlist, metadata)
    for patient in double_participantlist:
        variantfile = multiple_participant_filters(patient, metadata)
        files.extend(variantfile)
    if os.path.exists("D:/Chantal/Data/patientfiles.txt"):
        os.remove("D:/Chantal/Data/patientfiles.txt")
    get_participantinformation(metadata, cbttcdata, files)
    metadata.close()
    cbttcdata.close()
main()
