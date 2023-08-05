import numpy as np


def delete(im_label, indices):
    """
    Deletes objects with values in 'indices' from label image, writing them over
    with zeros to assimilate with background.

    Parameters
    ----------
    im_label : array_like
        A label image generated by segmentation methods.
    indices : array_like
        An n-length array of strictly positive integer values to delete from
        'im_label'.

    Returns
    -------
    Deleted : array_like
        A label image where all values in 'indices' are set to zero.

    Notes:
    ------
    A call to CondenseLabel can squeeze label image values to fill in gaps from
    deleted values.

    See Also
    --------
    histomicstk.segmentation.label.condense

    """
    import scipy.ndimage.measurements as ms

    # initialize output
    Deleted = im_label.copy()

    # get extent of each object
    Locations = ms.find_objects(Deleted)

    # fill in new values
    for i in np.arange(indices.size):
        if Locations[indices[i]-1] is not None:
            Patch = Deleted[Locations[indices[i] - 1]]
            Patch[Patch == indices[i]] = 0

    return Deleted
