import json
import os
import zipfile
from unittest import TestCase
from lepub.epub import EPUB

location = lambda *path: os.path.join(os.path.dirname(os.path.realpath(__file__)), *path)


class TestEPUBBase(TestCase):
    def setUp(self):
        self.test_file_path = location('assets/black_cat.epub')
        self.example = EPUB(self.test_file_path)

    def test_location_expression(self):
        assert 'assets/black_cat.epub' in location('assets/black_cat.epub')

    def test_can_be_picked_up(self):
        assert isinstance(self.example._file, zipfile.ZipFile)


class TestEPUB(TestEPUBBase):
    def test_returns_root_file(self):
        assert self.example.get_opf_path() == 'OPS/fb.opf'

    def test_epub_has_title(self):
        assert self.example.metadata.title == 'The Black Cat'

    def test_epub_has_an_idenfier(self):
        assert self.example.metadata.identifier == 'urn:uuid:ab22d53e-f620-11e2-aca4-001cc0a62c0b'

    def test_epub_can_have_multiple_identifiers(self):
        assert len(self.example.metadata.identifiers()) == 2

    def test_epub_has_author(self):
        assert self.example.metadata.author == 'Edgar Allan Poe'

    def test_epub_has_publication_date(self):
        assert self.example.metadata.publication_date

    def test_epub_has_no_translator(self):
        assert self.example.metadata.translator is None

    def test_epub_file_has_manifest(self):
        assert self.example.manifest is not None

    def test_epub_manifest_contains_many_items(self):
        assert len(self.example.manifest) == 16

    def test_epub_manifest_behaves_like_a_list(self):
        assert self.example.manifest[0] is not None

    def test_epub_manifest_contains_different_media_types(self):
        css = self.example.manifest.filter('type', 'text/css')
        assert len(css) == 6

    def test_epub_manifest_supports_media_shortcuts(self):
        assert self.example.manifest.stylesheets
        assert self.example.manifest.documents
        assert self.example.manifest.media

    def test_epub_manifest_items_contain_href(self):
        html_docs = self.example.manifest.filter('type', 'application/xhtml+xml')
        assert html_docs[0].href == 'cover.xml'

    def test_epub_can_open_a_manifest_item(self):
        about_page = self.example.manifest.filter('id', 'about')[0]
        about_page_document = self.example.get(about_page)
        assert about_page_document.filename == 'about.xml'
        assert about_page_document.content()

    def test_epub_can_open_an_image(self):
        cover_image = self.example.manifest.filter('id', 'book-cover')[0]
        cover_image_document = self.example.get(cover_image)
        assert cover_image_document.filename == 'cover.png'
        assert cover_image_document.content()

    def test_epub_manifest_supports_iteration(self):
        assert [item for item in self.example.manifest]

    def test_epub_has_spine_items(self):
        assert len(self.example.spine.items) == 6

    def test_spine_knows_about_toc_id(self):
        assert self.example.spine.id == 'ncx'

    def test_epub_spine_items_return_manifest_items(self):
        assert self.example.spine.items[0] == self.example.manifest.documents[0]

    def test_epub_has_toc_items(self):
        assert len(self.example.toc.items) == 4

    def test_epub_toc_items_have_label(self):
        assert self.example.toc.items[0].label == 'Title'

    def test_epub_toc_items_have_src(self):
        assert self.example.toc.items[0].src == 'title.xml'

    def test_epub_toc_items_have_play_order(self):
        assert [item.order for item in self.example.toc.items] == [1, 2, 3, 4]

    def test_epub_has_guide_items(self):
        assert len(self.example.guide.items) == 6


class TestJSONInterface(TestEPUBBase):
    def test_epub_has_a_metadata_json_interface(self):
        assert self.example.metadata.json()
        assert json.loads(self.example.metadata.json()) == {
            "publisher": "Feedbooks",
            "description": "\"The Black Cat\" is a short story by Edgar Allan Poe. It was first published in the August 19, 1843, edition of The Saturday Evening Post. It is a study of the psychology of guilt, often paired in analysis with Poe's \"The Tell-Tale Heart\". In both, a murderer carefully conceals his crime and believes himself unassailable, but eventually breaks down and reveals himself, impelled by a nagging reminder of his guilt.",
            "language": "en", "title": "The Black Cat", "author": "Edgar Allan Poe", "publication_date": "2007-04-12",
            "date": "2007-04-12",
            "subject": ["Fiction", "Mystery & Detective", "Short Stories"],
            "identifier": "urn:uuid:ab22d53e-f620-11e2-aca4-001cc0a62c0b"
        }

    def test_epub_has_a_toc_json_interface(self):
        assert self.example.toc.json()
