import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import KNNImputer
import warnings

def fahrToKelv(temp):
    '''
    takes a temperature `temp` in fahrenheit and returns it in Kelvin
    '''

    kelvin = 5./9. * (temp - 32.) + 273.15

    return kelvin


def NumericalTransformation(df, col = [], na_treat = 'keep', na_fill = 0, knn_neighbors = 5, out_treat = False, 
                            out_upper = 0.75, out_lower = 0.25, scaling='no'):
    
    # The following section will test the paramters
    if str(type(df)) != "<class 'pandas.core.frame.DataFrame'>":
        raise TypeError('Error: df is not a valid pandas datafram')
    if str(type(col)) != "<class 'list'>":
        raise TypeError('Error: paramter col must be a list')
    if str(type(na_treat)) != "<class 'str'>":
        raise TypeError('Error: paramter na_treat must be a string')
    if not(str(type(na_fill)) == "<class 'int'>" or str(type(na_fill)) == "<class 'float'>"):
        raise TypeError('Error: paramter na_fill must be a number')
    if str(type(knn_neighbors)) != "<class 'int'>":
        raise TypeError('Error: paramter knn_neighbors must be an integer')
    if str(type(out_treat)) != "<class 'bool'>":
        raise TypeError('Error: paramter out_treat must be a boolean')
    if not(str(type(out_upper)) == "<class 'int'>" or str(type(out_upper)) == "<class 'float'>") or out_upper <= 0 or out_upper > 1:
        raise TypeError('Error: paramter out_upper must be a number grater than 0 and less than or equal to 1')
    if not(str(type(out_lower)) == "<class 'int'>" or str(type(out_lower)) == "<class 'float'>") or out_lower < 0 or out_lower >= 1:
        raise TypeError('Error: paramter out_lower must be a number grater than or equal to 0 and less than 1')
    if str(type(scaling)) != "<class 'str'>":
        raise TypeError('Error: paramter scaling must be a string')
        
    # The following section will scan the data types of the columns looking for numerical columns.
    
    if col == []:
        for c in df.columns:
            if df[c].dtype.name == 'int64' or df[c].dtype.name == 'float64':
                col.append(c)
    else:
        for c in col:
            if not(df[c].dtype.name == 'int64' or df[c].dtype.name == 'float64'):
                raise TypeError('Error: column ' + c + ' is not numeric')

            
#------------------------------------------------------------------
    
# The following section will treat the na values of the columns
    
    if na_treat == 'drop':                    # If na_treat = 'drop', all NaN values for the specified columns will be droped
        df = df.dropna(subset = col)
        
    elif na_treat == 'mean':                  # If na_treat = 'mean', all NaN values for the specified columns will be replaced with the column average
        for c in col:
            mean = df[c].mean()
            df.loc[:, c].fillna(mean, inplace=True)
            
    elif na_treat == 'mode':                  # If na_treat = 'mode', all NaN values for the specified columns will be replaced with the column mode
        for c in col:
            mode = df[c].mode()
            df.loc[:, c].fillna(mode, inplace=True)
            
    elif na_treat == 'min':                   # If na_treat = 'min', all NaN values for the specified columns will be replaced with the column minimum
        for c in col:
            mini = df[c].min()
            df.loc[:, c].fillna(mini, inplace=True)
            
    elif na_treat == 'max':                   # If na_treat = 'max', all NaN values for the specified columns will be replaced with the column maximum
        for c in col:
            maxi = df[c].max()
            df.loc[:, c].fillna(maxi, inplace=True)
            
    elif na_treat == 'fill':                  # If na_treat = 'fill', all NaN values for the specified columns will be replaced with the na_fill value (default is 0)
        for c in col:
            df.loc[:, c].fillna(na_fill, inplace=True)
            
    elif na_treat == 'knn_fill':              # If na_treat = 'knn_fill', all NaN values for the specified columns will be imputed using knn regressor
        imputer = KNNImputer(n_neighbors=knn_neighbors, copy = True)
        for c in col:
            df[c] = np.round_(imputer.fit_transform(df[[c]]))

        
    elif na_treat == 'keep':                  # If na_treat = 'keep', all NaN values for the specified columns will be kept with no change
        pass
        
    else:
        raise TypeError('Error: The na_treat variable ' + na_treat + ' is not a valid')

    #---------------------------------------------------------------------------------------------------    
    
    # The following section will treat outliers using tukey method
    
    if out_treat:
        if out_upper > out_lower and out_upper <= 1 and out_lower >= 0:
            upper_lower_dic = {}
            for c in col:
                Q3 = df[c].quantile(out_upper)
                Q1 = df[c].quantile(out_lower)
                IQR = Q3 - Q1
                lower_lim = Q1 - 1.5 * IQR
                upper_lim = Q3 + 1.5 * IQR
                upper_lower_dic[c+'_L'] = lower_lim
                upper_lower_dic[c+'_U'] = upper_lim
            for c in col:
                df.drop(df[df[c] < upper_lower_dic[c+'_L']].index, inplace=True)
                df.drop(df[df[c] > upper_lower_dic[c+'_U']].index, inplace=True)
                
        else:
            raise TypeError('Error: parameters out_upper and/or out_lower are not valid')
    #---------------------------------------------------------------------------------------------------
    
    # The following section will perform scaling
    if scaling == 'StandardScaler':
        scaler = StandardScaler()
        df[col] = scaler.fit_transform(df[col])
    elif scaling == 'MinMaxScaler':
        scaler = MinMaxScaler()
        df[col] = scaler.fit_transform(df[col])
    elif scaling == 'no':
        pass
    else:
        raise TypeError('Error: scaler ' + scaling + ' is not valid')
    #---------------------------------------------------------------------------------------------------
    
    # Return the final dataframe
    return df


