# TSVis
Script uses data from StackOverflow to show relations between users and tags. Main dependencies:

* [stackapi](https://github.com/AWegnerGitHub/stackapi) - crawling data
* [graphistry](https://github.com/graphistry/pygraphistry) - drawing data as a graph
* [pyarrow](https://github.com/apache/arrow/tree/master/python), [pandas](https://github.com/pandas-dev/pandas) and [numpy](https://github.com/numpy/numpy) - transforming data

## Data
TSVis gathers Q&A threads with the tags provided by you. In next step, it collects all users who answered in those threads. Gathered data is used to build a list of tags for each user. StackOverflow provides information for particular user about tags he/she was active in and we use it to prepare list of relations: user -> tag. At final stage those relations are drawn on the graph in Graphistry.

![Graphistry - sample result](https://github.com/data-hunters/tech-skills-visualizer/blob/main/assets/graphistry_bd.png?raw=true)

## Launching script
You need at least Python 3.7 to run it. Script takes list of tags (separated by semi-colon).

### Installation steps
```
git clone git@github.com:data-hunters/tech-skills-visualizer.git
cd tech-skills-visualizer
pip3 install -r requirements.txt
```

### Launching
```
export PYTHONPATH="${PYTHONPATH}:."
python3 tsvis/run.py --tags=bigdata --max-pages=10
```
Run `python3 tsvis/run.py --help` to check other options.
