# @file      crete_quad_config_from_single.py
# @author    Lukáš Marek <lukas.marek@advacam.com>
# @date      2021-09-29
# 
# Program should create a config for quad from single detector configs (outptu from calibration/eqv.)


import sys

f_in_path = './'
file_names = ['L09-W0096.xml', 'K09-W0096.xml'] 

f_out_path = f_in_path
f_out_name = 'K09-W0096-2.xml'


f_out = open(f_out_path + f_out_name, "w")


#-----------------------------------
#LAYOUT AND SETTINGS
#Just copied from the Heidelberg quad config
#-----------------------------------

layout_settings = """<?xml version="1.0" encoding="UTF-8"?>
<xml>
    <Layout>
        <Angles>0 0</Angles>
        <Chips>0 1</Chips>
        <Width>2</Width>
        <Height>1</Height>
    </Layout>
    <Settings>
        <Bias>200</Bias>
        <SensorRefreshEnabled>false</SensorRefreshEnabled>
        <SensorRefreshTime>0</SensorRefreshTime>
        <SensorRefresh>0.5,0;0.75,1.4;0.43,0.96;0.4,1</SensorRefresh>
        <ExtBiasSerial>-1</ExtBiasSerial>
        <ExtBiasSrcIndex>0</ExtBiasSrcIndex>
        <InterpolateMaskedPixels>false</InterpolateMaskedPixels>
        <InterpolateMaskedPixelsFlags>0</InterpolateMaskedPixelsFlags>
        <ReleativeTHL>0</ReleativeTHL>
        <UseCalibration>false</UseCalibration>
        <Polarity>true</Polarity>
        <ConvertToaTime>true</ConvertToaTime>
        <OperationMode>0</OperationMode>
    </Settings>"""

f_out.write(layout_settings)

#-----------------------------------
#INDIVIDUAL DETECTOR SETTINGS 
#1st is file_1 alias f1_name etc
#-----------------------------------

def check_string_in_file(file_path, search_string):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
            if search_string in contents:
                return True
            else:
                return False
    except FileNotFoundError:
        print("File not found.")
        return False

def extract_indiv_det_settings(file_in_path,file_in_name, file_out):
    file_in = open(file_in_path + file_in_name, "r")

    indiv_settings = "\n"
    do_load_indiv_settings = False

    include_e_cliba = check_string_in_file(file_in_path + file_in_name, "/calibt")

    final_string = "</MinThreshold>"
    if include_e_cliba:
        final_string = "</calibt>" 

    for line in file_in:
        if do_load_indiv_settings:
            indiv_settings += line

        if "</Settings>" in line:
            do_load_indiv_settings = True

        # there can be either min thrl or calibt based on the fact whether there is e calib or no
        if final_string in line:
            do_load_indiv_settings = False
    
    detector_name = indiv_settings[indiv_settings.find('<')+1:indiv_settings.find('>')]

    indiv_settings += "\t</" + detector_name + ">"

    file_in.close()
    file_out.write(indiv_settings)

for file_name in file_names:
    extract_indiv_det_settings(f_in_path, file_name, f_out)


#-----------------------------------
#PARAMETRS AND INFO
#Just copied from the Heidelberg quad config
#-----------------------------------

parameters_info = """
    <Parameters>
        <BlockCount>2</BlockCount>
        <DDBlockSize>50</DDBlockSize>
        <DDBuffSize>600</DDBuffSize>
        <DDDummyDataSpeed>24831</DDDummyDataSpeed>
        <DebugLog>false</DebugLog>
        <DummyAcqNegativePolarity>true</DummyAcqNegativePolarity>
        <ProcessData>true</ProcessData>
        <TrgCmos>false</TrgCmos>
        <TrgMulti>false</TrgMulti>
        <TrgReady>false</TrgReady>
        <TrgStg>3</TrgStg>
        <TrgT0SyncReset>false</TrgT0SyncReset>
        <TrgTimestamp>false</TrgTimestamp>
    </Parameters>
    <Info>
        <PixetVersion>1.7.5.915</PixetVersion>
        <DateTime>1608563554</DateTime>
        <DateTimeStr>Mon Dec 21 16:12:34.909207 2020</DateTimeStr>
    </Info>
</xml>
"""

f_out.write(parameters_info)

#-----------------------------------

f_out.close()