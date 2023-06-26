from nltk.tokenize import sent_tokenize
# import tabula
# tabula.read_pdf(file, pages = "all", multiple_tables = True, stream = True)
import camelot
import PyPDF2
import json
import pandas as pd
import numpy as np

class Preprocessor():
    def __init__(self, file) -> None:
        # pass pdf file here, will get preprocessed
        self.pdf_file = file
        pass

    def make_text(self, table, lim, rows, cols):
        text = []
        for column in range(1, cols):
            column_data = ""
            for i in range(lim):
                column_data += ' ' + table[f"{column}"][f"{i}"]
            
            for row in range(lim, rows):
                data = table[f"{column}"][f"{row}"]
                if data != "$" and data != "":
                  row_data = table[f"{0}"][f"{row}"]
                  text.append(f"{column_data} {row_data} : {data}.")
                
        return text

    def convert_table_to_text(self, table):
        df = pd.read_json(table)
        # print(df)
        rows, cols = df.shape
        table = json.loads(table)

        column_headers = []
        if table[f"0"][f"0"] != "":
            for column in range(cols):
                count = 0
                for row in range(1, rows):
                    if table[f"{column}"][f"{row}"] == "":
                        count+=1
                    else:
                        break
                column_headers.append(count+1)

        else:
            for column in range(cols):
                count = 0
                for row in range(rows):
                    if table[f"{column}"][f"{row}"] == "":
                        count+=1
                    else:
                        break
                column_headers.append(count)

        # take these 3 to create columns header
        column_lim = column_headers[0]
        
        text_as_list = self.make_text(table, column_lim, rows, cols)

        
        return text_as_list
    
    def read_tables(self, pdf_file):
        file = pdf_file
        lis = []
        tables = camelot.read_pdf(file, pages = 'all', flavor = 'stream', edge_tol=200)
        # print all the tables in the file
        for t in range(tables.n):
            if tables[t].df.shape[1] <= 3:
                continue
            lis.append((tables[t].df).to_json())

        text_list = []

        for item in lis:
            temp_lis = self.convert_table_to_text(item)
            # print(temp_lis)
            # print('\n\n\n\n\n\n')
            text_list.extend(temp_lis)

        # print('\n\n'.join(text_list))
        return '\n\n'.join(text_list)
    
    def read_pdf(self, pdffile):
        fulltext = ''
        reader = PyPDF2.PdfReader(pdffile)
        for page in reader.pages:
            text = page.extract_text()
            fulltext += text

        return fulltext

    def get_full_text(self):
        normal_text = self.read_pdf(self.pdf_file)
        table_text = self.read_tables(self.pdf_file)

        full_text = normal_text + '\n' + table_text
        full_text = sent_tokenize(full_text)
        full_text = np.array(full_text)
        
        return full_text
