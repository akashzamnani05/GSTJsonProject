import pandas as pd 


def change_purchase_column_name(df):
    new_columns = ['Type of Inward Supply',
            'GSTIN of Supplier/Self GSTIN',
            'Type of Document',
            'No./B/E',
            'Date Sales',
            "Port Code",
            'Taxable Value Sales',
            'Integrated Tax Sales',
            'Central Tax Sales',
            'State/Union Territory Tax Sales']
    
    df.columns = new_columns
    return df


def change_sale_column_name(df):
    new_columns = ['Type of Outward Supply',
            'Type of Document',
            'No',
            'Date Purchase',
            'Taxable Value Purchase',
            'Integrated Tax Purchase',
            'Central Tax Purchase',
            'State/Union Territory Tax Purchase']
    
    df.columns = new_columns
    return df