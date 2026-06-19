import csv
import os
import pandas as pd
import skimage
from PySide6.QtCore import QFileInfo
from PySide6.QtWidgets import QFileDialog, QWidget
from fpdf import FPDF

from GraphicItems.VAP_Point import VAP_Point


class ImageOperation(object):

    @staticmethod
    def LoadImages(parentWidget:QWidget):

        dlg = QFileDialog(parentWidget)
        dlg.setFileMode(QFileDialog.ExistingFiles)
        dlg.setWindowTitle("Load Images")
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        dlg.setNameFilter("Image Files (*.jpg *.jpeg *.png *.tif *.tiff)")
        imagePath = None

        if dlg.exec_() == QFileDialog.Accepted:
            imagePath = dlg.selectedFiles()[0]
            print("Selected file:", imagePath)


        return imagePath

    @staticmethod
    def save_points_to_excel(file_name, branch_points_list, tip_points_list):
        """
        Saves the given branch and tip point (VAP_Point objects) lists
        to an Excel file. Each point is saved as (x, y) coordinates.

        Parameters:
        file_name (str): Name of the Excel file to save (e.g., 'analysis_results.xlsx').
        branch_points_list (list): List of branch points consisting of VAP_Point objects.
        tip_points_list (list): List of tip points consisting of VAP_Point objects.
        """
        try:
            # Extract (x, y) coordinates from VAP_Point objects as strings
            # To appear in '(x, y)' format in Excel
            branch_coordinates = [f"({p.x}, {p.y})" for p in branch_points_list if isinstance(p, VAP_Point)]
            tip_coordinates = [f"({p.x}, {p.y})" for p in tip_points_list if isinstance(p, VAP_Point)]

            # If lists are empty or contain only non-VAP_Point elements,
            # pass empty lists to pandas.
            if not branch_coordinates and branch_points_list:
                print("Warning: 'branch_points_list' does not seem to contain VAP_Point objects.")
            if not tip_coordinates and tip_points_list:
                print("Warning: 'tip_points_list' does not seem to contain VAP_Point objects.")

            # Create pandas Series considering that lists may have different lengths.
            df = pd.DataFrame({
                'Branch Points (x, y)': pd.Series(branch_coordinates, dtype='object'),
                'Tip Points (x, y)': pd.Series(tip_coordinates, dtype='object')
            })

            # Create full path where file will be saved (script's working directory)
            save_path = os.path.join(os.getcwd(), file_name.replace('.tif', '.xlsx'))

            # Write DataFrame to Excel file
            # index=False parameter prevents DataFrame indices from being written to Excel.
            df.to_excel(save_path, index=False, engine='openpyxl')
            print(f"Data successfully saved to '{save_path}' file.")

        except ImportError:
            print("The 'pandas' and 'openpyxl' libraries must be installed for this function to work.")
            print("Please install with 'pip install pandas openpyxl' command.")
        except AttributeError:
            # This error usually occurs if list elements don't have expected 'x', 'y' attributes.
            print("Error: Objects in lists must be VAP_Point objects with 'x' and 'y' attributes.")
        except Exception as e:
            print(f"An error occurred while saving to Excel file: {e}")

    @staticmethod
    def SaveInfos(vap_image, informationDict, report_type=None):
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.Directory)
        folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)

        if folder_dialog.exec_() == QFileDialog.Accepted:
            # Get the selected folder path
            selected_folder = os.path.normpath(folder_dialog.selectedFiles()[0])

            image_report_name = os.path.splitext(vap_image.image_raw_name)[0]
            if report_type is not None:
                image_report_name = f"{report_type}_{image_report_name}"
            report_folder=selected_folder
            #report_folder = os.path.join(selected_folder, image_report_name)
            # Create the folder if it doesn't exist
            #if not os.path.exists(report_folder):
            #    os.makedirs(report_folder)
            csv_file_path = ImageOperation.SaveCsv(vap_image, report_folder, image_report_name, informationDict)
            pdf_file_path = ImageOperation.SaveAsPdf(vap_image, report_folder, image_report_name, informationDict)
            return csv_file_path, pdf_file_path
        else:
            return None,None

    @staticmethod
    def SaveCsv(vap_image, report_folder,image_report_name, informationDict):

        # Create a CSV file inside the folder

        csv_file_path = os.path.join(report_folder, image_report_name + ".csv")
        csv_file = open(csv_file_path, 'w', newline='')
        csv_writer = csv.writer(csv_file)
        #csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

        all_inf1 = ["vaf(%)", "branch points count", "tip point count", "vein count", "total vein length",
                    "average vein length"]
        field = [key for key in informationDict.keys() if informationDict[key] is True and key in all_inf1]
        csv_writer.writerow(field)

        row_dict = {'vaf(%)': vap_image.vascularAreaFraction, 'branch points count': len(vap_image.branchPoints),
                    'tip point count': len(vap_image.tipPoints), 'vein count': len(vap_image.vap_veins),
                    'total vein length': vap_image.total_vein_length,
                    'average vein length': vap_image.average_vein_length}

        row = [value for key, value in row_dict.items() if key in field]
        csv_writer.writerow(row)
        csv_writer.writerow([]) #one emty row
        all_inf2 = ["id", "length", "p1.x, p1.y", "p1_type", "[p1.x, p1.y],[p2.x, p2.y]", "p2.x, p2.y", "p2_type"]

        field = [key for key in informationDict.keys() if informationDict[key] is True and key in all_inf2]
        boolDf2IsExist = False

        for key in informationDict.keys():
            if key in all_inf2 and key != "id":
                if informationDict[key] is True:
                    boolDf2IsExist = True
                    break
        csv_writer.writerow(field)


        data_dict = {}
        for vap_vein in vap_image.vap_veins:
            vap_points = []
            vap_points.extend(vap_vein.tip_points)
            vap_points.extend(vap_vein.branch_points)
            if (len(vap_points) == 1):
                vap_points.append(vap_vein.vap_point_list[-1])
            try:
                data_dict['id'] = vap_vein.idn
                data_dict['length'] = vap_vein.length
                data_dict['p1.x, p1.y'] = "[" + str(vap_points[0].x) + "," + str(vap_points[0].y) + "]"
                data_dict['p1_type'] = vap_points[0].vp_type.name
                data_dict['p2.x, p2.y'] = "[" + str(vap_points[1].x) + "," + str(vap_points[1].y) + "]"
                data_dict['p2_type'] = vap_points[1].vp_type.name
                data_dict['[p1.x, p1.y],[p2.x, p2.y]'] = data_dict['p1.x, p1.y']+","+data_dict['p2.x, p2.y']
            except:
                print("An exception occurred")
            row = [data_dict[key] for key in field]
            csv_writer.writerow(row)

        csv_file.close()
        return csv_file_path

    @staticmethod
    def SaveAsPdf(vap_image, report_folder, image_report_name, informationDict):
        csv_file_path = os.path.join(report_folder, image_report_name + ".csv")
        pdf_file_path = os.path.join(report_folder, image_report_name + ".pdf")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', size=14)
        pdf.set_text_color(25, 25, 112)
        pdf.cell(200, 10, txt="VESSEL ANALYSIS REPORT", ln=True, align='C')

        df1 = pd.read_csv(csv_file_path, nrows=1)
        df2 = pd.read_csv(csv_file_path, skiprows=3)

        ImageOperation.AddTableToPdf(pdf, df1)
        if not df2.empty:
            ImageOperation.AddTableToPdf(pdf, df2)

        pdf.output(pdf_file_path)
        return pdf_file_path

    @staticmethod
    def AddTableToPdf(pdf, df):
        pdf.ln(10)

        # Fit the table to the printable page width instead of using a fixed
        # column width (which overflowed the page when many columns were shown).
        n_cols = max(len(df.columns), 1)
        usable_width = pdf.w - pdf.l_margin - pdf.r_margin
        col_w = usable_width / n_cols
        row_h = 8
        font_size = 9 if n_cols <= 5 else (8 if n_cols <= 8 else 7)

        def _fit(text):
            # Shrink overly long cell text so it never spills past its column.
            text = str(text)
            if pdf.get_string_width(text) <= col_w - 2:
                return text
            while len(text) > 1 and pdf.get_string_width(text + "...") > col_w - 2:
                text = text[:-1]
            return text + "..."

        # Function to add the header row
        def add_header():
            pdf.set_font("Arial", "B", font_size)
            pdf.set_text_color(25, 25, 112)
            for title in df.columns:
                pdf.cell(col_w, row_h, _fit(title), border=1, align='C')
            pdf.ln()

        # Add the header row initially
        add_header()

        pdf.set_font("Arial", size=font_size)
        pdf.set_text_color(0, 0, 0)
        page_bottom = pdf.h - pdf.b_margin - row_h
        for _, row in df.iterrows():
            # Check if the current page is running out of space
            if pdf.get_y() > page_bottom:
                pdf.add_page()
                add_header()
                pdf.set_font("Arial", size=font_size)
                pdf.set_text_color(0, 0, 0)
            for column in df.columns:
                value = str(row[column])
                if '.' in value and 'x' not in value:
                    value = str(round(float(value), 3))
                pdf.cell(col_w, row_h, _fit(value), border=1, align='C')
            pdf.ln()


