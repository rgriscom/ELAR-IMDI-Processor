#Last updated: 2019-09-05
#Author: Richard T. Griscom
#Contact: rgriscom@gmail.com
#Description: The script will take metadata from a spreadsheet with columns of data corresponding to metadata categories and rows of data corresponding to individual recording sessions (at the "bundle" level). It will create a new IMDI file for each bundle. The text for the IMDI file is modeled off of an IMDI file provided by ELAR.
        #It assumes you have a tab-delimited text file in the same folder as the script which has a first row with column names that correspond to metadata categories and subsequent rows that correspond to bundles/sessions.
        #It creates a folder called "Output" with IMDI files created for each bundle/session in the tab-delimited text file.

#Check OS
import os, datetime, platform, shutil
now = datetime.datetime.now()
if platform.system() == 'Windows':
    system_var = 'w'
    print('OS is Windows')
else:
    system_var = 'nw'
        

#Input and output directories
if system_var == 'w':
    input_dir = os.getcwd() + "\\"
    output_dir = os.getcwd() + "\\Output\\"
    print('Input dir: ' + input_dir)
    print('Output dir: ' + output_dir) 
else:
	input_dir = os.getcwd() + "/"
	output_dir = os.getcwd() + "/Output/"
print('Input dir: ' + input_dir)
print('Output dir: ' + output_dir)

#Creates Output folder, or deletes it if it already exists
dir_list = os.listdir(input_dir)
if "Output" in dir_list:
    try:
        shutil.rmtree(output_dir)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
os.mkdir(output_dir)

#Create a list of column names from the first row of the text file
#For each subsequent row
    #Create a new dictionary
    #For each entry in the list of column names
        #Create a KEY with the column name and a VALUE with each corresponding piece of data from the row
    #Create a IMDI file in the Output Folder and fill it out based on the data in the dictionary



###OLD CODE####
total_columns = int(input('How many columns of text data? '))
counter = 1
column_names = []
while counter < (total_columns + 1):
    column_names.append(input('What do you want to label column #' + str(counter) + "? "))
    counter += 1            
print(column_names)

for d in dir_list:
        if (".txt" in d) or (".TXT" in d) or (".csv" in d) or (".CSV" in d):
                if ".txt" in d:
                        extension = ".txt"
                if ".TXT" in d:
                        extension = ".TXT"
                if ".csv" in d:
                        extension = ".csv"
                if ".CSV" in d:
                        extension = ".CSV"
                oldname = input_dir + d
                newname = output_dir + d
                temp = d.split(extension)
                filename_stem = temp[0]
                newtextgridname = output_dir + filename_stem + ".TextGrid"
                neweafname = output_dir + filename_stem + ".eaf"
                dict = {}          
#Put REFID, Transcription, and Translation in Dictionary using the columns REFID, TRANSCR, and TRANSL
                with open(oldname) as csv_old, open(newname, "w") as csv_new:
                        annotation_counter = 1
                        column_data = []
                        for line in csv_old:
                                temp = line.split('\n')
                                rows = temp[0].split('\t')
                                dict[annotation_counter] = {}
                                dict[annotation_counter]['REFID'] = filename_stem + "_" + str(annotation_counter)
                                counter = 1
                                while counter < (total_columns + 1):
                                    try:
                                        dict[annotation_counter][column_names[(counter - 1)]] = rows[(counter - 1)]
                                    except IndexError:
                                        dict[annotation_counter][column_names[(counter - 1)]] = ""                                  
                                    counter += 1
                                annotation_counter = annotation_counter + 1
                        total_annotations = annotation_counter - 1
