import os
import logging
from PyPDF2 import PdfFileMerger
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window


Builder.load_file("main.kv")
logging.basicConfig(filename="find_and_merge_pdf.log")

class MyLayout(Widget):
    no_pdf = 0
    all_pdf = []
    
    try:
        def pdfFile_filter(self):
            logging.info("Searching for pdf files....")
            pdf_files = []
            self.ids.file_name.text = ""
            DIR_WITH_FILES = self.ids.search_input.text.replace("\\", "/")
            logging.info(f"Inputed PATH: {DIR_WITH_FILES}")
            list_pdf_file = [f for f in sorted(os.listdir(DIR_WITH_FILES)) if ((str(f))[-3:] == "pdf" or (str(f))[-3:] == "PDF")]
            list_pdf_with_path=[DIR_WITH_FILES+'/'+str(f) for f in list_pdf_file]
            self.all_pdf = list_pdf_with_path
            
            for i in range(len(list_pdf_with_path)):
                pdf_files.append(list_pdf_with_path[i].split('//')[1])
            self.no_pdf = len(self.all_pdf)
            self.ids.file_name.text = str(pdf_files[-len(list_pdf_with_path):]).replace(f",", "\n")
            logging.info(f"All the pdfs found in this PATH: {pdf_files[-len(list_pdf_with_path):]}")
        
        def merge_pdf(self):
            logging.info("Merging PDFs....")
            merger = PdfFileMerger()
            if self.no_pdf > 1:
                for pdf in self.all_pdf:
                    logging.info(f"Merging {pdf}")
                    merger.append(pdf)
                self.ids.file_name.font_size= 25
                self.ids.file_name.text = "Merged Successfully!!"    
                merger.write(self.ids.merge_input.text)
                merger.close()
                logging.info("Merged Successfully!!")
            else:
                logging.info("You have only 1 pdf file. Failed to merge!!")
    except Exception as e:
        print("An exception occured: ", e)
    

class PDF_FinderApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return MyLayout()

if __name__ == '__main__':
    PDF_FinderApp().run()