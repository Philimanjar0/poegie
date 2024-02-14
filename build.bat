call venv\Scripts\activate
echo Y | del dist
pyinstaller --noconsole --noconfirm .\src\poegie.py
echo f | xcopy resources\histogram_icons_3.csv dist\poegie\resources\histogram_icons_3.csv /E
echo f | xcopy resources\menu3.png dist\poegie\resources\menu3.png
"C:\Program Files\7-Zip\7z.exe" a "dist\poegie.zip" "dist\poegie\"