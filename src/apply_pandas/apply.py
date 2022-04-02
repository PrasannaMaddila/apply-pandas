"""
The apply() function converts a list of boolean expressions from strings
to python, and applies them on a Pandas DataFrame.

This module implements a Functor Class that wraps around apply()
in order to cleanly implement proper checking of the stringified
booleans before actually executing on the target DataFrame.

Author: PrasannaMaddila
Date: 01 March 2022
"""

from pandas import DataFrame


class Apply:
    """This class is a wrapper around the apply() function that
    converts a list of boolean expressions from strings to python,
    and applies them on a Pandas DataFrame.

    __verify__ will first create an empty DataFrame of the target, and
    check that evaluating the conditions on it work as intended i.e. they
    are boolean expressions, addressed to the correct DataFrame, and actually
    are compatible with that frame.

    Then, __apply__ will apply them on the actual DataFrame and return the results.
    """

    def __init__(self, frame: DataFrame, conditions: list) -> None:
        self.frame = frame
        self.conditions = conditions

    def __call__(self) -> DataFrame:
        if self.__verify__() is False:
            return None

        return self.__apply__()

    def __verify__(self) -> bool:
        """This function verifies the list of conditions in string form
        to see that they are syntactically correct

        All conditions have to be valid boolean conditions that can be used
        on a pandas DataFrame, but all references to the frame have to be
        called through `frame`, and not through the name of the actual
        DataFrame.

        Eg. Example use case:
            Notice that all conditions that will be used on myFrame
            are made out to a generic `frame`.

        >> myFrame = pd.DataFrame( ... , columns=['Slice', ... ] )
        >>  list_condns = ["frame['Slice']<10", "frame['Slice']%3 == 1"]
        >> Applicator = Apply(myFrame, list_condns)
        >> Applicator() # --> result

        To verify the conditions, the function creates an empty dataframe
        with the same columns as the argument, and checks to see if
        any (relevant) errors are raised. This way, everything is
        completely safe, as the only strings that pass are the ones
        that actually evaluate.

        Parameters
        ----------
        frame : pd.DataFrame
            The actual DataFrame that we'll be working on.

        Returns
        -------
        bool
            returns True if the passed list of conditions are syntactically correct,
            else returns False.
        """

        # First, we create a dummy to use for verification,
        # Note: This is implicitly used in the eval(condition),
        # but pylint et al. will not pick it up.
        frame = DataFrame(columns=self.frame.columns)

        for condition in self.conditions:
            try:
                eval(condition)
            except NameError:
                # This is a good error to have, but
                # all things have to be made out to `frame`,
                print(f"ERROR: {NameError.args}")

                # so if ...
                if "frame" not in str(NameError):
                    print("ERROR: Reference to `frame` not found.")
                    return False
            except Exception:
                # Any other error at all, we log it and return.
                print(f"ERROR: {Exception}")
                return False

        # So if we've not returned False yet,
        return True

    def __apply__(self):
        """
        This function applies a list of boolean conditions (in string form) to a
        pandas dataframe, and then sequentially applies them to the passsed DataFrame.

        ARGUMENTS
        ---------

        frame: Pandas DataFrame object.
            This is the data we'll operate on
        list_conditions: list of string
            This contains the !!properly formatted!! list of conditions to
            apply to our DataFrame.

        RETURNS
        -------
        self.frame: Pandas DataFrame object
            The processed frame containing all matching data.
        """
        for condition in self.conditions:
            condition = eval(
                condition.replace("frame", "self.frame")
            )  # This creates our Boolean expression
            self.frame = self.frame.loc[condition]  # ... which we use here.
        return self.frame


if __name__ == "__main__":
    # Driver code to illustrate the use of Apply:
    # First, we create our dummy data
    df = list(range(0, 100))
    df = DataFrame(df, columns=["Slice"])

    # Then a list of conditions to apply.
    list_condns = ["frame['Slice']<5", "frame['Slice']%3==1"]

    # To use the Apply() class,
    # First create an object that binds DataFrame and conditions,
    Applicator = Apply(df, list_condns)

    # Then, call for the application.
    result = Applicator()

    # You get the filtered DataFrame as a result.
    print("Result of Application : \n", result)
