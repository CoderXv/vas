__author__ = 'user'

from vtk import *
from VesselFileReader import VesselFileReader


class DataSet:
    def __init__(self, index):
        self.index = index
        self.vessels = []

        self.vessels.append({})
        self.vessels.append({})
        self.vessels.append({})
        self.vessels.append({})
        self.img_path = ''

        self.mraOriginalImage = None

        # mri image reader
        self.mra_image_reader = vtkMetaImageReader()

    def import_new_vessel(self, vessel_num, file_name, vessel_to_be_evaluated):
        # vessel_to_be_evaluated is a path, str
        self.vessels[vessel_num][file_name] = vessel_to_be_evaluated

    def load_vessel_to_be_evaluated(self, vessel_num, file_name):
        vessel_file_reader = VesselFileReader()
        vessel_file_reader.parse_vessel_file(self.vessels[vessel_num][file_name])
        vessel_file_reader.do_parse_vessel_file()
        self.vessels[vessel_num][file_name] = vessel_file_reader
        return self.vessels[vessel_num][file_name]
    '''
    def load_vessel_to_be_evaluated(self, file_path, index):
            # TODO: fetch file_name from file_path
            #
            # self.vessels[index][file_name] = file_path
            print 'todo'
    '''

    def get_mri_image(self):
        return self.mraOriginalImage

    def load_ref_by_vessel_index(self, index):
        vessel_file_reader = VesselFileReader()
        vessel_file_reader.parse_vessel_file(self.vessels[index]["reference"])
        vessel_file_reader.do_parse_vessel_file()
        self.vessels[index]["reference_data"] = vessel_file_reader
        return self.vessels[index]["reference_data"]

    def print_me(self):
        print "--------------------------------------------------------------------------------------"
        print self.vessel_0
        print self.vessel_1
        print self.vessel_2
        print self.vessel_3
        print self.img_path
        print "--------------------------------------------------------------------------------------"

    def load_mri_image(self):
        self.mra_image_reader.SetFileName(self.img_path)
        self.mra_image_reader.Update()
        self.mraOriginalImage = self.mra_image_reader.GetOutput()
        return self.mraOriginalImage

    # set function
    def set_point_a_path_by_vessel_index(self, index, a):
        self.vessels[index]["pointA"] = a

    def set_point_b_path_by_vessel_index(self, index, b):
        self.vessels[index]["pointB"] = b

    def set_point_e_path_by_vessel_index(self, index, e):
        self.vessels[index]["pointE"] = e

    def set_point_s_path_by_vessel_index(self, index, s):
        self.vessels[index]["pointS"] = s

    def set_point_ref_path_by_vessel_index(self, index, ref):
        self.vessels[index]["reference"] = ref

    def get_point_ref_path_by_vessel_index(self, index):
        return self.vessels[index]["reference"]

    def get_point_ref_data_by_vessel_index(self, index):
        return self.vessels[index]["reference_data"]

    def set_image_path(self, img_path):
        self.img_path = img_path

    def get_img_path(self):  # use
        return self.img_path

    def get_number_of_vessels(self):  # use
        return len(self.vessels)

    def get_items_of_vessel_file_in_data_set(self, index):
        return self.vessels[index].keys()

    def get_path_of_the_point_in_data_set(self, vessel_index, point_key):
        path = self.vessels[vessel_index][point_key]
        return path

    def get_vessels(self):
        return self.vessels