#
#     def save_as_pdf():
#         # Creating PDF
#         pdf = FPDF()
#
#         # Adding title to the PDF
#         pdf.add_page()
#         pdf.set_font("Arial", 'B', size=14)
#         pdf.set_text_color(25, 25, 112)
#         pdf.cell(200, 6, txt="VESSEL ANALYSE", ln=True, align='C')
#
#         all_inf2 = ["id", "length", "p1.x, p1.y", "p1_type", "p2.x, p2.y", "p2_type"]
#
#         field = [key for key in informationDict.keys() if informationDict[key] is True and key in all_inf2]
#
#         boolDf2IsExist = False
#
#         for key in informationDict.keys():
#             if key in all_inf2 and key != "id":
#                 if informationDict[key] is True:
#                     boolDf2IsExist = True
#                     break
#         csv_writer.writerow(field)
#
#         data_dict = {}
#         for vap_vein in vap_image.vap_veins:
#             vap_points = []
#             vap_points.extend(vap_vein.tip_points)
#             vap_points.extend(vap_vein.branch_points)
#             if (len(vap_points) == 1):
#                 vap_points.append(vap_vein.vap_point_list[-1])
#             try:
#                 data_dict['id'] = vap_vein.idn
#                 data_dict['length'] = vap_vein.length
#                 data_dict['p1.x, p1.y'] = str(vap_points[0].x) + "," + str(vap_points[0].y)
#                 data_dict['p1_type'] = vap_points[0].vp_type.name
#                 data_dict['p2.x, p2.y'] = str(vap_points[1].x) + "," + str(vap_points[1].y)
#                 data_dict['p2_type'] = vap_points[1].vp_type.name
#             except:
#                 print("An exception occurred")
#             row = [data_dict[key] for key in field]
#             csv_writer.writerow(row)
#
#         csv_file.close()
#
#         def save_as_pdf(df, pdf):
#
#     pdf.ln(10)
#
#     pdf.set_font("Arial", "B", 9)
#     pdf.set_text_color(25, 25, 112)
#     for title in df.columns:
#         pdf.cell(32, 10, str(title), border=1)
#     pdf.ln()
#
#     pdf.set_font("Arial", "B", 13)
#     pdf.set_text_color(0, 0, 0)
#     for index, row in df.iterrows():
#         for column in df.columns:
#             value = str(row[column])
#             if '.' in value and 'x' not in value:
#                 value = float(value)
#                 value = str(round(value, 3))
#             pdf.cell(32, 10, value, border=1)
#         pdf.ln()
#     return
#
#
# # Reading CSV data
# df1 = pd.read_csv(csv_file_path, nrows=1)
# df2 = pd.read_csv(csv_file_path, skiprows=2)
#
# save_as_pdf(df1, pdf)
#
# if boolDf2IsExist is True:
#     save_as_pdf(df2, pdf)
#
# # Saving PDF
# pdf.output(pdf_file_path)
#
# if (vap_image.image_raw is not None):
#     skimage.io.imsave(os.path.join(report_folder, image_report_name + "_raw.png"), vap_image.image_raw)
# if (vap_image.image_gray is not None):
#     skimage.io.imsave(os.path.join(report_folder, image_report_name + "_gray.png"),
#                       vap_image.image_gray)
# if (vap_image.image_segmented_byte8 is not None):
#     skimage.io.imsave(os.path.join(report_folder, image_report_name + "_segmented.png"),
#                       vap_image.image_segmented_byte8)
# if (vap_image.image_skeletonized_byte8 is not None):
#     skimage.io.imsave(os.path.join(report_folder, image_report_name + "_skeletonized.png"),
#                       vap_image.image_skeletonized_byte8)
#
# return pdf_file_path
#