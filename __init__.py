# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QGISTester
                                 A QGIS plugin
 Make testing on various platforms easy and reliable
                             -------------------
        begin                : 2014-11-09
        copyright            : (C) 2014 by Minoru Akagi
        email                : akaginch@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load QGISTester class from file QGISTester.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .qgis_tester import QGISTester
    return QGISTester(iface)
