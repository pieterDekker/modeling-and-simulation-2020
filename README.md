### Running

example, create outputs: 
```
python animate.py --delta-t 0.1 --output-interval 1 --t-total 50 --simulation-method barnes-hut --output-method pickle --output-dir "outputs/massless_1gal_output_pickle" --output-interval 1 setups/2gal_oscillating.json 
```

example, animate results of output:
```
python animate.py --simulation-method unpickle --output-method animate --output-dir "outputs/massless_1gal_output_pickle" setups/2gal_oscillating.json
```