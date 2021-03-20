
import csv
import datetime
import os
import pandas as pd
import re
import subprocess
import time
import tkinter
# import tkinter.messagebox
# from tkinter import *
# import tkinter.font as font


#Create dateTime var
now = datetime.datetime.now()
minute = '{:02d}'.format(now.minute)
dateTime = 'DATE '+str(now.year)+'/'+str(now.month)+'/'+str(now.day)+'  TIME '+str(now.hour)+"/"+str(minute)+"/"+str(now.second)

#Declare CWD variables
pathName = os.getcwd()
fileNames = os.listdir(pathName)

#Delete pre-existing decodes if present
for fileNames in fileNames:
    try:
        if fileNames.endswith(".CSV") or fileNames.endswith(".DAT") or fileNames.endswith(".txt") or fileNames.endswith(".LST"):
            os.remove(fileNames)
            print("% s has been removed successfully" % fileNames)
    except:
        pass

fileNames = os.listdir()

# detect if multiple decode files are in folder and allocate files per sysType
decodeFiles = []
datFiles = []
binFiles = []

for fileNames in fileNames:
    if fileNames != "BASE_kml.dat":
        if fileNames.endswith(".bin") or fileNames.endswith(".dat"):
            decodeFiles.append(fileNames)
            if fileNames.endswith(".bin"):
                binFiles.append(fileNames)
            elif fileNames.endswith(".dat"):
                datFiles.append(fileNames)

if len(decodeFiles) > 1:

    # create GUI
    gui = Tk(className=' KML_Generator')
    gui.geometry("800x200")
    gui.configure(background='#646264')

    # define theme font
    myFont = font.Font(family='Calibri',size = 16, font ='bold')

    # create Label
    label= Label(text="WARNING: This folder contains multiple data files")
    label.place(x=90, y=90)
    label['font'] = myFont
    label.configure(bg='#646264', fg='#EC322D', font=('Calibri',20))

    # create button
    button = Button(gui, text='Exit decoder', bg='#515050', fg='White', command = gui.destroy)
    button['font'] = myFont

    # add button to gui window
    button.pack(pady=40)
    gui.mainloop()

    #close script
    exit()

# decode Flight files 
# this example is from a work project with aircraft history files
# below is the decoding of them, which will not be needed in most examples

#Legacy

for binFiles in binFiles:
    try:
        p = subprocess.Popen(["FFS.exe", binFiles])
        returncode = p.wait() # wait for FFS.exe to exit
    except:
        pass

    try:
        p = subprocess.Popen(["FLT_HIST_V5_5.exe"])
        returncode = p.wait() # FLT_HIST_V5_5.exe to exit
        print('Decoding: ', binFiles)
    except:
        pass

#MKV-A
for datFiles in datFiles:
    try:
        os.system("FLT_HISTA.exe")
        print('Decoding: ', datFiles)
    except:
        pass

# set system tyoe flag to adjust headers of warn.csv file
if len(binFiles) > 0:
    sysType = 'legacy'
else:
    sysType = 'MKV-A'
print("System type: ", sysType)

#Set empty variable
LineNo = ""
RecID = ""
FltLeg = ""
OperTime = ""
Lat = ""
Long = ""
PosUncert = ""
CAS = ""
TAS = ""
Gspd = ""
MOS_VRef = ""
VFOM = ""
GPS_Alt = ""
Uncorr_Alt = ""
TACAlt = ""
RadAlt = ""
TerrElv = ""
AltRte = ""
MagTrk = ""
TruTrk = ""
TruHd = ""
Pitch = ""
Roll = ""
BAOA = ""
LAccl = ""
Naccl = ""
IV_Accl = ""
Glides = ""
LOC = ""
PosSrc = ""
SAT = ""
Rng1 = ""
Rng2 = ""
CorAltVFOM = ""
GeoAltVFOM = ""
GPSCal_Alt = ""
GPSCalVFOM = ""
RACal_Alt = ""
RACalVFOM = ""
RnwyCal_Alt = ""
RnwyCalVFOM = ""
TotShear = ""
ShearBias = ""
HorizBias = ""
PWSDataPt = ""
PWSAPDet = ""
PWSAPVal = ""
PWS_AzLt = ""
PWS_AzRt = ""
PWS_RngStart = ""
PWS_RngEnd = ""
GrDn = ""
FlpSel = ""
InAir = ""
Apprch = ""
WSApprch = ""
TADInh = ""
Disp1En = ""
Disp2En = ""
Tact_Sel = ""
AudioInh = ""
EnvMod = ""
NISF1 = ""
NISF2 = ""
SelMode = ""
CorrAlt = ""
HIL1 = ""
HIL2 = ""
SV_Vis1 = ""
SV_Trk1 = ""
SysInUse1 = ""
OpMode1 = ""
SV_Vis2 = ""
SV_Trk2 = ""
SysInUse2 = ""
OpMode2 = ""
FlpAng = ""
MOS = ""
StkShkr = ""
N2Left = ""
N2Right = ""

