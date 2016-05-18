

__author__ = 'user'

import os
import platform
import sys
from DataSet import DataSet


# noinspection PyBroadException
class SystemDataBase:
    def __init__(self, path):

        self.dataSetHandling = 'unknown'
        self.path = path
        self.extens = [".txt", ".mhd", ".raw"]
        self.dataSets = {}

    def load_mri_image_into_context_by_name(self, file_name):
        self.dataSetHandling = file_name
        return self.dataSets[file_name].load_mri_image()

    def load_vessel_to_be_evaluated(self, file_path, index):
        self.dataSets[self.dataSetHandling].load_vessel_to_be_evaluated(file_path, index)

    # data_sets and its elements's operation
    def get_number_of_dataset(self):
        return len(self.dataSets)

    def get_name_of_the_data_sets(self):
        return sorted(self.dataSets.keys())

    def get_number_of_vessel_folder(self, dataset_name):
        return self.dataSets[dataset_name].get_number_of_vessels()

    def get_path_of_the_image_file(self, dataset_name):
        return self.dataSets[dataset_name].get_img_path()

    def get_number_of_the_point_file_in_sys_db(self, dataset_name, vessel_index):
        return self.dataSets[dataset_name].get_items_of_vessel_file_in_data_set(vessel_index)

    def get_path_of_the_vessel_file(dataset_name,index, self=None):
        return self.dataSets[dataset_name].get_point_ref_path_by_vessel_index(index)

    def get_name_of_the_point_file(self, dataset_name):
        return self.dataSets[dataset_name].get_name_of_the_point_in_data_set()

    def get_the_path_of_the_point(self, dataset_name, vessel_index, point_key):
        return self.dataSets[dataset_name].get_path_of_the_point_in_data_set(vessel_index, point_key)

    def get_the_ref_data_of_the_point_by_index(self, dataset_name, index):
        return self.dataSets[dataset_name].load_ref_by_vessel_index(index)

    def get_data_set_vessels(self, dataset_name):
        return self.dataSets[dataset_name].get_vessels()

    def store_vessel_to_be_evaluated(self, single_path_dir, ds_name, vessel_file_name, vessel_num):
        self.dataSets[ds_name].import_new_vessel(vessel_num, vessel_file_name, single_path_dir)

    def load_vessel_to_be_evaluated(self, ds_name, vessel_num, file_name):
        return self.dataSets[ds_name].load_vessel_to_be_evaluated(vessel_num, file_name)

    # def get_the_name_of_file_by_folder_name(self, folder_name):

    def get_the_content_path_of_the_each_dataset(self, index, content_name, dataset_name):
        if content_name == 'pointA':
            self.dataSets[dataset_name].get_point_a_path_by_vessel_index(self, index)
        elif content_name == 'pointB':
            self.dataSets[dataset_name].get_point_b_path_by_vessel_index(self, index)
        elif content_name == 'pointE':
            self.dataSets[dataset_name].get_point_e_path_by_vessel_index(self, index)
        elif content_name == 'pointS':
            self.dataSets[dataset_name].get_point_s_path_by_vessel_index(self, index)
        elif content_name == 'reference':
            self.dataSets[dataset_name].get_point_ref_path_by_vessel_index(self, index)
        elif content_name == 'img_path':
            self.dataSets[dataset_name].get_img_path()

    def do_parse_data_sets(self):
        for root, dirs, fileNames in os.walk(self.path):
            for f in fileNames:
                file_name = os.path.join(root, f)
                if '.' not in f:
                    continue
                try:
                    ext = f[f.rindex('.'):]
                    if self.extens.count(ext) > 0:
                        self.do_analyse_file_path(file_name)
                except:
                    print "Error occur!"
                    pass

    # define each dataset then put it into the dict dataSets
    def do_analyse_file_path(self, filename):
        if 'dataset00' in filename:
            if 'dataset00' not in self.dataSets.keys():
                ds = DataSet(0)
                self.dataSets['dataset00'] = ds
        elif 'dataset01' in filename:
            if 'dataset01' not in self.dataSets.keys():
                ds = DataSet(1)
                self.dataSets['dataset01'] = ds
        elif 'dataset02' in filename:
            if 'dataset02' not in self.dataSets.keys():
                ds = DataSet(2)
                self.dataSets['dataset02'] = ds
        elif 'dataset03' in filename:
            if 'dataset03' not in self.dataSets.keys():
                ds = DataSet(3)
                self.dataSets['dataset03'] = ds
        elif 'dataset04' in filename:
            if 'dataset04' not in self.dataSets.keys():
                ds = DataSet(4)
                self.dataSets['dataset04'] = ds
        elif 'dataset05' in filename:
            if 'dataset05' not in self.dataSets.keys():
                ds = DataSet(5)
                self.dataSets['dataset05'] = ds
        elif 'dataset06' in filename:
            if 'dataset06' not in self.dataSets.keys():
                ds = DataSet(6)
                self.dataSets['dataset06'] = ds
        elif 'dataset07' in filename:
            if 'dataset07' not in self.dataSets.keys():
                ds = DataSet(7)
                self.dataSets['dataset07'] = ds
        elif 'dataset08' in filename:
            if 'dataset08' not in self.dataSets.keys():
                ds = DataSet(8)
                self.dataSets['dataset08'] = ds
        elif 'dataset09' in filename:
            if 'dataset09' not in self.dataSets.keys():
                ds = DataSet(9)
                self.dataSets['dataset09'] = ds
        elif 'dataset10' in filename:
            if 'dataset10' not in self.dataSets.keys():
                ds = DataSet(10)
                self.dataSets['dataset10'] = ds
        elif 'dataset11' in filename:
            if 'dataset11' not in self.dataSets.keys():
                ds = DataSet(11)
                self.dataSets['dataset11'] = ds
        elif 'dataset12' in filename:
            if 'dataset12' not in self.dataSets.keys():
                ds = DataSet(12)
                self.dataSets['dataset12'] = ds
        elif 'dataset13' in filename:
            if 'dataset13' not in self.dataSets.keys():
                ds = DataSet(13)
                self.dataSets['dataset13'] = ds
        elif 'dataset14' in filename:
            if 'dataset14' not in self.dataSets.keys():
                ds = DataSet(14)
                self.dataSets['dataset14'] = ds
        elif 'dataset15' in filename:
            if 'dataset15' not in self.dataSets.keys():
                ds = DataSet(15)
                self.dataSets['dataset15'] = ds
        elif 'dataset16' in filename:
            if 'dataset16' not in self.dataSets.keys():
                ds = DataSet(16)
                self.dataSets['dataset16'] = ds
        elif 'dataset17' in filename:
            if 'dataset17' not in self.dataSets.keys():
                ds = DataSet(17)
                self.dataSets['dataset17'] = ds
        elif 'dataset18' in filename:
            if 'dataset18' not in self.dataSets.keys():
                ds = DataSet(18)
                self.dataSets['dataset18'] = ds
        elif 'dataset19' in filename:
            if 'dataset19' not in self.dataSets.keys():
                ds = DataSet(19)
                self.dataSets['dataset19'] = ds
        elif 'dataset20' in filename:
            if 'dataset20' not in self.dataSets.keys():
                ds = DataSet(20)
                self.dataSets['dataset20'] = ds
        elif 'dataset21' in filename:
            if 'dataset21' not in self.dataSets.keys():
                ds = DataSet(21)
                self.dataSets['dataset21'] = ds
        elif 'dataset22' in filename:
            if 'dataset22' not in self.dataSets.keys():
                ds = DataSet(22)
                self.dataSets['dataset22'] = ds
        elif 'dataset23' in filename:
            if 'dataset23' not in self.dataSets.keys():
                ds = DataSet(23)
                self.dataSets['dataset23'] = ds
        elif 'dataset24' in filename:
            if 'dataset24' not in self.dataSets.keys():
                ds = DataSet(24)
                self.dataSets['dataset24'] = ds
        elif 'dataset25' in filename:
            if 'dataset25' not in self.dataSets.keys():
                ds = DataSet(25)
                self.dataSets['dataset25'] = ds
        elif 'dataset26' in filename:
            if 'dataset26' not in self.dataSets.keys():
                ds = DataSet(26)
                self.dataSets['dataset26'] = ds
        elif 'dataset27' in filename:
            if 'dataset27' not in self.dataSets.keys():
                ds = DataSet(27)
                self.dataSets['dataset27'] = ds
        elif 'dataset28' in filename:
            if 'dataset28' not in self.dataSets.keys():
                ds = DataSet(28)
                self.dataSets['dataset28'] = ds
        elif 'dataset29' in filename:
            if 'dataset29' not in self.dataSets.keys():
                ds = DataSet(29)
                self.dataSets['dataset29'] = ds
        elif 'dataset30' in filename:
            if 'dataset30' not in self.dataSets.keys():
                ds = DataSet(30)
                self.dataSets['dataset30'] = ds
        elif 'dataset31' in filename:
            if 'dataset31' not in self.dataSets.keys():
                ds = DataSet(31)
                self.dataSets['dataset31'] = ds
        elif 'dataset32' in filename:
            if 'dataset32' not in self.dataSets.keys():
                ds = DataSet(32)
                self.dataSets['dataset32'] = ds
        self.do_analyse_file_name(filename)

    def do_analyse_file_name(self, filename):
        if platform.system() == 'Windows':
            temp = filename.split('CoronaryData_CTA\\')
            temp1 = temp[1].split('\\')
        else:
            temp = filename.split('CoronaryData_CTA/')
            temp1 = temp[1].split('/')

        if len(temp1) is 2:
            if temp1[1].__contains__('mhd'):
                self.dataSets[temp1[0]].set_image_path(filename)
        elif len(temp1) is 3:
            get_index = temp1[1].split('vessel')
            index = int(get_index[1])
            if temp1[2].__contains__('A'):
                self.dataSets[temp1[0]].set_point_a_path_by_vessel_index(index, filename)
            elif temp1[2].__contains__('B'):
                self.dataSets[temp1[0]].set_point_b_path_by_vessel_index(index, filename)
            elif temp1[2].__contains__('E'):
                self.dataSets[temp1[0]].set_point_e_path_by_vessel_index(index, filename)
            elif temp1[2].__contains__('S'):
                self.dataSets[temp1[0]].set_point_s_path_by_vessel_index(index, filename)
            elif temp1[2].__contains__('ref'):
                self.dataSets[temp1[0]].set_point_ref_path_by_vessel_index(index, filename)
