index:
	awk -f indexer.awk dataset/*.txt > index.txt

clean:
	python3 limpia_indice.py

search:
	python3 search_engine.py

all: index clean search
