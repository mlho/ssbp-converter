import collections
import math
import pprint
import struct
import sys

DATA_VERSION = 3

VERTEX_FLAG_ONE		 = 1 << 4	# color blend only

# frame data flags
INVISIBLE		     = 1 << 0
FLIP_H			     = 1 << 1
FLIP_V			     = 1 << 2
# optional parameter flags
CELL_INDEX		     = 1 << 3
POSITION_X		     = 1 << 4
POSITION_Y		     = 1 << 5
POSITION_Z		     = 1 << 6

PIVOT_X			     = 1 << 7
PIVOT_Y              = 1 << 8
ROTATION_X	         = 1 << 9
ROTATION_Y		     = 1 << 10
ROTATION_Z		     = 1 << 11
SCALE_X		         = 1 << 12
SCALE_Y			     = 1 << 13
OPACITY			     = 1 << 14

SIZE_X			     = 1 << 17
SIZE_Y			     = 1 << 18

U_MOVE			     = 1 << 19
V_MOVE			     = 1 << 20
UV_ROTATION		     = 1 << 21
U_SCALE			     = 1 << 22
V_SCALE			     = 1 << 23

BOUNDING_RADIUS	     = 1 << 24

VERTEX_TRANSFORM     = 1 << 16
COLOR_BLEND		     = 1 << 15

INSTANCE_KEYFRAME	 = 1 << 25
INSTANCE_START	     = 1 << 26
INSTANCE_END		 = 1 << 27
INSTANCE_SPEED	     = 1 << 28
INSTANCE_LOOP		 = 1 << 29
INSTANCE_LOOP_FLG    = 1 << 30


SIZE_OF = {
    'SHORT' : 2,
    'INT' : 4,
    'FLOAT' : 4,
    'STRING' : 4
}

TOP_LUMP = collections.OrderedDict([
    ('dataId', 'INT'),
    ('currentDataVersion', 'INT'),
    ('headFlag', 'INT'),
    ('imageBaseDir', 'INT'),
    ('cellsData', 'INT'),
    ('packDataArray', 'INT'),
    ('effectFileArray', 'INT'),
    ('cellListSize', 'SHORT'),
    ('animeListSize', 'SHORT'),
    ('effectFileSize', 'SHORT')
])

CELL = collections.OrderedDict([
    ('name', 'STRING'),
    ('cellMapData', 'INT'),
    ('cellIndex', 'SHORT'),
    ('posX', 'SHORT'),
    ('posY', 'SHORT'),
    ('sizeX', 'SHORT'),
    ('sizeY', 'SHORT'),
    ('RESERVED', 'SHORT'),
    ('pivotX', 'FLOAT'),
    ('pivotY', 'FLOAT')
])

CELL_MAP = collections.OrderedDict([
    ('name', 'STRING'),
    ('imagePath', 'STRING'),
    ('mapIndex', 'SHORT'),
    ('wrapMode', 'SHORT'),
    ('filterMode', 'SHORT'),
    ('RESERVED', 'SHORT')
])

ANIME_PACK = collections.OrderedDict([
    ('name', 'STRING'),
    ('partDataArray', 'INT'),
    ('animeDataArray', 'INT'),
    ('partListSize', 'SHORT'),
    ('animeListSize', 'SHORT')
])

PART = collections.OrderedDict([
    ('name', 'STRING'),
    ('arrayIndex', 'SHORT'),
    ('parentIndex', 'SHORT'),
    ('partType', 'SHORT'),
    ('boundsType', 'SHORT'),
    ('alphaBlendType', 'SHORT'),
    ('refAnimeLength', 'SHORT'),
    ('refAnime', 'STRING'),
    ('effectName', 'STRING'),
    ('colorLabel', 'STRING')
])

ANIME_DATA = collections.OrderedDict([
    ('name', 'STRING'),
    ('initialDataArray', 'INT'),
    ('frameDataIndexArray', 'INT'),
    ('userDataIndexArray', 'INT'),
    ('labelDataIndexArray', 'INT'),
    ('animeEndFrame', 'SHORT'),
    ('fps', 'SHORT'),
    ('labelIdx', 'SHORT'),
    ('canvasSizeX', 'SHORT'),
    ('canvasSizeY', 'SHORT'),
    ('DUMMY', 'SHORT')
])

