"""Authors: Cody Baker, Alessio Buccino."""
import uuid
from datetime import datetime
from warnings import warn

from pynwb import NWBFile
from pynwb.file import Subject

from ..utils import dict_deep_update


def get_module(nwbfile: NWBFile, name: str, description: str = None):
    """Check if processing module exists. If not, create it. Then return module."""
    if name in nwbfile.processing:
        if description is not None and nwbfile.modules[name].description != description:
            warn(
                "Custom description given to get_module does not match existing module description! "
                "Ignoring custom description."
            )
        return nwbfile.processing[name]
    else:
        if description is None:
            description = "No description."
        return nwbfile.create_processing_module(name=name, description=description)


def get_default_nwbfile_metadata():
    """
    Return structure with defaulted metadata values required for a NWBFile.

    These standard defaults are
        metadata["NWBFile"]["session_description"] = "no description"
        metadata["NWBFile"]["session_start_time"] = datetime(1970, 1, 1)
    Proper conversions should override these fields prior to calling NWBConverter.run_conversion()
    """
    metadata = dict(
        NWBFile=dict(
            session_description="no description",
            identifier=str(uuid.uuid4()),
        )
    )
    return metadata


def make_nwbfile_from_metadata(metadata: dict):
    """Make NWBFile from available metadata."""
    metadata = dict_deep_update(get_default_nwbfile_metadata(), metadata)
    nwbfile_kwargs = metadata["NWBFile"]
    if "Subject" in metadata:
        # convert ISO 8601 string to datetime
        if "date_of_birth" in metadata["Subject"] and isinstance(metadata["Subject"]["date_of_birth"], str):
            metadata["Subject"]["date_of_birth"] = datetime.fromisoformat(metadata["Subject"]["date_of_birth"])
        nwbfile_kwargs.update(subject=Subject(**metadata["Subject"]))
    # convert ISO 8601 string to datetime
    assert "session_start_time" in nwbfile_kwargs, (
        "'session_start_time' was not found in metadata['NWBFile']! Please add the correct start time of the "
        "session in ISO8601 format (%Y-%m-%dT%H:%M:%S) to this key of the metadata."
    )
    if isinstance(nwbfile_kwargs.get("session_start_time", None), str):
        nwbfile_kwargs["session_start_time"] = datetime.fromisoformat(metadata["NWBFile"]["session_start_time"])
    return NWBFile(**nwbfile_kwargs)
