# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 22:49:01 2021

@author: Team B 2022
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
import holoviews as hv; hv.extension('bokeh', 'matplotlib')
import pandas as pd
pd.options.plotting.backend = 'holoviews'

class BrushingDataframe(pd.DataFrame):
    """
    The class is used to extend the properties of Dataframes to a prticular
    type of Dataframes in the Risk Indistry. 
    It provides the end user with both general and specific cleaning functions, 
    though they never reference a specific VARIABLE NAME.
    
    It facilitates the End User to perform some Date Feature Engineering,
    Scaling, Encoding, etc. to avoid code repetition.
    """

    #Initializing the inherited pd.DataFrame
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
    
    @property
    def _constructor(self):
        def func_(*args,**kwargs):
            df = BrushingDataframe(*args,**kwargs)
            return df
        return func_
    
#-----------------------------------------------------------------------------
                        # DATA HANDLING
#-----------------------------------------------------------------------------

    def SetAttributes(self, kwargs):
        """
        The function will update the type of the variable submitted for change.
        It will veify first that the key is present in the desired dataframe.
        If present, it will try to change the type to the desired format.
        If not possible, it will continue to the next element.         
        Parameters
        ----------
        **kwargs : The key-argument pair of field-type relationship that
        wants to be updated.
        Returns
        -------
        None.
        """
        if self.shape[0] > 0:
            for key,vartype in kwargs.items():
                if key in self.columns:
                    try:
                        self[key] = self[key].astype(vartype)
                    except:
                        print("Undefined type {}".format(str(vartype)))
                else:
                    print("The dataframe does not contain variable {}.".format(str(key)))
        else:
            print("The dataframe has not yet been initialized")

#-----------------------------------------------------------------------------
                        # SUPERVISED - BINARY CLASSIFICATION - DATA CLEANING
#-----------------------------------------------------------------------------    
    def cleaning_missing(self, input_vars=[] ):
        """
        TO BE IMPLEMENTED: data cleaning (provide methods for data scanning and cleaning, 
            for example: scan each column, indicating if droping or keeping the variable for 
            modelling and why, for the ones keeping indicates which cleaning / transformation 
            is recommended for the missing values and if scalling / dummy creation is recommended, 
            if not always inform that is not necessary);
        Returns
        -------
          A print with the analysis or new clean columns .

        """
        if input_vars:
            self = self[input_vars]
            
        for column in self.columns.values:
        # Replace NaNs with the median or mode of the column depending on the column type
            try:
                self[column].fillna(self[column].median(), inplace=True)
            except TypeError:
                most_frequent = self[column].mode()
                if len(most_frequent) > 0:
                    self[column].fillna(self[column].mode()[0], inplace=True)
                else:
                    self[column].fillna(method='bfill', inplace=True)
                    self[column].fillna(method='ffill', inplace=True)
   
        return self
    def cleaning_missing_display(self, input_vars=[] ):
       
        """
        TO BE IMPLEMENTED: data cleaning (provide methods for data scanning and cleaning, 
            for example: scan each column, indicating if droping or keeping the variable for 
            modelling and why, for the ones keeping indicates which cleaning / transformation 
            is recommended for the missing values and if scalling / dummy creation is recommended, 
            if not always inform that is not necessary);
        Returns
        -------
          A print with the analysis or new clean columns .

        """
        if input_vars:
            self = self[input_vars]
        ## Check Null Values    
        null_df = self.isna().sum().to_frame("Null Counts")
        null_df = null_df.loc[null_df ['Null Counts']>0].rename_axis('Features').reset_index()
        null_table = hv.Table(null_df, label='Features with Null Values')
        ## Check data types
        types_df  = self.dtypes.to_frame("Data Types").rename_axis('Features').reset_index()
        types_df ["Data Types"] = types_df ["Data Types"].astype(str)
        types_df.loc[(types_df['Features'].str.contains("date", case=False)) |(types_df['Features'].str.contains("year", case=False))
        |(types_df['Features'].str.contains("month", case=False)),"Recomendation"] = "Consider convert to Date or Time type"
        types_df = types_df.fillna("")
        typ_table = hv.Table(types_df , label='Features data types')
        ## Plot Histogram for numericals
        hist_plots = []
        for column in self._get_numeric_data().columns:
            hist_plots.append(self[column].plot.hist(bins=100, bin_range=(0, self[column].max()), title='Histogram and Box Plot ' + column, width=500))
            hist_plots.append(self[column].plot.box(invert=True, width=500).opts(xrotation=90))
        histplots = hv.Layout(hist_plots).cols(2)
        ## Plot for categorical
        cat_plots = []
        for column in self.select_dtypes(include=['object']).dtypes.index:
            if self[column].nunique() < 25:
                cat_plots.append(self[column].value_counts().sort_index().plot.bar(title=column, xlabel=column,ylabel='counts', width=800, height=350))
        catplots = hv.Layout(cat_plots)
        p = (null_table.opts(height=100) + typ_table.opts(width=800, height=400) + histplots + catplots ).cols(1)
        return p
    
 
    def recommended_transformation(self, input_vars=[], target='' ):
        """

        TO BE IMPLEMENTED: data preparation (for each column provide methods to perform
        transformations - for example: time calculation like age, days as customers, 
        days to due date, label encoding, imputation, standard scalling, dummy creation 
        or replacement of category value by its probability of default depending, justify 
        transformation depending of the variable type, or explain why transformation is 
        not necessary);

        Returns
        -------
          A print with the analysis or new transformed columns.                
        """
        return "To be implemented."
    