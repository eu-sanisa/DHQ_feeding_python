# DHQ_feeding_python

Both scripts work by running them in the folder where the output of the respective softwares are stored,
and sumarize their results into a single file.

# toxtrac_summary.py 
Using the files obtained from the Toxtrac software (Rodriguez et al. 2018), this python script calculates:
* average speed of movement, 
* mobility rate (percent of time moving), 
* exploration rate (number of areas visited when dividing the arena in a 10x10 grid), and 
* frequency individuals visited the arena’s center considering a 1.5 cm margin.


# boris_latency.py
Using the log files obtained from the BORIS software (Friard and Gamba 2016), this python script calculates:
* the latency to each behavior


# References
Rodriguez, A., Zhang, H., Klaminder, J., Brodin, T., Andersson, P. L. and Andersson, M. (2018). ToxTrac: a fast and robust software for tracking organisms. Methods in Ecology and Evolution, 9(3):460-464.

Friard, O., and Gamba, M. (2016). BORIS: a free, versatile open‐source event‐logging software for video/audio coding and live observations. Methods in Ecology and Evolution, 7(11): 1325-1330.
