from typing import Any, Dict, Iterable, List, Union

import numpy as np

from ._feeds import (_create_feed, _delete_feed, _get_feed_id, _load_feed,
                     _load_subfeed, _watch_for_new_messages)
from ._mutables import (_get, _set, _delete)

from ._load_file import _load_file, _load_bytes, _load_text, _load_json, _load_npy, _load_pkl
from ._store_file import _store_file, _store_text, _store_json, _store_npy, _store_pkl, _link_file
from ._daemon_connection import _get_node_id
from ._uri_handling import KacheryUri, _build_uri, _parse_uri

def load_file(
    uri: str,
    dest: Union[str, None]=None,
    local_only: bool=False,
    channel: Union[str, None]=None
) -> Union[str, None]:
    """Load a file either from local kachery storage or from a remote kachery node

    Args:
        uri (str): The kachery URI for the file to load: sha1://...
        dest (Union[str, None], optional): Optional location to copy the file to. Defaults to None.
        local_only (bool, optional): Optionally only load file from local kachery directory. Defaults to False.

    Returns:
        Union[str, None]: If found, the local path of the loaded file, else None
    """
    return _load_file(uri=uri, dest=dest, local_only=local_only, channel=channel)

def load_bytes(uri: str, start: int, end: int, *, write_to_stdout=False, channel: Union[str, None]=None) -> Union[bytes, None]:
    """Load a subset of bytes from a file in local storage or from remote nodes in the kachery network

    Args:
        uri (str): The kachery URI for the file to load: sha1://...
        start (int): The start byte (inclusive)
        end (int): The end byte (not inclusive)

    Returns:
        Union[bytes, None]: The bytes if found, else None
    """
    return _load_bytes(uri=uri, start=start, end=end, write_to_stdout=write_to_stdout, channel=channel)

def load_json(uri: str, *, channel: Union[str, None]=None) -> Union[dict, None]:
    """Load an object (Python dict) either from local kachery storage or from a remote kachery node

    Args:
        uri (str): The kachery URI for the file to load: sha1://...

    Returns:
        Union[dict, None]: If found, the Python dict, else None
    """
    return _load_json(uri=uri, channel=channel)

def load_text(uri: str, *, channel: Union[str, None]=None) -> Union[str, None]:
    """Load a text string either from local kachery storage or from a remote kachery node

    Args:
        uri (str): The kachery URI for the file to load: sha1://...

    Returns:
        Union[str, None]: If found, the text string, else None
    """
    return _load_text(uri=uri, channel=channel)

def load_npy(uri: str, *, channel: Union[str, None]=None) -> Union[np.ndarray, None]:
    """Load a Numpy array either from local kachery storage or from a remote kachery node

    Args:
        uri (str): The kachery URI for the .npy file to load: sha1://...

    Returns:
        Union[str, None]: If found, the Numpy array, else None
    """
    return _load_npy(uri=uri, channel=channel)

def load_pkl(uri: str, *, channel: Union[str, None]=None) -> Union[Any, None]:
    """Load a Python item from a restricted pickle format either from local kachery storage or from a remote kachery node

    Args:
        uri (str): The kachery URI for the .pkl file to load: sha1://...

    Returns:
        Union[str, None]: If found, result, else None
    """
    return _load_pkl(uri=uri, channel=channel)

def store_file(path: str, basename: Union[str, None]=None) -> str:
    """Store file in the local kachery storage (will therefore be available on the kachery network) and return a kachery URI

    Args:
        path (str): Path of the file to store
        basename (Union[str, None], optional): Optional base file name to append to the sha1:// URI. Defaults to None.

    Returns:
        str: The kachery URI: sha1://...
    """
    return _store_file(path=path, basename=basename)

def link_file(path: str, basename: Union[str, None]=None) -> str:
    """Link a local file in the local kachery storage (will therefore be available on the kachery network) and return a kachery URI

    Args:
        path (str): Path of the file to link
        basename (Union[str, None], optional): Optional base file name to append to the sha1:// URI. Defaults to None.

    Returns:
        str: The kachery URI: sha1://...
    """
    return _link_file(path=path, basename=basename)

def store_json(object: Union[dict, list, int, float, str], basename: Union[str, None]=None) -> str:
    """Store object (Python dict, list or other jsonable) in the local kachery storage (will therefore be available on the kachery network) and return a kachery URI

    Args:
        object (dict): The Python dict to store
        basename (Union[str, None], optional): Optional base file name to append to the sha1:// URI. Defaults to None.

    Returns:
        str: The kachery URI: sha1://...
    """
    return _store_json(object=object, basename=basename)

def store_text(text: str, basename: Union[str, None]=None) -> str:
    """Store text in the local kachery storage (will therefore be available on the kachery network) and return a kachery URI

    Args:
        text (str): The text string to store
        basename (Union[str, None], optional): Optional base file name to append to the sha1:// URI. Defaults to None.

    Returns:
        str: The kachery URI: sha1://...
    """
    return _store_text(text=text, basename=basename)

def store_npy(array: np.ndarray, basename: Union[str, None]=None) -> str:
    """Store Numpy array in the local kachery storage (will therefore be available on the kachery network) and return a kachery URI

    Args:
        array (np.ndarray): The Numpy array to store
        basename (Union[str, None], optional): Optional base file name to append to the sha1:// URI. Defaults to None.

    Returns:
        str: The kachery URI: sha1://...
    """
    return _store_npy(array=array, basename=basename)

