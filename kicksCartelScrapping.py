import requests
import bs4

numpag = [i for i in range(1,22)]
cadenaPrincipal='https://www.kickscartelmx.com/products?page='
producto, precios, pagina = [],[],[]
disponible, enlaceDirecto=[],[]

def strToMoney(string):
  string=list(string)
  try:
    string.pop(0)
    string.remove(',')
  except ValueError:
    pass
  finally:
    string = ''.join(string)
  return(float(string))

for i in numpag:
  response=requests.get(cadenaPrincipal+str(i))
  response.encoding = 'utf-8'
  soup=bs4.BeautifulSoup(response.text,'html.parser')
  #extrayendo nombres
  sneakers=soup.select('.product_name')
  sneakers_encontrados=[j.get_text() for j in sneakers]
  producto+=sneakers_encontrados
  #extrayendo precios
  precio = soup.select('.product_price')
  precios_encontrados=[strToMoney(j.get_text()) for j in precio]
  precios+=precios_encontrados
  #añadiendo el numero de pagina
  for k in range(1,len(precios_encontrados)+1):
    pagina.append(i)
  #añadiendo el enlace directo
  enlaces=soup.select('.product')
  enlaces_encontrados=[j.a['href'] for j in enlaces]
  enlaceDirecto+=enlaces_encontrados
  #añadiendo status
  status = soup.select('.product_status')
  status_encontrados=[j.get_text() for j in status]
  disponible += status_encontrados

for i in range(0,len(enlaceDirecto)):
  enlaceDirecto[i]='https://www.kickscartelmx.com'+enlaceDirecto[i]


with open('datosKicksCartel.csv','w') as archivo:
  archivo.writelines('nombreProducto*precio*#pagina*disponibilidad*enlace\n')
  for i in range(len(producto)):
    linea=[producto[i],'*',str(precios[i]),'*',str(pagina[i]),'*',disponible[i],'*',enlaceDirecto[i],'\n']
    archivo.writelines(linea)
