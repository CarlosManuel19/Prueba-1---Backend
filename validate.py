
def validate(proposed, actual):
    """Check if the proposed solution is the same as the actual solution.

    Feel free to modify this function as we will be testing your code with
    our copy of this function.

    :param proposed: The proposed solution
    :param actual: The actual solution
    :return: True if they are the same. Else, return False.
    """
    if proposed is None:
        print ("Oops! Looks like your proposed result is None")
        return False
    proposed_items = [item for sublist in proposed for item in sublist]
    actual_items = [item for sublist in actual for item in sublist]
    if len(proposed_items) != len(actual_items):
        print ("Oops! There don't seem to be the same number of elements")
        return False
    if proposed_items != actual_items:
        print ("Oops! Looks like your proposed solution is not right...")
        return False
    return True

global validate1