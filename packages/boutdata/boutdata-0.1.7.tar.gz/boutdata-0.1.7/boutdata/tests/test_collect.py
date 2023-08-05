from glob import glob
import numpy as np
import numpy.testing as npt
from pathlib import Path
import pytest

from boutdata.collect import collect
from boutdata.squashoutput import squashoutput

from boutdata.tests.make_test_data import (
    apply_slices,
    create_dump_file,
    concatenate_data,
    expected_attributes,
    make_grid_info,
    remove_xboundaries,
    remove_yboundaries,
    remove_yboundaries_upper_divertor,
)

# Note - using tmp_path fixture requires pytest>=3.9.0

collect_kwargs_list = [
    {"xguards": True, "yguards": "include_upper"},
    {"xguards": False, "yguards": "include_upper"},
    {"xguards": True, "yguards": True},
    {"xguards": False, "yguards": True},
    {"xguards": True, "yguards": False},
    {"xguards": False, "yguards": False},
]

squash_params_list = [
    (False, {}),
    (True, {}),
    (True, {"parallel": 2}),
]


def check_collected_data(
    expected,
    *,
    fieldperp_global_yind,
    doublenull,
    path,
    squash,
    collect_kwargs,
    squash_kwargs={},
):
    """
    Use `collect()` to read 'actual' data from the files. Test that 'actual' and
    'expected' data and attributes match.

    Parameters
    ----------
    expected : dict {str: numpy array}
        dict of expected data (key is name, value is scalar or numpy array of data).
        Arrays should be global (not per-process).
    fieldperp_global_yind : int
        Global y-index where FieldPerps are expected to be defined.
    path : pathlib.Path or str
        Path to collect data from.
    squash : bool
        If True, call `squashoutput()` and delete the `BOUT.dmp.*.nc` files (so that we
        can only read the 'squashed' data) before collecting and checking data.
    collect_kwargs : dict
        Keyword arguments passed to `collect()`.
    squash_kwargs : dict, optional
        Keyword arguments passed to `squashoutput()`.
    """
    # Apply effect of arguments to expected data
    if not collect_kwargs["xguards"]:
        remove_xboundaries(expected, expected["MXG"])
    if collect_kwargs["yguards"] is True and doublenull:
        remove_yboundaries_upper_divertor(
            expected, expected["MYG"], expected["ny_inner"]
        )
    if not collect_kwargs["yguards"]:
        remove_yboundaries(expected, expected["MYG"], expected["ny_inner"], doublenull)

    collect_kwargs = collect_kwargs.copy()
    if squash:
        squashoutput(path, outputname="boutdata.nc", **collect_kwargs, **squash_kwargs)
        collect_kwargs["prefix"] = "boutdata"
        # Delete dump files to be sure we do not read from them
        dump_names = glob(str(path.joinpath("BOUT.dmp.*.nc")))
        for x in dump_names:
            Path(x).unlink()
        # Reset arguments that are taken care of by squashoutput
        for x in ("tind", "xind", "yind", "zind"):
            if x in collect_kwargs:
                collect_kwargs.pop(x)
        # Never remove x-boundaries when collecting from a squashed file without them
        collect_kwargs["xguards"] = True
        # Never remove y-boundaries when collecting from a squashed file without them
        collect_kwargs["yguards"] = "include_upper"

    for varname in expected:
        actual = collect(varname, path=path, **collect_kwargs)
        check_variable(
            varname,
            actual,
            expected[varname],
            expected_attributes.get(varname, None),
            fieldperp_global_yind,
        )


def check_variable(
    varname, actual, expected_data, expected_attributes, fieldperp_global_yind
):
    """
    Check a single variable

    Parameters
    ----------
    varname : str
        Name of the variable
    actual : BoutArray
        The collected variable
    expected_data : np.Array
        Expected data for the variable
    expected_attributes : dict or None
        Expected attributes for the variable
    fieldperp_global_yind : int
        Global y-index where FieldPerps have been created
    """
    npt.assert_array_equal(expected_data, actual)
    actual_keys = list(actual.attributes.keys())
    if expected_attributes is not None:
        for a in expected_attributes:
            assert actual.attributes[a] == expected_attributes[a]
            actual_keys.remove(a)

    if "fieldperp" in varname:
        assert actual.attributes["yindex_global"] == fieldperp_global_yind
        actual_keys.remove("yindex_global")

    assert actual_keys == ["bout_type"]

    if "field3d_t" in varname:
        assert actual.attributes["bout_type"] == "Field3D_t"
    elif "field3d" in varname:
        assert actual.attributes["bout_type"] == "Field3D"
    elif "field2d_t" in varname:
        assert actual.attributes["bout_type"] == "Field2D_t"
    elif "field2d" in varname:
        assert actual.attributes["bout_type"] == "Field2D"
    elif "fieldperp_t" in varname:
        assert actual.attributes["bout_type"] == "FieldPerp_t"
    elif "fieldperp" in varname:
        assert actual.attributes["bout_type"] == "FieldPerp"
    elif "_t" in varname or varname == "t_array":
        assert actual.attributes["bout_type"] == "scalar_t"
    else:
        assert actual.attributes["bout_type"] == "scalar"


