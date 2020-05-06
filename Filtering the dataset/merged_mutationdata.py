import os

def merge_mutationdata(merged_filename, mutationlist, mutationfile):
    """
    :param merged_filename: The name that will be assigned to the file that results from this function
    :param mutationlist: A list that contains the mutationtypes that will be tooken in this function
    :param mutationfile: The file in which is searched for mutations.
    This function loops through the file merged_maffiles.txt. If one line contains a mutationtype that is available in the
    mutationlist, than this line will be written to a file.
    """
    filename = "D:/Chantal/Data/" + merged_filename
    print(filename)
    if os.path.exists(filename):
        os.remove(filename)
    mergedmutationfile = open(filename, "a")
    with open(mutationfile) as mergedfile:
        for line in mergedfile:
            if(line.split("\t")[10]) in mutationlist:
                mergedmutationfile.write(line)
    mergedmutationfile.close()

def main():
    """
    This script collects all of the interesting mutations that are available in the file merged_maffiles.txt.
    The function is called twice. The script takes the frame shift deletions/insertions, in frame insertions/deletions
    and the missense/nonsense/nonstop mutations in both cases and the second time it also collects silent mutations,
    RNA mutations, mutations in the 5' UTR and the 3' UTR region, splice region mutations and splice site mutations.
    It writes the whole line to a file. The output of this file will be used to calculate the mutation types.
    """
    mutationlist = ["Frame_Shift_Del", "Frame_Shift_Ins", "In_Frame_Del", "In_Frame_Ins", "Missense_Mutation",
                    "Nonsense_Mutation", "Nonstop_Mutation"]
    merge_mutationdata("merged_mutation_file.txt", mutationlist, "D:/Chantal/Data/merged_maffiles.txt")
    mutationlist_silent = ["Frame_Shift_Del", "Frame_Shift_Ins", "In_Frame_Del", "In_Frame_Ins", "Missense_Mutation",
                    "Nonsense_Mutation", "Nonstop_Mutation", "Silent"]
    merge_mutationdata("merged_mutation_file_silent.txt", mutationlist_silent, "D:/Chantal/Data/merged_maffiles.txt")

main()
