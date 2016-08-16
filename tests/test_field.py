# coding: utf-8
from __future__ import unicode_literals

import tempfile
from unittest import TestCase

import os
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

    def test_generic(self):
        field = FileField(name='test', upload_to=self.upload_to)
        fake_model = type(b'fake', (object,), {field.name: None})
        _file = FieldFile(field=field, instance=fake_model(), name='')
        _file._committed = False
        with open(self.archive, 'rb') as f:
            _file.save('test.zip', ContentFile(f.read()), save=False)


