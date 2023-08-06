This is a python library to generate parkinsonian tremor data.

The function takes in the trained model, the length of the sequences of the time series data you want to generate,
the scaler that was used to scale the data to train the mode, and the number of sequences you want to generate.

The function returns a numpy array of size n*m.
Where n is the number of sequences you want to generate.
And m is the length of the sequence.

You can specify three sequence lengths: either 10, for 10 seconds
						    or 5, for 5 seconds
						    or 2, for 2 seconds
