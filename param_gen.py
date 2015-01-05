# !/usr/bin/env python
# -*- coding: utf-8 -*-

def make_16_films(sprites, duration):
    """generate list of dictionnaries
    parametring syncloop film animations in 16 directions
    needs list of 3 list of sprite names corresponding to
    0, 22.5 and 45 degrees
    (we compute the other orientations)"""
    anims = []
    nb_frames = len(sprites[0])
    durations = [duration]*nb_frames
    base = {'type': 'SyncLoop', 'durations': durations}
    transformations = [
    (0, ''),
    (1, ''),
    (2, ''),
    (1, 'CWrot:Hsym'),
    (0, 'CWrot'),
    (1, 'CWrot'),
    (2, 'Hsym'),
    (1, 'Hsym'),
    (0, 'Hsym'),
    (1, 'Hsym:Vsym'),
    (2, 'Hsym:Vsym'),
    (1, 'CWrot:Vsym'),
    (0, 'CWrot:Vsym'),
    (1, 'CWrot:Hsym:Vsym'),
    (2, 'Vsym'),
    (1, 'Vsym')
    ]
    
    for i, transfo in transformations:
        names = []
        # add keywords behind sprites names for software transformations
        transfo = transfo.split(':')
        for sprite in sprites[i]:
            for t in transfo:
                sprite = sprite+':'+t
            names.append(sprite)
        
        dic = base.copy()
        dic.update({'sprites': names})
        anims.append(dic)
    return anims
