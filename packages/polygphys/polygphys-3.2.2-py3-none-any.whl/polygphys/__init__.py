#!python
# -*- coding: utf-8 -*-
"""
Module utilitaire pour des tâches de laboratoire.

    - `outils` fournis les outils
    - les autres sous-modules sont des applications configurables.

Created on Mon Nov 15 15:17:28 2021

@author: ejetzer
"""

import logging
import sys
import pathlib

from .outils.journal import Formats

logger = logging.getLogger(__name__)


def main(dossier=None):
    """Exemple des fonctionnalités du module."""
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)

    fmt = logging.Formatter(Formats().détails)
    ch.setFormatter(fmt)

    logger.info('Démonstration du module polytechnique:')

    if dossier is None:
        if len(sys.argv) > 1:
            dossier = pathlib.Path(sys.argv[1]).resolve()
        else:
            fichier = pathlib.Path(__file__).expanduser().resolve()
            dossier = fichier.parent

    import polygphys.outils.database
    polygphys.outils.database.logger.addHandler(ch)
    polygphys.outils.database.logger.setLevel(logging.DEBUG)
    base, md = polygphys.outils.database.main(dossier)

    import polygphys.outils.config
    polygphys.outils.config.logger.addHandler(ch)
    polygphys.outils.config.logger.setLevel(logging.DEBUG)
    config = polygphys.outils.config.main(dossier)

    fichier_db = str(dossier / 'demo.db')
    swap_db = config.get('bd', 'adresse')
    config.set('bd', 'adresse', f'sqlite:///{fichier_db!s}')

    import polygphys.outils.interface.tkinter.onglets
    polygphys.outils.interface.tkinter.onglets.logger.addHandler(ch)
    polygphys.outils.interface.tkinter.onglets.logger.setLevel(logging.DEBUG)
    racine, onglets = polygphys.outils.interface.tkinter.onglets.main(
        config, md)

    config.set('bd', 'adresse', swap_db)

    logger.info('Fin.')