def store_pkl(x: Any, basename: Union[str, None]=None) -> str:
    """Store Python item in the local kachery storage using a restricted pickle format and return a kachery URI

    Args:
        array (Any): The item to store
        basename (Union[str, None], optional): Optional base file name to append to the sha1:// URI. Defaults to None.

    Returns:
        str: The kachery URI: sha1://...
    """
    return _store_pkl(x=x, basename=basename)

def get_node_id(daemon_port=None) -> str:
    """Return the Node ID for this kachery node

    Args:
        daemon_port ([type], optional): Optionally override the port of the API daemon. Defaults to None.

    Returns:
        str: The node ID
    """
    return _get_node_id(daemon_port=daemon_port)

################################################

def create_feed(feed_name: Union[str, None]=None):
    """Create a new local feed and optionally associate it with a local name

    Args:
        feed_name (Union[str, None], optional): Optional name for local retrieval. Defaults to None.

    Returns:
        Feed: The newly-created local writeable feed
    """
    return _create_feed(feed_name=feed_name)

def delete_feed(feed_name_or_uri: str) -> None:
    """Delete a feed with a particular name or URI

    Args:
        feed_name_or_uri (str): The name or URI of the feed to delete
    """
    return _delete_feed(feed_name_or_uri=feed_name_or_uri)    

def get_feed_id(feed_name: str, *, create: bool=False) -> Union[None, str]:
    """Return the ID of a feed by name, and optionally create a new feed if it does not exist

    Args:
        feed_name (str): The local name of the feed ID to retrieve
        create (bool, optional): Whether to create a new feed if none exists with this name. Defaults to False.

    Returns:
        Union[None, str]: The feed ID, if exists, else None
    """
    return _get_feed_id(feed_name=feed_name, create=create)

def load_subfeed(subfeed_uri: str, *, channel: str='*local*'):
    """Load a subfeed by URI

    Args:
        subfeed_uri (str): the URI of the subfeed
        channel (str): the kachery channel to listen on (or '*local*' to only load locally)

    Returns:
        Subfeed: The subfeed associated with the URI
    """
    return _load_subfeed(subfeed_uri=subfeed_uri, channel=channel)
        
def load_feed(feed_name_or_uri: str, *, timeout_sec: Union[None, float]=None, create=False):
    """Load a feed by URI or local name

    Args:
        feed_name_or_uri (str): Either the local name or the URI of the feed to load
        timeout_sec (Union[None, float], optional): An optional timeout for searching for the feed. Defaults to None.
        create (bool, optional): Whether to create if doesn't exist (only applies when supplying a local feed name). Defaults to False.

    Returns:
        Feed: The loaded feed
    """
    return _load_feed(feed_name_or_uri=feed_name_or_uri, timeout_sec=timeout_sec, create=create)

def watch_for_new_messages(subfeed_watches: Dict[str, dict], *, wait_msec, channel: str='*local*', signed=False) -> Dict[str, Any]:
    """Watch for new messages on one or more subfeeds

    Args:
        subfeed_watches (List[dict]): A list of subfeed watches (TODO: more details needed)
        wait_msec ([type]): The wait duration for retrieving the messages

    Returns:
        List[dict]: The list of retrieved messages (TODO: more details needed)
    """
    return _watch_for_new_messages(subfeed_watches=subfeed_watches, wait_msec=wait_msec, channel=channel, signed=signed)

################################################

def set(key: Union[str, dict, list], value: Union[str, dict, list], update: bool=True):
    """Set a mutable value (only available locally)

    Args:
        key (Union[str, dict, list]): The key
        value (Union[str, dict, list]): The value
        update (bool): If False does not overwrite existing value, and returns False if new value was not set. Default is True.

    Returns:
        bool: whether the value was successfully set
    """
    return _set(key=key, value=value, update=update)

def get(key: Union[str, dict, list]):
    """Get a mutable value (only available locally)

    Args:
        key (Union[str, dict, list]): The key

    Returns:
        value (Union[str, dict, list, None]): The value if found, else None
    """
    return _get(key=key)

def get_string(key: Union[str, dict, list]):
    """Get a mutable value as a string (only available locally)

    Args:
        key (Union[str, dict, list]): The key

    Returns:
        value (Union[str, None]): The value as a string if found, else None
    """
    v = get(key)
    return str(v) if v is not None else None

def delete(key: Union[str, dict, list]):
    """Delete a mutable value (only available locally)

    Args:
        key (Union[str, dict, list]): The key

    Returns:
        None
    """
    return _delete(key=key)

################################################

def parse_uri(uri: str):
    """Convert a URI into an instance of a class with semantically meaningful
    members.

    Args:
        uri (str): URI to parse.

    Returns:
        KacheryUri: A meaningfully parsed representation of the URI.
    """
    return _parse_uri(uri=uri)

def build_uri(uri_object: KacheryUri):
    """Returns a string URI from the named component elements.

    Args:
        uri_object (KacheryUri): Object representation of the URI.

    Returns:
        str: A usable URI string.
    """    
    return _build_uri(uri_object=uri_object)
