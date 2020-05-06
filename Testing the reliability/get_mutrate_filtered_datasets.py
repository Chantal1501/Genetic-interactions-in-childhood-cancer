import os


def get_mutrate(file, dataset, ctype_pos):
    """
    :param file: The file for which will be looked how many mutations are available per sample.
    :param dataset: The dataset for which will be looked how many mutations are available per sample.
    :param ctype_pos: The index of the cancer type in the genesample file.
    This function loops through a genesample file of a certain dataset. For the dataset is counted how many mutations
    every sample has. The number of mutations per sample is written to the file mutation_rate_datasets.txt.
    """
    mutratefile = open("D:/Chantal/Data/mutation_rate_datasets.txt", "a")
    last_sample = ""
    with open(file) as genesampletab:
        for line in genesampletab:
            sample = (line.split("\t")[0])
            ctype = line.split("\t")[ctype_pos]
            print(ctype)
            if sample != "caseID":
                if sample != last_sample:
                    if last_sample != "":
                        mutratefile.write(dataset + "\t" + last_sample + "\t" + str(count) + "\t" + ctype + "\n")
                    count = 1
                    last_sample = sample
                else:
                    count += 1
                print(sample, count)
    mutratefile.write(dataset + "\t" + last_sample + "\t" + str(count) + "\t" + ctype + "\n")
    mutratefile.close()


def main():
    if os.path.exists("D:/Chantal/Data/mutation_rate_datasets.txt"):
        os.remove("D:/Chantal/Data/mutation_rate_datasets.txt")
    get_mutrate("D:/Chantal/Data/gene_sample_tab/CBTTC_GeneSample.txt", "CBTTC", 1)
    get_mutrate("D:/Chantal/Data/gene_sample_tab/Dkfz_hyGeneSample.txt", "DKFZ", 1)
    get_mutrate("D:/Chantal/Data/gene_sample_tab/StJudeGeneSample.txt", "TARGET", 2)


main()
