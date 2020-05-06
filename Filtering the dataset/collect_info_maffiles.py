import os

def main():
    """
    This script collects all the needed information from all of the maffiles into one .txt file. It only takes
    the columns that are probably needed for the rest of the research. On top of that it only takes mutations
    that are not in an intergenic region.
    """
    if os.path.exists("D:/Chantal/Data/merged_maffiles.txt"):
        os.remove("D:/Chantal/Data/merged_maffiles.txt")
    mergedfile = open("D:/Chantal/Data/merged_maffiles.txt", "a")
    patientfile = open("D:/Chantal/Data/patientfiles.txt", "r")
    header = False
    for x in patientfile:
        filename = x.split("\t")[0]
        biospecimen = x.split("\t")[1]
        patientidentifier = x.split("\t")[2]
        cancertype = x.split("\t")[3]
        subtype = x.split("\t")[4].rstrip("\n")
        openname = "L:/gen/jdaub/extdata/cbttc/data_files/" + filename
        print(openname)
        with open(openname) as file:
            for line in file:
               linelist = line.split("\t")
               if header == False:
                    if linelist[0] == "Hugo_Symbol":
                        mergedfile.write("Filename" + "\t" + "Identifier" + "\t" + "Patientidentifier" + "\t" +  "Cancer type" + "\t"
                                         + "Cancer subtype" + "\t" + linelist[0] + "\t" + linelist[1] + "\t" + linelist[4] + "\t" +
                                         linelist[5] + "\t" + linelist[6] + "\t" + linelist[8] + "\t" + linelist[9] + "\t" + linelist[10]
                                         + "\t" + linelist[11] + "\t" + linelist[12] + "\t" + linelist[34] + "\t" + linelist[35] + "\t" +
                                         linelist[37] + "\t" + linelist[47] + "\t" + linelist[63] + "\n")
                        header = True
               if (len(linelist) > 1 and linelist[8] != "IGR" and linelist[0] != "Hugo_Symbol"):
                   mergedfile.write(filename + "\t" + biospecimen + "\t" + patientidentifier + "\t" + cancertype + "\t" +
                                    subtype + "\t" + linelist[0] + "\t" + linelist[1] + "\t" + linelist[4] + "\t" +
                                    linelist[5] + "\t" + linelist[6] + "\t" + linelist[8] + "\t" + linelist[9] + "\t" + linelist[10]
                                    + "\t" + linelist[11] + "\t" + linelist[12] + "\t" + linelist[34] + "\t" + linelist[35] + "\t" +
                                    linelist[37] + "\t" + linelist[47] + "\t" + linelist[63] + "\n")
    mergedfile.close()
main()
