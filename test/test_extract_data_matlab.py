import pytest
import numpy as np
import os
from my_project.inspect_data.MScharacteristics_functions import extract_data_matlab
from scipy.io import loadmat


@pytest.fixture
def setup_example_file():
    '''set up the example testing file from test folder'''
    test_dir = "test"
    file_name = "gandalf_100718a_msMats.mat"
    example_file_path = os.path.join(test_dir, file_name)

    return test_dir, file_name

def test_extract_data_valid_column(setup_example_file):
    """Test the function with a certain column number"""
    test_dir, file_name = setup_example_file
    column_number = 1  # Numerical data column, supposed to be 'cortex trial' 
    data_key = "msMats"
    
    #calling the function with column number 1
    result = extract_data_matlab(file_name, column_number=column_number, DATA_PATH=test_dir, data_key=data_key)
    
    #we Expected values for column 2 (index 1) 'cortex trial'
    expected = [21.0, 21.0, 48.0, 48.0, 48.0, 58.0, 58.0, 66.0, 80.0, 80.0, 88.0, 88.0, 
                95.0, 132.0, 132.0, 140.0, 181.0, 181.0, 181.0, 253.0, 261.0, 277.0, 
                277.0, 293.0, 306.0, 306.0, 306.0, 317.0, 356.0, 356.0, 356.0]
    #this is column 2 acording to the test file data
    
    np.testing.assert_array_equal(result, expected)

def test_extract_data_invalid_column(setup_example_file):
    """Test extracting a non-existent column.
    verify that the function raises an IndexError when getting a non-existent colomn number"""
    test_dir, file_name = setup_example_file
    column_number = 100  # non-existing colonm number
    data_key = "msMats"

    with pytest.raises(IndexError):
        extract_data_matlab(
            file_name, column_number, DATA_PATH=test_dir, data_key=data_key
        )