INITIAL_ANIMATION = collections.OrderedDict([
    ('index', 'SHORT'),
    ('DUMMY1', 'SHORT'),
    ('flags', 'INT'),
    ('cellIndex', 'SHORT'),
    ('posX', 'SHORT'),
    ('posY', 'SHORT'),
    ('posZ', 'SHORT'),
    ('opacity', 'SHORT'),
    ('DUMMY2', 'SHORT'),
    ('pivotX', 'FLOAT'),
    ('pivotY', 'FLOAT'),
    ('rotationX', 'FLOAT'),
    ('rotationY', 'FLOAT'),
    ('rotationZ', 'FLOAT'),
    ('scaleX', 'FLOAT'),
    ('scaleY', 'FLOAT'),
    ('size_X', 'FLOAT'),
    ('size_Y', 'FLOAT'),
    ('uv_move_X', 'FLOAT'),
    ('uv_move_Y', 'FLOAT'),
    ('uv_rotation', 'FLOAT'),
    ('uv_scale_X', 'FLOAT'),
    ('uv_scale_Y', 'FLOAT'),
    ('boundingRadius', 'FLOAT')
])

FRAME_DATA = collections.OrderedDict([
    ('index', 'SHORT'),
    ('sp_flag', 'INT'),
])

FRAME_DATA_OPT = collections.OrderedDict([
    ('invisible', 'SHORT'),
    ('flip_h', 'SHORT'),
    ('flip_v', 'SHORT'),

    ('cell_index', 'SHORT'),
    ('position_x', 'SHORT'),
    ('position_y', 'SHORT'),
    ('position_z', 'SHORT'),

    ('pivot_x', 'FLOAT'),
    ('pivot_y', 'FLOAT'),
    ('rotation_x', 'FLOAT'),
    ('rotation_y', 'FLOAT'),
    ('rotation_z', 'FLOAT'),
    ('scale_x', 'FLOAT'),
    ('scale_y', 'FLOAT'),
    ('opacity', 'SHORT'),

    ('size_x', 'FLOAT'),
    ('size_y', 'FLOAT'),

    ('u_move', 'FLOAT'),
    ('v_move', 'FLOAT'),
    ('uv_rotation', 'FLOAT'),
    ('u_scale', 'FLOAT'),
    ('v_scale', 'FLOAT'),

    ('bounding_radius', 'FLOAT'),

    ('vertex_transform', 'SHORT'),
    ('vtX', 'SHORT'),
    ('vtY', 'SHORT'),

    ('color_blend', 'SHORT'),
    ('color_rate', 'SHORT'),
    ('color_ARGB', 'SHORT'),

    ('instance_keyframe', 'SHORT'),
    ('instance_start', 'SHORT'),
    ('instance_end', 'SHORT'),
    ('instance_speed', 'SHORT'),
    ('instance_loop', 'SHORT'),
    ('instance_loop_flg', 'SHORT')
])



def convert_bytes(data, index, dtype):
    buf = bytes(data[index : index + SIZE_OF[dtype]])

    if dtype is 'SHORT':
        return struct.unpack('<h', buf)[0]

    elif dtype is 'INT':
        return struct.unpack('<i', buf)[0]

    elif dtype is 'FLOAT':
        return struct.unpack('<f', buf)[0]

    elif dtype is 'STRING':
        ref = struct.unpack('<i', buf)[0]

        str = ""
        while data[ref] != 0:
            str += chr(data[ref])
            ref += 1

        return str

def get_top_lump(data):
    index = 0
    lump = {}

    for key, dtype in TOP_LUMP.items():
        val = convert_bytes(data, index, dtype)
        index += SIZE_OF[dtype]

        lump.update({key : val})

    return lump

def get_cells(data, index, num_cells):
    arr = []

    for n in range(num_cells):
        lump = {}
        for key, dtype in CELL.items():
            val = convert_bytes(data, index, dtype)
            index += SIZE_OF[dtype]

            if key is 'cellMapData':
                val = get_cell_map(data, val)

            lump.update({key : val})

        arr += [lump]

    return arr

def get_cell_map(data, index):
    lump = {}

    for key, dtype in CELL_MAP.items():
        val = convert_bytes(data, index, dtype)
        index += SIZE_OF[dtype]

        lump.update({key : val})

    return lump

def get_pack_data(data, index, anime_list_size):
    arr = []

    for n in range(anime_list_size):
        lump = {}

        for key, dtype in ANIME_PACK.items():
            val = convert_bytes(data, index, dtype)
            index += SIZE_OF[dtype]

            lump.update({key : val})

        parts = get_part_data_array(data, lump['partDataArray'], lump['partListSize'])
        lump.update({'partDataArray' : parts})

        anime = get_anime_data_array(data, lump['animeDataArray'], lump['animeListSize'], lump['partListSize'])
        lump.update({'animeDataArray' : anime})

        arr += [lump]

    return arr

