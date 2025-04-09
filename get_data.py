import pandas as pd


class GetSales:
    def __init__(self):
        self.cols_mapping = {
            'Type of Outward Supply':'Type of Outward Supply',
            'Type of Document':'Type of Document',
            'No':'Invoice No',
            'Date': "Invoice Date",
            'Taxable Value': 'Taxable Value',
            'Integrated Tax': 'IGST',
            'Central Tax': 'CGST',
            'State/Union Territory Tax':'SGST',
        }     
        self.cols_mapping_cdnr = {
            'Type of Outward Supply':'Type of Outward Supply',
            'Type of Document':'Type of Document',
            'No':'Note No',
            'Date': "Note Date",
            'Taxable Value': 'Taxable Value',
            'Integrated Tax': 'IGST',
            'Central Tax': 'CGST',
            'State/Union Territory Tax':'SGST',
        }

    def get_final_frame(self,dfs):
        
        new_dfs = []
        for df in dfs:
            # if else based on type of doc , for cdnr different mapping
            if 'Credit Note' in  df['Type of Document'].value_counts().keys() :
                # Filter only columns present in the current df
                available_mapping = {k: v for k, v in self.cols_mapping_cdnr.items() if v in df.columns}
                temp_df = df[list(available_mapping.values())].rename(columns={v: k for k, v in available_mapping.items()})
                temp_df['Date'] = pd.to_datetime(temp_df['Date']).dt.strftime('%d-%m-%Y')
            else:
                available_mapping = {k: v for k, v in self.cols_mapping.items() if v in df.columns}
                temp_df = df[list(available_mapping.values())].rename(columns={v: k for k, v in available_mapping.items()})
                if "Date" not in temp_df.columns:
                    temp_df["Date"] = ''
                
                if 'B2C-Small' in temp_df['Type of Outward Supply'].value_counts().keys() :
                    temp_df['No'] = 'B2COTH'
                    temp_df['Date'] = ''
                    # print(temp_df.info())
                    temp_df = self.condense_dataframe(temp_df)
                    
                # now here we have b2cs and b2b , so we ll check if it is b2cs we ll sum the data and add
            temp_df['Date'] = pd.to_datetime(temp_df['Date']).dt.strftime('%d-%m-%Y')
            print(temp_df.shape)
            new_dfs.append(temp_df)

        return pd.concat(new_dfs, ignore_index=True)
    
    def condense_dataframe(self,df):
        condensed_data = {}

        for col in df.columns:
            try:
                # Try converting column to numeric (force errors to NaN), then sum
                numeric_col = pd.to_numeric(df[col], errors='coerce')
                if numeric_col.notna().all():  # if all values are numeric
                    condensed_data[col] = numeric_col.sum()
                else:
                    raise ValueError  # treat as non-numeric
            except:
                # If conversion fails or not fully numeric, keep first value
                condensed_data[col] = df[col].iloc[0]

        return pd.DataFrame([condensed_data])
    
    def get_sales(self, file_path):
        
        purchase = pd.ExcelFile(file_path)
        sheet_dataframes = []
        for sheet in purchase.sheet_names:
            
            df = self.create_df(sheet_name=sheet,file_path=file_path)
            if sheet == 'B2CS':
                df['Type of Outward Supply'] = 'B2C-Small'
                df['Type of Document'] = 'Invoice/Bill of Entry'
            elif sheet == 'CDNR' :
                df['Type of Outward Supply'] = 'B2B'
                df['Type of Document'] = 'Credit Note'
            elif sheet == 'B2B':
                df['Type of Outward Supply'] = 'B2B'
                df['Type of Document'] = 'Invoice/Bill of Entry'



            if sheet != 'EXP':
                print(sheet)
                sheet_dataframes.append(df)

        return sheet_dataframes
    
    def create_df(self,sheet_name,file_path):
        df = pd.read_excel(file_path,header=None,sheet_name=sheet_name)
        start_index = 0
        for row in df.itertuples():
            if  'Return Period' in row:
                start_index =row.Index
        frame = df.loc[start_index+1:]
        column_names = df.loc[start_index]
        frame.columns = column_names
        return frame
    
    
    
