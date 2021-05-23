from baguette_bi.core.utils import class_to_name


def test_class_to_name():
    assert class_to_name("ClassName") == "Class Name"
    assert class_to_name("NameOfClass") == "Name of Class"
    assert class_to_name("NameOfAClass") == "Name of a Class"
    assert class_to_name("NamesOf2Classes") == "Names of 2 Classes"
    assert class_to_name("NamesOf42Classes") == "Names of 42 Classes"
    assert class_to_name("NameOfTheUSAClass") == "Name of the USA Class"
    assert class_to_name("NamesOfAllThe50USAStates") == "Names of All the 50 USA States"
