import xml.dom.minidom as xml
import pandas as pd


class XMLReader:
    def __init__(self, xml_path):
        self.xml_data = xml.parse(xml_path)

    def get_width(self):
        width_node = self.xml_data.getElementsByTagName('width')
        width = int(width_node.item(0).firstChild.data)
        return width

    def get_height(self):
        height_node = self.xml_data.getElementsByTagName('height')
        height = int(height_node.item(0).firstChild.data)
        return height

    def get_name(self):
        if self.xml_data.getElementsByTagName('filename').item(0) is not None:
            filename_node = self.xml_data.getElementsByTagName('filename')
            filename = filename_node.item(0).firstChild.data
        elif self.xml_data.getElementsByTagName('file').item(0) is not None:
            file_node = self.xml_data.getElementsByTagName('file')
            file = file_node.item(0).firstChild.data
            filename = file + '.jpg'
        return filename

    def get_dataset(self):
        if self.xml_data.getElementsByTagName('filename').item(0) is not None:
            filename_node = self.xml_data.getElementsByTagName('filename')
            filename = filename_node.item(0).firstChild.data
        elif self.xml_data.getElementsByTagName('file').item(0) is not None:
            file_node = self.xml_data.getElementsByTagName('file')
            file = file_node.item(0).firstChild.data
            filename = file + '.jpg'

        if 'Android' in filename:
            dataset = 'Android'
        elif 'IMG' in filename:
            dataset = 'iPhone'
        elif 'IMG' in filename:
            dataset = 'iPhone'
        elif 'uplabs' in filename or 'Login' in filename:
            dataset = 'Uplabs'
        elif 'wf' in filename:
            dataset = 'Wireframes'
        else:
            dataset = 'Rico'
        return dataset

    def get_components(self):
        object_nodes = self.xml_data.getElementsByTagName('object')
        nb_object = object_nodes.length
        name_list = []
        xmin_list = []
        ymin_list = []
        xmax_list = []
        ymax_list = []
        center_x_list = []
        center_y_list = []

        index = list(range(0, nb_object))
        columns = ('type', 'xmin', 'ymin', 'xmax', 'ymax', 'center_x', 'center_y', 'text')
        df = pd.DataFrame(0, index=index, columns=columns)

        for i in range(nb_object):
            # get the component type, the bounding box and the position
            name_node = object_nodes.item(i).getElementsByTagName('name')
            name_list.append(name_node.item(0).firstChild.data)
            bndbox_node = object_nodes.item(i).getElementsByTagName('bndbox')
            xmin = int(float(bndbox_node.item(0).getElementsByTagName('xmin').item(0).firstChild.data))
            ymin = int(float(bndbox_node.item(0).getElementsByTagName('ymin').item(0).firstChild.data))
            xmax = int(float(bndbox_node.item(0).getElementsByTagName('xmax').item(0).firstChild.data))
            ymax = int(float(bndbox_node.item(0).getElementsByTagName('ymax').item(0).firstChild.data))
            xmin_list.append(xmin)
            ymin_list.append(ymin)
            xmax_list.append(xmax)
            ymax_list.append(ymax)
            center_box = (int((xmax - xmin) / 2 + xmin), int((ymax - ymin) / 2 + ymin))
            center_x_list.append(center_box[0])
            center_y_list.append(center_box[1])

        df.type = name_list
        df.xmin = xmin_list
        df.ymin = ymin_list
        df.xmax = xmax_list
        df.ymax = ymax_list
        df.center_x = center_x_list
        df.center_y = center_y_list

        return df
