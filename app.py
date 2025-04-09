import streamlit as st
from get_data import GetPurchase,GetSales
from get_json import GetJson
from utils import change_purchase_column_name,change_sale_column_name
import pandas as pd

st.title("GST JSON Generator")

gstin = st.text_input("Enter GSTIN")
fromfp = st.text_input("Enter From FP (Format: MMYYYY)")
tofp = st.text_input("Enter To FP (Format: MMYYYY)")

st.markdown("### Upload Excel Files")
# info_file = st.file_uploader("Upload Info Excel", type=["xlsx", "xls"])
purchase_file = st.file_uploader("Upload Purchase Excel", type=["xlsx", "xls"])
sales_file = st.file_uploader("Upload Sales Excel", type=["xlsx", "xls"])





# Button to generate JSON
if st.button("Give JSON"):
    if not gstin or not fromfp or not tofp:
        st.error("Please fill in all required fields (GSTIN, From FP, To FP).")
    elif not tofp or not purchase_file or not sales_file:
        st.error("Please upload all three Excel files.")
    else:
        metadata = {'gstin':gstin,'fromFp':fromfp,"toFp":tofp,"refundRsn":"INVITC","version":"2.0"}

        pur = GetPurchase(metadata=metadata)
        sales = GetSales()

        ## for purhcase
        dfs_pur = pur.get_purchase(purchase_file)
        purchase_df = pur.get_final_frame(dfs=dfs_pur)

        ## for sale 
        dfs_sale = sales.get_sales(sales_file)
        sales_df = sales.get_final_frame(dfs=dfs_sale)

        sales_df = change_sale_column_name(sales_df)
        purchase_df = change_purchase_column_name(purchase_df)

        # print(sales_df.columns)
        # print(purchase_df.columns)

        final_frame = pd.concat([purchase_df, sales_df], axis=1)

        json = GetJson(final_df=final_frame,metadata=metadata)
        json_file = json.get_json_file()
        st.download_button(
        label="Download JSON",
        data=json_file,
        file_name="output.json",
        mime="application/json"
    )