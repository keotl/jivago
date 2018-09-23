class Runnable(object):

    def run(self):
        raise NotImplementedError

    def cleanup(self):
        pass
