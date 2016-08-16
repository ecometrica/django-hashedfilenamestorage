# coding: utf-8
from __future__ import unicode_literals

import tempfile
from unittest import TestCase

import os
import shutil
from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models import FileField
from django.db.models.fields.files import FieldFile


class FileFieldTestCase(TestCase):
    def setUp(self):
        self.archive = tempfile.mktemp()
        open(self.archive, 'wb')
        self.upload_to = 'archive'

    def tearDown(self):
        os.unlink(self.archive)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT)

    def test_generic(self):
        field = FileField(name='test', upload_to=self.upload_to)
        fake_model = type(b'fake', (object,), {field.name: None})
        _file = FieldFile(field=field, instance=fake_model(), name='')
        _file._committed = False
        with open(self.archive, 'rb') as f:
            _file.save('test.zip', ContentFile(f.read()), save=False)

        self.assertEqual(_file.name, 'archive/da39a3ee5e6b4b0d3255bfef95601890afd80709.zip')

        _file.delete(save=False)
