### Installation

Run `./install.sh`. This assumes that you have python3.6 installed.

### Running
First, activate the virtual environment by running `source venv/bin/activate`

Run 
```
python simulate.py --help
```
To get a list of options and their explanations.

example, create outputs: 
```
python simulate.py --delta-t 0.1 --output-interval 1 --t-total 50 --simulation-method barnes-hut --output-method pickle --output-dir "outputs/massless_1gal_output_pickle" --output-interval 1 setups/2gal_oscillating.json 
```

example, animate results of output:
```
python simulate.py --simulation-method unpickle --output-method animate --output-dir "outputs/massless_1gal_output_pickle" setups/2gal_oscillating.json
```
