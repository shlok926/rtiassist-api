import re

# Patch app.js
with open('d:/Desktop/rtiassist-api/assets/js/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

functions = set(re.findall(r'^(?:async )?function\s+([a-zA-Z0-9_]+)\(', app_js, re.MULTILINE))
variables = set(re.findall(r'^(?:let|const|var)\s+([a-zA-Z0-9_]+)\s*=', app_js, re.MULTILINE))

exports = "\n// --- VITE WINDOW EXPORTS ---\n"
for func in functions:
    exports += f"window.{func} = {func};\n"
for var in variables:
    exports += f"window.{var} = {var};\n"

if "// --- VITE WINDOW EXPORTS ---" not in app_js:
    with open('d:/Desktop/rtiassist-api/assets/js/app.js', 'a', encoding='utf-8') as f:
        f.write(exports)

# Patch legal_examples.js
with open('d:/Desktop/rtiassist-api/assets/js/legal_examples.js', 'r', encoding='utf-8') as f:
    legal_js = f.read()

if "window.LEGAL_EXAMPLES" not in legal_js:
    with open('d:/Desktop/rtiassist-api/assets/js/legal_examples.js', 'a', encoding='utf-8') as f:
        f.write("\nwindow.LEGAL_EXAMPLES = LEGAL_EXAMPLES;\n")

# Create main.js
main_js = """import '../css/style.css';
import './legal_examples.js';
import './ui_translations.js';
import './app.js';
"""
with open('d:/Desktop/rtiassist-api/assets/js/main.js', 'w', encoding='utf-8') as f:
    f.write(main_js)

print("Patching complete!")