TestforEOFpattern = ''
TestforEOF = ''
numFiles = []
fileNames = os.listdir(pathName)

###Creat dictionaries for fault tests
GPS_POSdrops = {}
GPS_Altdrops = {}
RA_Altdrops = {}
TestforRAjumps = {}
warnID = {}

#################### make KLM file
kmlbeginning = open("BASE_kml.dat", 'r')
try:
    os.remove('GoogleEarth_Plot.KML')
except:
    pass
    #OSError as e:  ## if failed, report it back to the user ##
    #print ("Error: %s - %s." % (e.filename, e.strerror))
kmlfile = open('GoogleEarth_Plot.KML', 'w')
for l in kmlbeginning:
    kmlfile.write(l)

for fileNames in fileNames:
    if fileNames.endswith("Warn.CSV"):
        numFiles.append(fileNames)
#print(numFiles)

for i in numFiles:
    file = open(os.path.join(pathName, i), "r")
    reader = csv.reader(file, delimiter=',')
    header = next(reader)

    for row in reader:
        for column in reader:
            TestforEOFpattern = re.compile('Index Summary')
            TestforEOF = TestforEOFpattern.findall(str(column))
            #print(TestforEOF)
            if TestforEOF == ['Index Summary']:
                #print(TestforEOF)
                break
            if sysType == 'MKV-A':
                try:
                    LineNo = column[0]
                    RecID = column[1]
                    FltLeg = column[2]
                    OperTime = column[3]
                    Lat = column[4]
                    Long = column[5]
                    PosUncert = column[6]
                    CAS = column[7]
                    TAS = column[8]
                    Gspd = column[9]
                    MOS_VRef = column[10]
                    VFOM = column[11]
                    GPS_Alt = column[12]
                    Uncorr_Alt = column[13]
                    TACAlt = column[14]
                    RadAlt = column[15]
                    TerrElv = column[16]
                    AltRte = column[17]
                    MagTrk = column[18]
                    TruTrk = column[19]
                    TruHd = column[20]
                    Pitch = column[21]
                    Roll = column[22]
                    BAOA = column[23]
                    LAccl = column[24]
                    Naccl = column[25]
                    IV_Accl = column[26]
                    Glides = column[27]
                    Loc = column[28]
                    PosSrc = column[29]
                    SAT = column[30]
                    Rng1 = column[31]
                    Rng2 = column[32]
                    CorAltVFOM = column[33]
                    GeoAltVFOM = column[34]
                    GPSCal_Alt = column[35]
                    GPSCalVFOM = column[36]
                    RACal_Alt = column[37]
                    RACal_Alt = RACal_Alt.replace('*','')
                    #print(RACal_Alt)
                    RACalVFOM = column[38]
                    RnwyCal_Alt = column[39]
                    RnwyCalVFOM = column[40]
                    TotShear = column[41]
                    ShearBias = column[42]
                    HorizBias = column[43]
                    PWSDataPt = column[44]
                    PWSAPDet = column[45]
                    PWSAPVal = column[46]
                    PWS_AzLt = column[47]
                    PWS_AzRt = column[48]
                    PWS_RngStart = column[49]
                    PWS_RngEnd = column[50]
                    GrDn = column[51]
                    FlpSel = column[52]
                    InAir = column[53]
                    Apprch = column[54]
                    WSApprch = column[55]
                    TADInh = column[56]
                    Disp1En = column[57]
                    Disp2En = column[58]
                    Tact_Sel = column[59]
                    AudioInh = column[60]
                    EnvMod = column[61]
                    NISF1 = column[62]
                    NISF2 = column[63]
                    SelMode = column[64]
                    CorrAlt = column[65]
                    HIL1 = column[66]
                    HIL2 = column[67]
                    SV_Vis1 = column[68]
                    SV_Trk1 = column[69]
                    SysInUse1 = column[70]
                    OpMode1 = column[71]
                    SV_Vis2 = column[72]
                    SV_Trk2 = column[73]
                    SysInUse2 = column[74]
                    OpMode2 = column[75]
                    FlpAng = column[76]
                    MOS = column[77]
                    StkShkr = column[78]
                    N2Left = column[79]
                    N2Right = column[80]
                except:
                    pass
            if sysType == 'legacy':
                try:
                    LineNo = column[0]
                    RecID = column[1]
                    FltLeg = column[2]
                    Lat = column[3]
                    Long = column[4]
                    PosUncert = column[5]
                    CAS = column[6]
                    TAS = column[7]
                    Gspd = column[8]
                    MOS_VRef = column[9]
                    VFOM = column[10]
                    GPS_Alt = column[11]
                    Uncorr_Alt = column[12]
                    TACAlt = column[13]
                    RadAlt = column[14]
                    AltRte = column[15]
                    MagTrk = column[16]
                    TruTrk = column[17]
                    TruHd = column[18]
                    Pitch = column[29]
                    Roll = column[20]
                    BAOA = column[21]
                    LAccl = column[22]
                    Naccl = column[23]
                    IV_Accl = column[24]
                    Glides = column[25]
                    Loc = column[26]
                    PosSrc = column[27]
                    SAT = column[28]
                    Rng1 = column[29]
                    Rng2 = column[30]
                    GrDn = column[31]
                    FlpSel = column[32]
                    TADInh = column[33]
                    Disp1En = column[34]
                    Disp2En = column[35]
                    NISF1 = column[36]
                    NISF2 = column[37]
                    SelMode = column[38]
                    CorrAlt= column[39]
                    HIL1 = column[40]
                    HIL2 = column[41]
                    SV_Vis1 = column[42]
                    SV_Trk1 = column[43]
                    SysInUse1 = column[44]
                    OpMode1 = column[45]
                    SV_Vis2 = column[46]
                    SV_Trk2 = column[47]
                    SysInUse2 = column[48]
                    OpMode2 = column[49]
                    FlpAng = column[50]
                    MOS = column[51]
                    StkShkr = column[52]
                    N2Left = column[53]
                    N2Right = column[54]
                except:
                    pass
            #################### kml placemark
            TestforGPSPOSnull = re.compile('0.000')
            TestforGPSPOSouttage = re.compile('\*')
            TestforGPSALTouttage = re.compile('\*')
            TestforRAaltouttage = re.compile('\*')
            GPSALTouttage = TestforGPSALTouttage.findall(str(GPS_Alt))
            GPSPOSouttage = TestforGPSPOSouttage.findall(str(Lat))
            GPSPOSnull = TestforGPSPOSnull.findall(str(Lat))
            RAaltouttage = TestforRAaltouttage.findall(str(RadAlt))
            if  GPSPOSnull == ['0.000']:
                break
            # GPS position data invalid causing erroneous position alerts
            elif GPSPOSouttage == ['*']:
                GPS_POSdrops[int(LineNo)] = 'Latitude: '+ Lat.strip()+ '  Longitude: '+Long.strip()
            elif RAaltouttage == ['*']:
                RA_Altdrops[int(LineNo)] = 'RadAlt: '+ RadAlt.strip()
            elif GPSALTouttage == ['*']:
                GPS_Altdrops[int(LineNo)] = 'GPS_ALT: '+ GPS_Alt.strip()
            elif RecID.strip() != 'DATA':
                warnID[int(LineNo)] = RecID
            else:
                TestforRAjumps[int(LineNo)] = float(RadAlt.strip())

            ##Appedning base KML and saving as new##
            kmlfile.write("		<Placemark>\n")
            if RecID.strip() != 'DATA':
                kmlfile.write("			<name>"+RecID+"</name>\n")
            elif RecID.strip() == 'DATA':
                kmlfile.write("			<name>"+LineNo+"</name>\n")
            kmlfile.write("			<styleUrl>#pointStyleMap</styleUrl>\n")
            kmlfile.write("			<Style id=\"inline\">\n")
            kmlfile.write("				<IconStyle>\n")
            kmlfile.write("					<color>ffffffff</color>\n")
            kmlfile.write("					<colorMode>normal</colorMode>\n")
            if RecID.strip() != 'DATA':
                kmlfile.write("					<Icon><href>http://maps.google.com/mapfiles/kml/paddle/red-diamond.png</href></Icon>\n")
                #print "Warning"
            elif RecID.strip() == 'DATA':
                kmlfile.write("					<Icon><href>http://maps.google.com/mapfiles/kml/paddle/grn-diamond.png</href></Icon>\n")
                #print "Data"
            kmlfile.write("				</IconStyle>\n")
            kmlfile.write("				<LineStyle><color>ffffffff</color><colorMode>normal</colorMode></LineStyle>\n")
            kmlfile.write("				<PolyStyle><color>ffffffff</color><colorMode>normal</colorMode></PolyStyle>\n")
            kmlfile.write("			</Style>\n")
            kmlfile.write("			<ExtendedData>\n")
            kmlfile.write("				<SchemaData schemaUrl=\"EGPWS_Plot\">\n")
            if RecID.strip() != 'DATA':
                kmlfile.write("					<SimpleData name=\"Description\">"+RecID+"</SimpleData>\n")
            elif RecID.strip() == 'DATA':
                kmlfile.write("					<SimpleData name=\"Description\">"+LineNo+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"Latitude\">"+Lat+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"Longitude\">"+Long+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"RA Altitude\">"+RACal_Alt+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"GPS Altitude\">"+GPS_Alt+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"Terrain Elevation\">"+TerrElv+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"Altitute Rate\">"+AltRte+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"Operating Time\">"+OperTime+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"Calculated Airspeed\">"+CAS+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"True Airspeed\">"+TAS+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"Glideslope\">"+Glides+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"Localizer\">"+LOC+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"Position Source\">"+PosSrc+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"Gear Down\">"+GrDn+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"Flap Select\">"+FlpSel+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"Flap Angle\">"+FlpAng+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"PWS data pt\">"+PWSDataPt+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"Stick Shaker\">"+StkShkr+"</SimpleData>\n")
            kmlfile.write("					<SimpleData name=\"Icon\">1</SimpleData>\n")
            kmlfile.write("				</SchemaData>  </ExtendedData>\n")
            kmlfile.write("	        <LookAt><longitude>"+str(Long)+"</longitude><latitude>"+str(Lat)+"</latitude><altitude>"+str(RACal_Alt)+"</altitude><range>18000</range><tilt>68</tilt><heading>76</heading></LookAt>\n")
            kmlfile.write("			<Point><extrude>1</extrude><altitudeMode>relativeToGround</altitudeMode><coordinates>"+Long+','+Lat+','+RACal_Alt+"</coordinates></Point>\n")
            kmlfile.write("		</Placemark>\n")
            kmlfile.write("\n")
        #################### kml placemark		^^^
            TestforEOFpattern = re.compile('Index Summary')
            TestforEOF = TestforEOFpattern.findall(str(column))
        if TestforEOF == ['Index Summary']:
            #print(TestforEOF)
            break
    #Saving kml
    kmlfile.write("	</Folder></Document></kml>")
