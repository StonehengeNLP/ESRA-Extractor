# Explainable Scientific Research Assistant (ESRA)

0. (Optional) Initialize a container
``` sh
docker run --runtime=nvidia -it -d --name esra_extractor nvidia/cuda
docker exec -it esra_extractor bash

# These all are needed
apt-get install git python3 python3-pip wget
```

1. Python3.7 environments
``` sh
apt-get update \
&& apt-get install -y software-properties-common curl \
&& add-apt-repository ppa:deadsnakes/ppa \
&& apt-get update \
&& apt-get install -y python3.7 python3.7-venv virtualenv
```

2. Setting up

``` sh
git clone --recursive https://github.com/StonehengeNLP/ESRA-Extractor.git
cd ./ESRA-Extractor

# Activate virtual environment
virtualenv --python=3.7 env
source env/bin/activate

# Install dependencies
scripts/setup.sh
pip install -r requirements.txt
```

3. Evaluating the model
``` sh
python ./evaluator.py
```

4. Extract abstracts
``` sh
# edit the abstracts and run
python ./esra.py
```
