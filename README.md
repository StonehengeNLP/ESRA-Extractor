# Explainable Scientific Research Assistant (ESRA)

1. Setting up
``` sh
git clone --recursive https://github.com/StonehengeNLP/esra.git
cd ./ESRA
scripts/setup.sh
```

2. Unit testing
``` sh
pytest ./test
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
