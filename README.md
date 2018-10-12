# A word on what this data is about
Each data file contains the data corresponding to a synthetic experiment of the [dynamic clicks task](https://arxiv.org/abs/1710.05945). In particular, it contains:  
- the timing of the clicks for both the right and left streams  
- the timing of the change points, for N trials  
- the true environmental state at the beginning and end of each trial  
- the responses, on each trial, of two types of decision models. 
  - One is the Bayes-optimal decision model, with Gaussian perturbation noise applied at click times to the log-posterior odds ratio;
  - the other one is the so-called _linear model_ described in the aforementioned paper, with the same kind of perturbation noise already described.
- meta data such as
  - total number of trials (N), 
  - trial duration, 
  - hazard rate of the stimulus,
  - discounting parameters of each decision model
  - magnitude (STDEV) of noise for each model

I make this data freely available in an effort to promote reproducible research.

# Data format
I use the [HDF5](https://support.hdfgroup.org/HDF5/) data format. All major scientific computing languages (R,MATLAB,Python) offer ways to read this format.

# Where to find existing data
You may download data by clicking on the appropriate URL in the 'db_url' column of the [dbdb.csv](https://github.com/aernesto/Data_IO_Clicks_Project/blob/design/dbdb.csv) file.

I claim no copyright on this data.

# How to read the data with MATLAB
I suggest you first take a close look at this [manual](https://github.com/aernesto/Data_IO_Clicks_Project/blob/design/Manual_Reading_Data.m).

Then, you may use 

# How to create new data with Python 3 and MATLAB
Creating a new HDF5 database is (currently) a 3-step procedure. 

First, you need to execute this [script](https://github.com/aernesto/Data_IO_Clicks_Project/blob/design/create_db.py) from a (bash) Shell terminal, with the correct arguments, as explained in the script. You will need the proper python modules installed. 

Then, you need to call (in any order) the two MATLAB functions [`fill_lin_dec.m`](https://github.com/aernesto/Data_IO_Clicks_Project/blob/design/fill_lin_dec.m) and [`fill_nonlin_dec`](https://github.com/aernesto/Data_IO_Clicks_Project/blob/design/fill_nonlin_dec.m) with the appropriate arguments, as described in the function files.

I strongly encourage you to make your data freely and publicly available, and to add your own line to the [dbdb.csv](https://github.com/aernesto/Data_IO_Clicks_Project/blob/design/dbdb.csv) file (Pull Requests are the best option for this). 

# Dependencies
Many functions from this repo use (without much warning), functions from the following the repo:
[`ideal_obs_dyn_clicks`](https://github.com/aernesto/ideal_obs_dyn_clicks/tree/dev). I personally use [ToolboxToolbox](https://github.com/ToolboxHub/ToolboxToolbox) in MATLAB to automatically manage these dependencies.

The code that I am currently writing to analyze this data may be found in [this repo](https://github.com/aernesto/analysis_and_fits_dyn_clicks/tree/dev).