kmlfile.close()
#################### make KLM file 	            ^^^^

####Parse template for PDF build ######################
fileNames = os.listdir()

responseTemplate = open('FWH Analysis Template.txt', 'w')
tempParsingData = open('TempParsingData.txt', 'w')
partNumber = ''
serialNum = ''
modStat = ''
progPins = ''
appSW = ''
configSW = ''
TDBver = ''
EMBver = ''
acftCN = ''
audioMenu = ''
calloutMenu = ''
fltLeg = ''

for fileNames in fileNames:
        if fileNames.endswith("Counts.txt"):
            with open("Counts.txt", 'r') as Counts:
                for ln in Counts:
                    print(ln.strip())
                    partNumber = re.compile('Part Number:', re.IGNORECASE)
                    serialNum = re.compile('Serial Number:', re.IGNORECASE)
                    modStat = re.compile('Mod Status:', re.IGNORECASE)
                    bootSW = re.compile('Boot Software:', re.IGNORECASE)
                    progPins = re.compile('PROGRAM PIN', re.IGNORECASE)
                    if partNumber.findall(ln):
                        responseTemplate.write(ln.strip()+'\n')
                    elif serialNum.findall(ln):
                        responseTemplate.write(ln.strip()+'\n')
                    elif modStat.findall(ln):
                        responseTemplate.write(ln.strip()+'\n')
                        responseTemplate.write('\n')
                    elif progPins.findall(ln):
                        PP = ln.strip()+'\n'
                        responseTemplate.write(PP)
                        # test for Porgram Pin of 0, which is an invalid config
                        if PP[0] == str(0):
                            responseTemplate.write('NOTE: Porgram Pin of 0 is NOT a valid config')
            Counts.close()
            responseTemplate.write('\n')

        if fileNames.endswith("Status.txt"):
            with open("Status.txt", 'r') as Status:
                for ln in Status:
                    appSW = re.compile("Application S/W Version:", re.IGNORECASE)
                    configSW = re.compile("Configuration S/W Version:", re.IGNORECASE)
                    TDBver = re.compile("Terrain Database Version:" , re.IGNORECASE)
                    EMBver = re.compile("Envelope Mod. Database Version:", re.IGNORECASE)
                    acftCN = re.compile("Aircraft Configuration Number:", re.IGNORECASE)
                    audioMenu = re.compile("Audio Menu Index:", re.IGNORECASE)
                    calloutMenu = re.compile("Callout Menu Index:", re.IGNORECASE)
                    if appSW.findall(ln):
                        tempParsingData.write(ln.strip()+'\n')
                    elif configSW.findall(ln):
                        tempParsingData.write(ln.strip()+'\n')
                    elif TDBver.findall(ln):
                        tempParsingData.write(ln.strip()+'\n')
                    elif EMBver.findall(ln):
                        tempParsingData.write(ln.strip()+'\n')
                    elif acftCN.findall(ln):
                        tempParsingData.write(ln.strip()+'\n')
                    elif audioMenu.findall(ln):
                        tempParsingData.write(ln.strip()+'\n')
                    elif calloutMenu.findall(ln):
                        tempParsingData.write(ln.strip()+'\n')
            Status.close()

