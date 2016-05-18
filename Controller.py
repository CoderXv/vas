__author__ = 'Xu'


class Controller:
    def __init__(self, system_data_base):
        self.systemDataBase = system_data_base

    def load_mri_image_into_context_by_name(self, fname):
        return self.systemDataBase.load_mri_image_into_context_by_name(fname)

    # the first layer of the tree
    def get_number_of_dataset(self):
        return self.systemDataBase.get_number_of_dataset()

    def get_first_level_folders(self):
        return self.systemDataBase.get_name_of_the_data_sets()

    # the second layer of the tree
    def get_number_of_vessel_folder(self, dataset_name):
        return self.systemDataBase.get_number_of_vessel_folder(dataset_name)

    def get_path_of_vessel_ref_file_by_index(self, dataset_name, index):
        return self.systemDataBase.get_path_of_the_vessel_file(dataset_name, index)

    def get_path_of_the_image_file(self, dataset_name):
        return self.systemDataBase.get_path_of_the_image_file(dataset_name)

    # the third layer of the tree
    def get_number_of_the_point_file(self, dataset_name, vessel_index):
        return self.systemDataBase.get_number_of_the_point_file_in_sys_db(dataset_name, vessel_index)

    def get_name_of_the_point_file(self):
        return self.systemDataBase.get_name_of_the_point_file()

    def get_the_path_of_the_point(self, ds_name, vessel_index, point_key):
        return self.systemDataBase.get_the_path_of_the_point(ds_name, vessel_index, point_key)

    def get_the_ref_data_of_dataset_by_index(self, ds_name, vessel_index):
        return self.systemDataBase.get_the_ref_data_of_the_point_by_index(ds_name, vessel_index)

    def get_vessels_from_dataset(self, ds_name):
        return self.systemDataBase.get_data_set_vessels(ds_name)

    def store_vessel_to_be_evaluated(self, single_path_dir, ds_name, file_name, vessel_num):
        self.systemDataBase.store_vessel_to_be_evaluated(single_path_dir, ds_name, file_name, vessel_num)

    def load_vessel_to_be_evaluated(self, ds_name, vessel_num, file_name):
        return self.systemDataBase.load_vessel_to_be_evaluated(ds_name, vessel_num, file_name)
