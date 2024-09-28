from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup


# Configurar el driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# URL de la página de productos
marca_url = "https://www.impomotors.com.ar/productos.html#/productos"
driver.get(marca_url)

# Esperar a que la página se cargue completamente
time.sleep(1) # Ajusta el tiempo según sea necesario

# Lista para almacenar los productos
productos = []

# Encuentra todos los enlaces de las categorías
enlaces_categorias = driver.find_elements(By.CSS_SELECTOR, "ul.shop-sidebar li a")

for enlace in enlaces_categorias:
    categoria_url = enlace.get_attribute("href")
    categoria_nombre = enlace.text
    print(f"Accediendo a la categoría: {categoria_nombre}")
    html = driver.page_source

    # Analizar el HTML con Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Buscar productos en la categoría
    productos_lista = soup.find_all('div', class_='shop-item-container-in')  # Ajusta el selector según tu HTML

    # Navegar a la categoría
    driver.get(categoria_url)
    time.sleep(2)  # Esperar a que los productos se carguen

    try:
        # Esperar hasta que el contenedor de productos esté presente
        productos_lista = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.col-md-4.col-sm-4.col-xs-12.text-center.item.ng-scope'))
        )

        print(f"Cantidad de productos encontrados en {categoria_nombre}: {len(productos_lista)}")

        if productos_lista:
            for producto in productos_lista:
                print("Procesando un producto...")

                try:
                    # Extraer el nombre del producto
                    nombre_producto_element = producto.find_element(By.TAG_NAME, 'h4')
                    nombre_producto = nombre_producto_element.text
                except Exception as e:
                    nombre_producto = 'N/A'
                    print(f"Error al extraer el nombre del producto: {e}")

                try:
                    descripcion_producto = producto.find_element(By.TAG_NAME, 'p').text
                except Exception as e:
                    descripcion_producto = 'N/A'
                    print(f"Error al extraer la descripción del producto: {e}")

                try:
                    url_imagen = producto.find_element(By.TAG_NAME, 'img').get_attribute('src')
                except Exception as e:
                    url_imagen = 'N/A'
                    print(f"Error al extraer la URL de la imagen: {e}")

                try:
                    marca_codigo = producto.find_element(By.CLASS_NAME, 'badge').text  # Cambia según tu selector
                except Exception as e:
                    marca_codigo = 'N/A'
                    print(f"Error al extraer la marca y código: {e}")

                # Almacenar los datos en un diccionario
                productos.append({
                    "Marca y Código": marca_codigo,
                    "Nombre": nombre_producto,
                    "Descripción": descripcion_producto,
                    "URL de Imagen": url_imagen,
                })
        else:
            print(f"No se encontraron productos en la categoría {categoria_nombre}.")
    except Exception as e:
        print(f"No se pudieron buscar productos en la categoría {categoria_nombre}: {e}")

# Verificar la cantidad de productos extraídos
print(f"Total de productos extraídos: {len(productos)}")

# Cerrar el navegador
driver.quit()

# Verifica el contenido de la lista
for producto in productos:
    print(producto)
