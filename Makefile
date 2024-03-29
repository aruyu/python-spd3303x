all:
	mkdir ./dist/ ; cp spd3303x.py ./dist/spd3303x

binary: spd3303x.py
	~/.local/bin/pyinstaller --onefile spd3303x.py

install:
	cp ./dist/spd3303x /usr/bin/

uninstall:
	rm /usr/bin/spd3303x

clean:
	rm -r build dist __pycache__ *.spec
