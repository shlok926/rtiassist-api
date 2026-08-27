import os
import ast

def check_architecture():
    violations = []
    for root, _, files in os.walk('d:\\Desktop\\rtiassist-api'):
        if 'venv' in root or 'node_modules' in root or '.git' in root or '__pycache__' in root:
            continue
        for file in files:
            if not file.endswith('.py'):
                continue
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            try:
                tree = ast.parse(content)
            except:
                continue
                
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    # Route importing ORM directly?
                    if 'routes' in path and 'models.orm' in (node.module or ''):
                        if 'User' not in [n.name for n in node.names]: # user auth is fine
                            violations.append(f"Route {path} directly imports ORM: {node.module}")
                    
                    # Agent importing ORM?
                    if 'agents' in path and 'models.orm' in (node.module or ''):
                        violations.append(f"Agent {path} directly imports ORM: {node.module}")
                        
                    # Route importing Agent directly?
                    if 'routes' in path and 'agents' in (node.module or ''):
                        violations.append(f"Route {path} directly imports Agent: {node.module}")
                        
                    # Telegram importing ORM directly?
                    if 'integrations\\telegram' in path and 'models.orm' in (node.module or ''):
                        if 'User' not in [n.name for n in node.names]:
                            violations.append(f"Telegram {path} directly imports ORM: {node.module}")
                            
    for v in violations:
        print(v)

if __name__ == '__main__':
    print("Checking Architecture...")
    check_architecture()
    print("Done")
