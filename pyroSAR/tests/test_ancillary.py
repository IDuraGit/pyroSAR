import os
import pytest
import subprocess as sp
import spatialist.ancillary as anc
from pyroSAR.ancillary import seconds, groupbyTime, groupby


def test_dissolve_with_lists():
    assert anc.dissolve([[1, 2], [3, 4]]) == [1, 2, 3, 4]
    assert anc.dissolve([[[1]]]) == [1]
    assert anc.dissolve(((1, 2,), (3, 4))) == [1, 2, 3, 4]
    assert anc.dissolve(((1, 2), (1, 2))) == [1, 2, 1, 2]


def test_union():
    assert anc.union([1], [1]) == [1]


def test_parse_literal():
    assert anc.parse_literal(['1', '2.2', 'a']) == [1, 2.2, 'a']
    with pytest.raises(TypeError):
        anc.parse_literal(1)


def test_seconds():
    assert seconds('test_20151212T234411') == 3658952651.0


def test_run(tmpdir, testdata):
    log = os.path.join(str(tmpdir), 'test_run.log')
    out, err = anc.run(cmd=['gdalinfo', testdata['tif']],
                       logfile=log, void=False)
    with pytest.raises(OSError):
        anc.run(['foobar'])
    with pytest.raises(sp.CalledProcessError):
        anc.run(['gdalinfo', 'foobar'])


def test_which():
    env = os.environ['PATH']
    os.environ['PATH'] = '{}{}{}'.format(os.environ['PATH'], os.path.pathsep, os.path.dirname(os.__file__))
    program = anc.which(os.__file__, os.F_OK)
    assert os.path.isfile(program)
    assert anc.which(program, os.F_OK) == program
    assert anc.which('foobar') is None
    os.environ['PATH'] = env


def test_multicore():
    add = lambda x, y, z: x + y + z
    assert anc.multicore(add, cores=2, multiargs={'x': [1, 2]}, y=5, z=9) == [15, 16]
    assert anc.multicore(add, cores=2, multiargs={'x': [1, 2], 'y': [5, 6]}, z=9) == [15, 17]
    with pytest.raises(AttributeError):
        anc.multicore(add, cores=2, multiargs={'foobar': [1, 2]}, y=5, z=9)
    with pytest.raises(AttributeError):
        anc.multicore(add, cores=2, multiargs={'x': [1, 2]}, y=5, foobar=9)
    with pytest.raises(AttributeError):
        anc.multicore(add, cores=2, multiargs={'x': [1, 2], 'y': [5, 6, 7]}, foobar=9)


def test_finder(tmpdir):
    dir = str(tmpdir)
    dir_sub1 = os.path.join(dir, 'testdir1')
    dir_sub2 = os.path.join(dir, 'testdir2')
    os.makedirs(dir_sub1)
    os.makedirs(dir_sub2)
    with open(os.path.join(dir_sub1, 'testfile1.txt'), 'w') as t1:
        t1.write('test')
    with open(os.path.join(dir_sub2, 'testfile2.txt'), 'w') as t2:
        t2.write('test')
    assert len(anc.finder(dir, ['test*'], foldermode=0)) == 2
    assert len(anc.finder(dir, ['test*'], foldermode=0, recursive=False)) == 0
    assert len(anc.finder(dir, ['test*'], foldermode=1)) == 4
    assert len(anc.finder(dir, ['test*'], foldermode=2)) == 2
    assert len(anc.finder([dir_sub1, dir_sub2], ['test*'])) == 2
    with pytest.raises(TypeError):
        anc.finder(1, [])


def test_rescale():
    assert anc.rescale([1000, 2000, 3000], [1, 3]) == [1, 2, 3]
    with pytest.raises(RuntimeError):
        anc.rescale([1000, 1000])


def test_groupby():
    """
    Test correct grouping of filenames by their attributes
    Methodology is to provide a list of partially overlapping filenames
    and ensure the resultant list of lists contains the correct entry numbers
    """
    filenames = ['S1A__IW___A_20150309T173017_VV_grd_mli_geo_norm_db.tif',
                 'S1A__IW___A_20150309T173017_HH_grd_mli_geo_norm_db.tif',
                 'S2A__IW___A_20180309T173017_HH_grd_mli_geo_norm_db.tif']
    sensor_groups = groupby(filenames, 'sensor')
    print(sensor_groups)
    assert len(sensor_groups) == 2
    assert isinstance(sensor_groups[0], list)
    assert len(sensor_groups[0]) == 2

    filenames += ['S2A__IW___A_20180309T173017_VV_grd_mli_geo_norm_db.tif']

    polarization_groups = groupby(filenames, 'polarization')
    print(polarization_groups)
    assert len(polarization_groups) == 2
    assert isinstance(polarization_groups[0], list)
    assert isinstance(polarization_groups[1], list)
    assert len(polarization_groups[0]) == 2
    assert len(polarization_groups[1]) == 2

    filenames += ['S2A__IW___A_20180309T173017_HV_grd_mli_geo_norm_db.tif']

    polarization_groups = groupby(filenames, 'polarization')
    print(polarization_groups)
    assert len(polarization_groups) == 3
    assert isinstance(polarization_groups[0], list)
    assert isinstance(polarization_groups[1], list)
    assert isinstance(polarization_groups[2], list)
    assert len(polarization_groups[0]) == 2
    assert len(polarization_groups[1]) == 1
    assert len(polarization_groups[2]) == 2


def test_groupbyTime():
    filenames = ['S1__IW___A_20151212T120000',
                 'S1__IW___A_20151212T120100',
                 'S1__IW___A_20151212T120300']
    groups = groupbyTime(filenames, seconds, 60)
    print(groups)
    assert len(groups) == 2
    assert isinstance(groups[0], list)
    assert len(groups[0]) == 2

    filenames = ['S1__IW___A_20151212T120000',
                 'S1__IW___A_20151212T120100',
                 'S1__IW___A_20151212T120200']
    groups = groupbyTime(filenames, seconds, 60)
    print(groups)
    assert len(groups[0]) == 3
