from fpdf import FPDF
import tempfile
import base64
import os
from pathlib import Path

class WaterQualityReport:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.add_page()
        
        font_paths = [
            Path('C:/Windows/Fonts/arial.ttf'),
            Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),
            Path('/System/Library/Fonts/Helvetica.ttc')
        ]
        
        font_found = False
        for font_path in font_paths:
            if font_path.exists():
                self.pdf.add_font('Arial', '', str(font_path), uni=True)
                font_found = True
                break
                
        if not font_found:
            self.pdf.set_font('Arial', '', 14)
        else:
            self.pdf.set_font('Arial', '', 14)

    def generate_report(self, water_data: dict) -> str:
        temp_files = []

        try:
            self.pdf.cell(0, 10, 'Отчет по анализу качества воды', 0, 1, 'C')
            self.pdf.ln(10)

            self.pdf.set_font('Arial', '', 12)
            self.pdf.cell(0, 10, f'Водоем: {water_data.get("waterName", "Не указан")}', 0, 1)
            
            water_quality = water_data.get("waterQualityClass", {})
            quality_label = water_quality.get("label", "Не определен")
            self.pdf.cell(0, 10, f'Класс качества воды: {quality_label}', 0, 1)

            coordinates = water_data.get("coordinates", {})
            lat = coordinates.get("lat")
            lng = coordinates.get("lng")
            if lat and lng:
                self.pdf.cell(0, 10, f'Координаты водоема: {lat}, {lng}', 0, 1)

            self.pdf.ln(5)

            self.pdf.cell(0, 10, 'Спрогнозированные параметры:', 0, 1)
            predictions = water_data.get("predictions", {})
            for param, value in predictions.items():
                try:
                    value_float = float(value)
                    self.pdf.cell(0, 10, f'{param}: {value_float:.2f}', 0, 1)
                except (ValueError, TypeError):
                    self.pdf.cell(0, 10, f'{param}: {value}', 0, 1)

            plot_data = water_data.get("plot")
            if plot_data:
                self.pdf.ln(5)
                self.pdf.cell(0, 10, 'График сравнения показателей:', 0, 1)

                temp_img = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                temp_files.append(temp_img.name)

                try:
                    img_data = base64.b64decode(plot_data)
                    temp_img.write(img_data)
                    temp_img.flush()
                    temp_img.close()

                    image_width = 180
                    x = (210 - image_width) / 2
                    y = self.pdf.get_y() + 5  
                    self.pdf.image(temp_img.name, x=x, y=y, w=image_width)
                    self.pdf.ln(90)  
                except Exception as e:
                    raise Exception(f"Ошибка при обработке изображения: {str(e)}")

            temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            temp_files.append(temp_pdf.name)
            temp_pdf.close()

            self.pdf.output(temp_files[-1], 'F')
            return temp_files[-1]

        except Exception as e:
            raise Exception(f"Ошибка при создании отчета: {str(e)}")

        finally:
            for temp_file in temp_files[:-1]:
                try:
                    if os.path.exists(temp_file):
                        os.unlink(temp_file)
                except Exception:
                    pass