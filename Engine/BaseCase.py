# -*- coding: utf-8 -*-

from Engine.Base import INIT

Flag = True


class Case(INIT):
    def __init__(self):
        super().__init__()

        self.params()

    def run(self):
        global Flag
        try:
            self.preprocess()
        except Exception as e:
            Flag = False
            print('error info :', e)
            raise
        else:
            try:
                self.process()
            except Exception as e:
                Flag = False
                print('error info :', e)
                raise
        finally:
            self.postprocess()
            self.result()

    def params(self):
        pass

    def preprocess(self):
        pass

    def process(self):
        pass

    def postprocess(self):
        pass

    def result(self):
        if Flag:
            print(self.__class__.__name__, ' --------------- PASS')
        else:
            print(self.__class__.__name__, ' --------------- FAILED')


if __name__ == '__main__':
    pass
