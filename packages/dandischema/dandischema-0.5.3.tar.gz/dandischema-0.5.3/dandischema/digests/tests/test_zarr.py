from __future__ import annotations

import pytest

from dandischema.digests.zarr import (
    ZarrChecksum,
    ZarrChecksumListing,
    ZarrChecksums,
    ZarrJSONChecksumSerializer,
    get_checksum,
)


def test_zarr_checksum_sort_order():
    # The a < b in the path should take precedence over z > y in the md5
    a = ZarrChecksum(path="1/2/3/a/z", md5="z")
    b = ZarrChecksum(path="1/2/3/b/z", md5="y")
    assert sorted([b, a]) == [a, b]


# ZarrChecksums tests


def test_zarr_checkums_is_empty():
    assert ZarrChecksums(directories=[], files=[]).is_empty
    assert not ZarrChecksums(
        directories=[ZarrChecksum(md5="md5", path="path")], files=[]
    ).is_empty
    assert not ZarrChecksums(
        directories=[], files=[ZarrChecksum(md5="md5", path="path")]
    ).is_empty


a = ZarrChecksum(path="a", md5="a")
b = ZarrChecksum(path="b", md5="b")
c = ZarrChecksum(path="c", md5="c")


@pytest.mark.parametrize(
    ("initial", "new_checksums", "expected"),
    [
        ([], [], []),
        ([a], [], [a]),
        ([], [a], [a]),
        ([a], [a], [a]),
        ([b], [a], [a, b]),
        ([a, c], [b], [a, b, c]),
        ([b], [c, a], [a, b, c]),
    ],
)
def test_zarr_checkums_add_file_checksums(initial, new_checksums, expected):
    checksums = ZarrChecksums(directories=[], files=initial)
    checksums.add_file_checksums(new_checksums)
    assert checksums.files == expected
    assert checksums.directories == []


@pytest.mark.parametrize(
    ("initial", "new_checksums", "expected"),
    [
        ([], [], []),
        ([a], [], [a]),
        ([], [a], [a]),
        ([a], [a], [a]),
        ([b], [a], [a, b]),
        ([a, c], [b], [a, b, c]),
        ([b], [c, a], [a, b, c]),
    ],
)
def test_zarr_checkums_add_directory_checksums(initial, new_checksums, expected):
    checksums = ZarrChecksums(directories=initial, files=[])
    checksums.add_directory_checksums(new_checksums)
    assert checksums.directories == expected
    assert checksums.files == []


@pytest.mark.parametrize(
    (
        "initial_files",
        "initial_directories",
        "removed_checksums",
        "expected_files",
        "expected_directories",
    ),
    [
        ([], [], [], [], []),
        ([a], [], ["a"], [], []),
        ([], [a], ["a"], [], []),
        ([a], [b], ["a"], [], [b]),
        ([a], [b], ["b"], [a], []),
        ([a, b, c], [], ["b"], [a, c], []),
        ([], [a, b, c], ["b"], [], [a, c]),
    ],
)
def test_zarr_checkums_remove_checksums(
    initial_files,
    initial_directories,
    removed_checksums,
    expected_files,
    expected_directories,
):
    checksums = ZarrChecksums(files=initial_files, directories=initial_directories)
    checksums.remove_checksums(removed_checksums)
    assert checksums.files == expected_files
    assert checksums.directories == expected_directories


# ZarrJSONChecksumSerializer tests


@pytest.mark.parametrize(
    "file_checksums,directory_checksums,checksum",
    [
        ([], [], "481a2f77ab786a0f45aafd5db0971caa"),
        (
            [ZarrChecksum(path="foo/bar", md5="a")],
            [],
            "cdcfdfca3622e20df03219273872549e",
        ),
        (
            [],
            [ZarrChecksum(path="foo/bar", md5="a")],
            "243aca82c6872222747183dd738b6fcb",
        ),
        (
            [
                ZarrChecksum(path="foo/bar", md5="a"),
                ZarrChecksum(path="foo/baz", md5="b"),
            ],
            [],
            "785295076ae9156b363e442ef6d485e0",
        ),
        (
            [],
            [
                ZarrChecksum(path="foo/bar", md5="a"),
                ZarrChecksum(path="foo/baz", md5="b"),
            ],
            "ebca8bb8e716237e0f71657d1045930f",
        ),
        (
            [ZarrChecksum(path="foo/baz", md5="a")],
            [ZarrChecksum(path="foo/bar", md5="b")],
            "9c34644ba03b7e9f58ebd1caef4215ad",
        ),
    ],
)
def test_zarr_checksum_serializer_aggregate_checksum(
    file_checksums, directory_checksums, checksum
):
    serializer = ZarrJSONChecksumSerializer()
    assert (
        serializer.aggregate_checksum(
            ZarrChecksums(files=file_checksums, directories=directory_checksums)
        )
        == checksum
    )


def test_zarr_checksum_serializer_generate_listing():
    serializer = ZarrJSONChecksumSerializer()
    checksums = ZarrChecksums(
        files=[ZarrChecksum(path="foo/bar", md5="a")],
        directories=[ZarrChecksum(path="foo/baz", md5="b")],
    )
    assert serializer.generate_listing(checksums) == ZarrChecksumListing(
        checksums=checksums, md5="23076057c0da63f8ab50d0a108db332c"
    )


def test_zarr_serialize():
    serializer = ZarrJSONChecksumSerializer()
    assert (
        serializer.serialize(
            ZarrChecksumListing(
                checksums=ZarrChecksums(
                    files=[ZarrChecksum(path="foo/bar", md5="a")],
                    directories=[ZarrChecksum(path="bar/foo", md5="b")],
                ),
                md5="c",
            )
        )
        == '{"checksums":{"directories":[{"md5":"b","path":"bar/foo"}],"files":[{"md5":"a","path":"foo/bar"}]},"md5":"c"}'  # noqa: E501
    )


def test_zarr_deserialize():
    serializer = ZarrJSONChecksumSerializer()
    assert serializer.deserialize(
        '{"checksums":{"directories":[{"md5":"b","path":"bar/foo"}],"files":[{"md5":"a","path":"foo/bar"}]},"md5":"c"}'  # noqa: E501
    ) == ZarrChecksumListing(
        checksums=ZarrChecksums(
            files=[ZarrChecksum(path="foo/bar", md5="a")],
            directories=[ZarrChecksum(path="bar/foo", md5="b")],
        ),
        md5="c",
    )


@pytest.mark.parametrize(
    "files,directories,checksum",
    [
        (
            {"foo/bar": "a"},
            {},
            "cdcfdfca3622e20df03219273872549e",
        ),
        (
            {},
            {"foo/bar": "a"},
            "243aca82c6872222747183dd738b6fcb",
        ),
        (
            {"foo/bar": "a", "foo/baz": "b"},
            {},
            "785295076ae9156b363e442ef6d485e0",
        ),
        (
            {},
            {"foo/bar": "a", "foo/baz": "b"},
            "ebca8bb8e716237e0f71657d1045930f",
        ),
        (
            {},
            {"foo/baz": "b", "foo/bar": "a"},
            "ebca8bb8e716237e0f71657d1045930f",
        ),
        (
            {"foo/baz": "a"},
            {"foo/bar": "b"},
            "9c34644ba03b7e9f58ebd1caef4215ad",
        ),
    ],
)
def test_zarr_get_checksum(files, directories, checksum):
    assert get_checksum(files=files, directories=directories) == checksum


def test_zarr_get_checksum_empty():
    with pytest.raises(ValueError):
        get_checksum(files={}, directories={})
