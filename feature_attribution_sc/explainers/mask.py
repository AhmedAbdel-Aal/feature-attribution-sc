import torch

def apply_mask(x, y, feature_importance, threshold):
    """
    Apply the mask of a feature importance metrics
    :param x: batch of input data
    :param y: batch of corresponding cell types
    :param feature_importance: feature importance method
    :param threshold: threshold of the feature importance
    :return: masked batch of input data
    """
    if feature_importance == 'None':  # don't apply feature importance, if subset, use random
        mask = torch.distributions.Bernoulli(probs=1. - threshold).sample(x.size())
        # upscale inputs to compensate for masking
        masked_outputs = (inputs * mask)  # scale possible with 1. / (1. - threshold)
        return masked_outputs
    else:
        print('Not implemented yet, this should call fancy feature attribution methods')