# compile_messages.py
import os
import polib
import glob

def compile_po_files():
    """Compile all .po files to .mo files"""
    print("Starting manual compilation of translation files...")
    
    # Install polib if it's not already installed
    try:
        import polib
    except ImportError:
        print("Installing polib...")
        os.system("pip install polib")
        import polib
    
    # Find all .po files in the locale directory
    po_files = []
    for root, dirs, files in os.walk('locale'):
        for file in files:
            if file.endswith('.po'):
                po_files.append(os.path.join(root, file))
    
    if not po_files:
        print("No .po files found in the locale directory.")
        return
        
    # Compile each .po file to a .mo file
    for po_file_path in po_files:
        mo_file_path = po_file_path.replace('.po', '.mo')
        try:
            po = polib.pofile(po_file_path)
            po.save_as_mofile(mo_file_path)
            print(f"Compiled: {po_file_path} -> {mo_file_path}")
        except Exception as e:
            print(f"Error compiling {po_file_path}: {str(e)}")
    
    print("Compilation complete!")

if __name__ == "__main__":
    compile_po_files()