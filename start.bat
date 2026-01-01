@echo off
echo ========================================
echo   Wood Knots Detection App
echo ========================================
echo.

:: Start Backend
echo [1/2] Starting Backend (Flask)...
start "Backend" cmd /k "cd backend && python app.py"

:: Wait 2 seconds for backend to start
timeout /t 2 /nobreak > nul

:: Start Frontend
echo [2/2] Starting Frontend (Vite)...
start "Frontend" cmd /k "cd frontend && npm run dev"

:: Wait 2 seconds
timeout /t 2 /nobreak > nul

echo.
echo ========================================
echo   Application Started!
echo ========================================
echo.
echo   Backend:  http://localhost:5000
echo   Frontend: http://localhost:5173  (buka di browser)
echo.
echo   Tekan tombol apapun untuk membuka browser...
pause > nul

start http://localhost:5173
