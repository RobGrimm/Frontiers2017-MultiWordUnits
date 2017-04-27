Code for obtaining results described in the following [paper](http://journal.frontiersin.org/article/10.3389/fpsyg.2017.00555/full?&utm_source=Email_to_authors_&utm_medium=Email&utm_content=T1_11.5e1_author&utm_campaign=Email_publication&field=&journalName=Frontiers_in_Psychology&id=253632#): 

> Grimm R., Cassani G., Gillis S. and Daelemans W. (2017). Facilitatory Effects of Multi-Word Units in Lexical Processing and Word Learning: A Computational Investigation. Frontiers in Psychology.

## OS and Dependencies

This project is written in Python (version 3.4.3) and R (version 3.3.3), both on Ubuntu 14.04. The biggest part of the code is written in Python, and a small part for statistical analysis is written in R. 
The Python component requires the following packages (the version we used is given in parentheses):
> numpy (1.12.1)  
nltk (3.2.2)  
scipy (0.19.0)  

The R scripts require these packages:  
> boot (1.3)  
ppcor (1.1)


## Get the Corpus Data

#### Prepare the CHILDES corpora 

We use several corpora from the [CHILDES data base](http://childes.talkbank.org/).  

Get the North American corpora [here](http://childes.talkbank.org/data-xml/Eng-NA/).    
Then unzip them to: Frontiers_MultiWordUnits/CHILDES/corpora/NA/

Then, get the British English corpora [here](http://childes.talkbank.org/data-xml/Eng-UK/).  
Unzip them to: Frontiers_MultiWordUnits/CHILDES/corpora/BE/

Download the following North American corpora:
> Bates, Bernstein, Bliss, Bloom70, Bloom73, Bohannon, Braunwald, Brent, Brown, Carterette, Clark, Cornell, Demetras1, Demetras2, ErvinTripp, Evans, Feldman, Garvey, Gathercole,  Gleason, HSLLD, Hall, Higginson, Kuczaj, MacWhinney, McCune, McMillan, Morisset, Nelson, NewEngland, Peters, Post, Providence, Rollins, Sachs, Snow, Soderstrom, Sprott, Suppes, Tardif, Valian, VanHouten, VanKleeck, Warren, Weist

And the following British English corpora:  
> Belfast, Fletcher, Manchester, Thomas, Tommerdahl, Wells, Forrester, Lara

#### Get the British National Corpus

You also need (to purchase) a copy of the [British National Corpus](http://www.natcorp.ox.ac.uk/) (BNC), XML version. From the corpus directory, copy the *Text* folder to: Frontiers_MultiWordUnits/BNC/corpus/   


## Run the experiments 

The project's root directory contains Python and R scripts, numbered 1 through 9, which you need to run one after the other in order to carry out the experiments. 

*1-pre_process_cds_corpora.py*      
Pre-process the British English CHILDES corpora.

*2-pre_process_ads_corpora.py*      
Pre-process the spoken demographic component of the BNC.

*3-pre_process_aofp_corpus.py*        
Pre-process the American English CHILDES corpora.

*4-induce_aofp.py*       
Collect age of first production (AoFP) values for words used by the children in the American English CHILDES corpora.

*5-run_chunk_based_learner.py*        
Run the Chunk-Based Learner on the ADS and CDS corpora and save extracted multi-word units to hard drive.

*6-data_to_csv.py*  
Compute statistics and write results to CSV file for statistical analysis in R.

*7-experiment_2_ADS_vs_CDS.R*  
Perform calculations for Experiment 2.

*8-experiment_3_random_baseline.R*  
Perform calculations for Experiment 3.

*9-experiment_4_across_dependent_variables.R*  
Perform calculations for Experiment 4.

To get the results for experiment 1 and various tables and figures, check the scripts in: Frontiers_MultiWordUnits/TablesFigures
