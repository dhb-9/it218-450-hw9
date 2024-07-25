# pylint: disable=missing-module-docstring, missing-function-docstring, line-too-long
# import os
from pathlib import Path
from unittest import mock
import pytest

from app.services.qr_service import list_qr_codes, generate_qr_code, delete_qr_code, create_directory

def test_list_qr_codes():
    directory_path = Path('/some/fake/directory')
    with mock.patch('os.listdir', return_value=['file1.png', 'file2.png', 'file3.txt']):
        result = list_qr_codes(directory_path)
        assert result == ['file1.png', 'file2.png']

    with mock.patch('os.listdir', side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            list_qr_codes(directory_path)

    with mock.patch('os.listdir', side_effect=OSError("OS Error")):
        with pytest.raises(OSError):
            list_qr_codes(directory_path)

def test_generate_qr_code(tmp_path):
    data = "test data"
    file_path = tmp_path / "test.png"

    generate_qr_code(data, file_path)
    assert file_path.exists()

    with mock.patch('qrcode.QRCode.make_image', side_effect=Exception("QR generation failed")):
        with pytest.raises(Exception):
            generate_qr_code(data, file_path)

def test_delete_qr_code(tmp_path):
    file_path = tmp_path / "test.png"
    file_path.touch()  # Create the file

    delete_qr_code(file_path)
    assert not file_path.exists()

    with pytest.raises(FileNotFoundError):
        delete_qr_code(file_path)

def test_create_directory(tmp_path):
    directory_path = tmp_path / "new_directory"

    create_directory(directory_path)
    assert directory_path.exists()

    create_directory(directory_path)  # Should not raise an exception if it already exists

    with mock.patch('pathlib.Path.mkdir', side_effect=PermissionError("Permission denied")):
        with pytest.raises(PermissionError):
            create_directory(directory_path)

    with mock.patch('pathlib.Path.mkdir', side_effect=Exception("Unexpected error")):
        with pytest.raises(Exception):
            create_directory(directory_path)
