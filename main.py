import pandas as pd 
from get_data import GetPurchase,GetSales
from get_json import GetJson



if __name__=="__main__":
    pur = GetPurchase()
    sales = GetSales()

    ## for purhcase
    dfs_pur = pur.get_purchase('Refund Application/1_Purchase Report.xlsx')
    purchase_df = pur.get_final_frame(dfs=dfs_pur)

    ## for sale 
    dfs_sale = sales.get_sales('Refund Application/2_Sales Report.xlsx')
    sales_df = sales.get_final_frame(dfs=dfs_sale)

    final_frame = pd.concat([purchase_df, sales_df], axis=1)
    final_frame.to_excel('final1.xlsx')

    print(final_frame.tail())
    print(final_frame.shape)

    metadata = {"gstin":"27AACCR2605R1Z1","fromFp":"012024","toFp":"032024","refundRsn":"INVITC","version":"2.0"}

    json = GetJson(final_df=final_frame,metadata=metadata)
    print(json.get_json())