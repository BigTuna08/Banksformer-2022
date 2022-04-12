# Banksformer - A Transformer based model for generating sythetic Banking data based on real data.  

This model can be used with the example dataset, which is a processed version of the Czech Banking data available here: https://data.world/lpetrocelli/some-translatedreformatted-czech-banking-data



Notes:  
- If you are using the unprocessed data from data.world, place it in 'raw_czech' and run 'nb0-1_create_dataset.ipynb' to do some basic preprocessing.

- If you want to run everything over again from scratch, run 'nb0-2_clear_old.ipynb', which clears all the created files besides the processed dataset.


Workflow:
Run the notebooks in the order: nb1, nb2, nb3. (Notebooks beginning with nb0- may or may not be necessary). Specifically:
- 'nb1_set_configs.ipynb' - Here you need to set some information if you are using a new dataset.  This nb ensures correct fields exist in dataframe, and stores information about the configurations used. 
- 'nb2_create_tensors.ipynb' - This nb takes the dataframe produced by nb1, and encodes the data as tensors, used for training the networks.
- 'nb3_banksformer.ipynb' - This nb trains banksformer models on the tensors, and then uses the trained models to generate synthetic datasets.


The nb 'visualize_bf.ipynb' can be used to load a trained Banksformer model and visualize how it generates data.
