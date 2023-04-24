# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/02_TEG_XML_Parser.ipynb.

# %% auto 0
__all__ = ['TEGXMLProcessor']

# %% ../notebooks/02_TEG_XML_Parser.ipynb 5
from collections import abc
from loguru import logger as log
import ast
import json
import os
import re
import sys
import xmltodict 

# %% ../notebooks/02_TEG_XML_Parser.ipynb 7
class TEGXMLProcessor:
    """Pipeline for TEG6s XML processing."""

    ROOT_TAG = bytes("Cartridge", encoding="utf-8")  # assumption that this will be true
  
    def __init__(
        self,
        filepath: str  # path to input XML file
    ):
        self.filepath = filepath
        self.read_xml()

    def read_xml(self):
        """Read raw contents of the file."""
        try:
            with open(self.filepath, "rb") as f:
                self.contents = f.read()
            self.raw_length = len(self.contents)
            log.info(f"Read {self.raw_length:,d} bytes of raw XML data")
        except Exception as e:
            log.error(f"unable to read file: {e}")

    def find_xml_offsets(self):
        """Scans for XML fragments."""
        xml_open_bytes = [x.start() for x in re.finditer(b"<\?xml", self.contents)]
        xml_close_bytes = [x.end() for x in re.finditer(self.ROOT_TAG+b">", self.contents)]
        if len(xml_open_bytes) != len(xml_close_bytes):
            log.error("XML heads not equal XML tails")
        else:
            xml_offsets = [(start, end) for start, end in zip(xml_open_bytes, xml_close_bytes)]
            log.info(f"found {len(xml_offsets)} XML fragment(s)")
            return xml_offsets
