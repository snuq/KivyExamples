rmdir /s /q "dist"
python -m PyInstaller -w "BasicApp Windows.spec"
cmd /k