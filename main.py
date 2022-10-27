# -*- coding: utf-8 -*-
"""
@date: 2022

@author: Jonas Vollhueter
"""
import pandas as pd
from lxml import etree
import Pre
import Calculate
import Post

path_to_xml = 'settings.xml'


class Project():
    # This class reads the xml setting file and defines the content of the
    # file as attributes of the class Project.

    def __init__(self, path_to_xml):

        def findChild(parent, key):
            child = parent.find(key)
            if child is None:
                raise KeyError("Section '" + key + "' is missing in xml file")
            return child

        tree = etree.parse(path_to_xml)
        root = tree.getroot()

        for tag in root.iter():
            tag.text = tag.text.strip()

        self.name = findChild(root, 'name').text

        self.mode = findChild(root, 'mode').text

        external_files = findChild(root, 'external_files')

        file_1 = findChild(external_files, 'input_P_c_1')
        self.input_c_1_type = findChild(file_1, 'type').text
        self.input_c_1_path = findChild(file_1, 'path').text

        file_2 = findChild(external_files, 'input_P_c_2')
        self.input_c_2_type = findChild(file_2, 'type').text
        self.input_c_2_path = findChild(file_2, 'path').text

        file_3 = findChild(external_files, 'samples_c')
        self.sample_file_type = findChild(file_3, 'type').text
        self.sample_file_path = findChild(file_3, 'path').text

        uz = findChild(root, 'unsateraded_zone')
        self.uz_type = findChild(uz, 'type').text
        self.uz_path = findChild(uz, 'path').text

        lpm = findChild(root, 'lpm')
        self.lpm_type = findChild(lpm, 'type').text

        parametrisation = findChild(root, 'parametrisation')
        self.mean_gw_age = int(findChild(parametrisation, 'mean_gw_age').text)
        self.halftime_1 = float(findChild(parametrisation, 'halftime_1').text)
        self.halftime_2 = float(findChild(parametrisation, 'halftime_2').text)
        self.PD = float(findChild(parametrisation, 'PD').text)
        self.eta = float(findChild(parametrisation, 'eta').text)

        post = findChild(root, 'post')
        self.write_output = findChild(post, 'write_output').text
        not_tracer = findChild(post, 'mode_not_tracer')
        date = findChild(not_tracer, 'date').text
        self.date = pd.to_datetime(date)
        figure = findChild(post, 'figure')
        self.out_fig_type = findChild(figure, 'type').text
        self.out_fig_path = findChild(figure, 'path').text
        text_file = findChild(post, 'text_file')

        self.out_text_type = findChild(text_file, 'type').text
        self.out_text_path = findChild(text_file, 'path').text
        self.weighted = False


par = Project(path_to_xml)

data_frames = Pre.PreSettingOne(par)

if par.mode == 'tracer':

    calc = Calculate.Tracer(par, data_frames.c_in_1)

    Post.Post.tracer(calc.result, data_frames.c_in_1, data_frames.sample, par)

elif par.mode == 'tracer_tracer':

    calc = Calculate.TracerTracer(par, data_frames.c_in_1, data_frames.c_in_2)

    Post.Post.tracerTracer(calc.result, data_frames, par)

elif par.mode == 'tritium_helium':

    calc = Calculate.TracerTracer(par, data_frames.c_in_1, data_frames.c_in_2)

    Post.Post.triHeVis1(calc.result, data_frames, par)

else:
    raise KeyError("""Section mode in xml file has a not known value.
Please check for typos and if necessary read the manual.""")
