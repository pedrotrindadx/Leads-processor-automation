"""
Build script for CAIXA Lead Processor
Creates a standalone executable using PyInstaller
"""

import os
import shutil
import subprocess
import sys
import importlib.util
from pathlib import Path

def build_executable():
    """Build the standalone executable"""
    
    print("🚀 Building CAIXA Lead Processor...")
    
    # Get current directory
    app_dir = Path(__file__).parent
    
    # Define build configuration
    app_name = "CAIXA_Lead_Processor"
    main_script = "caixa_lead_gui.py"
    icon_file = app_dir / "icons" / "CAIXA.jpeg"  # Will be converted to .ico
    
    # Check if main script exists
    if not (app_dir / main_script).exists():
        print(f"❌ Error: {main_script} not found!")
        return False
    
    # Install PyInstaller if not already installed
    if importlib.util.find_spec("PyInstaller") is not None:
        print("✅ PyInstaller found")
    else:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Create dist and build directories
    dist_dir = app_dir / "dist"
    build_dir = app_dir / "build"
    
    # Clean previous builds
    if dist_dir.exists():
        print("🧹 Cleaning previous builds...")
        shutil.rmtree(dist_dir)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    # Convert JPEG icon to ICO format (Windows requirement)
    ico_file = None
    if icon_file.exists():
        try:
            from PIL import Image
            ico_file = app_dir / "icons" / "CAIXA.ico"
            img = Image.open(icon_file)
            img.save(ico_file, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
            print("✅ Icon converted to ICO format")
        except ImportError:
            print("⚠️ Pillow not found, installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
            from PIL import Image
            ico_file = app_dir / "icons" / "CAIXA.ico"
            img = Image.open(icon_file)
            img.save(ico_file, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
            print("✅ Icon converted to ICO format")
        except Exception as e:
            print(f"⚠️ Warning: Could not convert icon: {e}")
            ico_file = None
    
    # Build PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--name", app_name,
        "--clean",  # Clean PyInstaller cache
        "--distpath", str(dist_dir),
        "--workpath", str(build_dir),
        "--specpath", str(app_dir),
    ]
    
    # Add icon if available
    if ico_file and ico_file.exists():
        cmd.extend(["--icon", str(ico_file)])
    
    # Add hidden imports for common issues
    hidden_imports = [
        "PyQt5.QtCore",
        "PyQt5.QtGui", 
        "PyQt5.QtWidgets",
        "PyQt5.QtSvg",
        "selenium.webdriver.chrome.service",
        "selenium.webdriver.common.service",
        "webdriver_manager.chrome",
    ]
    
    for import_name in hidden_imports:
        cmd.extend(["--hidden-import", import_name])
    
    # Add data files
    data_files = [
        ("icons", "icons"),
        ("config", "config"),
        ("data", "data"),
    ]
    
    for src, dst in data_files:
        src_path = app_dir / src
        if src_path.exists():
            cmd.extend(["--add-data", f"{src_path};{dst}"])
    
    # Add main script
    cmd.append(str(app_dir / main_script))
    
    print("🔨 Running PyInstaller...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, cwd=app_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build successful!")
            
            # Check if executable was created
            exe_file = dist_dir / f"{app_name}.exe"
            if exe_file.exists():
                size_mb = exe_file.stat().st_size / (1024 * 1024)
                print(f"📦 Executable created: {exe_file}")
                print(f"📏 Size: {size_mb:.1f} MB")
                
                # Create a simple installer script
                create_installer_script(app_dir, exe_file)
                
                print("\n🎉 Build completed successfully!")
                print(f"📂 Output directory: {dist_dir}")
                print(f"🚀 Executable: {exe_file}")
                
                return True
            else:
                print("❌ Executable not found after build!")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                return False
        else:
            print("❌ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error during build: {e}")
        return False

def create_installer_script(app_dir, exe_file):
    """Create a simple installer script"""
    try:
        installer_script = app_dir / "install.bat"
        
        installer_content = f"""@echo off
echo ============================================
echo   CAIXA Lead Processor - Installer
echo ============================================
echo.

set "INSTALL_DIR=%USERPROFILE%\\CAIXA_Lead_Processor"
set "DESKTOP_SHORTCUT=%USERPROFILE%\\Desktop\\CAIXA Lead Processor.lnk"
set "START_MENU_SHORTCUT=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\CAIXA Lead Processor.lnk"

echo Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo Copying application files...
copy "{exe_file.name}" "%INSTALL_DIR%\\" >nul

echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP_SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\\{exe_file.name}'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'CAIXA Lead Processor'; $Shortcut.Save()"

echo Creating start menu shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU_SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\\{exe_file.name}'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'CAIXA Lead Processor'; $Shortcut.Save()"

echo.
echo ============================================
echo   Installation completed successfully!
echo ============================================
echo.
echo Application installed to: %INSTALL_DIR%
echo Desktop shortcut created
echo Start menu shortcut created
echo.
echo You can now run the application from:
echo - Desktop shortcut
echo - Start menu
echo - Or directly from: %INSTALL_DIR%\\{exe_file.name}
echo.
pause
"""
        
        with open(installer_script, 'w', encoding='utf-8') as f:
            f.write(installer_content)
        
        print(f"✅ Installer script created: {installer_script}")
        
    except Exception as e:
        print(f"⚠️ Warning: Could not create installer script: {e}")

if __name__ == "__main__":
    print("CAIXA Lead Processor - Build Script")
    print("=" * 50)
    
    success = build_executable()
    
    if success:
        print("\n🎯 Next steps:")
        print("1. Test the executable in dist/ folder")
        print("2. Run install.bat to install on your system")
        print("3. Share the dist/ folder or create a ZIP file")
        input("\nPress Enter to exit...")
    else:
        print("\n❌ Build failed. Check the errors above.")
        input("\nPress Enter to exit...")