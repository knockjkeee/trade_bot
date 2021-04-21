class Data(object):
    """"""

    def __init__(self):
        self.data = []
        """Constructor for data"""

    def set_item_to_data(self, item):
        self.data.append(item)

    def get_items(self):
        return self.data