class GetPurchase:
    def __init__(self):
        self.cols_mapping_b2b:dict = {
            'Type of Inward Supply':'Type of Inward Supply',
            'GSTIN of Supplier/Self GSTIN':'GSTIN of supplier',
            'Type of Document':'Type of Document',
            'No./B/E': 'Invoice No',
            'Date': 'Invoice Date',
            "Port Code":"Port Code",
            'Taxable Value': 'Taxable Value',
            'Integrated Tax': 'IGST',
            'Central Tax': 'CGST',
            'State/Union Territory Tax':"SGST"
                
        }

        self.cols_mapping_cdnr = {
            'Type of Inward Supply':'Type of Inward Supply',
            'GSTIN of Supplier/Self GSTIN':'GSTIN of supplier',
            'Type of Document':'Type of Document',
            'No./B/E': 'Note No',
            'Date': 'Note Date',
            "Port Code":"Port Code",
            'Taxable Value': 'Taxable Value',
            'Integrated Tax': 'IGST',
            'Central Tax': 'CGST',
            'State/Union Territory Tax':"SGST"       
        }
        self. cols_mapping_impg = {
            'Type of Inward Supply':'Type of Inward Supply',
            'GSTIN of Supplier/Self GSTIN':'GSTIN of supplier',
            'Type of Document':'Type of Document',
            'No./B/E': 'Bill Number',
            'Date': 'Bill Date',
            "Port Code":"Port Code",
            'Taxable Value': 'Taxable Value',
            'Integrated Tax': 'IGST',
            # 'Central Tax': 'CGST',
            # 'State/Union Territory Tax':"SGST"        
        }
    def get_final_frame(self,dfs):
        new_dfs = []
        for df in dfs:
            # if else based on type of doc , for cdnr different mapping
            if 'Credit Note' in  df['Type of Document'].value_counts().keys() :
                # Filter only columns present in the current df
                available_mapping = {k: v for k, v in self.cols_mapping_cdnr.items() if v in df.columns}
                temp_df = df[list(available_mapping.values())].rename(columns={v: k for k, v in available_mapping.items()})
            else:
                if 'Inward Supply from Registered Person' in df['Type of Inward Supply'].value_counts().keys():
                    available_mapping = {k: v for k, v in self.cols_mapping_b2b.items() if v in df.columns}
                    temp_df = df[list(available_mapping.values())].rename(columns={v: k for k, v in available_mapping.items()})
                else:
                    available_mapping = {k: v for k, v in self.cols_mapping_impg.items() if v in df.columns}
                    temp_df = df[list(available_mapping.values())].rename(columns={v: k for k, v in available_mapping.items()})
                    df['Central Tax'] = ''
                    df['State/Union Territory Tax'] = ''

            temp_df['Date'] = pd.to_datetime(temp_df['Date']).dt.strftime('%d-%m-%Y')
            print(temp_df.shape)
            new_dfs.append(temp_df)

        return pd.concat(new_dfs, ignore_index=True)
    
    def get_purchase(self,file_path):
        purchase = pd.ExcelFile(file_path)
        sheet_dataframes = []
        for sheet in purchase.sheet_names:
            
            df = self.create_df(sheet_name=sheet,file_path=file_path)
            ## adding port code as impg contains it , rest dont , so later they can be easily joined
            if sheet == 'B2B':
                df['Type of Inward Supply'] = 'Inward Supply from Registered Person'
                df['Type of Document'] = 'Invoice/Bill of Entry'
                df['Port Code'] = ''
            elif sheet == 'CDNR':
                df['Type of Inward Supply'] = 'Inward Supply from Registered Person'
                df['Type of Document'] = 'Credit Note'
                df['Port Code'] = ''
            elif sheet == 'IMPG':
                df['Type of Inward Supply'] = 'Import of Goods/Supplies from SEZ to DTA'
                df['Type of Document'] = 'Invoice/Bill of Entry'
                
            print(sheet)
            sheet_dataframes.append(df)

        return sheet_dataframes
    
    def create_df(self,sheet_name,file_path):
        df = pd.read_excel(file_path,header=None,sheet_name=sheet_name)
        start_index = 0
        for row in df.itertuples():
            if  'Period' in row:
                start_index =row.Index
        frame = df.loc[start_index+1:]
        column_names = df.loc[start_index]
        frame.columns = column_names
        return frame
    
    


    



# class GetInfo:
#     def __init__(self):
#         self.infodict = {}

#     def get_info(self,file_path):
#         excel = pd.read_excel(file_path)
#         print(excel)

