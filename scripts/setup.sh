# Setup for SpERT
cd ./spert
pip3 install -r ./requirements.txt
chmod 777 ./scripts/fetch_datasets.sh
chmod 777 ./scripts/fetch_models.sh
./scripts/fetch_datasets.sh
./scripts/fetch_models.sh
cd ..

# Setup for ?
pip3 install -r requirements.txt