__author__ = 'Ronaldo'

from pandas.util.testing import assert_frame_equal

def is_equal(pandas_dataframe_1,pandas_dataframe_2):
    try:
        assert_frame_equal(pandas_dataframe_1, pandas_dataframe_2)
        return True
    except:
        return False
