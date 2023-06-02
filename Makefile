
spd3303x: spd3303x.py
	~/.local/bin/pyinstaller --onefile spd3303x.py

install:
	cp ./dist/spd3303x /usr/bin/

clean:
	rm -r build dist *.spec
