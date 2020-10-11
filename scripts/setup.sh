# Setup for SpERT
cd ./spert
pip install -r ./requirements.txt
chmod 777 ./scripts/fetch_datasets.sh
chmod 777 ./scripts/fetch_models.sh
./scripts/fetch_datasets.sh
./scripts/fetch_models.sh
cd ..

# Setup for ?
pip install -r requirements.txt