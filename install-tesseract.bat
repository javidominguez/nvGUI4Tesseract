@echo off
echo.
echo Tesseract is required for this app to work.
echo If your copy does not have the necessary executables or you want to obtain a more recent version, you can download it from here:
echo.
echo https://github.com/UB-Mannheim/tesseract/wiki
echo Download tesseract 32bit https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v5.2.0.20220712.exe
echo Download Tesseract 64bit https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.2.0.20220712.exe
echo Best (most accurate) trained LSTM models: https://github.com/tesseract-ocr/tessdata_best
echo.
:question
set /p r=Do you want to install Tesseract now via winget (y/n?
if %r%==y goto install
if %r%==Y goto install
if %r%==n goto end
if %r%==N goto end
goto question

:install
winget install UB-Mannheim.TesseractOCR
:end
