# # ANTES (SRP)
# import json
# from datetime import datetime

# class ReportManager:
#     def run_report(self):
#         # cargar datos
#         data = {"ventas": 1200, "fecha": str(datetime.now())}

#         # formatear
#         text = f"REPORTE: ventas={data['ventas']} fecha={data['fecha']}"

#         # persistir
#         with open("reporte.txt", "w", encoding="utf-8") as f:
#             f.write(text)

#         # presentar
#         print(text)

# if __name__ == "__main__":
#     ReportManager().run_report()

    # ANTES (SRP)
import json
from datetime import datetime

class ReportData:
        # cargar datos
    def load(self):
        data = {"ventas": 1200, "fecha": str(datetime.now())}
        return data
class Reportformatter:
        # formatear
    def format(self , data: dict) -> str:
        return f"REPORTE: ventas={data['ventas']} fecha={data['fecha']}"

class ReportPersistence:
    def save(self, text: str, filename = "reporte.txt"):
        # persistir
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
class ReportPresent:
    def show(self,text:str):
        # presentar
        print(text)

class ReportManager:
    def __init__(self):
        self.data_loader = ReportData()
        self.formatter = Reportformatter()
        self.persistence = ReportPersistence()
        self.presenter = ReportPresent()
    def run_report(self):
        data = self.data_loader.load()
        text = self.formatter.format(data)
        self.persistence.save(text)
        self.presenter.show(text)

if __name__ == "__main__":
    ReportManager().run_report()