#Put time code in dictionary using the columns XMIN and XMAX
                        textgrid_old = open(input_dir + filename_stem + ".TextGrid")
                        annotation_counter = 1    
                        for line in textgrid_old:
                            if "xmin" in line:
                                temp = line.split('= ')
                                temp_xmin = float(temp[1])
                            if "xmax" in line:
                                temp = line.split('= ')
                                temp_xmax = float(temp[1])
                            if "text = \"***\"" in line:
                                dict[annotation_counter]['XMIN'] = temp_xmin
                                dict[annotation_counter]['XMAX'] = temp_xmax
                                annotation_counter += 1
                            if "tiers? <exists>" in line:
                                final_xmax = temp_xmax
                                        
                                
                                
                        

#Populate new tab-delimited file
                        annotation_counter = 1
                        while annotation_counter < (total_annotations + 1):
                            csv_new.write(dict[annotation_counter]['REFID'] + '\t' + str(dict[annotation_counter]['XMIN']) + '\t' + str(dict[annotation_counter]['XMAX']))
                            counter = 1
                            while counter < (total_columns + 1):
                                csv_new.write('\t' + dict[annotation_counter][column_names[(counter - 1)]]) 
                                counter += 1
                            csv_new.write('\n')
                            annotation_counter += 1
                        csv_old.close()
                        csv_new.close()
                        textgrid_old.close()                            
#Populate new .TextGrid file, with three tiers: unique REF ID, transcription, and translation
                        
                        with open(newtextgridname, "w") as textgrid_new:
                                
#Fill out the beginning of the TextGrid file
                                textgrid_new.write("File type = \"ooTextFile\"\nObject class = \"TextGrid\"\n\nxmin = 0\nxmax = " + str(final_xmax) + "\ntiers? <exists>\nsize = " + str((total_columns + 1)) + "\nitem []:\n")
                                tier_counter = 1
#Fill out the beginning of each tier in the TextGrid
                                while tier_counter < (total_columns + 2):
                                        
                                        textgrid_new.write("    item [" + str(tier_counter) + "]:\n")
                                        textgrid_new.write("        class = \"IntervalTier\"\n")
                                        if tier_counter == 1:
                                            textgrid_new.write("        name = \"REFID\"\n")
                                        else:
                                            textgrid_new.write("        name = \"" + column_names[(tier_counter - 2)] + "\"\n")
                                        
                                        textgrid_new.write("        xmin = 0\n")
                                        textgrid_new.write("        xmax = " + str(final_xmax) + "\n")
                                        textgrid_new.write("        intervals: size = " + str((total_annotations * 2) + 1) + "\n")
#Fill out each TextGrid interval using the DataFrame
                                        annotation_counter = 1
                                        while annotation_counter < (total_annotations + 1):
                                            if annotation_counter == 1:
                                                temp_prev_xmax = 0
                                            else:
                                                temp_prev_xmax = dict[annotation_counter - 1]['XMAX']
                                            temp_next_xmin = dict[annotation_counter]['XMIN']
                                            textgrid_new.write("        intervals [" + str(((annotation_counter * 2) - 1)) + "]:\n")
                                            if annotation_counter == 1:
                                                textgrid_new.write("            xmin = 0\n")
                                            else:
                                                textgrid_new.write("            xmin = " + str(temp_prev_xmax) + "\n")
                                            textgrid_new.write("            xmax = " + str(temp_next_xmin) + "\n")
                                            textgrid_new.write("            text = \"\"\n")
                                            textgrid_new.write("        intervals [" + str(annotation_counter * 2) + "]:\n")
                                            textgrid_new.write("            xmin = " + str(dict[annotation_counter]['XMIN']) + "\n")
                                            textgrid_new.write("            xmax = " + str(dict[annotation_counter]['XMAX']) + "\n")
                                            if tier_counter == 1:
                                                textgrid_new.write("            text = \"" + str(dict[annotation_counter]['REFID']) + "\"\n")
                                            else:
                                                textgrid_new.write("            text = \"" + str(dict[annotation_counter][column_names[(tier_counter - 2)]]) + "\"\n")
                                            annotation_counter += 1
                                        textgrid_new.write("        intervals [" + str((((annotation_counter - 1) * 2) + 1)) + "]:\n")
                                        xmax_of_final_annotation = dict[total_annotations]['XMAX']
                                        textgrid_new.write("            xmin = " + str(xmax_of_final_annotation) + "\n")
                                        textgrid_new.write("            xmax = " + str(final_xmax) + "\n")
                                        textgrid_new.write("            text = \"\"\n")
                                        tier_counter += 1
                        textgrid_new.close()                                 

