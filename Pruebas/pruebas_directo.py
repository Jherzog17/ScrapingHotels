import sys
from pathlib import Path

carpeta_root = Path(__file__).parent.parent
sys.path.insert(0, str(carpeta_root))

from Scraping.scrapBooking import ejecutar_script_booking
from Scraping.scrapeDreams import ejecutar_script_edreams
from Scraping.scrapAmimir import ejecutar_script_amimir

if __name__ == "__main__":
    ejecutar_script_amimir("Zaragoza", "resultados_amimir_zaragoza.csv")
    ejecutar_script_booking("Ibiza", "resultados_booking_ibiza.csv")
    ejecutar_script_edreams("Zaragoza", "resultados_edreams_zaragoza.csv")
    
    