def get_part_data_array(data, index, num_parts):
    arr = []

    for n in range(num_parts):
        lump = {}

        for key, dtype in PART.items():
            val = convert_bytes(data, index, dtype)
            index += SIZE_OF[dtype]

            lump.update({key : val})
        arr += [lump]

    return arr

def get_anime_data_array(data, index, num_anime, num_parts):
    arr = []

    for n in range(num_anime):
        lump = {}

        for key, dtype in ANIME_DATA.items():
            val = convert_bytes(data, index, dtype)
            index += SIZE_OF[dtype]

            if key is 'initialDataArray':
                val = get_initial_data_array(data, val, num_parts)

            lump.update({key : val})

        index_list = get_frame_data_index_array(data, lump['frameDataIndexArray'], lump['animeEndFrame'])

        lump.update({'frameDataIndexArray' : get_frame_data_array(data, index_list, num_parts)})

        arr += [lump]

    return arr

def get_initial_data_array(data, index, num_parts):
    arr = []

    for n in range(num_parts):
        lump = {}

        for key, dtype in INITIAL_ANIMATION.items():
            val = convert_bytes(data, index, dtype)
            index += SIZE_OF[dtype]

            lump.update({key : val})
        arr += [lump]

    return arr

def get_frame_data_index_array(data, index, end_frame):
    arr = []
    dtype = 'INT'

    for n in range(end_frame):
        val = convert_bytes(data, index, dtype)
        index += SIZE_OF[dtype]
        arr += [val]

    return arr

def get_frame_data_array(data, index_array, num_parts):
    arr = []

    for index in index_array:
        frame = []

        for n in range(num_parts):
            lump = {}

            for key, dtype in FRAME_DATA.items():
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({key : val})

            sp_flag = lump['sp_flag']

            if sp_flag & INVISIBLE:
                lump.update({'invisible' : 1})

            if sp_flag & FLIP_H:
                lump.update({'flip_h' : 1})

            if sp_flag & FLIP_V:
                lump.update({'flip_v' : 1})


            # optional parameter flags
            if sp_flag & CELL_INDEX:
                dtype = 'SHORT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'cell_index' : val})

            if sp_flag & POSITION_X:
                dtype = 'SHORT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'pos_x' : val / 10})

            if sp_flag & POSITION_Y:
                dtype = 'SHORT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'pos_y' : val / 10})

            if sp_flag & POSITION_Z:
                dtype = 'SHORT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'pos_z' : val / 10})


            if sp_flag & PIVOT_X:
                dtype = 'FLOAT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'pivot_x' : val})

            if sp_flag & PIVOT_Y:
                dtype = 'FLOAT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'pivot_y' : val})

            if sp_flag & ROTATION_X:
                dtype = 'FLOAT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'rotation_x' : val})

            if sp_flag & ROTATION_Y:
                dtype = 'FLOAT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'rotation_y' : val})

            if sp_flag & ROTATION_Z:
                dtype = 'FLOAT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'rotation_z' : val})

            if sp_flag & SCALE_X:
                dtype = 'FLOAT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'scale_x' : val})

            if sp_flag & SCALE_Y:
                dtype = 'FLOAT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'scale_y' : val})

            if sp_flag & OPACITY:
                dtype = 'SHORT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'opacity' : val})


            if sp_flag & SIZE_X:
                dtype = 'FLOAT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'size_x' : val})

            if sp_flag & SIZE_Y:
                dtype = 'FLOAT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'size_y' : val})


            if sp_flag & U_MOVE:
                dtype = 'FLOAT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'u_move' : val})

            if sp_flag & V_MOVE:
                dtype = 'FLOAT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'v_move' : val})

            if sp_flag & UV_ROTATION:
                dtype = 'FLOAT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'uv_rotation' : val})

            if sp_flag & U_SCALE:
                dtype = 'FLOAT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'u_scale' : val})

            if sp_flag & V_SCALE:
                dtype = 'FLOAT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'v_scale' : val})


            if sp_flag & BOUNDING_RADIUS:
                dtype = 'FLOAT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'bounding_radius' : val})


            if sp_flag & VERTEX_TRANSFORM:
                dtype = 'SHORT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'vt_flag' : val})

                vt_flag = lump['vt_flag']

                for vtxNo in range(4):
                    if vt_flag & (1 << vtxNo):
                        dtype = 'SHORT'

                        val = convert_bytes(data, index, dtype)
                        index += SIZE_OF[dtype]
                        lump.update({'vt_x' + str(vtxNo) : val})

                        val = convert_bytes(data, index, dtype)
                        index += SIZE_OF[dtype]
                        lump.update({'vt_y' + str(vtxNo) : val})


            if sp_flag & COLOR_BLEND:
                dtype = 'SHORT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'typeAndFlags' : val})

                cb_flag = lump['typeAndFlags'] >> 8

                if cb_flag & VERTEX_FLAG_ONE:
                    dtype = 'FLOAT'
                    val = convert_bytes(data, index, dtype)
                    index += SIZE_OF[dtype]
                    lump.update({'color_value' : val})

                    dtype = 'INT'
                    val = convert_bytes(data, index, dtype)
                    index += SIZE_OF[dtype]
                    lump.update({'color_ARGB' : val})
                else:
                    for vtxNo in range(4):
                        if cb_flag & (1 << vtxNo):

                            dtype = 'FLOAT'
                            val = convert_bytes(data, index, dtype)
                            index += SIZE_OF[dtype]
                            lump.update({'color_value' : val})

                            dtype = 'INT'
                            val = convert_bytes(data, index, dtype)
                            index += SIZE_OF[dtype]
                            lump.update({'color_ARGB' : val})


            if sp_flag & INSTANCE_KEYFRAME:
                dtype = 'SHORT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'current_keyframe' : val})

            if sp_flag & INSTANCE_START:
                dtype = 'SHORT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'start_frame' : val})

            if sp_flag & INSTANCE_END:
                dtype = 'SHORT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'end_frame' : val})

            if sp_flag & INSTANCE_SPEED:
                dtype = 'FLOAT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'speed' : val})

            if sp_flag & INSTANCE_LOOP:
                dtype = 'SHORT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'loop_num' : val})

            if sp_flag & INSTANCE_LOOP_FLG:
                dtype = 'SHORT'
                val = convert_bytes(data, index, dtype)
                index += SIZE_OF[dtype]
                lump.update({'iflag' : val})

            frame += [lump]

        arr += [frame]

    return arr

