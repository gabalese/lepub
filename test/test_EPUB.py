import os
import zipfile
from unittest import TestCase

from lepub.epub import EPUB

location = lambda *path: os.path.join(os.path.dirname(os.path.realpath(__file__)), *path)


class TestEPUB(TestCase):
    def setUp(self):
        self.test_file_path = location('assets/black_cat.epub')
        self.example_file = EPUB(self.test_file_path)

    def test_location_expression(self):
        assert 'assets/black_cat.epub' in location('assets/black_cat.epub')

    def test_can_be_picked_up(self):
        assert isinstance(self.example_file._file, zipfile.ZipFile)

    def test_returns_root_file(self):
        assert self.example_file.get_opf_path() == 'OPS/fb.opf'

    def test_epub_has_title(self):
        assert self.example_file.title == 'The Black Cat'

    def test_epub_has_author(self):
        assert self.example_file.author == 'Edgar Allan Poe'

    def test_epub_has_no_translator(self):
        assert self.example_file.translator is None

    def test_epub_file_has_manifest(self):
        assert self.example_file.manifest is not None

    def test_epub_manifest_contains_many_items(self):
        assert len(self.example_file.manifest) == 16

    def test_epub_manifest_behaves_like_a_list(self):
        assert self.example_file.manifest[0] is not None

    def test_epub_manifest_contains_different_media_types(self):
        css = self.example_file.manifest.filter('type', 'text/css')
        assert len(css) == 6

    def test_epub_manifest_items_contain_href(self):
        html_docs = self.example_file.manifest.filter('type', 'application/xhtml+xml')
        assert html_docs[0].href == 'cover.xml'
