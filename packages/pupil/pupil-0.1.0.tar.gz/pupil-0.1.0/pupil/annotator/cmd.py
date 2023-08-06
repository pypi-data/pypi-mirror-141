from pupil.db.database import DataBase
from pupil.sampler import Sampler
import numpy as np

class CMD:
    def __init__(self, db: DataBase, sampler:Sampler):
        self.db = db
        self.sampler = sampler

    def do(self):
        ind = self.sampler.sample(n=5)
        print('Index: ',ind, self.db.metadb.label, self.db.get(ind , return_emb=False))
        inp = int(input("Label?"))
        self.db.metadb.set_label(ind, inp)
        