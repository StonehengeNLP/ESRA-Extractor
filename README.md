# Explainable Scientific Research Assistant (ESRA)

0. (Optional) Initialize a container
``` sh
docker run --runtime=nvidia -it -d --name esra_extractor nvidia/cuda
docker exec -it esra_extractor bash
```

1. Setting up

``` sh
git clone --recursive https://github.com/StonehengeNLP/ESRA-Extractor.git
cd ./ESRA-Extractor

# Install dependencies
scripts/setup.sh
pip install -r requirements.txt
```

2. Evaluating the model
``` sh
python ./evaluator.py
```

3. Extract abstracts
``` sh
# edit the abstracts and run
python ./esra.py
```
