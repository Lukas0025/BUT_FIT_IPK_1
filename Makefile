src.zip:
	rm -rf src/__pycache__
	cp src/fileget.py src/fileget
	chmod +x src/fileget
	zip -j src.zip src/* README.md
	rm src/fileget

self-test:
	mkdir self-test
	cd self-test && \
	python3 ../src/fileget.py -n 147.229.176.19:3333 -f fsp://blue.server/000093.text && \
	python3 ../src/fileget.py -n 147.229.176.19:3333 -f fsp://blue.server/000020.pdf && \
	python3 ../src/fileget.py -n 147.229.176.19:3333 -f fsp://blue.server/000052.xls && \
	python3 ../src/fileget.py -n 147.229.176.19:3333 -f fsp://red.server/index && \
	python3 ../src/fileget.py -n 147.229.176.19:3333 -f fsp://green.server/* && \
	zip out.zip *
	mv self-test/out.zip ./
	rm -rf self-test

serv:
	cd test && ./fsptest -r ipkdata/ -p 127.0.0.1:3333

clean:
	rm -f src.zip
	rm -rf src/__pycache__
	rm -f out.zip