def main():
    fn = sys.argv[1]

    with open(fn, 'rb') as f:
        data = list(f.read())

    top_lump = get_top_lump(data)

    if top_lump['currentDataVersion'] is not DATA_VERSION:
        print('NOT SUPPORTED: DATA_VERSION ' + str(top_lump['currentDataVersion']))
        return

    cells = get_cells(data, top_lump['cellsData'], top_lump['cellListSize'])

    texture_url_array = []

    for cell in cells:
        imagePath = cell['cellMapData']['imagePath']

        if imagePath not in texture_url_array:
            texture_url_array += [imagePath]

    pack_data_array = get_pack_data(data, top_lump['packDataArray'], top_lump['animeListSize'])

    initial_data_json = {}
    frame_data_json = {}
    parts_data_json = {}

    for anime_pack in pack_data_array:
        part_data_array = anime_pack['partDataArray']
        parts_data_json.update({anime_pack['name'] : anime_pack['partDataArray']})

        anime_data_array = anime_pack['animeDataArray']
        initial_data = []
        frame_data = []

        for anime_data in anime_data_array:
            initial_data += [{anime_data['name'] : anime_data['initialDataArray']}]
            frame_data += [{anime_data['name'] : anime_data['frameDataIndexArray']}]

        initial_data_json.update({anime_pack['name'] : initial_data})
        frame_data_json.update({anime_pack['name'] : frame_data})

    print('Running...')

    with open('cellsArray.js', 'wt') as out:
        out.write('var cellsArray = ')
        pprint.pprint(cells, out)
    print('[OK] cellsArray.js')

    with open('textureURLArray.js', 'wt') as out:
        out.write('var filename = \'' + fn + '\';\n')
        out.write('var textureURLArray = ')
        pprint.pprint(texture_url_array, out)
    print('[OK] textureURLArray.js')

    with open('partsJSON.js', 'wt') as out:
        out.write('var partsJSON = ')
        pprint.pprint(parts_data_json, out)
    print('[OK] partsJSON.js')

    with open('initialAnimeJSON.js', 'wt') as out:
        out.write('var initialAnimeJSON = ')
        pprint.pprint(initial_data_json, out)
    print('[OK] initialAnimeJSON.js')

    with open('framesJSON.js', 'wt') as out:
        out.write('var framesJSON = ')
        pprint.pprint(frame_data_json, out)
    print('[OK] framesJSON.js')

    print('Done.')

if __name__ == '__main__':
  main()
