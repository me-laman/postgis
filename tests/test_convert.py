from geoalchemy2.shape import to_shape
from post_gis.views_helpers import build_geom


async def test_build_geom():
    geom = [[0, 0], [0, 5], [0, 5], [5, 0], [5, 0]]
    geom_shape = build_geom(geom)
    assert str(to_shape(geom_shape)) == 'POLYGON ((0 0, 0 5, 0 5, 5 0, 5 0, 0 0))'


async def test_build_geom_convert():
    geom = [[0, 0], [0, 5], [0, 5], [5, 0], [5, 0]]
    from_coordinates = 'epsg:3857'

    geom_shape = build_geom(geom, from_coordinates)
    assert str(to_shape(geom_shape)) == 'POLYGON ((0 -7.081154551613622e-10, 0 557305.2572745753,' \
                                        ' 0 557305.2572745753, 556597.4539663672 ' \
                                        '-7.081154551613622e-10, 556597.4539663672 ' \
                                        '-7.081154551613622e-10, 0 -7.081154551613622e-10))'