lnCount = 0
latestRev = []

# Radio altitude should not be jumping within just a few seconds: test for it! ##
TestforRAjumpsOffset = {}
RAjumps = {}

    # Create offset for test cases

for k,v in TestforRAjumps.items():
    TestforRAjumpsOffset[k+1] = v

for k, v in TestforRAjumps.items():
    for key,value in TestforRAjumpsOffset.items():
        if key == k:
            if abs(v) > (abs(value) + 50):
                RAjumps[k] = 'RA_Alt: '+ str(v)

# build template matrix around WARN's

GPS_POSdropsFinal = {}
GPS_AltdropsFinal  = {}
RAjumpsFinal = {}
RAaltouttageFinal = {}

for k, v in warnID.items():
    for key,value in GPS_Altdrops.items():
        if key == k-3 or key == k-2 or key == k-1 or key == k:
            GPS_AltdropsFinal[key] = value

for k, v in warnID.items():
    for key,value in GPS_POSdrops.items():
        if key == k-3 or key == k-2 or key == k-1 or key == k:
            GPS_POSdropsFinal[key] = value

for k, v in warnID.items():
    for key,value in RAjumpsFinal.items():
        if key == k-3 or key == k-2 or key == k-1 or key == k:
            RAjumpsFinal[key] = value

