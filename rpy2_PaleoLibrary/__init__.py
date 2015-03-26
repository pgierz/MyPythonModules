from rpy2.robjects.packages import importr

base = importr('base')
stats = importr('stats')

# Import the paleolibrary?
pallib = importr('../paleoLibrary/src/header.R')
