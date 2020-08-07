import file_converter
import pytest


@pytest.mark.parametrize("test_input,expected", [(1, "label"), (2, "Id"), (0, "link")])
def test_element_name(test_input, expected):
    core_attribute_val = file_converter.element_name(test_input)
    assert core_attribute_val == expected


@pytest.fixture
def load_list_from_file():
    tab_row_cols = file_converter.read_and_clean_file("sample_recs2.csv", ",", 1, 0)
    return tab_row_cols


def test_read_and_clean_file(load_list_from_file):
    assert load_list_from_file == [['Meat & Fish', "179549", "browse/179549", "", "", "", "", "", "", "", "", ""],
                                   ["Meat & Fish", "179549", "browse/179549", "Fish", "176741", "browse/179549/176741",
                                    "", "",
                                    "", "", "", ""]
                                   ]


def test_get_node_with_level():
    node = file_converter.get_node_with_level(['Meat & Fish', "179549", "browse/179549"])
    assert node == {'label': 'Meat & Fish', 'Id': '179549', 'link': 'browse/179549', 'level': 1}


def test_build_tree(load_list_from_file):
    tab_row_cols = load_list_from_file
    main_data_list = []
    file_converter.build_tree(tab_row_cols,main_data_list)
    expected_val = [{'label': 'Meat & Fish', 'Id': '179549', 'link': 'browse/179549',
                     'children': [{'label': 'Fish', 'Id': '176741', 'link': 'browse/179549/176741', 'children': []}]}]
    if expected_val == main_data_list:
        assert_val = True
    else:
        assert_val = False
    assert assert_val