#Populate new .EAF file
                        #Fill out the beginning of the EAF file
                        with open(neweafname, "w") as eaf_new:
                                eaf_new.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
                                eaf_new.write("<ANNOTATION_DOCUMENT AUTHOR=\"unspecified\" DATE=\"" + str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "T" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "-08:00\" FORMAT=\"3.0\" VERSION=\"3.0\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"http://www.mpi.nl/tools/elan/EAFv3.0.xsd\">\n")
                                eaf_new.write("    <HEADER MEDIA_FILE=\"\" TIME_UNITS=\"milliseconds\">\n")
#Fixes slashes in Windows directories
                                if system_var == 'w':
                                        win_input_dir = ""
                                        for l in input_dir:
                                                if l == "\\":
                                                        win_input_dir += "/"
                                                else:
                                                        win_input_dir += l                     
                                        eaf_new.write("        <MEDIA_DESCRIPTOR MEDIA_URL=\"file:///" + win_input_dir + filename_stem + ".wav\" MIME_TYPE=\"audio/x-wav\" RELATIVE_MEDIA_URL=\"./" + filename_stem + ".wav\"/>\n")
                                else:
                                        eaf_new.write("        <MEDIA_DESCRIPTOR MEDIA_URL=\"file://" + input_dir + filename_stem + ".wav\" MIME_TYPE=\"audio/x-wav\" RELATIVE_MEDIA_URL=\"./" + filename_stem + ".wav\"/>\n")
                                eaf_new.write("        <PROPERTY NAME=\"URN\">urn:nl-mpi-tools-elan-eaf:93cd58ea-4af9-44d5-a6d5-d468217ccf5e</PROPERTY>\n")
                                eaf_new.write("        <PROPERTY NAME=\"lastUsedAnnotationId\">" + str((5 * total_annotations)) + "</PROPERTY>\n")
                                eaf_new.write("    </HEADER>\n")
                                eaf_new.write("    <TIME_ORDER>\n")                       

                        #Fill out time slots
                                annotation_counter = 1
                                while annotation_counter < (total_annotations + 1):
                                    eaf_new.write("        <TIME_SLOT TIME_SLOT_ID=\"ts" + str((annotation_counter * 2) - 1) + "\" TIME_VALUE=\"" + str(int(1000 * dict[annotation_counter]['XMIN'])) + "\"/>\n")
                                    eaf_new.write("        <TIME_SLOT TIME_SLOT_ID=\"ts" + str((annotation_counter * 2)) + "\" TIME_VALUE=\"" + str(int(1000 * dict[annotation_counter]['XMAX'])) + "\"/>\n")
                                    annotation_counter += 1
                        #Fill out RFID annotations
                                eaf_new.write("    </TIME_ORDER>\n")
                                eaf_new.write("    <TIER DEFAULT_LOCALE=\"en\" LINGUISTIC_TYPE_REF=\"REFID\" TIER_ID=\"REFID\">\n")
                                annotation_counter = 1
                                while annotation_counter < (total_annotations + 1):
                                    eaf_new.write("        <ANNOTATION>\n")
                                    eaf_new.write("            <ALIGNABLE_ANNOTATION ANNOTATION_ID=\"a" + str((2 * total_annotations) + annotation_counter) + "\" TIME_SLOT_REF1=\"ts" + str((annotation_counter * 2) -1) + "\" TIME_SLOT_REF2=\"ts" + str(annotation_counter * 2) + "\">\n")
                                    eaf_new.write("                <ANNOTATION_VALUE>" + str(dict[annotation_counter]['REFID']) + "</ANNOTATION_VALUE>\n")
                                    eaf_new.write("            </ALIGNABLE_ANNOTATION>\n")
                                    eaf_new.write("        </ANNOTATION>\n")
                                    annotation_counter += 1
                                eaf_new.write("    </TIER>\n")
                        
                        #Fill out transcription and translation annotations
                                tier_counter = 1
                                while tier_counter < total_columns + 1:
                                
                                    eaf_new.write("    <TIER DEFAULT_LOCALE=\"en\" LINGUISTIC_TYPE_REF=\"" + column_names[(tier_counter - 1)] + "\" PARENT_REF=\"REFID\" TIER_ID=\"" + column_names[(tier_counter - 1)] + "\">\n")
                                    annotation_counter = 1
                                    while annotation_counter < (total_annotations + 1):
                                        eaf_new.write("        <ANNOTATION>\n")
                                        eaf_new.write("            <REF_ANNOTATION ANNOTATION_ID=\"a" + str(((tier_counter + 2) * total_annotations) + annotation_counter) + "\" ANNOTATION_REF=\"a" + str((2 * total_annotations) + annotation_counter) + "\">\n")
                                        eaf_new.write("                <ANNOTATION_VALUE>" + str(dict[annotation_counter][column_names[(tier_counter - 1)]]) + "</ANNOTATION_VALUE>\n")
                                        eaf_new.write("            </REF_ANNOTATION>\n")
                                        eaf_new.write("        </ANNOTATION>\n")
                                        annotation_counter += 1
                                    eaf_new.write("    </TIER>\n")
                                    tier_counter += 1
                        
                                
                        #Fill out end of the EAF file
                                eaf_new.write("    <LINGUISTIC_TYPE GRAPHIC_REFERENCES=\"false\" LINGUISTIC_TYPE_ID=\"REFID\" TIME_ALIGNABLE=\"true\"/>\n")
                                counter = 1
                                while counter < (total_columns + 1):
                                    eaf_new.write("    <LINGUISTIC_TYPE CONSTRAINTS=\"Symbolic_Association\" GRAPHIC_REFERENCES=\"false\" LINGUISTIC_TYPE_ID=\"" + column_names[(counter - 1)] + "\" TIME_ALIGNABLE=\"false\"/>\n")    
                                    counter += 1
                                eaf_new.write("    <LOCALE COUNTRY_CODE=\"US\" LANGUAGE_CODE=\"en\"/>\n")
                                eaf_new.write("    <CONSTRAINT DESCRIPTION=\"Time subdivision of parent annotation's time interval, no time gaps allowed within this interval\" STEREOTYPE=\"Time_Subdivision\"/>\n")
                                eaf_new.write("    <CONSTRAINT DESCRIPTION=\"Symbolic subdivision of a parent annotation. Annotations refering to the same parent are ordered\" STEREOTYPE=\"Symbolic_Subdivision\"/>\n")
                                eaf_new.write("    <CONSTRAINT DESCRIPTION=\"1-1 association with a parent annotation\" STEREOTYPE=\"Symbolic_Association\"/>\n")
                                eaf_new.write("    <CONSTRAINT DESCRIPTION=\"Time alignable annotations within the parent annotation's time interval, gaps are allowed\" STEREOTYPE=\"Included_In\"/>\n")
                                eaf_new.write("</ANNOTATION_DOCUMENT>")
                                eaf_new.close()
                        print('REFID\t' + 'XMIN\t' + 'XMAX', end='')
                        for x in column_names:
                            print('\t' + x, end='')
                        print('')
                        annotation_counter = 1
                        while annotation_counter < (total_annotations + 1):
                            print(dict[annotation_counter]['REFID'] + '\t' + str(dict[annotation_counter]['XMIN']) + '\t' + str(dict[annotation_counter]['XMAX']), end='')
                            for y in column_names:
                                print('\t' + dict[annotation_counter][y], end='')
                            annotation_counter+=1
                            print('')    
                        print("Processing complete for: " + d)
input("Press Enter to continue...")
