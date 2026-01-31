"""
Quick test script to verify both backend and frontend are ready to run.
Run this before starting the servers to catch any configuration issues.
"""

import os
import sys
import json

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_env_file():
    """Check if .env file exists and has GROQ_API_KEY"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'GROQ_API_KEY' not in content:
            print("❌ GROQ_API_KEY not found in .env")
            return False
        if 'your_groq_api_key_here' in content:
            print("⚠️  Warning: GROQ_API_KEY appears to be placeholder")
            return False
    
    print("✅ .env file configured")
    return True

def check_python_dependencies():
    """Check if required Python packages are installed"""
    required = [
        'fastapi',
        'uvicorn',
        'crewai',
        'groq',
        'requests',
        'pydantic'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing Python packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("✅ All Python dependencies installed")
    return True

def check_backend_files():
    """Check if backend files exist"""
    required_files = [
        'backend/main.py',
        'backend/start.py',
        'agents.py',
        'tools.py',
        'tasks.py'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"❌ Missing backend files: {', '.join(missing)}")
        return False
    
    print("✅ All backend files present")
    return True

def check_frontend_files():
    """Check if frontend files exist"""
    required_files = [
        'frontend/package.json',
        'frontend/src/App.jsx',
        'frontend/src/main.jsx',
        'frontend/src/index.css',
        'frontend/index.html'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"❌ Missing frontend files: {', '.join(missing)}")
        return False
    
    print("✅ All frontend files present")
    return True

def check_node_modules():
    """Check if node_modules exists"""
    if not os.path.exists('frontend/node_modules'):
        print("❌ node_modules not found")
        print("   Run: cd frontend && npm install")
        return False
    
    print("✅ Frontend dependencies installed")
    return True

def check_frontend_components():
    """Check if all React components exist"""
    components = [
        'frontend/src/components/DriverDashboard.jsx',
        'frontend/src/components/OwnerDashboard.jsx',
        'frontend/src/components/CustomerDashboard.jsx',
        'frontend/src/components/MapComponent.jsx',
        'frontend/src/components/WeatherWidget.jsx',
        'frontend/src/components/Sidebar.jsx',
        'frontend/src/services/api.js'
    ]
    
    missing = []
    for component in components:
        if not os.path.exists(component):
            missing.append(component)
    
    if missing:
        print(f"❌ Missing components: {', '.join(missing)}")
        return False
    
    print("✅ All React components present")
    return True

def main():
    print("=" * 60)
    print("🔍 Route-Rakshak Full Stack Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment Variables", check_env_file),
        ("Python Dependencies", check_python_dependencies),
        ("Backend Files", check_backend_files),
        ("Frontend Files", check_frontend_files),
        ("Frontend Dependencies", check_node_modules),
        ("React Components", check_frontend_components)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        results.append(check_func())
    
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (name, _) in enumerate(checks):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{status} - {name}")
    
    print()
    print(f"Result: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Ready to start the application.")
        print("\n📝 Next Steps:")
        print("   1. Terminal 1: cd backend && python start.py")
        print("   2. Terminal 2: cd frontend && npm run dev")
        print("   3. Open browser: http://localhost:5173")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("   See STARTUP_GUIDE.md for detailed instructions.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
