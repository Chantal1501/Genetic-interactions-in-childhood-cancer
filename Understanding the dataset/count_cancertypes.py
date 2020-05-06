import os


def make_cantypelist():
    """
    This function makes a list with in it all the cancertypes that are available in the dataset.
    :return types: List with in it all the cancertypes that are present in the dataset.
    """
    types = []
    with open("D:/Chantal/Data/patientfiles.txt", "r") as filedata:
        for x in filedata:
            ctype = x.split("\t")[5].rstrip("\n")
            if ctype not in types:
                types.append(ctype)
    return types


def make_cantypedict(types):
    """
    :param types: List with in it all the cancertypes that are present in the dataset.
    This function makes a cancertype dictionary with for every cancertype a list of 2 zeros. This will be eventually
    the counts of this cancertype in the original and the final dataset.
    :return cancertype_dict: Dictionary with in it how often each cancertype is present in the dataset.
    """
    cancertype_dict = {}
    for ctype in types:
        cancertype_dict[ctype] = [0, 0]
    return cancertype_dict


def medulloblastoma_highgrade(fileidentifier, mb_hg):
    """
    :param fileidentifier: The fileidentifier of a certain line in the metadatafile.
    :param mb_hg: The type of a certain medulloblastoma or high-grade glioma.
    This function assign a abbreviation to a certain line in the metadatafile.
    :return mb_hg: The type of a certain medulloblastoma or high-grade glioma.
    """
    with open("D:/Chantal/Data/patientfiles.txt", "r") as filedata:
        for line in filedata:
            if line.split("\t")[0] == fileidentifier:
                mb_hg = line.split("\t")[5].rstrip("\n")
    return mb_hg


def old_counts(cancertype_dict):
    """
    :param cancertype_dict: Dictionary with in it how often each cancertype is present in the dataset.
    This function counts how often a certain cancertype is present in the original CBTTC metadata. For every line
    in the metadata file it looks what the abbreviation of this type is and it counts + 1 for this cancertype in the
    cancertype_dict.
    :return cancertype_dict: Dictionary with in it how often each cancertype is present in the dataset.
    """
    abbreviation_dict = abbreviation_dictionary()
    abbreviation_keys = abbreviation_dict.keys()
    with open("C:/Users/cbon/Documents/Chantal/CBTTC metadata/CBTTC_metadata.csv") as metadata:
        for line in metadata:
            ctype = line.split(",")[9]
            if ctype in abbreviation_keys:
                abbreviation = abbreviation_dict[ctype][0]
                cancertype_dict[abbreviation][0] += 1
            if ctype == "Medulloblastoma":
                mb_hg = medulloblastoma_highgrade(line.split(",")[1], "MB-other")
                cancertype_dict[mb_hg][0] += 1
            if ctype == "High-grade glioma/astrocytoma (WHO grade III/IV)":
                mb_hg = medulloblastoma_highgrade(line.split(",")[1], "HGG-other")
                cancertype_dict[mb_hg][0] += 1
    return cancertype_dict


def abbreviation_dictionary():
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


def new_counts(cancertype_dict):
    """
    :param cancertype_dict: Dictionary with in it how often each cancertype is present in the dataset.
    This function counts how often each cancertype is present in the final dataset. To count this, it opens the smutfile
    of a specific cancertype and it took the first line. In this line is a list of biospecimen. This list is taken
    and it counts how many items are present in this list. This count is assigned to the second value in the list in the
    cancertype_dict.
    :return cancertype_dict: Dictionary with in it how often each cancertype is present in the dataset.
    """
    with open("D:/Chantal/Data/cantypes.txt") as cantypes:
        for line in cantypes:
            ctype = line.rstrip("\n")
            filename = "D:/Chantal/Data/Mutationlists/" + ctype + "/" + ctype + "_smut_list.txt"
            with open(filename) as smutfile:
                cancertype_dict[ctype][1] = len(smutfile.readline().split(" ")[1].split(","))
    return cancertype_dict


def results_to_file(cancertype_dict):
    """
    :param cancertype_dict: Dictionary with in it how often each cancertype is present in the dataset.
    This function writes the counts of the original dataset and the final dataset to a file. The cancertypes are sorted
    in alphabetical order.
    :return:
    """
    if os.path.exists("D:/Chantal/data/cancertype_counts.txt"):
        os.remove("D:/Chantal/data/cancertype_counts.txt")
    countfile = open("D:/Chantal/data/cancertype_counts.txt", "a")
    for key in sorted(cancertype_dict):
        print(key, cancertype_dict[key])
        countfile.write(key + "\t" + str(cancertype_dict[key][0]) + "\t" + str(cancertype_dict[key][1]) + "\n")
    countfile.close()


def main():
    types = make_cantypelist()
    cancertype_dict = make_cantypedict(types)
    cancertype_dict = old_counts(cancertype_dict)
    cancertype_dict = new_counts(cancertype_dict)
    results_to_file(cancertype_dict)


main()
