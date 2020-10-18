# Setup for SpERT
cd ./spert
pip3 install -r ./requirements.txt
chmod 777 ./scripts/fetch_datasets.sh
chmod 777 ./scripts/fetch_models.sh
./scripts/fetch_datasets.sh
./scripts/fetch_models.sh
cd ..


# Setup for SciERC
cd ./SciERC
pip3 install -r ./requirements.txt

CUR_PATH="$PWD"
cd /usr/local/lib/python3.7/site-packages/tensorflow
ln -s libtensorflow_framework.so.1 libtensorflow_framework.so
cd $CUR_PATH

chmod 777 ./scripts/fetch_required_data.sh
chmod 777 ./scripts/fetch_coref_model.sh
chmod 777 ./scripts/build_custom_kernels.sh
./scripts/fetch_required_data.sh
./scripts/fetch_coref_model.sh
./scripts/build_custom_kernels.sh
ln -s libtensorflow_framework.so.1 -f libtensorflow_framework.so
cd ..


# Setup for ESRA
pip3 install -r requirements.txt
python3 -m spacy download en_core_web_lg
python3 -m spacy download en_core_web_md
python3 -m spacy download en_core_web_sm