#*********************************************
def CategoricalNominalTransformation(df, col = [], na_treat = 'keep', na_fill = 'missing', knn_neighbors = 5, 
                                     transform = False, maximum_cat = 10, start_from = 0, increment_by = 1):
    
    
    # The following section will test the paramters
    if str(type(df)) != "<class 'pandas.core.frame.DataFrame'>":
        raise TypeError('Error: df is not a valid pandas datafram')
    if str(type(col)) != "<class 'list'>":
        raise TypeError('Error: paramter col must be a list')
    if str(type(na_treat)) != "<class 'str'>":
        raise TypeError('Error: paramter na_treat must be a string')
    if str(type(na_fill)) != "<class 'str'>":
        raise TypeError('Error: paramter na_fill must be a string')
    if str(type(knn_neighbors)) != "<class 'int'>":
        raise TypeError('Error: paramter knn_neighbors must be an integer')
    if str(type(transform)) != "<class 'bool'>":
        raise TypeError('Error: paramter transform must be a boolean')
    if str(type(maximum_cat)) != "<class 'int'>" or maximum_cat < 0:
        raise TypeError('Error: paramter maximum_cat must be an integer number greater than or equal to 0')
    if not(str(type(start_from)) == "<class 'int'>" or str(type(start_from)) == "<class 'float'>"):
        raise TypeError('Error: paramter start_from must be a number')
    if not(str(type(increment_by)) == "<class 'int'>" or str(type(increment_by)) == "<class 'float'>"):
        raise TypeError('Error: paramter increment_by must be a number')
        
    # The following section will scan the data types of the columns looking for catagorical columns.
    if col == []:
        for c in df.columns:
            if df[c].dtype.name == 'object' or df[c].dtype.name == 'category':
                col.append(c)
                

    #---------------------------------------------------------------------------------------------------
    
    # The following section will treat the na values of the columns
    knn = False
    if na_treat == 'drop':                    # If na_treat = 'drop', all NaN values for the specified columns will be droped
        df = df.dropna(subset = col)
            
    elif na_treat == 'mode':                  # If na_treat = 'mode', all NaN values for the specified columns will be replaced with the column mode
        for c in col:
            mode = df[c].mode()
            df.loc[:, c].fillna(mode[0], inplace=True)
            
    elif na_treat == 'fill':                  # If na_treat = 'fill', all NaN values for the specified columns will be replaced with the na_fill value (default is 'missing')
        for c in col:
            df.loc[:, c].fillna(na_fill, inplace=True)
            
    elif na_treat == 'knn_fill':              # If na_treat = 'knn_fill', all NaN values for the specified columns will be imputed using knn regressor This step will be done after transformation
        knn = True
        
    elif na_treat == 'keep':                  # If na_treat = 'keep', all NaN values for the specified columns will be kept with no change
        pass
        
    else:
        raise TypeError('Error: The na_treat variable ' + na_treat + ' is not a valid')
    #---------------------------------------------------------------------------------------------------
    
    if transform:
        dropped_col = []
        for c in col:
            if len(df[c].unique()) <= maximum_cat: 
                df_in = df
                ohe = OneHotEncoder(sparse=False, drop='first')
                ohe.fit(df_in[[c]])
                df = pd.DataFrame(ohe.transform(df_in[[c]]),
                columns = ohe.get_feature_names([c]))
                df.set_index(df_in.index, inplace=True)
                df = pd.concat([df_in, df], axis=1).drop([c], axis=1)
                dropped_col.append(c)
            else:
                for i in range(start_from,(len(df[c].unique())*increment_by) + start_from, increment_by):
                    df.loc[df[c] == df[c].unique()[int((i-start_from)/increment_by)], c] = i
            col = list(set(col)-set(dropped_col))
                    
    if knn: # If na_treat = 'knn_fill', all NaN values for the specified columns will be imputed using knn
        imputer = KNNImputer(n_neighbors=knn_neighbors, copy = True)
        for c in col:
            df[c] = np.round_(imputer.fit_transform(df[[c]]))



    #---------------------------------------------------------------------------------------------------
    
    # Return the final dataframe
    return df
