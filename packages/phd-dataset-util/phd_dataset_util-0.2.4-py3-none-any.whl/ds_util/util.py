import numpy as np
import pandas as pd

def get_nearest_value(sim_values,value):
    """
        Given a value and a values list this method return from the the nearest element to the value
    """
    absolute_val_array = np.abs(sim_values - value)
    return sim_values[absolute_val_array.argmin()]

def block_dataset(raw_dfa,raw_dfb,blk_att_a,blk_att_b,
                    id_a='voter_id',id_b='voter_id',
                    key_lenght=3):
    """
        Block a dataset considering one attributes
        - raw_dfa : dataset a
        - raw_dfa : dataset b
        - blk_att_a : attribute to block
        - blk_att_b : attribute to block
        - id_a : id attribute (default: voter_id)
        - id_b : id attribute (default: voter_id)
        - key_lenght : key kength
    """
    raw_dfa['BLK'] = raw_dfa[blk_att_a].str[:key_lenght]
    raw_dfb['BLK'] = raw_dfb[blk_att_b].str[:key_lenght]

    comps = []

    for block in raw_dfa['BLK'].unique():
        fdfa = raw_dfa[raw_dfa['BLK']==block]
        fdfb = raw_dfb[raw_dfb['BLK']==block]

        if len(fdfb) > 0:
            for ida in fdfa[id_a].unique():
                for idb in fdfb[id_b].unique():
                    comps.append([ida,idb]) #adiciona a comparacao
    
    comps = pd.DataFrame(comps)
    comps.columns = ['id1','id2']
    return comps