class TestCollect:
    @pytest.mark.parametrize("squash_params", squash_params_list)
    @pytest.mark.parametrize("collect_kwargs", collect_kwargs_list)
    def test_core_min_files(self, tmp_path, squash_params, collect_kwargs):
        """
        Check output from a core-only case using the minimum number of processes
        """
        squash, squash_kwargs = squash_params

        grid_info = make_grid_info()

        fieldperp_global_yind = 3
        fieldperp_yproc_ind = 0

        rng = np.random.default_rng(100)

        # core
        # core includes "ylower" and "yupper" even though there is no actual y-boundary
        # because collect/squashoutput collect these points
        dump_params = [
            (0, ["xinner", "xouter", "ylower", "yupper"], fieldperp_global_yind),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        check_collected_data(
            expected,
            fieldperp_global_yind=fieldperp_global_yind,
            doublenull=False,
            path=tmp_path,
            squash=squash,
            collect_kwargs=collect_kwargs,
            squash_kwargs=squash_kwargs,
        )

    @pytest.mark.parametrize(
        "time_split",
        [
            (None, None),
            (1, None),
            (2, None),
            (2, 3),
            (3, None),
            (4, None),
            (5, None),
            (6, None),
            (7, None),
        ],
    )
    def test_core_min_files_existing_squash_file_raises(self, tmp_path, time_split):
        """
        Check output from a core-only case using the minimum number of processes
        """
        time_split_size, time_split_first_label = time_split

        squash_kwargs = {}
        if time_split_size is not None:
            squash_kwargs["time_split_size"] = time_split_size
        if time_split_first_label is not None:
            squash_kwargs["time_split_first_label"] = time_split_first_label

        grid_info = make_grid_info()

        fieldperp_global_yind = 3

        rng = np.random.default_rng(100)

        # core
        # core includes "ylower" and "yupper" even though there is no actual y-boundary
        # because collect/squashoutput collect these points
        dump_params = [
            (0, ["xinner", "xouter", "ylower", "yupper"], fieldperp_global_yind),
        ]
        for i, boundaries, fieldperp_yind in dump_params:
            create_dump_file(
                tmpdir=tmp_path,
                rng=rng,
                grid_info=grid_info,
                i=i,
                boundaries=boundaries,
                fieldperp_global_yind=fieldperp_yind,
            )

        if time_split_size is None:
            filenames = ["boutdata.nc"]
        else:
            first = 0 if time_split_first_label is None else time_split_first_label
            # Assumes 'nt' is always 6, as set by make_grid_info() and
            # create_dump_file()
            n_output = (6 + time_split_size - 1) // time_split_size
            filenames = [f"boutdata{i}.nc" for i in range(first, first + n_output)]

        for f in filenames:
            # Create file named f
            existing_file = tmp_path.joinpath(f)
            existing_file.touch()

            with pytest.raises(
                ValueError,
                match=r" will not overwrite. Also, for some filenames collect may try "
                r"to read from this file, which is presumably not desired behaviour.",
            ):
                squashoutput(tmp_path, outputname="boutdata.nc", **squash_kwargs)

            # Remove 'existing_file' so we can check the next one
            existing_file.unlink()

    @pytest.mark.parametrize(
        "time_split",
        [
            (1, None),
            (2, None),
            (2, 3),
            (3, None),
            (4, None),
            (5, None),
            (6, None),
            (7, None),
        ],
    )
    @pytest.mark.parametrize("parallel", [False, 2])
    def test_core_min_files_time_split(self, tmp_path, time_split, parallel):
        """
        Check output from a core-only case using the minimum number of processes
        """
        collect_kwargs = {"xguards": True, "yguards": "include_upper"}
        squash_kwargs = {"time_split_size": time_split[0], "parallel": parallel}
        if time_split[1] is not None:
            squash_kwargs["time_split_first_label"] = time_split[1]

        grid_info = make_grid_info()

        fieldperp_global_yind = 3
        fieldperp_yproc_ind = 0

        rng = np.random.default_rng(100)

        # core
        # core includes "ylower" and "yupper" even though there is no actual y-boundary
        # because collect/squashoutput collect these points
        dump_params = [
            (0, ["xinner", "xouter", "ylower", "yupper"], fieldperp_global_yind),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        # Copy of check_collected_data code, modified to test series of output
        # files created when setting time_split_size
        ######################################################################

        # Always squash
        squashoutput(
            tmp_path, outputname="boutdata.nc", **collect_kwargs, **squash_kwargs
        )
        collect_prefix = "boutdata"
        # Delete dump files to be sure we do not read from them
        dump_names = glob(str(tmp_path.joinpath("BOUT.dmp.*.nc")))
        for x in dump_names:
            Path(x).unlink()

        # Assumes 'nt' is always 6, as set by make_grid_info() and create_dump_file()
        n_output = (6 + time_split[0] - 1) // time_split[0]
        if time_split[1] is None:
            start_ind = 0
        else:
            start_ind = time_split[1]

        for i in range(n_output):
            for varname in expected:
                actual = collect(
                    varname,
                    prefix=collect_prefix + str(start_ind + i),
                    path=tmp_path,
                    **collect_kwargs,
                )

                if "_t" in actual.attributes["bout_type"]:
                    expected_data = expected[varname][
                        i * time_split[0] : (i + 1) * time_split[0]
                    ]
                else:
                    expected_data = expected[varname]

                check_variable(
                    varname,
                    actual,
                    expected_data,
                    expected_attributes.get(varname, None),
                    fieldperp_global_yind,
                )

    def test_core_min_files_append_time_split_raises(self, tmp_path):
        """
        Check output from a core-only case using the minimum number of processes
        """
        collect_kwargs = {"xguards": True, "yguards": "include_upper"}
        squash_kwargs = {"time_split_size": 2, "append": True}

        grid_info = make_grid_info()

        fieldperp_global_yind = 3

        rng = np.random.default_rng(100)

        # core
        # core includes "ylower" and "yupper" even though there is no actual y-boundary
        # because collect/squashoutput collect these points
        dump_params = [
            (0, ["xinner", "xouter", "ylower", "yupper"], fieldperp_global_yind),
        ]
        for i, boundaries, fieldperp_yind in dump_params:
            create_dump_file(
                tmpdir=tmp_path,
                rng=rng,
                grid_info=grid_info,
                i=i,
                boundaries=boundaries,
                fieldperp_global_yind=fieldperp_yind,
            )

        with pytest.raises(
            ValueError, match="'time_split_size' is not compatible with append=True"
        ):
            squashoutput(
                tmp_path, outputname="boutdata.nc", **collect_kwargs, **squash_kwargs
            )

    @pytest.mark.parametrize("squash_params", squash_params_list)
    @pytest.mark.parametrize("collect_kwargs", collect_kwargs_list)
    def test_core(self, tmp_path, squash_params, collect_kwargs):
        """
        Check output from a core-only case using a large number of processes. 'Large'
        means there is at least one process in each region with no edges touching
        another region.
        """
        squash, squash_kwargs = squash_params

        grid_info = make_grid_info(nxpe=3, nype=3)

        fieldperp_global_yind = 3
        fieldperp_yproc_ind = 0

        rng = np.random.default_rng(101)

        # core
        # core includes "ylower" and "yupper" even though there is no actual y-boundary
        # because collect/squashoutput collect these points
        dump_params = [
            (0, ["xinner", "ylower"], fieldperp_global_yind),
            (1, ["ylower"], fieldperp_global_yind),
            (2, ["xouter", "ylower"], fieldperp_global_yind),
            (3, ["xinner"], -1),
            (4, [], -1),
            (5, ["xouter"], -1),
            (6, ["xinner", "yupper"], -1),
            (7, ["yupper"], -1),
            (8, ["xouter", "yupper"], -1),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        check_collected_data(
            expected,
            fieldperp_global_yind=fieldperp_global_yind,
            doublenull=False,
            path=tmp_path,
            squash=squash,
            collect_kwargs=collect_kwargs,
            squash_kwargs=squash_kwargs,
        )

    @pytest.mark.parametrize("squash_params", squash_params_list)
    @pytest.mark.parametrize("collect_kwargs", collect_kwargs_list)
    def test_sol_min_files(self, tmp_path, squash_params, collect_kwargs):
        """
        Check output from a SOL-only case using the minimum number of processes
        """
        squash, squash_kwargs = squash_params

        grid_info = make_grid_info(ixseps1=0, ixseps2=0)

        fieldperp_global_yind = 3
        fieldperp_yproc_ind = 0

        rng = np.random.default_rng(102)

        # SOL
        dump_params = [
            (0, ["xinner", "xouter", "ylower", "yupper"], fieldperp_global_yind),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        check_collected_data(
            expected,
            fieldperp_global_yind=fieldperp_global_yind,
            doublenull=False,
            path=tmp_path,
            squash=squash,
            collect_kwargs=collect_kwargs,
            squash_kwargs=squash_kwargs,
        )

    @pytest.mark.parametrize("squash_params", squash_params_list)
    @pytest.mark.parametrize("collect_kwargs", collect_kwargs_list)
    def test_sol(self, tmp_path, squash_params, collect_kwargs):
        """
        Check output from a SOL-only case using a large number of processes. 'Large'
        means there is at least one process in each region with no edges touching
        another region.
        """
        squash, squash_kwargs = squash_params

        grid_info = make_grid_info(nxpe=3, nype=3, ixseps1=0, ixseps2=0)

        fieldperp_global_yind = 3
        fieldperp_yproc_ind = 0

        rng = np.random.default_rng(103)

        # SOL
        dump_params = [
            (0, ["xinner", "ylower"], fieldperp_global_yind),
            (1, ["ylower"], fieldperp_global_yind),
            (2, ["xouter", "ylower"], fieldperp_global_yind),
            (3, ["xinner"], -1),
            (4, [], -1),
            (5, ["xouter"], -1),
            (6, ["xinner", "yupper"], -1),
            (7, ["yupper"], -1),
            (8, ["xouter", "yupper"], -1),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        check_collected_data(
            expected,
            fieldperp_global_yind=fieldperp_global_yind,
            doublenull=False,
            path=tmp_path,
            squash=squash,
            collect_kwargs=collect_kwargs,
            squash_kwargs=squash_kwargs,
        )

    @pytest.mark.parametrize("squash_params", squash_params_list)
    @pytest.mark.parametrize("collect_kwargs", collect_kwargs_list)
    def test_singlenull_min_files(self, tmp_path, squash_params, collect_kwargs):
        """
        Check output from a single-null case using the minimum number of processes
        """
        squash, squash_kwargs = squash_params

        grid_info = make_grid_info(nype=3, ixseps1=4, xpoints=1)

        fieldperp_global_yind = 7
        fieldperp_yproc_ind = 1

        rng = np.random.default_rng(104)

        dump_params = [
            # inner divertor leg
            (0, ["xinner", "xouter", "ylower"], -1),
            # core
            (1, ["xinner", "xouter"], fieldperp_global_yind),
            # outer divertor leg
            (2, ["xinner", "xouter", "yupper"], -1),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        check_collected_data(
            expected,
            fieldperp_global_yind=fieldperp_global_yind,
            doublenull=False,
            path=tmp_path,
            squash=squash,
            collect_kwargs=collect_kwargs,
            squash_kwargs=squash_kwargs,
        )

    @pytest.mark.parametrize("squash_params", squash_params_list)
    @pytest.mark.parametrize("collect_kwargs", collect_kwargs_list)
    def test_singlenull_min_files_lower_boundary_fieldperp(
        self, tmp_path, squash_params, collect_kwargs
    ):
        """
        Check output from a single-null case using the minimum number of processes. This
        test puts the FieldPerp in the lower boundary.
        """
        squash, squash_kwargs = squash_params

        grid_info = make_grid_info(nype=3, ixseps1=4, xpoints=1)

        fieldperp_global_yind = 1
        fieldperp_yproc_ind = 0

        rng = np.random.default_rng(104)

        dump_params = [
            # inner divertor leg
            (0, ["xinner", "xouter", "ylower"], fieldperp_global_yind),
            # core
            (1, ["xinner", "xouter"], -1),
            # outer divertor leg
            (2, ["xinner", "xouter", "yupper"], -1),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        check_collected_data(
            expected,
            fieldperp_global_yind=fieldperp_global_yind,
            doublenull=False,
            path=tmp_path,
            squash=squash,
            collect_kwargs=collect_kwargs,
            squash_kwargs=squash_kwargs,
        )

    @pytest.mark.parametrize("squash_params", squash_params_list)
    @pytest.mark.parametrize("collect_kwargs", collect_kwargs_list)
    def test_singlenull_min_files_upper_boundary_fieldperp(
        self, tmp_path, squash_params, collect_kwargs
    ):
        """
        Check output from a single-null case using the minimum number of processes. This
        test puts the FieldPerp in the upper boundary.
        """
        squash, squash_kwargs = squash_params

        grid_info = make_grid_info(nype=3, ixseps1=4, xpoints=1)

        fieldperp_global_yind = 14
        fieldperp_yproc_ind = 2

        rng = np.random.default_rng(104)

        dump_params = [
            # inner divertor leg
            (0, ["xinner", "xouter", "ylower"], -1),
            # core
            (1, ["xinner", "xouter"], -1),
            # outer divertor leg
            (2, ["xinner", "xouter", "yupper"], fieldperp_global_yind),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        check_collected_data(
            expected,
            fieldperp_global_yind=fieldperp_global_yind,
            doublenull=False,
            path=tmp_path,
            squash=squash,
            collect_kwargs=collect_kwargs,
            squash_kwargs=squash_kwargs,
        )

    @pytest.mark.parametrize("squash_params", squash_params_list)
    def test_singlenull_min_files_fieldperp_on_two_yproc_different_index(
        self, tmp_path, squash_params
    ):
        """
        Check output from a single-null case using the minimum number of processes. This
        test has FieldPerps created with inconsistent y-indices to check this produces
        an error.
        """
        squash, squash_kwargs = squash_params

        collect_kwargs = {"xguards": True, "yguards": "include_upper"}

        grid_info = make_grid_info(nype=3, ixseps1=4, xpoints=1)

        fieldperp_global_yind = 7
        fieldperp_yproc_ind = 1

        rng = np.random.default_rng(104)

        dump_params = [
            # inner divertor leg
            (0, ["xinner", "xouter", "ylower"], 2),
            # core
            (1, ["xinner", "xouter"], 7),
            # outer divertor leg
            (2, ["xinner", "xouter", "yupper"], -1),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        with pytest.raises(ValueError, match="Found FieldPerp"):
            check_collected_data(
                expected,
                fieldperp_global_yind=fieldperp_global_yind,
                doublenull=False,
                path=tmp_path,
                squash=squash,
                collect_kwargs=collect_kwargs,
                squash_kwargs=squash_kwargs,
            )

    @pytest.mark.parametrize("squash_params", squash_params_list)
    def test_singlenull_min_files_fieldperp_on_two_yproc_same_index(
        self, tmp_path, squash_params
    ):
        """
        Check output from a single-null case using the minimum number of processes. This
        test has FieldPerps created on different y-processes to check this produces an
        error.
        """
        squash, squash_kwargs = squash_params

        collect_kwargs = {"xguards": True, "yguards": "include_upper"}

        grid_info = make_grid_info(nype=3, ixseps1=4, xpoints=1)

        fieldperp_global_yind = 7
        fieldperp_yproc_ind = 1

        rng = np.random.default_rng(104)

        dump_params = [
            # inner divertor leg
            (0, ["xinner", "xouter", "ylower"], 7),
            # core
            (1, ["xinner", "xouter"], 7),
            # outer divertor leg
            (2, ["xinner", "xouter", "yupper"], -1),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        with pytest.raises(ValueError, match="Found FieldPerp"):
            check_collected_data(
                expected,
                fieldperp_global_yind=fieldperp_global_yind,
                doublenull=False,
                path=tmp_path,
                squash=squash,
                collect_kwargs=collect_kwargs,
                squash_kwargs=squash_kwargs,
            )

    @pytest.mark.parametrize("squash_params", squash_params_list)
    @pytest.mark.parametrize("collect_kwargs", collect_kwargs_list)
    def test_singlenull(self, tmp_path, squash_params, collect_kwargs):
        """
        Check output from a single-null case using a large number of processes. 'Large'
        means there is at least one process in each region with no edges touching
        another region.
        """
        squash, squash_kwargs = squash_params

        grid_info = make_grid_info(nxpe=3, nype=9, ixseps1=7, xpoints=1)

        fieldperp_global_yind = 19
        fieldperp_yproc_ind = 4

        rng = np.random.default_rng(105)

        dump_params = [
            # inner divertor leg
            (0, ["xinner", "ylower"], -1),
            (1, ["ylower"], -1),
            (2, ["xouter", "ylower"], -1),
            (3, ["xinner"], -1),
            (4, [], -1),
            (5, ["xouter"], -1),
            (6, ["xinner"], -1),
            (7, [], -1),
            (8, ["xouter"], -1),
            # core
            (9, ["xinner"], -1),
            (10, [], -1),
            (11, ["xouter"], -1),
            (12, ["xinner"], fieldperp_global_yind),
            (13, [], fieldperp_global_yind),
            (14, ["xouter"], fieldperp_global_yind),
            (15, ["xinner"], -1),
            (16, [], -1),
            (17, ["xouter"], -1),
            # outer divertor leg
            (18, ["xinner"], -1),
            (19, [], -1),
            (20, ["xouter"], -1),
            (21, ["xinner"], -1),
            (22, [], -1),
            (23, ["xouter"], -1),
            (24, ["xinner", "yupper"], -1),
            (25, ["yupper"], -1),
            (26, ["xouter", "yupper"], -1),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        check_collected_data(
            expected,
            fieldperp_global_yind=fieldperp_global_yind,
            doublenull=False,
            path=tmp_path,
            squash=squash,
            collect_kwargs=collect_kwargs,
            squash_kwargs=squash_kwargs,
        )

    @pytest.mark.parametrize(
        "squash_kwargs",
        (
            # {"parallel": False},
            {"parallel": 1},
            {"parallel": 2},
            {"parallel": 3},
            {"parallel": 4},
            {"parallel": 5},
            {"parallel": 6},
            {"parallel": 7},
            {"parallel": 8},
            {"parallel": True},
        ),
    )
    def test_singlenull_squashoutput_np(self, tmp_path, squash_kwargs):
        """
        Check output from a single-null case using a large number of processes. 'Large'
        means there is at least one process in each region with no edges touching
        another region.
        """
        grid_info = make_grid_info(nxpe=3, nype=9, ixseps1=7, xpoints=1)

        fieldperp_global_yind = 19
        fieldperp_yproc_ind = 4

        rng = np.random.default_rng(105)

        dump_params = [
            # inner divertor leg
            (0, ["xinner", "ylower"], -1),
            (1, ["ylower"], -1),
            (2, ["xouter", "ylower"], -1),
            (3, ["xinner"], -1),
            (4, [], -1),
            (5, ["xouter"], -1),
            (6, ["xinner"], -1),
            (7, [], -1),
            (8, ["xouter"], -1),
            # core
            (9, ["xinner"], -1),
            (10, [], -1),
            (11, ["xouter"], -1),
            (12, ["xinner"], fieldperp_global_yind),
            (13, [], fieldperp_global_yind),
            (14, ["xouter"], fieldperp_global_yind),
            (15, ["xinner"], -1),
            (16, [], -1),
            (17, ["xouter"], -1),
            # outer divertor leg
            (18, ["xinner"], -1),
            (19, [], -1),
            (20, ["xouter"], -1),
            (21, ["xinner"], -1),
            (22, [], -1),
            (23, ["xouter"], -1),
            (24, ["xinner", "yupper"], -1),
            (25, ["yupper"], -1),
            (26, ["xouter", "yupper"], -1),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        check_collected_data(
            expected,
            fieldperp_global_yind=fieldperp_global_yind,
            doublenull=False,
            path=tmp_path,
            squash=True,
            collect_kwargs={"xguards": True, "yguards": "include_upper"},
            squash_kwargs=squash_kwargs,
        )

    @pytest.mark.parametrize("squash_params", squash_params_list)
    # This parametrize passes tuples for 'tind', 'xind', 'yind' and 'zind'. The first
    # value is the 'tind'/'xind'/'yind'/'zind' argument to pass to collect() or
    # squashoutput(), the second is the equivalent slice() to use on the expected
    # output.
    #
    # Note that the 3-element list form of the argument is inconsistent with the
    # 2-element form as the 3-element uses an exclusive end index (like slice()) while
    # the 2-element uses an inclusive end index (for backward compatibility).
    @pytest.mark.parametrize(
        ("tind", "xind", "yind", "zind"),
        [
            # t-slicing
            (
                (2, slice(2, 3)),
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                (slice(4), slice(4)),
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                ([0, 3], slice(4)),
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                (slice(2, None), slice(2, None)),
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                ([2, -1], slice(2, None)),
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                (slice(2, 4), slice(2, 4)),
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                ([2, 3], slice(2, 4)),
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                (slice(None, None, 3), slice(None, None, 3)),
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                ([0, -1, 3], slice(None, -1, 3)),
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                (slice(1, 5, 2), slice(1, 5, 2)),
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                ([1, 4, 2], slice(1, 4, 2)),
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            # x-slicing
            (
                (None, slice(None)),
                (7, slice(7, 8)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                (slice(8), slice(8)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                ([0, 8], slice(9)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                (slice(4, None), slice(4, None)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                ([5, -1], slice(5, None)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                (slice(6, 10), slice(6, 10)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                ([4, 8], slice(4, 9)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                (slice(None, None, 4), slice(None, None, 4)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                ([0, -1, 3], slice(None, -1, 3)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                (slice(3, 10, 3), slice(3, 10, 3)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                ([4, 8, 4], slice(4, 8, 4)),
                (None, slice(None)),
                (None, slice(None)),
            ),
            # y-slicing
            (
                (None, slice(None)),
                (None, slice(None)),
                (17, slice(17, 18)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                (slice(30), slice(30)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                ([0, 28], slice(29)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                (slice(5, None), slice(5, None)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                ([6, -1], slice(6, None)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                (slice(7, 28), slice(7, 28)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                ([8, 27], slice(8, 28)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                (slice(None, None, 5), slice(None, None, 5)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                ([0, -1, 6], slice(None, -1, 6)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                (slice(9, 26, 7), slice(9, 26, 7)),
                (None, slice(None)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                ([5, 33, 4], slice(5, 33, 4)),
                (None, slice(None)),
            ),
            # z-slicing
            (
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
                (1, slice(1, 2)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
                (slice(3), slice(3)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
                ([0, 2], slice(3)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
                (slice(1, None), slice(1, None)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
                ([1, -1], slice(1, None)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
                (slice(1, 3), slice(1, 3)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
                ([1, 2], slice(1, 3)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
                (slice(None, None, 2), slice(None, None, 2)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
                ([0, -1, 2], slice(None, -1, 2)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
                (slice(1, 4, 2), slice(1, 4, 2)),
            ),
            (
                (None, slice(None)),
                (None, slice(None)),
                (None, slice(None)),
                ([1, 3, 2], slice(1, 3, 2)),
            ),
            # combined slicing
            ((2, slice(2, 3)), (7, slice(7, 8)), (17, slice(17, 18)), (1, slice(1, 2))),
            (
                (slice(4), slice(4)),
                (slice(8), slice(8)),
                (slice(30), slice(30)),
                (slice(3), slice(3)),
            ),
            (
                ([0, 3], slice(4)),
                ([0, 9], slice(10)),
                ([0, 28], slice(29)),
                ([0, 2], slice(3)),
            ),
            (
                (slice(2, None), slice(2, None)),
                (slice(4, None), slice(4, None)),
                (slice(5, None), slice(5, None)),
                (slice(1, None), slice(1, None)),
            ),
            (
                ([2, -1], slice(2, None)),
                ([5, -1], slice(5, None)),
                ([6, -1], slice(6, None)),
                ([1, -1], slice(1, None)),
            ),
            (
                (slice(2, 4), slice(2, 4)),
                (slice(6, 10), slice(6, 10)),
                (slice(7, 28), slice(7, 28)),
                (slice(1, 3), slice(1, 3)),
            ),
            (
                ([2, 3], slice(2, 4)),
                ([4, 8], slice(4, 9)),
                ([8, 27], slice(8, 28)),
                ([1, 2], slice(1, 3)),
            ),
            (
                (slice(None, None, 3), slice(None, None, 3)),
                (slice(None, None, 4), slice(None, None, 4)),
                (slice(None, None, 5), slice(None, None, 5)),
                (slice(None, None, 2), slice(None, None, 2)),
            ),
            (
                ([0, -1, 3], slice(None, -1, 3)),
                ([0, -1, 3], slice(None, -1, 3)),
                ([0, -1, 6], slice(None, -1, 6)),
                ([0, -1, 2], slice(None, -1, 2)),
            ),
            (
                (slice(1, 5, 2), slice(1, 5, 2)),
                (slice(3, 10, 3), slice(3, 10, 3)),
                (slice(9, 26, 7), slice(9, 26, 7)),
                (slice(1, 4, 2), slice(1, 4, 2)),
            ),
            (
                ([1, 4, 2], slice(1, 4, 2)),
                ([4, 8, 4], slice(4, 8, 4)),
                ([5, 33, 4], slice(5, 33, 4)),
                ([1, 3, 2], slice(1, 3, 2)),
            ),
        ],
    )
    def test_singlenull_tind_xind_yind_zind(
        self, tmp_path, squash_params, tind, xind, yind, zind
    ):
        """
        Check output from a single-null case using a large number of processes. 'Large'
        means there is at least one process in each region with no edges touching
        another region. This test checks the 'tind', 'xind', 'yind' and 'zind' arguments
        to `collect()` and `squashoutput()`.
        """
        tind, tslice = tind
        xind, xslice = xind
        yind, yslice = yind
        zind, zslice = zind

        squash, squash_kwargs = squash_params

        collect_kwargs = {
            "xguards": True,
            "yguards": "include_upper",
            "tind": tind,
            "xind": xind,
            "yind": yind,
            "zind": zind,
        }

        grid_info = make_grid_info(nxpe=3, nype=9, ixseps1=7, xpoints=1)

        fieldperp_global_yind = 19
        fieldperp_yproc_ind = 4

        rng = np.random.default_rng(106)

        dump_params = [
            # inner divertor leg
            (0, ["xinner", "ylower"], -1),
            (1, ["ylower"], -1),
            (2, ["xouter", "ylower"], -1),
            (3, ["xinner"], -1),
            (4, [], -1),
            (5, ["xouter"], -1),
            (6, ["xinner"], -1),
            (7, [], -1),
            (8, ["xouter"], -1),
            # core
            (9, ["xinner"], -1),
            (10, [], -1),
            (11, ["xouter"], -1),
            (12, ["xinner"], fieldperp_global_yind),
            (13, [], fieldperp_global_yind),
            (14, ["xouter"], fieldperp_global_yind),
            (15, ["xinner"], -1),
            (16, [], -1),
            (17, ["xouter"], -1),
            # outer divertor leg
            (18, ["xinner"], -1),
            (19, [], -1),
            (20, ["xouter"], -1),
            (21, ["xinner"], -1),
            (22, [], -1),
            (23, ["xouter"], -1),
            (24, ["xinner", "yupper"], -1),
            (25, ["yupper"], -1),
            (26, ["xouter", "yupper"], -1),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        # Can only apply here (before effect of 'xguards' and 'yguards' is applied in
        # check_collected_data) because we keep 'xguards=True' and
        # 'yguards="include_upper"' for this test, so neither has an effect.
        apply_slices(expected, tslice, xslice, yslice, zslice)

        check_collected_data(
            expected,
            fieldperp_global_yind=fieldperp_global_yind,
            doublenull=False,
            path=tmp_path,
            squash=squash,
            collect_kwargs=collect_kwargs,
            squash_kwargs=squash_kwargs,
        )

    @pytest.mark.parametrize("squash_params", squash_params_list)
    @pytest.mark.parametrize("collect_kwargs", collect_kwargs_list)
    def test_connected_doublenull_min_files(
        self, tmp_path, squash_params, collect_kwargs
    ):
        """
        Check output from a connected double-null case using the minimum number of
        processes
        """
        squash, squash_kwargs = squash_params

        grid_info = make_grid_info(nype=6, ixseps1=4, ixseps2=4, xpoints=2)

        fieldperp_global_yind = 7
        fieldperp_yproc_ind = 1

        rng = np.random.default_rng(107)

        dump_params = [
            # inner, lower divertor leg
            (0, ["xinner", "xouter", "ylower"], -1),
            # inner core
            (1, ["xinner", "xouter"], fieldperp_global_yind),
            # inner, upper divertor leg
            (2, ["xinner", "xouter", "yupper"], -1),
            # outer, upper divertor leg
            (3, ["xinner", "xouter", "ylower"], -1),
            # outer core
            (4, ["xinner", "xouter"], -1),
            # outer, lower divertor leg
            (5, ["xinner", "xouter", "yupper"], -1),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        check_collected_data(
            expected,
            fieldperp_global_yind=fieldperp_global_yind,
            doublenull=True,
            path=tmp_path,
            squash=squash,
            collect_kwargs=collect_kwargs,
            squash_kwargs=squash_kwargs,
        )

    @pytest.mark.parametrize("squash_params", squash_params_list)
    @pytest.mark.parametrize("collect_kwargs", collect_kwargs_list)
    def test_connected_doublenull(self, tmp_path, squash_params, collect_kwargs):
        """
        Check output from a connected double-null case using a large number of
        processes. 'Large' means there is at least one process in each region with no
        edges touching another region.
        """
        squash, squash_kwargs = squash_params

        grid_info = make_grid_info(nxpe=3, nype=18, ixseps1=7, ixseps2=7, xpoints=2)

        fieldperp_global_yind = 19
        fieldperp_yproc_ind = 4

        rng = np.random.default_rng(108)

        dump_params = [
            # inner, lower divertor leg
            (0, ["xinner", "ylower"], -1),
            (1, ["ylower"], -1),
            (2, ["xouter", "ylower"], -1),
            (3, ["xinner"], -1),
            (4, [], -1),
            (5, ["xouter"], -1),
            (6, ["xinner"], -1),
            (7, [], -1),
            (8, ["xouter"], -1),
            # inner core
            (9, ["xinner"], -1),
            (10, [], -1),
            (11, ["xouter"], -1),
            (12, ["xinner"], fieldperp_global_yind),
            (13, [], fieldperp_global_yind),
            (14, ["xouter"], fieldperp_global_yind),
            (15, ["xinner"], -1),
            (16, [], -1),
            (17, ["xouter"], -1),
            # inner, upper divertor leg
            (18, ["xinner"], -1),
            (19, [], -1),
            (20, ["xouter"], -1),
            (21, ["xinner"], -1),
            (22, [], -1),
            (23, ["xouter"], -1),
            (24, ["xinner", "yupper"], -1),
            (25, ["yupper"], -1),
            (26, ["xouter", "yupper"], -1),
            # outer, upper divertor leg
            (27, ["xinner", "ylower"], -1),
            (28, ["ylower"], -1),
            (29, ["xouter", "ylower"], -1),
            (30, ["xinner"], -1),
            (31, [], -1),
            (32, ["xouter"], -1),
            (33, ["xinner"], -1),
            (34, [], -1),
            (35, ["xouter"], -1),
            # outer core
            (36, ["xinner"], -1),
            (37, [], -1),
            (38, ["xouter"], -1),
            (39, ["xinner"], -1),
            (40, [], -1),
            (41, ["xouter"], -1),
            (42, ["xinner"], -1),
            (43, [], -1),
            (44, ["xouter"], -1),
            # outer, lower divertor leg
            (45, ["xinner"], -1),
            (46, [], -1),
            (47, ["xouter"], -1),
            (48, ["xinner"], -1),
            (49, [], -1),
            (50, ["xouter"], -1),
            (51, ["xinner", "yupper"], -1),
            (52, ["yupper"], -1),
            (53, ["xouter", "yupper"], -1),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        check_collected_data(
            expected,
            fieldperp_global_yind=fieldperp_global_yind,
            doublenull=True,
            path=tmp_path,
            squash=squash,
            collect_kwargs=collect_kwargs,
            squash_kwargs=squash_kwargs,
        )

    @pytest.mark.parametrize("squash_params", squash_params_list)
    @pytest.mark.parametrize("collect_kwargs", collect_kwargs_list)
    def test_disconnected_doublenull_min_files(
        self, tmp_path, squash_params, collect_kwargs
    ):
        """
        Check output from a disconnected double-null case using the minimum number of
        processes
        """
        squash, squash_kwargs = squash_params

        grid_info = make_grid_info(nype=6, ixseps1=3, ixseps2=5, xpoints=2)

        fieldperp_global_yind = 7
        fieldperp_yproc_ind = 1

        rng = np.random.default_rng(109)

        dump_params = [
            # inner, lower divertor leg
            (0, ["xinner", "xouter", "ylower"], -1),
            # inner core
            (1, ["xinner", "xouter"], fieldperp_global_yind),
            # inner, upper divertor leg
            (2, ["xinner", "xouter", "yupper"], -1),
            # outer, upper divertor leg
            (3, ["xinner", "xouter", "ylower"], -1),
            # outer core
            (4, ["xinner", "xouter"], -1),
            # outer, lower divertor leg
            (5, ["xinner", "xouter", "yupper"], -1),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        check_collected_data(
            expected,
            fieldperp_global_yind=fieldperp_global_yind,
            doublenull=True,
            path=tmp_path,
            squash=squash,
            collect_kwargs=collect_kwargs,
            squash_kwargs=squash_kwargs,
        )

    @pytest.mark.parametrize("squash_params", squash_params_list)
    @pytest.mark.parametrize("collect_kwargs", collect_kwargs_list)
    @pytest.mark.parametrize("mxg", [0, 1, 2])
    @pytest.mark.parametrize("myg", [0, 1, 2])
    def test_disconnected_doublenull(
        self, tmp_path, squash_params, collect_kwargs, mxg, myg
    ):
        """
        Check output from a disconnected double-null case using a large number of
        processes. 'Large' means there is at least one process in each region with no
        edges touching another region.
        """
        squash, squash_kwargs = squash_params

        grid_info = make_grid_info(
            mxg=mxg, myg=myg, nxpe=3, nype=18, ixseps1=6, ixseps2=11, xpoints=2
        )

        fieldperp_global_yind = 19
        fieldperp_yproc_ind = 4

        rng = np.random.default_rng(110)

        dump_params = [
            # inner, lower divertor leg
            (0, ["xinner", "ylower"], -1),
            (1, ["ylower"], -1),
            (2, ["xouter", "ylower"], -1),
            (3, ["xinner"], -1),
            (4, [], -1),
            (5, ["xouter"], -1),
            (6, ["xinner"], -1),
            (7, [], -1),
            (8, ["xouter"], -1),
            # inner core
            (9, ["xinner"], -1),
            (10, [], -1),
            (11, ["xouter"], -1),
            (12, ["xinner"], fieldperp_global_yind),
            (13, [], fieldperp_global_yind),
            (14, ["xouter"], fieldperp_global_yind),
            (15, ["xinner"], -1),
            (16, [], -1),
            (17, ["xouter"], -1),
            # inner, upper divertor leg
            (18, ["xinner"], -1),
            (19, [], -1),
            (20, ["xouter"], -1),
            (21, ["xinner"], -1),
            (22, [], -1),
            (23, ["xouter"], -1),
            (24, ["xinner", "yupper"], -1),
            (25, ["yupper"], -1),
            (26, ["xouter", "yupper"], -1),
            # outer, upper divertor leg
            (27, ["xinner", "ylower"], -1),
            (28, ["ylower"], -1),
            (29, ["xouter", "ylower"], -1),
            (30, ["xinner"], -1),
            (31, [], -1),
            (32, ["xouter"], -1),
            (33, ["xinner"], -1),
            (34, [], -1),
            (35, ["xouter"], -1),
            # outer core
            (36, ["xinner"], -1),
            (37, [], -1),
            (38, ["xouter"], -1),
            (39, ["xinner"], -1),
            (40, [], -1),
            (41, ["xouter"], -1),
            (42, ["xinner"], -1),
            (43, [], -1),
            (44, ["xouter"], -1),
            # outer, lower divertor leg
            (45, ["xinner"], -1),
            (46, [], -1),
            (47, ["xouter"], -1),
            (48, ["xinner"], -1),
            (49, [], -1),
            (50, ["xouter"], -1),
            (51, ["xinner", "yupper"], -1),
            (52, ["yupper"], -1),
            (53, ["xouter", "yupper"], -1),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        check_collected_data(
            expected,
            fieldperp_global_yind=fieldperp_global_yind,
            doublenull=True,
            path=tmp_path,
            squash=squash,
            collect_kwargs=collect_kwargs,
            squash_kwargs=squash_kwargs,
        )

    @pytest.mark.parametrize(
        "squash_kwargs",
        [
            {},
            {"compress": True, "complevel": 1},
            {"compress": True, "complevel": 2},
            {"compress": True, "complevel": 3},
            {"compress": True, "complevel": 4},
            {"compress": True, "complevel": 5},
            {"compress": True, "complevel": 5},
            {"compress": True, "complevel": 7},
            {"compress": True, "complevel": 8},
            {"compress": True, "complevel": 9},
        ],
    )
    def test_disconnected_doublenull_with_compression(self, tmp_path, squash_kwargs):
        """
        Check output from a disconnected double-null case using a large number of
        processes. 'Large' means there is at least one process in each region with no
        edges touching another region. This test checks some compression options that
        can be used with `squashoutput()`, verifying that they do not modify data.
        """
        grid_info = make_grid_info(nxpe=3, nype=18, ixseps1=6, ixseps2=11, xpoints=2)

        fieldperp_global_yind = 19
        fieldperp_yproc_ind = 4

        rng = np.random.default_rng(111)

        dump_params = [
            # inner, lower divertor leg
            (0, ["xinner", "ylower"], -1),
            (1, ["ylower"], -1),
            (2, ["xouter", "ylower"], -1),
            (3, ["xinner"], -1),
            (4, [], -1),
            (5, ["xouter"], -1),
            (6, ["xinner"], -1),
            (7, [], -1),
            (8, ["xouter"], -1),
            # inner core
            (9, ["xinner"], -1),
            (10, [], -1),
            (11, ["xouter"], -1),
            (12, ["xinner"], fieldperp_global_yind),
            (13, [], fieldperp_global_yind),
            (14, ["xouter"], fieldperp_global_yind),
            (15, ["xinner"], -1),
            (16, [], -1),
            (17, ["xouter"], -1),
            # inner, upper divertor leg
            (18, ["xinner"], -1),
            (19, [], -1),
            (20, ["xouter"], -1),
            (21, ["xinner"], -1),
            (22, [], -1),
            (23, ["xouter"], -1),
            (24, ["xinner", "yupper"], -1),
            (25, ["yupper"], -1),
            (26, ["xouter", "yupper"], -1),
            # outer, upper divertor leg
            (27, ["xinner", "ylower"], -1),
            (28, ["ylower"], -1),
            (29, ["xouter", "ylower"], -1),
            (30, ["xinner"], -1),
            (31, [], -1),
            (32, ["xouter"], -1),
            (33, ["xinner"], -1),
            (34, [], -1),
            (35, ["xouter"], -1),
            # outer core
            (36, ["xinner"], -1),
            (37, [], -1),
            (38, ["xouter"], -1),
            (39, ["xinner"], -1),
            (40, [], -1),
            (41, ["xouter"], -1),
            (42, ["xinner"], -1),
            (43, [], -1),
            (44, ["xouter"], -1),
            # outer, lower divertor leg
            (45, ["xinner"], -1),
            (46, [], -1),
            (47, ["xouter"], -1),
            (48, ["xinner"], -1),
            (49, [], -1),
            (50, ["xouter"], -1),
            (51, ["xinner", "yupper"], -1),
            (52, ["yupper"], -1),
            (53, ["xouter", "yupper"], -1),
        ]
        dumps = []
        for i, boundaries, fieldperp_yind in dump_params:
            dumps.append(
                create_dump_file(
                    tmpdir=tmp_path,
                    rng=rng,
                    grid_info=grid_info,
                    i=i,
                    boundaries=boundaries,
                    fieldperp_global_yind=fieldperp_yind,
                )
            )

        expected = concatenate_data(
            dumps, nxpe=grid_info["NXPE"], fieldperp_yproc_ind=fieldperp_yproc_ind
        )

        collect_kwargs = {"xguards": True, "yguards": "include_upper"}

        check_collected_data(
            expected,
            fieldperp_global_yind=fieldperp_global_yind,
            doublenull=True,
            path=tmp_path,
            squash=True,
            collect_kwargs=collect_kwargs,
            squash_kwargs=squash_kwargs,
        )
