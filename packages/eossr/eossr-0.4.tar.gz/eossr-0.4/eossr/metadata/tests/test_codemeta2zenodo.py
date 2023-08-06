import json
import unittest
from os.path import dirname, join, realpath

import pytest

from eossr.metadata import codemeta2zenodo

SAMPLES_DIR = join(dirname(realpath(__file__)), "samples")
ROOT_DIR = dirname(realpath("codemeta.json"))


codemeta_entries = [
    "@context",
    "@type",
    "name",
    "description",
    "license",
    "softwareVersion",
    "developmentStatus",
    "codeRepository",
    "dateCreated",
    "isAccessibleForFree",
    "isPartOf",
    "contIntegration",
    "issueTracker",
    "readme",
    "buildInstructions",
    "operatingSystem",
    "author",
    "contributor",
    "maintainer",
    "funder",
    "funding",
    "programmingLanguage",
    "softwareRequirements",
    "keywords",
    "downloadUrl",
    "dateModified",
    "datePublished",
    "runtimePlatform",
    "releaseNotes",
    "readme",
]

zenodo_entries = [
    "upload_type",
    "title",
    "description",
    "language",
    "access_right",
    "version",
    "keywords",
    "notes",
    "license",
    "publication_date",
    "creators",
    # #"communities",
    # #"grants",
    # #"contributors",
    # #"references",
]


@pytest.fixture()
def tmp_dir(tmp_path):
    test_dir = tmp_path
    test_dir.mkdir(exist_ok=True)
    return test_dir


def test_Codemeta2ZenodoController():
    codemeta_file = join(ROOT_DIR, "codemeta.json")
    converter = codemeta2zenodo.CodeMeta2ZenodoController.from_file(codemeta_file)
    assert converter.codemeta_data != {}
    assert all(key in converter.codemeta_data.keys() for key in codemeta_entries)

    converter.convert()
    assert converter.zenodo_data != {}
    assert converter.zenodo_data["language"] == "eng"
    assert converter.zenodo_data["access_right"] == "open"
    assert all(key in converter.zenodo_data.keys() for key in zenodo_entries)

    converter.add_escape2020_community()
    assert converter.zenodo_data["communities"] == [{"identifier": "escape2020"}]
    converter.add_escape2020_grant()
    assert converter.zenodo_data["grants"] == [{"id": "10.13039/501100000780::824064"}]


def test_add_author_metadata():

    with open(join(SAMPLES_DIR, "codemeta_contributors_sample.json")) as f:
        codemeta_metadata = json.load(f)
    zenodo_metadata = {}

    assert all(person in codemeta_metadata.keys() for person in codemeta2zenodo.codemeta_allowed_person_fields)

    for person in codemeta2zenodo.codemeta_allowed_person_fields:
        codemeta2zenodo.add_author_metadata(zenodo_metadata, codemeta_metadata[person], person)

    assert 'creators' in zenodo_metadata
    # 4 'creators' one repeated, should not be duplicated.
    # Maintainer and Contributor. Author and Creator are the same person
    assert len(zenodo_metadata['creators']) == 3

    assert 'contributors' in zenodo_metadata
    # Editor, Producer, Publisher, Provider and Sponsor
    assert len(zenodo_metadata['contributors']) == 5


def test_parse_person_schema_property():

    with open(join(SAMPLES_DIR, "codemeta_contributors_sample.json")) as f:
        codemeta_metadata = json.load(f)

    for person in codemeta2zenodo.codemeta_contributors_fields:
        zenodo_metadata = codemeta2zenodo.parse_person_schema_property(codemeta_metadata[person], person)
        if person == 'editor':
            assert zenodo_metadata['type'] == 'Editor'
        elif person == 'producer':
            assert zenodo_metadata['type'] == 'Producer'
        elif person == 'sponsor':
            assert zenodo_metadata['type'] == 'Sponsor'
        else:
            assert zenodo_metadata['type'] == 'Other'


# class TestConverting(unittest.TestCase):


def test_converter():
    with open(join(SAMPLES_DIR, "codemeta_sample1.json")) as file:
        codemeta = json.load(file)
    zenodo = codemeta2zenodo.converter(codemeta)
    assert zenodo['communities'][0]['identifier'] == 'escape2020'


def test_sample_file_conversion(tmp_dir):
    codemeta2zenodo.parse_codemeta_and_write_zenodo_metadata_file(join(SAMPLES_DIR, "codemeta_sample1.json"), tmp_dir)
    with open(tmp_dir.joinpath('.zenodo.json').name, 'r') as f:
        zen_meta = json.load(f)
    assert 'related_identifiers' in zen_meta
    assert "https://readme.com" in [ri['identifier'] for ri in zen_meta['related_identifiers']]


def test_root_codemeta_conversion(tmp_dir):
    codemeta2zenodo.parse_codemeta_and_write_zenodo_metadata_file(join(ROOT_DIR, "codemeta.json"), tmp_dir)
    with open(tmp_dir.joinpath('.zenodo.json').name, 'r') as f:
        json.load(f)


class TestLicense(unittest.TestCase):
    def test_license1(self):

        converter = codemeta2zenodo.CodeMeta2ZenodoController({})
        converter.convert_license()
        assert 'license' not in converter.zenodo_data

        converter.codemeta_data['license'] = 'https://spdx.org/licenses/MIT'
        converter.convert_license()
        assert converter.zenodo_data['license'] == 'MIT'

        converter.codemeta_data['license'] = './COPYING'
        converter.convert_license()
        assert converter.zenodo_data['license'] == 'other-open'
