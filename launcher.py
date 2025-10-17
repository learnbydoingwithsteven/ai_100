"""
Master Launcher for 100 AI Applications
Interactive menu system to browse and run all applications
"""

import os
import sys
import subprocess
from pathlib import Path

class AIAppLauncher:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.apps = self.load_applications()
        
    def load_applications(self):
        """Load all application metadata"""
        apps = []
        for i in range(1, 101):
            app_dir = self.base_dir / f"app_{i:03d}"
            if app_dir.exists():
                readme_path = app_dir / "README.md"
                if readme_path.exists():
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                        title = first_line.replace('#', '').strip()
                else:
                    title = f"Application {i}"
                
                apps.append({
                    'id': i,
                    'dir': app_dir,
                    'title': title,
                    'path': app_dir / 'app.py'
                })
        return apps
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*80)
        print("🤖 100 AI APPLICATIONS - MASTER LAUNCHER")
        print("="*80)
        print("\nCategories:")
        print("  [1-20]   Healthcare & Medical AI")
        print("  [21-40]  Finance & Business Intelligence")
        print("  [41-60]  Computer Vision & Image Processing")
        print("  [61-80]  NLP & Text Analysis")
        print("  [81-100] IoT, Robotics & Specialized AI")
        print("\nCommands:")
        print("  list [category]  - List applications (e.g., 'list 1-20')")
        print("  run [number]     - Run specific application (e.g., 'run 1')")
        print("  search [keyword] - Search applications by keyword")
        print("  info [number]    - Show application details")
        print("  quit             - Exit launcher")
        print("="*80)
    
    def list_apps(self, start=1, end=100):
        """List applications in range"""
        print(f"\n📋 Applications {start}-{end}:")
        print("-"*80)
        for app in self.apps:
            if start <= app['id'] <= end:
                status = "✅" if app['path'].exists() else "⏳"
                print(f"  {status} [{app['id']:03d}] {app['title']}")
        print("-"*80)
    
    def search_apps(self, keyword):
        """Search applications by keyword"""
        keyword = keyword.lower()
        results = [app for app in self.apps if keyword in app['title'].lower()]
        
        if results:
            print(f"\n🔍 Search results for '{keyword}':")
            print("-"*80)
            for app in results:
                status = "✅" if app['path'].exists() else "⏳"
                print(f"  {status} [{app['id']:03d}] {app['title']}")
            print("-"*80)
        else:
            print(f"\n❌ No applications found matching '{keyword}'")
    
    def show_info(self, app_id):
        """Show detailed application information"""
        app = next((a for a in self.apps if a['id'] == app_id), None)
        if not app:
            print(f"\n❌ Application {app_id} not found")
            return
        
        print(f"\n📖 Application {app_id:03d} - {app['title']}")
        print("="*80)
        
        readme_path = app['dir'] / 'README.md'
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Show first 500 characters
                print(content[:500])
                if len(content) > 500:
                    print("\n... (truncated, see README.md for full details)")
        else:
            print("No detailed information available")
        
        print("="*80)
        print(f"📁 Location: {app['dir']}")
        print(f"🔧 Status: {'Ready' if app['path'].exists() else 'In Development'}")
    
    def run_app(self, app_id):
        """Run specific application"""
        app = next((a for a in self.apps if a['id'] == app_id), None)
        if not app:
            print(f"\n❌ Application {app_id} not found")
            return
        
        if not app['path'].exists():
            print(f"\n⏳ Application {app_id} is still in development")
            return
        
        print(f"\n🚀 Launching: {app['title']}")
        print(f"📁 Directory: {app['dir']}")
        print("-"*80)
        
        try:
            # Change to app directory and run
            os.chdir(app['dir'])
            subprocess.run([sys.executable, 'app.py'])
        except Exception as e:
            print(f"\n❌ Error running application: {e}")
        finally:
            # Return to base directory
            os.chdir(self.base_dir)
    
    def run(self):
        """Main launcher loop"""
        self.display_menu()
        
        while True:
            try:
                command = input("\n💻 Enter command: ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    print("\n👋 Goodbye!")
                    break
                
                elif command.startswith('list'):
                    parts = command.split()
                    if len(parts) > 1 and '-' in parts[1]:
                        start, end = map(int, parts[1].split('-'))
                        self.list_apps(start, end)
                    else:
                        self.list_apps()
                
                elif command.startswith('run'):
                    parts = command.split()
                    if len(parts) > 1:
                        try:
                            app_id = int(parts[1])
                            self.run_app(app_id)
                        except ValueError:
                            print("❌ Invalid application number")
                    else:
                        print("❌ Usage: run [number]")
                
                elif command.startswith('search'):
                    parts = command.split(maxsplit=1)
                    if len(parts) > 1:
                        self.search_apps(parts[1])
                    else:
                        print("❌ Usage: search [keyword]")
                
                elif command.startswith('info'):
                    parts = command.split()
                    if len(parts) > 1:
                        try:
                            app_id = int(parts[1])
                            self.show_info(app_id)
                        except ValueError:
                            print("❌ Invalid application number")
                    else:
                        print("❌ Usage: info [number]")
                
                elif command == 'help' or command == '?':
                    self.display_menu()
                
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    launcher = AIAppLauncher()
    launcher.run()
