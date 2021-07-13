from data.transforms import load_audio_file


def check_length(filename, required_length):
    try:
        sample = load_audio_file(filename)
    except RuntimeError:
        return False

    return sample.shape[1] == required_length
