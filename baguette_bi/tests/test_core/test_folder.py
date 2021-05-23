from baguette_bi.core.folder import Folder


def test_hash():
    fd = Folder("test")
    assert hash(fd) == hash(id(fd))


def test_init():
    fd = Folder("test")
    assert fd.children == []
    assert fd.charts == []
    assert fd.parent is None
    assert fd.id == "a9a2a02d3377149b68388dad1d0230b4"


def test_init_appends_to_parent_children():
    par = Folder("parent")
    fd = Folder("test", parent=par)
    assert len(par.children) == 1
    assert par.children[0] == fd
