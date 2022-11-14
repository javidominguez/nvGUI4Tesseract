# nvGUI for Tesseract  

### What is?  

nvGUI for Tesseract is a light graphical interface to handle the OCR Tesseract, designed to be fully accessible with screen readers. It provides the basic functions for recognizing text in image files as well as scanning images from a WIA compatible scanner.  
  
### Interface Description  

The interface consists of a read-only text box, in which the recognition result is displayed, which occupies almost the entire window, with a menu at the top and a status bar at the bottom. There is also a small panel with the list of processed pages in the lower right corner, which can be shown/hidden by pressing F6. In the page list, the applications key displays a context menu with more options.  
Most keyboard shortcuts are indicated in their corresponding option in the menu. Here is a complete list:  
  
#### Keyboard shortcuts  

* control+N creates a new document
* control+O opens a document
* control+S saves the current document
* control+shift+S saves a copy of the current document to another location
* control+shift+X exports all recognized text to a txt file
* control+F loads an image file and recognizes it
* control+D digitizes an image from the scanner and recognizes it
* F6 shows/hides page list
* control+pageDown moves to the next page
* control+pageUp moves to the previous page
* F1 displays this document
* control+Q closes the app  
  
### Licenses<a name="licenses"></a>  

nvGUI for Tesseract is free software. Copying, distribution and modification is permitted under the license
[GNU General Public License GPL 3.0.](https://www.gnu.org/licenses/gpl-3.0.html)  
nvGUI for Tesseract makes use of third party software under the following licenses:  

* [Tesseract](https://github.com/UB-Mannheim/tesseract/), [Apache 2.0](https://directory.fsf.org/wiki/License:Apache-2.0)  
* [wia-cmd-scanner](https://github.com/nagimov/wia-cmd-scanner/), [GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.html)  
* [xpdf-tools](http://www.xpdfreader.com/), [GPL 2.0](https://www.gnu.org/licenses/old-licenses/lgpl-2.0.html)  
* nvdaControllerClient of [NVDA](https://www.nvaccess.org), [GPL 2.0](https://www.gnu.org/licenses/old-licenses/lgpl-2.0.html)  
Also, all the Python modules and libraries used are open source.  
