import json 
import pandas as pd
import numpy as np
import os 
import io



class GetJson:
    def __init__(self, final_df, metadata):
        # self.mapping = {
        #     'Type of Inward Supply':'istype',
        #     'GSTIN of Supplier/Self GSTIN':'stin',
        #     'Type of Document':'idtype',
        #     'No./B/E':'inum',
        #     'Date':'idt',
        #     'Port Code':'portcd',
        #     'Taxable Value':'val',
        #     'Integrated Tax':'iamt',
        #     'Central Tax':'camt',
        #     'State/Union Territory Tax':'samt',
        #     'Type of Outward Supply':'ostype',
        #     'Type of Document':'odtype',
        #     'No':'oinum',
        #     'Dateo':'oidt',

        # }
        self.new_columns = ["istype","stin","idtype","inum","idt","portcd","val","iamt","camt","samt","ostype","odtype","oinum","oidt","oval","oiamt","ocamt","osamt"]
        self.final_df = final_df
        self.metadata = metadata


    def get_json(self):
        self.final_df.columns = self.new_columns
        data_records = [
            {"sno": i + 1, **{k: v for k, v in row.items() if pd.notna(v)}}
            for i, row in enumerate(self.final_df.to_dict(orient='records'))
        ]

        # Combine both
        final_json = self.metadata.copy()
        final_json["stmt01A"] = data_records

        return final_json

        
    def get_json_file(self):
        final_json = self.get_json()  # use the above method

        # Create in-memory file-like object
        json_str = json.dumps(final_json, indent=4)
        json_bytes = io.BytesIO(json_str.encode("utf-8"))
        json_bytes.name = "output.json"

        return json_bytes