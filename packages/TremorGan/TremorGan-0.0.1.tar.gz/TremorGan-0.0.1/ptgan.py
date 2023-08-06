def generate_tremor(model, length, scaler, n_sequences):
    import numpy as np
    window = 0
    latent_dim = 0
    if length == 10:
        window = 1000
        latent_dim = 2000
    elif length == 5:
        window = 500
        latent_dim = 1000
    elif length == 2:
        window = 200
        latent_dim = 150
    if length == 10 or length == 5 or length == 2:
        generator = model
        generated_sequences = np.zeros((n_sequences, window))
        generated_sequences[:] = np.nan
        for _i_ in range(n_sequences):
            vector = np.random.randn(latent_dim)
            vector = vector.reshape(1, latent_dim)
            seq = generator.predict(vector)
            seq = seq.reshape(1, window)
            prediction = scaler.inverse_transform(seq)
            generated_sequences[_i_] = prediction[0]
        return generated_sequences
    else:
        print("Please specify the proper length of time series to be generated")