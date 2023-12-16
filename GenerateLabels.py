#!/usr/bin/env python3
from utilities import Document
from templates import *
from components import *



def create_document():
    # Set the name of the file to be created
    file_name = "Labels.pdf"

    # Select the correct type of paper you want to print on.  Current layouts are "Avery_5260", "Avery_L7157", "EJ_Range_24"
    sheet_layout = "Avery_5260"

    # Select your font; built in fonts are "Helvetica", "Times-Roman", "Courier", "Symbol", "ZapfDingbats"
    default_font = "Arial-Bold"

    # Select your font size
    default_font_size = 12

    # Indicate whether you want outlines around the labels
    label_outlines = True

    # Indicate whether you want to fill the page with labels
    fill_page = True





    return Document(sheet_layout, file_name).configure(default_font=default_font, default_font_size=default_font_size, label_outlines=label_outlines, fill_page=fill_page)



def main() -> None:

    

    create_document().render()



if __name__ == "__main__":
    main()
