python src/scripts/mine.py data/queries.txt data/mined

python src/scripts/annotate.py data/mined data/annots

python src/scripts/split.py data/mined data/annots output/data

python src/scripts/train.py