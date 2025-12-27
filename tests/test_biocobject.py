import pytest
from copy import copy
from biocutils.bioc_object import BiocObject
from biocutils.named_list import NamedList


def test_init_empty():
    """Test initialization with default values."""
    obj = BiocObject()
    assert isinstance(obj.metadata, NamedList)
    assert len(obj.metadata) == 0

def test_init_with_dict():
    """Test initialization with a dictionary."""
    meta = {"author": "jkanche", "version": 1}
    obj = BiocObject(metadata=meta)

    assert isinstance(obj.metadata, NamedList)
    assert len(obj.metadata) == 2

def test_init_validation():
    """Test that invalid metadata raises TypeError."""
    with pytest.raises(TypeError, match="must be a dictionary or NamedList"):
        BiocObject(metadata="invalid_string")

def test_metadata_property_setter():
    """Test the pythonic @property setter (in-place)."""
    obj = BiocObject()
    new_meta = {"tag": "experiment_1"}
    obj.metadata = new_meta

    assert len(obj.metadata) == 1
    assert isinstance(obj.metadata, NamedList)

def test_set_metadata_copy():
    """Test functional style set_metadata (copy-on-write)."""
    obj = BiocObject(metadata={"id": 1})
    original_id = id(obj)

    new_obj = obj.set_metadata({"id": 2})

    assert id(new_obj) != original_id
    assert len(new_obj.metadata) == 1

    assert len(obj.metadata) == 1

def test_set_metadata_inplace():
    """Test imperative style set_metadata (in-place)."""
    obj = BiocObject(metadata={"id": 1})
    original_id = id(obj)

    new_obj = obj.set_metadata({"id": 2}, in_place=True)

    assert id(new_obj) == original_id
    assert new_obj is obj
    assert len(obj.metadata) == 1

def test_inheritance():
    """Test that subclasses maintain their type when copying."""
    class GenomicContainer(BiocObject):
        pass

    obj = GenomicContainer(metadata={"genome": "hg38"})
    new_obj = obj.set_metadata({"genome": "mm10"})

    assert isinstance(new_obj, GenomicContainer)
    assert new_obj is not obj

def test_shallow_copy_behavior():
    heavy_data = ["large", "data"]

    obj = BiocObject()
    obj._heavy_data = heavy_data
    new_obj = obj.set_metadata({"new": "meta"})
    assert new_obj is not obj
    assert new_obj._heavy_data is obj._heavy_data
