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
    def noktalari_excele_kaydet(dosya_adi, dallanma_noktalari_listesi, tip_noktalari_listesi):
        """
        Verilen dallanma ve tip noktası (VAP_Point nesneleri) listelerini
        bir Excel dosyasına kaydeder. Her nokta (x, y) koordinatı olarak kaydedilir.

        Parametreler:
        dosya_adi (str): Kaydedilecek Excel dosyasının adı (örneğin, 'analiz_sonuclari.xlsx').
        dallanma_noktalari_listesi (list): VAP_Point nesnelerinden oluşan dallanma noktaları listesi.
        tip_noktalari_listesi (list): VAP_Point nesnelerinden oluşan tip noktaları listesi.
        """
        try:
            # VAP_Point nesnelerinden (x, y) koordinatlarını string olarak çıkar
            # Excel'de '(x, y)' formatında görünmesi için
            dallanma_koordinatlari = [f"({p.x}, {p.y})" for p in dallanma_noktalari_listesi if isinstance(p, VAP_Point)]
            tip_koordinatlari = [f"({p.x}, {p.y})" for p in tip_noktalari_listesi if isinstance(p, VAP_Point)]

            # Eğer listeler boşsa veya sadece VAP_Point olmayan elemanlar içeriyorsa,
            # pandas'a boş listeler geçirelim.
            if not dallanma_koordinatlari and dallanma_noktalari_listesi:
                print("Uyarı: 'dallanma_noktalari_listesi' VAP_Point nesneleri içermiyor gibi görünüyor.")
            if not tip_koordinatlari and tip_noktalari_listesi:
                print("Uyarı: 'tip_noktalari_listesi' VAP_Point nesneleri içermiyor gibi görünüyor.")

            # Listelerin farklı uzunluklarda olabileceği durumları göz önünde bulundurarak
            # pandas Serileri oluşturuyoruz.
            df = pd.DataFrame({
                'Dallanma Noktaları (x, y)': pd.Series(dallanma_koordinatlari, dtype='object'),
                'Tip Noktaları (x, y)': pd.Series(tip_koordinatlari, dtype='object')
            })

            # Dosyanın kaydedileceği tam yolu oluştur (script'in çalıştığı klasör)
            kayit_yolu = os.path.join(os.getcwd(), dosya_adi.replace('.tif', '.xlsx'))

            # DataFrame'i Excel dosyasına yaz
            # index=False parametresi, DataFrame indexlerinin Excel'e yazılmasını engeller.
            df.to_excel(kayit_yolu, index=False, engine='openpyxl')
            print(f"Veriler başarıyla '{kayit_yolu}' dosyasına kaydedildi.")

        except ImportError:
            print("Bu fonksiyonun çalışması için 'pandas' ve 'openpyxl' kütüphanelerinin kurulu olması gerekmektedir.")
            print("Lütfen 'pip install pandas openpyxl' komutu ile kurun.")
        except AttributeError:
            # Bu hata genellikle liste elemanları beklenen 'x', 'y' özelliklerine sahip değilse oluşur.
            print("Hata: Listelerdeki nesneler 'x' ve 'y' özelliklerine sahip VAP_Point nesneleri olmalıdır.")
        except Exception as e:
            print(f"Excel dosyasına kaydetme sırasında bir hata oluştu: {e}")

    @staticmethod
    def SaveInfos(vap_image, informationDict):
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.Directory)
        folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)

        if folder_dialog.exec_() == QFileDialog.Accepted:
            # Get the selected folder path
            selected_folder = os.path.normpath(folder_dialog.selectedFiles()[0])

            image_report_name = os.path.splitext(vap_image.image_raw_name)[0]
            report_folder = os.path.join(selected_folder, image_report_name)
            # Create the folder if it doesn't exist
            if not os.path.exists(report_folder):
                os.makedirs(report_folder)
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
        all_inf2 = ["id", "length", "p1.x, p1.y", "p1_type", "p2.x, p2.y", "p2_type"]

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


        # Function to add the header row
        def add_header():
            pdf.set_font("Arial", "B", 9)
            pdf.set_text_color(25, 25, 112)
            for title in df.columns:
                pdf.cell(32, 10, str(title), border=1)
            pdf.ln()

        # Add the header row initially
        add_header()

        pdf.set_font("Arial", size=9)
        pdf.set_text_color(0, 0, 0)
        for _, row in df.iterrows():
            # Check if the current page is running out of space
            if pdf.get_y() > 270:  # Adjust this value based on your page layout
                pdf.add_page()
                add_header()  # Add the header row on the new page
                pdf.set_font("Arial", size=9)
                pdf.set_text_color(0, 0, 0)
            for column in df.columns:
                value = str(row[column])
                if '.' in value and 'x' not in value:
                    value = str(round(float(value), 3))
                pdf.cell(32, 10, value, border=1)
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
