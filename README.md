### Profiling

Create the profile: `python -m cProfile -o output.profile main.py`

Generate the grapgh: `python -m gprof2dot -f pstats output.profile -o graph.dot`