#*********************************************
def CategoricalOrdinalTransformation(df, col = [], na_treat = 'keep', na_fill = 'missing', knn_neighbors = 5, 
                                     transform = False, cat_dict = 'auto', start_from = 0, increment_by = 1):
    
    # The following section will test the paramters
    if str(type(df)) != "<class 'pandas.core.frame.DataFrame'>":
        raise TypeError('Error: df is not a valid pandas datafram')
    if str(type(col)) != "<class 'list'>":
        raise TypeError('Error: paramter col must be a list')
    if str(type(na_treat)) != "<class 'str'>":
        raise TypeError('Error: paramter na_treat must be a string')
    if str(type(na_fill)) != "<class 'str'>":
        raise TypeError('Error: paramter na_fill must be a string')
    if str(type(knn_neighbors)) != "<class 'int'>":
        raise TypeError('Error: paramter knn_neighbors must be an integer')
    if str(type(transform)) != "<class 'bool'>":
        raise TypeError('Error: paramter transform must be a boolean')
    if not(str(type(cat_dict)) == "<class 'dict'>" or str(type(cat_dict)) == "<class 'str'>"):
        raise TypeError("Error: paramter cat_dict must be a dictionary or 'auto'")
    if not(str(type(start_from)) == "<class 'int'>" or str(type(start_from)) == "<class 'float'>"):
        raise TypeError('Error: paramter start_from must be a number')
    if not(str(type(increment_by)) == "<class 'int'>" or str(type(increment_by)) == "<class 'float'>"):
        raise TypeError('Error: paramter increment_by must be a number')
    
    # The following section will scan the data types of the columns looking for catagorical columns.
    if col == []:
        for c in df.columns:
            if df[c].dtype.name == 'object' or df[c].dtype.name == 'category':
                col.append(c)

    #---------------------------------------------------------------------------------------------------
    
    # The following section will treat the na values of the columns
    knn = False
    if na_treat == 'drop':                    # If na_treat = 'drop', all NaN values for the specified columns will be droped
        df = df.dropna(subset = col)
            
    elif na_treat == 'mode':                  # If na_treat = 'mode', all NaN values for the specified columns will be replaced with the column mode
        for c in col:
            mode = df[c].mode()
            df.loc[:, c].fillna(mode[0], inplace=True)
            
    elif na_treat == 'fill':                  # If na_treat = 'fill', all NaN values for the specified columns will be replaced with the na_fill value (default is 'missing')
        for c in col:
            df.loc[:, c].fillna(na_fill, inplace=True)
            
    elif na_treat == 'knn_fill':              # If na_treat = 'knn_fill', all NaN values for the specified columns will be imputed using knn regressor This step will be done after transformation
        knn = True
        
    elif na_treat == 'keep':                  # If na_treat = 'keep', all NaN values for the specified columns will be kept with no change
        pass
        
    else:
        raise TypeError('Error: The na_treat variable ' + na_treat + ' is not a valid')
    #---------------------------------------------------------------------------------------------------
    
    if transform:
        if cat_dict == 'auto':
            for c in col:
                c_list = sorted(x for x in df[c].unique() if pd.isnull(x) == False)   
                for i in range(start_from,(len(c_list) * increment_by) + start_from, increment_by):
                    df.loc[df[c] == c_list[int((i-start_from)/increment_by)], c] = i
        else:
            for c in col:
                df[c] = df[c].replace(cat_dict)
                    
    if knn:                                   # If na_treat = 'knn_fill', all NaN values for the specified columns will be imputed using knn regressor
        imputer = KNNImputer(n_neighbors=knn_neighbors, copy = True)
        for c in col:
            df[c] = np.round_(imputer.fit_transform(df[[c]]))


    #---------------------------------------------------------------------------------------------------
    
    # Return the final dataframe
    return df