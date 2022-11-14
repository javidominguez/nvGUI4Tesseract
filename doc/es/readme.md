# nvGUI para Tesseract  

### ¿Qué es?  

nvGUI para Tesseract es una interfaz gráfica ligera para manejar el OCR Tesseract, diseñada para ser totalmente accesible con lectores de pantalla. Proporciona las funciones básicas para reconocer texto en archivos de imagen así como digitalizar imágenes desde un escáner WIA compatible.  
  
### Descripción de la interfaz  

La interfaz consta de un cuadro de texto de sólo lectura, en el que se muestra el resultado del reconocimiento, que ocupa casi toda la ventana, con un menú en la parte superior y una barra de estado en la inferior. También hay un pequeño panel con la lista de las páginas procesadas en la esquina inferior derecha, que se puede mostrar/ocultar pulsando F6. En la lista de páginas, la tecla aplicaciones despliega un menú contextual con más opciones.  
La mayoría de atajos de teclado se indican en su correspondiente opción en el menú. Aquí hay una lista completa:  
  
#### Atajos de teclado  

* control+N crea un documento nuevo
* control+O abre un documento
* control+S guarda el documento actual
* control+shift+S guarda una copia del documento actual en otra ubicación
* control+shift+X exporta todo el texto reconocido a un archivo txt
* control+F carga un archivo de imágen y lo reconoce
* control+D digitaliza una imagen desde el escáner y la reconoce
* F6 muestra/oculta la lista de páginas
* control+pageDown se mueve a la página siguiente
* control+pageUp se mueve a la página anterior
* F1 muestra este documento
* control+Q cierra la aplicación  
  
### Licencias<a name=·licenses"></a>  

nvGUI para Tesseract es software libre. Se permite su copia, distribución y modificación bajo la licencia
[GNU General Public License GPL 3.0.](https://www.gnu.org/licenses/gpl-3.0.html)  
nvGUI para Tesseract hace uso de software de terceras partes con las siguientes licencias:  

* [Tesseract](https://github.com/UB-Mannheim/tesseract/), [Apache 2.0](https://directory.fsf.org/wiki/License:Apache-2.0)  
* [wia-cmd-scanner](https://github.com/nagimov/wia-cmd-scanner/), [GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.html)  
* [xpdf-tools](http://www.xpdfreader.com/), [GPL 2.0](https://www.gnu.org/licenses/old-licenses/lgpl-2.0.html)  
* nvdaControllerClient de [NVDA](https://www.nvaccess.org), [GPL 2.0](https://www.gnu.org/licenses/old-licenses/lgpl-2.0.html)  
Asimismo, todos los módulos y librerías Python usados son open source.  
  
### Descargo de responsabilidad

Este software se ofrece "tal cual", sin garantías de ningún tipo, ni explícitas ni implícitas. Ni los autores o colaboradores ni quienes distribuyan el software deberán responder en ningún caso por reclamaciones, daños, pérdida de datos u otras responsabilidades, ya sean contractuales, extracontractuales o de cualquier otro tipo, derivados del software, de su uso o de cualquier otra actividad realizada con el mismo o relacionados con dicho software.