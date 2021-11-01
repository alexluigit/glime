#!/usr/bin/env python
import os
import fnmatch
import re
import argparse
import datetime
import json
from glim_layouts import Glyph_mappings, Layouts, Extra_No_Auto
from lua_helper import dump_lua


def glyph_encoding(glyph_dict):
    dict_json = json.load(open(glyph_dict, "r"))
    layout_types = {"full": "I"}
    for k, v in Layouts.items():
        layout_types[k] = v["mapping"]
    with open(glyph_lua_table, "a") as table_out:
        glyph_tables = {}
        for layout_type, mappings in Glyph_mappings.items():
            glyph_encoding_lua = {}
            for i in dict_json:
                lvl = int(i["level"])
                word = i["character"]
                auto = lvl < 3 and word not in Extra_No_Auto
                glyph_encoding_lua[word] = {
                    "ch1": mappings[i["first_py"]]["map"],
                    "ch2": mappings[i["last_py"]]["map"],
                    "gl1": i["first_part"],
                    "gl2": i["last_part"],
                    "auto": auto,
                }
            glyph_tables[layout_type] = glyph_encoding_lua
        table_out.write("-- This file is auto generated by glim, be careful when editing it by hand. --\n\n")
        table_out.write("local glyph_tables =\n")
        table_out.write(dump_lua(glyph_tables))
        table_out.write("\nlocal layout_types =\n")
        table_out.write(dump_lua(layout_types))
        table_out.write(
            "\nreturn function(layout) return glyph_tables[layout_types[layout]] end"
        )


def main(args):
    glyph_encoding(xiaohe_glyph_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Glim 辅助码码表生成工具。")
    parser.add_argument(
        "--dev", "-d", help="生成开发相关词典数据.", action=argparse.BooleanOptionalAction
    )
    args = parser.parse_args()
    lua_out = "../cache/lua/"
    xiaohe_glyph_dict = "../assets/xiaohe-8105.json"
    glyph_lua_table = lua_out + "/glyph_table.lua"
    if os.path.exists(glyph_lua_table):
        os.remove(glyph_lua_table)
    if not os.path.exists(lua_out):
        os.makedirs(lua_out)
    exit(main(args))
