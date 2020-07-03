class Bear(object):

    def __init__(self, **kwargs):
        self.bear_id = kwargs.get('bear_id')
        self.bear_type = kwargs.get('bear_type')
        self.bear_name = kwargs.get('bear_name')
        self.bear_age = kwargs.get('bear_age')

    @property
    def name(self):
        return self.bear_name.upper() if self.bear_name is not None else None

    @property
    def age(self):
        return float(self.bear_age) if self.bear_age is not None else None
