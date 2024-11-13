
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


def scraping(busqueda, max_results):
    s = Service(ChromeDriverManager().install())
    opc = Options()
    opc.add_argument("--window-size=1020,1200")
    navegador = webdriver.Chrome(service=s, options=opc)
    #Se pasa la ruta del navegador
    navegador.get("https://www.gandhi.com.mx/?srsltid=AfmBOoo1S3tnooKe9jDGcVUCAKCOjhAnZ8PkbGUOYFHeJhObXjhWMzj7")
    time.sleep(10)
    txt_input = navegador.find_element(By.XPATH, '''//*[@id="downshift-1-input"]''')
    txt_input.send_keys(busqueda)
    txt_input.send_keys(Keys.ENTER)

    data = {"titulo":[], "autor":[], "editorial":[], "formato":[], "precio":[]}
    while len(data["titulo"]) < max_results:
        time.sleep(15)
        #navegador.save_screenshot(f"imagenes/{busqueda}_{pag}.png")
        #Se necesita el html para pasarlo a beautiful soup
        soup = BeautifulSoup(navegador.page_source, "html5lib")
        #Beautiful soup para sacar la info y selenium para buscar
        #div: etiqueta en html de la pagina
        libros = soup.find_all("div", attrs={"class": "vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--grid pa4"})

        for item in libros:
            if len(data["titulo"]) >= max_results:
                break

            titulo = item.find("span", attrs={"class": "vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body"})
            autor = item.find("span", attrs={"class": "gandhi-gandhi-components-0-x-productAuthorLabel gandhi-gandhi-components-0-x-productAuthorLabel--product-summary-general-author"})
            editorial = item.find("span", attrs={"class": "gandhi-gandhi-components-0-x-ProductEditorialLink gandhi-gandhi-components-0-x-ProductEditorialLink--product-summary-general-editorial"})
            formato = item.find("span", attrs={"class": "gandhi-gandhi-components-0-x-productTypelabel gandhi-gandhi-components-0-x-productTypelabel--product-summary-general-type"})
            precio = item.find("span", attrs={"class": "vtex-product-price-1-x-currencyInteger vtex-product-price-1-x-currencyInteger--product-summary-general-selling-price"})
            #para que salga mas bonito
            #print(item.prettify())

            # IF SIGUIENTE ES DIFERENTE A NONE (NULO) SIGUE, SINO UN MENSAJE
            if titulo:
                data["titulo"].append(titulo.text)
                print(titulo.text)
            else:
                data["titulo"].append("null")

            if autor:
                data["autor"].append(autor.text)
                print(autor.text)
            else:
                data["autor"].append("null")

            if editorial:
                data["editorial"].append(editorial.text)
                print(editorial.text)
            else:
                data["editorial"].append("null")

            if formato:
                data["formato"].append(formato.text)
                print(formato.text)
            else:
                data["formato"].append("null")

            if precio:
                print(precio.text)
                data["precio"].append(precio.text)
            else:
                data["precio"].append("$0.0")

        time.sleep(3)
        try:
            mostrar_mas = navegador.find_element(By.XPATH, "//a[div[text()='Mostrar más']]")
            #vtex-button__label flex items-center justify-center h-100 ph5
            #/html/body/div[2]/div/div[1]/div/div[2]/div/div/section/div[2]/div/div[6]/section/div/div/div/div/a
            #vtex-button bw1 ba fw5 v-mid relative pa0 lh-solid br2 min-h-small t-action--small bg-action-primary b--action-primary c-on-action-primary hover-bg-action-primary hover-b--action-primary hover-c-on-action-primary pointer inline-flex items-center no-underline
            #vtex-button__label flex items-center justify-center h-100 ph5
            mostrar_mas.click()
            time.sleep(5)
        except:
            print("No se pudo encontrar o hacer clic en el botón 'Mostrar más'. Se han cargado todos los resultados.")
            break
    navegador.quit()

    df = pd.DataFrame(data)
    df.to_csv("datasets/libros.csv")


if __name__=="__main__":
    busqueda = "libros"
    max_results = 400
    scraping(busqueda, max_results)