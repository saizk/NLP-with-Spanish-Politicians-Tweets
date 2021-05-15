from .util import traverse_dict

__all__ = ["MAIN_PARTIES", "PARTIES_TWITTERS"]


MAIN_PARTIES = {
    "PSOE": ["PSOE", "psoe"],
    "PP": ["PP", "pp"],
    "CiudadanosCs": ["Ciudadanos"],
    "Unidas Podemos": ["Podemos"],
    "Vox": ["VOX", "vox"]
}

TR_MAIN_PARTIES = traverse_dict(MAIN_PARTIES)

PARTIES_TWITTERS = {
    "PSOE": ["psoe", "gpscongreso"],
    "PP": ["populares", "gppopular"],
    "CiudadanosCs": ["ciudadanoscs"],
    "Unidas Podemos": ["podemos"],
    "Vox": ["vox_es"],
    "Más País": ["maspais_es"],
    "Navarra Suma": ["navarrasuma_pna"],
    "EHBildu": ["ehbildu"],
    "Esquerra Republicana": ["esquerra_erc"],
    "Coalición Canaria": ["coalicion"],
    "BNG": ["obloque"],
    "JxCAT": ["juntsxcat"],
    "CUP-PR": ["cupnacional"],
    "PSC": ["socialistes_cat"],
    "PSE-EE-PSOE": ["socialistavasco"],
    "PSdeG-PSOE": ["psdeg"],
    "En Comú Podem": ["encomu_podem"],
    "MésCompromís": ["compromis"],
    "Teruel Existe": ["teruelexiste_"],
    "EAJ-PNV": ["eajpnv"],
    "PRC": ["prcantabria"],
    "EnComún": ["encomun_gal"]
}
