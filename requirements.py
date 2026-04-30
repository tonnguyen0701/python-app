from pathlib import Path

req = Path('requirements.txt')
text = req.read_text()
if 'mysql-connector-python' not in text:
    req.write_text(text.rstrip() + '\nmysql-connector-python\n')
    print('Added mysql-connector-python to requirements.txt')

for path in Path('src/database').glob('*.py'):
    text = path.read_text()
    if '?' in text:
        path.write_text(text.replace('?', '%s'))
        print(f'Updated placeholders in {path}')
