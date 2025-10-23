@echo off
echo Installing Twitter Scanner Dependencies...
echo =========================================
echo.

echo Installing Flask and basic dependencies...
pip install flask flask-sqlalchemy flask-cors requests

echo.
echo Testing installation...
python -c "import flask; print('Flask installed successfully')"

echo.
echo Installation complete!
echo You can now run: python app_minimal.py
echo.
pause

