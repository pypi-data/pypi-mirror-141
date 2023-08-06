#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.options.display.max_columns = None

class WaterQualityAssessor:
    
    #initialize
    def __init__(self, df, cols):
        '''
        Inputs
        - df: pandas.DataFrame
        - cols: list, list of analytical columns
        '''
        self.df = df
        self.cols = cols
        self.epa_standards = {'Alkalinity (mg/L HCO3)': 100, 'Aluminum (mg/L)': 0.05, 'Ammonia (mg/L)': 0.25,
                    'Antimony (mg/L)': 0.006, 'Arsenic (mg/L)': 0.01, 'Barium (mg/L)': 2, 'Beryllium (mg/L)': 0.004, 
                    'Boron (mg/L)': 3, 'Bromine (mg/L)': 6, 'Bismuth (mg/L)': 0.01, 'Cadmium (mg/L)': 0.005, 
                    'Calcium (mg/L)': 50, 'Cobalt (mg/L)': 0.006, 'Cerium (mg/L)': 0.0221, 'Chromium (mg/L)': 0.1, 
                    'Chloride (mg/L)': 250, 'Copper (mg/L)': 1.0, 'Dysprosium (mg/L)': 0.00015, 'DOC (mg/L)': 2, 
                    'Europium (mg/L)': 0.0001, 'Erbium (mg/L)': 0.000285, 'Fluoride (mg/L)': 4.0, 'pH': 8.5,
                    'Gadolinium (mg/L)': 0.000218, 'Gallium (mg/L)': 0.00001, 'Holmium (mg/L)': 0.000055, 'Iron (mg/L)': 0.3, 
                    'Lead (mg/L)': 0.015, 'Lithium (mg/L)': 0.04, 'Lanthanum (mg/L)':0.001749, 'Lutetium (mg/L)': 0.000169, 
                    'Mercury (mg/L)': 0.002, 'Magnesium (mg/L)': 10, 'Manganese (mg/L)': 0.3, 'Molybdenum (mg/L)': 0.04, 
                    'Nitrate (mg/L)': 10, 'Nickel (mg/L)': 0.1,'Neodymium (mg/L)': 0.0018, 'Praseodymium (mg/L)': 0.000071,
                    'Potassium (mg/L)': 165.6, 'Phosphorus (mg/L)': 0.1, 'Rubidium (mg/L)': 0.0006,'Selenium (mg/L)': 0.05, 
                    'Silica (mg/L)': 3.3, 'Sodium (mg/L)': 20, 'Samarium (mg/L)': 0.000094,'Tin (mg/L)': .010, 
                    'Titanium (mg/L)': 0.0005, 'Thallium (mg/L)': 0.002,  'Terbium (mg/L)': 0.000088, 'Tungsten (mg/L)': 0.0002,
                    'Thulium (mg/L)': 0.00022, 'Sulfate (mg/L)': 250, 'Sulfur (mg/L)': 250, 'Strontium (mg/L)': 4, 
                    'Silver (mg/L)': 0.1, 'TDS (mg/L)': 500, 'TSS (mg/L)': 155, 'TDN (mg/L)': 1, 'Uranium (mg/L)': 0.03, 
                    'Vanadium (mg/L)': 0.015, 'Yttrium (mg/L)': 0.001188, 'Ytterbium (mg/L)': 0.000195, 'Zinc (mg/L)': 5}
                    
    
    def cleanup(self):
        
        '''
        Function to remove NaN's and special characters from dataframe

        Inputs: 
        - Unedited dataframe

        Output:
        - Returns dataframe with no special characters or NaN's
        '''
    
        # Removes special characters from attributes
        #cols = self.df.columns
        special_character = ['<','>','--', 'ND', '\xa0']
        
        #Make dictionary of old name and new name
        newname = {}
        for col in self.cols:
            new = col
            
            #<add your logic checks on col here>
            for sc in special_character:
                new = new.replace(sc,' ')
            #Strip double spaces
            while '  ' in new:
                new=new.replace('  ',' ').strip()
            
            newname[col] = new
            
        self.df.rename(columns=newname,inplace=True)
        self.cols = list(newname.values()) #double check this<<
                
        # Converts all strings to floating-point numbers
        self.df[self.cols] = self.df[self.cols].apply(pd.to_numeric,errors='coerce') 
    
    
    def same_units(self):    
    
        '''
        Function that checks units of the water quality samples and returns dataframe with data displayed in units of mg/L
        Only works for µg/L - for other units, multiply dataframe values by the appropriate conversion factor

        Inputs:
        - Cleaned up DataFrame of water quality samples

        Output:
        - Returns DataFrame with samples in units of mg/L and sample names sorted in alphabetical order
        '''
        # Replaces µg/L with mg/L and performs appropriate unit conversion
        # To convert other units to mg/L, change the unit conversion factor in the code below

        newcols = self.cols.copy()
    
        for col in self.cols:
            if 'µg/L' in str(col):
                self.df[col.replace('µg/L','mg/L')] = self.df[col] * 0.001
                newcols.remove(col)
                newcols.append(col.replace('µg/L','mg/L'))
                
        self.cols = newcols
        new_df = self.df.filter(regex='mg/L')

        return new_df.sort_index(axis=1)
    
    def assessor(self):
        
        '''
        Function that loops through all samples in dataframe and compares values to maximum contaminant level (MCL)
        established by the EPA, then displays the samples that measured higher than its corresponding MCL.
        
        Inputs:
        - DataFrame of water quality samples

        Output:
        - Assessment of sample values compared to corresponding MCL of that metal
        '''
            
        for index, row in self.df.iterrows():
            for col in self.cols:
                if row[col] == np.nan: continue
                try:
                    self.df.at[index,col+'T'] = row[col] >= self.epa_standards[col]
                except IndexError:
                    value = None
                
        # Remove NaN's from dataframe
        self.df.fillna('', inplace=True)

    def print_exce(self):
    
        '''
        Function that lists the exceedances by frequency of occurence in descending order.
        
        Inputs:
        - DataFrame of water quality samples
        
        Output:
        - Returns ranked list of samples in descending order according to the exceedance frequency 
        '''
        global list_exce
        list_exce = []
        for index, row in self.df.iterrows():
            for col in self.cols: #iterrate through columns
                if row[col+'T']:
                    list_exce.append([index, col, round(row[col], 5)]) #adjust as needed
           
        df_exce = pd.DataFrame(list_exce, columns=['Sample_Number','Sample_Name','Concentration (mg/L)'])
        ranked_exce = df_exce['Sample_Name'].value_counts().sort_index(ascending=False).sort_values(ascending=False)
        return ranked_exce
    
    def plot_exce(self):
        '''
        Function that displays boxplots of the 4 samples with the largest ocurrence of exceedances
        
        Inputs:
        - Sorted DataFrame of the list of exceedances according to element frequency
        
        Output:
        - Box-and-Whisker plots of the 4 samples with the highest frequency of exceedances
        '''
        # Sort DataFrame by frequency of exceedances
        df_exce = pd.DataFrame(list_exce, columns=['Sample_Number','Sample_Name','Concentration (mg/L)'])
        df_exce['count'] = df_exce.groupby('Sample_Name')['Sample_Name'].transform('count')
        df_exce.sort_values(['count'], inplace=True, ascending=False)
        
        rowN = df_exce['Sample_Name'].unique().shape[0] / 2
        rowN = math.ceil(rowN)
        
        #Plot the top 4 elements with the highest frequency of exceedances
        plt.figure(figsize=(15, 5*rowN))
        plt.subplots_adjust(hspace=0.5)
        plt.suptitle('Top 4 Elements with Highest Frequency of Exceedances', fontsize=18, y=0.95)
        
        i=0
        for coc, group in df_exce.groupby('Sample_Name', sort=False):
            print(i,coc,group.shape[0])
            ax = plt.subplot(rowN, 2, i + 1)
            group.boxplot(by='Sample_Name',column='Concentration (mg/L)',ax=ax)
            ax.set_ylabel('Concentration (mg/L)')
            ax.set_xlabel('')
            i +=1
            if i == 4:
                break

