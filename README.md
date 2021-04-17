# README #

Repository for the AEA project. All code goes here. Link relevant info in this file!

# Project info
* Sponsor: David Minarsch (david.minarsch@fetch.ai)
* Academic Supervisor: Thomas Orton (thomas.orton@st-hughs.ox.ac.uk)
* Group number: 8

# Set up
Clone this repository with
```
git clone https://OlafC@bitbucket.org/OlafC/gdp.git
```
Then, follow the [AEA Framework Installation Instructions](https://docs.fetch.ai/aea/quickstart/#option-2-automated-install-script).

# Testing
From the root directory run
```
python -m unittest
```
This will autodiscover all tests in the `tests` subdirectory, as long as
* all test classes are importable from the project root
* all files containing test classes start with `test_`
* all test methods start with `test_`

### Contribution guidelines ###

* Everything happens on master
* Only push code that works
* If you do happen to push changes that break something, please fix it quickly so the others can continue working

# Resources
* [AEA Project Design Specification](https://docs.google.com/document/d/1yW-G3PwM8LSF0rP7QbxBdjW7P8ET7lRGUL2m7ZZIMzQ/edits]
