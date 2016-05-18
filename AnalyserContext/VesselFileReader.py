import threading
import time
import mmap


class VesselFileReader:
    # this class represent all the titleNames and values in the file
    def __init__(self):
        self.fileName = ""
        self.fileType = ""
        self.filePath = ""
        self.rowCount = 0
        self.columnCount = 0
        self.vesselValues = {"abscissa": [],
                             "ordinate": [],
                             "iso": [],
                             "radius": [],
                             "err": []}

        self.vessel_file_parse_thread = threading.Thread(None, self.do_parse_vessel_file)

    def parse_vessel_file(self, file_path):
        self.filePath = file_path
        # self.do_parse_vessel_file()
        # self.vessel_file_parse_thread.start()
        # self.vessel_file_parse_thread.join()

    def get_filename(self):
        return self.fileName

    def set_filename(self, filename):
        self.fileName = filename

    def get_file_type(self):
        return self.fileType

    def set_file_type(self, file_type):
        self.fileType = file_type

    def get_row_count(self):
        return self.rowCount

    def set_row_count(self, row_count):
        self.rowCount = row_count

    def get_column_count(self):
        return self.columnCount

    def get_abscissa_value_at(self, index):
        return self.vesselValues["abscissa"][index]

    def get_ordinate_value_at(self, index):
        return self.vesselValues["ordinate"][index]

    def get_iso_value_at(self, index):
        return self.vesselValues["iso"][index]

    def get_radius_value_at(self, index):
        return self.vesselValues["radius"][index]

    def get_err_value_at(self, index):
        return self.vesselValues["err"][index]

    def get_ordinate_value_at(self, index):
        return self.vesselValues["ordinate"][index]

    def get_len_of_vassel_value(self):
        return len(self.vesselValues["abscissa"])

    def do_parse_vessel_file(self):
        start = time.time()
        with open(self.filePath, "r+b") as f:
            # memory-mapInput the file, size 0 means whole file
            map_input = mmap.mmap(f.fileno(), 0)

            # read content via standard file methods
            for s in iter(map_input.readline, ""):
                s = s.translate(None, "\r\n")
                a_line_of_values = s.split(" ")
                #  print a_line_of_values
                if len(a_line_of_values) == 5:
                    self.vesselValues["abscissa"].append(float(a_line_of_values[0]))
                    self.vesselValues["ordinate"].append(float(a_line_of_values[1]))
                    self.vesselValues["iso"].append(float(a_line_of_values[2]))
                    self.vesselValues["radius"].append(float(a_line_of_values[3]))
                    self.vesselValues["err"].append(float(a_line_of_values[4]))
                else:
                    self.vesselValues["abscissa"].append(float(a_line_of_values[0]))
                    self.vesselValues["ordinate"].append(float(a_line_of_values[1]))
                    self.vesselValues["iso"].append(float(a_line_of_values[2]))

            map_input.close()
            end = time.time()
            print "Time for completion", end - start
