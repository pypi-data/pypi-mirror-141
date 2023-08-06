import yaml
import configparser
from dotenv import load_dotenv

#
# class Read_File:
#
#     def __init__(self, file_name):
#         self.file_name = file_name


def read_yml(file_name):
    if ".yaml" not in file_name:
        print("Not a valid yaml file. Valid file format is '.yaml'")
        return 1
    else:
        file_to_write = file_name.split(".")
        with open(file_name, "r") as yml_read:
            data = yaml.load(yml_read, Loader=yaml.FullLoader)
            print(data)
            with open(file_to_write[0]+".json", "w") as yml_write:
                yml_write.write(str(data))
        return 0



def read_conf(file_name):
    if ".cfg" in file_name or ".conf"  in file_name:
        conf_read = configparser.ConfigParser()
        conf_read.read(file_name)
        file_to_write = file_name.split(".")
        conf_write = open(file_to_write[0] + ".env", "a")
        for parse in conf_read.sections():
            for k, v in conf_read.items(parse):
                print("k:", k, "v:", v)
                conf_write.write(str(k))
                conf_write.write(":")
                conf_write.write(str(v))
                conf_write.write("\n")

        conf_write.close()
        load_dotenv(file_to_write[0]+".env")
        return 0
    else:
        print("Not a valid configuration file. Valid file format is '*.cfg' or '*.conf'")
        return 1


