import sys
import os
from os import path
from PyQt5.QtWidgets import QApplication , QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUiType
from PIL import Image

FORM_CLASS,_ = loadUiType(path.join(path.dirname("__file__"),"main.ui"))

class my_form(QMainWindow,FORM_CLASS ):
        
    def __init__(self):
        
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.go_btn.clicked.connect(self.check_input)
        self.clear_btn.clicked.connect(self.clear_all)
        self.show()
        
        self.total_images = 0
        self.converted_images = 0
        self.failed_images = 0
        self.table_row = 0 # to keep track for the status table


    def check_input(self):
        
        # checking if the input is empty
        if self.directory_input.text() == "" or self.output_folder.text() =="" :
            self.error_label.setText("Input Error!")
        else:
            self.error_label.clear()
            
            # if the user enables the radio bottom, the program copies PNG
            # images first, then it converts JPG images
            self.copy_png_images() 
            self.convert_jpg()


    def copy_png_images(self):
        
        if self.copy_png.isChecked() :
            files = os.listdir(self.directory_input.text())
            for file_name in files :
                if file_name.endswith('.png') :
                    self.total_images += 1
                    try:
                        image_path = os.path.join(self.directory_input.text(), file_name)
                        image  = Image.open(image_path, mode='r')
                    except:
                        print ('error')
                    else:
                        save_path = os.path.join(self.output_folder.text(), file_name)
                        image.save(save_path)
                        self.print_to_table(file_name, save_path, self.table_row)
                        image.close()
                    self.table_row +=1 


    def convert_jpg(self):
        
        files = os.listdir(self.directory_input.text())
        for file_name in files:
            if file_name.endswith('.jpg') :
                self.total_images += 1
                try:
                    image_path = os.path.join(self.directory_input.text(), file_name)
                    image  = Image.open(image_path, mode='r')
                except:
                    print ('error')
                else:
                    image_name = file_name.split('.')[0]
                    image_full_name = image_name + '.png'
                    save_path = os.path.join(self.output_folder.text(), image_full_name)
                    image.save(save_path)
                    self.print_to_table(file_name, save_path, self.table_row)
                    image.close()
                self.table_row += 1 


    def print_to_table(self, image_name, image_full_path, table_index):
        
        image_name_cell = QTableWidgetItem(image_name)
        if os.path.exists(image_full_path) :
            # if the path exists, then the conversion process is done !
            status = "converted successfully!"
            self.converted_images += 1
            status_cell = QTableWidgetItem(status)
            self.table.setItem(table_index, 0 , image_name_cell)
            self.table.setItem(table_index, 1 , status_cell)
        else :
            status = "conversion error!"
            self.failed_images += 1 
            status_cell = QTableWidgetItem(status)
            self.table.setItem(table_index, 0 , image_name_cell)
            self.table.setItem(table_index, 1 , status_cell)
        self.total_images_label.setText("Total images in directory: " + str(self.total_images))
        self.converted_label.setText("Successfully converted: " + str(self.converted_images))
        self.conversion_failed_label.setText("Failed: " + str(self.failed_images))

    def clear_all(self):
        
        # reseting all widgets in the GUI
        self.converted_label.setText("")
        self.total_images_label.setText("")
        self.conversion_failed_label.setText("")
        self.directory_input.clear()
        self.output_folder.clear()
        self.error_label.clear()
        self.table.clear()
        self.table.setHorizontalHeaderLabels(["Image name", "Status"])


if __name__ == "__main__":
    application = QApplication(sys.argv)
    window = my_form()
    window.show()
    sys.exit(application.exec_())
    
# Osama Muhammad
# 25/7/2020