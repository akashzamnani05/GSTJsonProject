import pandas as pd 
from get_data import GetPurchase,GetSales
from get_json import GetJson
from utils import change_purchase_column_name,change_sale_column_name



if __name__=="__main__":
    metadata = {"gstin":"27AACCR2605R1Z1","fromFp":"012024","toFp":"032024","refundRsn":"INVITC","version":"2.0"}
        
    pur = GetPurchase(metadata=metadata)
    sales = GetSales()


    ## for purhcase
    dfs_pur = pur.get_purchase('Refund Application/1_Purchase Report.xlsx')
    purchase_df = pur.get_final_frame(dfs=dfs_pur)

    ## for sale 
    dfs_sale = sales.get_sales('Refund Application/2_Sales Report.xlsx')
    sales_df = sales.get_final_frame(dfs=dfs_sale)

    sales_df = change_sale_column_name(sales_df)
    purchase_df = change_purchase_column_name(purchase_df)

    # print(sales_df.columns)
    # print(purchase_df.columns)

    final_frame = pd.concat([purchase_df, sales_df], axis=1)
    final_frame.to_excel('final1.xlsx')

    # print(final_frame.tail())
    # print(final_frame.shape)

    json = GetJson(final_df=final_frame,metadata=metadata)
    # print(json.get_json())