for k, v in warnID.items():
    for key,value in RAaltouttageFinal.items():
        if key == k-3 or key == k-2 or key == k-1 or key == k:
            RAaltouttageFinal[key] = value

templateMatrix = []

for k,v in GPS_POSdropsFinal.items():
    templateMatrix.append('Line_No: '+ str(k) + ' ' + v)
for k,v in GPS_AltdropsFinal.items():
    templateMatrix.append('Line_No: '+ str(k) + ' ' + v)
for k,v in RAjumpsFinal.items():
    templateMatrix.append('Line_No: '+ str(k) + ' ' + v)
for k,v in warnID.items():
    templateMatrix.append('Line_No: '+ str(k) + ' ' + v)
for k,v in RAaltouttageFinal.items():
    templateMatrix.append('Line_No: '+ str(k) + ' ' + v)

# Write template
s = templateMatrix
print( *s, sep='\n')

tempParsingData = open('TempParsingData.txt', 'r+')
for ln in tempParsingData:
    lnCount += 1
    latestRev.append(ln)
for i in latestRev[lnCount-6:]:
    responseTemplate.write(i)
responseTemplate.write('\n')
responseTemplate.write('** Listing the leading causes of warnings (GPS postion / alt loss and RA loss. Bank rate added soon) **'+'\n')
responseTemplate.write('** If within 3 Line_No of all the warnings in WARN file printed below **'+'\n')
for l in s:
    responseTemplate.write(l+'\n')

tempParsingData.close()
responseTemplate.close()

pathName = os.getcwd()
fileNames = os.listdir(pathName)
for fileNames in fileNames:
    if fileNames.endswith("TempParsingData.txt"):
        os.remove(fileNames)
    #if fileNames.endswith('FWH Analysis Template.txt'):
    contents = open('FWH Analysis Template.txt','r')
    with open("FWH_Template.html", "w") as e:
        x = '"'+pathName+'\HeaderforEGPWSTemplate.png'+'"'
        e.write("</pre>")
        e.write("<img src ="+x+">"" <br />")
        for lines in contents.readlines():
            e.write("</pre>"+ lines + "<br />")
        e.write("</pre>")


print("\n",'Decode completed',dateTime)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
### Created by Lee Brunovsky Dec 2020 ###
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
