"""`lvr` comes with example data sets from real life."""

from json import load
from collections import OrderedDict

from pkg_resources import resource_filename

from lvr.helpers import get_example

data_sets = []

def data_set(func):
    data_sets.append(func)
    return func

@data_set
def missing_teeth():
    """Number of missing teeth of 966 young German adults (35 to 44 years).

    Source: `Institute of German Dentists, Cologne`_: Fifth German Oral Health Study
    (DMS V), ISBN 978-3-7691-0020-4.

    .. _Institute of German Dentists, Cologne: http://www.idz-koeln.de
    """
    return get_example('data/missing_teeth.csv')


@data_set
def bells():
    """Weights of 9,605 church bells in kg of the German
    archbishoprics of `Cologne`_, `Aachen`_ and `Essen`_.

    Source: expert-HOFFMANN GmbH, Köln, 2016.

    .. _Cologne: http://glockenbuecherebk.de
    .. _Aachen: http://www.glockenbuecherbaac.de
    .. _Essen: http://www.glockenbuecherbes.de
    """
    return get_example('data/bells.csv')

@data_set
def women_intercourse():
    """Number of vaginal sex partners of 11,110 women.

    Source: Jakob Pastötter, Nicolas Drey, Anthony Pryce: Sex Study 2008 - Sexual
    Behaviour in Germany. DGSS and City University London.
    """
    return get_example('data/women_intercourse.csv')


@data_set
def boxoffice():
    """Boxoffice revenue of 4,189 movies in US Dollars.

    Source: `OMDb`_.

    .. _OMDb: https://github.com/rstudio/shiny-examples/tree/master/051-movie-explorer
    """
    return get_example('data/boxoffice.csv')


@data_set
def wkzs():
    """Area designated for wind power usage in ha in 315 of 396
    municipalities of North Rhine Westphalia, Germany 2012-2016.
    The remaining municipalities do not have designated any area
    for wind power usage.

    Source: State Office for Nature, Environment and Consumer
      Affairs of North-Rhine Westphalia (`LANUV`_) based on data
      of planning regions; municipalities mentioned below, 2016.
      The data may not be complete for some parts. Data state for
      planning regions Münster, Arnsberg und Köln: July 2015,
      Detmold: June 2015. RVR: Late 2014, Düsseldorf: January 2011.
      Municipalities Anröchte, Drensteinfurt, Drolshagen, Eslohe
      (Sauerland), Hemer, Kaarst, Lippstadt, Mettmann, Metelen,
      Warendorf, Wickede (Ruhr), Wülfrath: 2016.

    .. _LANUV: http://lanuv.nrw.de
    """
    return get_example('data/wkzs.csv')


@data_set
def euro_coins():
    """Nominal value of Euro coins in circulation in million Euro as per December 2016.

    Source: European Central Bank: `Banknotes and coins circulation`_, 2017.

    .. _Banknotes and coins circulation: http://www.ecb.europa.eu/stats/money/euro/circulation/html/index.en.html
    """
    return [0.01*32734, 0.02*25114, 0.05*19509, 0.1*14148, 0.2*10778, 0.5*5901, 1*6977, 2*5815]


@data_set
def euro_banknotes():
    """Nominal value of Euro bank notes in circulation in million Euro as per December 2016.

    Source: European Central Bank: `Banknotes and coins circulation`_, 2017.

    .. _Banknotes and coins circulation: http://www.ecb.europa.eu/stats/money/euro/circulation/html/index.en.html
    """
    return [5*1805, 10*2387, 20*3590, 50*9231, 100*2433, 200*234, 500*540]


@data_set
def hopei_rain():
    """Daily precipitation in mm on Hohenpeißenberg, Germany
    (the world's oldest mountain weather station) from 1781 to 2015.

    Source: `German Meteorological Office`_, 2016.

    .. _German Meteorological Office: http://www.dwd.de
    """
    return get_example('data/hopei_rain.csv')


@data_set
def hopei_sun():
    """Daily sun hours on Hohenpeißenberg, Germany
    (the world's oldest mountain weather station) from 1937 to 2015.

    Source: `German Meteorological Office`_, 2016.

    .. _German Meteorological Office: http://www.dwd.de
    """
    return get_example('data/hopei_sun.csv')


@data_set
def german_rivers():
    """Lengths of 267 longest German rivers in km.

    Source: `Wikipedia`_, 2016.

    .. _Wikipedia: https://de.wikipedia.org/w/index.php?title=Liste_von_Flüssen_in_Deutschland&oldid=158665390
    """
    return [1236, 1091, 866, 744, 524, 371, 300, 290, 256, 220, 219, 208,
            188, 185, 182, 176, 169, 166, 165, 153, 153, 150, 143, 128,
            124, 121, 118, 114, 107, 105, 105, 102, 101, 97, 97, 92, 91,
            90, 80, 75, 73, 72, 72, 70, 68, 68, 67, 67, 65, 67, 63, 63,
            62, 62, 61, 60, 60, 59, 59, 58, 57, 57, 57, 57, 57, 56, 55,
            54, 52, 52, 52, 51, 50, 49, 49, 49, 48, 47, 47, 46, 45, 45,
            45, 45, 45, 44, 43, 42, 42, 40, 40, 40, 40, 40, 40, 40, 39,
            39, 38, 37, 37, 37, 36, 35, 35, 35, 35, 35, 35, 34, 34, 34,
            34, 33, 33, 33, 33, 32, 31, 31, 31, 31, 30, 30, 30, 30, 30,
            30, 30, 30, 30, 30, 29, 29, 29, 28, 28, 28, 28, 28, 28, 27,
            27, 27, 27, 27, 26, 26, 26, 25, 25, 25, 25, 25, 25, 25, 25,
            24, 24, 24, 24, 24, 23, 23, 23, 23, 23, 22, 22, 22, 22, 22,
            22, 22, 22, 22, 22, 22, 22, 21, 21, 21, 21, 21, 21, 21, 21,
            21, 20, 20, 20, 20, 20, 19, 18, 18, 18, 18, 18, 18, 18, 18,
            17, 17, 17, 17, 17, 17, 16, 16, 16, 16, 16, 16, 16, 16, 16,
            16, 16, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 14, 14,
            14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 12, 12, 12, 12, 12,
            12, 12, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
            11, 10, 10, 10, 10]


@data_set
def german_motorways():
    """Lengths of 120 German federal motorways (Autobahnen) in km.

    Source: `Bundesanstalt für Straßenwesen`_, 2016.

    .. _Bundesanstalt für Straßenwesen: http://www.bast.de
    """
    return get_example('data/german_motorways.csv')


@data_set
def german_highways():
    """Lengths of 393 German federal highways (Bundesstraßen) in km.

    Source: `Bundesanstalt für Straßenwesen`_, 2016.

    .. _Bundesanstalt für Straßenwesen: http://www.bast.de
    """
    return get_example('data/german_highways.csv')


@data_set
def us_bridges():
    """Length of 614,387 bridges in the United States of America in metres.

    Source: `Federal Highway Administration`, 2016.

    .. _Federal Highway Administration: https://www.fhwa.dot.gov/bridge/nbi/ascii.cfm?year=2016
    """
    return get_example('data/us_bridges.csv')


@data_set
def flight_delays():
    """Departure delays in minutes of 434,354 flights in the United States in November 2016.

    Source: Bureau of Transportation Statistics, `TranStats`_, 2017.

    .. _TranStats: http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time
    """
    return get_example('data/flight_delays.csv')


@data_set
def jre_rail_passengers():
    """Japanese Eastern Railways passenger frequency of 860 stations in 2015.

    Source: `JREast`_, 2016.

    .. _JREast: http://www.jreast.co.jp/passenger/index.html
    """
    return get_example('data/jre_rail_passengers.csv')


@data_set
def french_rail_passengers():
    """French railway passenger frequency of 3,034 stations in 2015.

    Source: `SNCF`_, February 2017.

    .. _SNCF: http://ressources.data.sncf.com/explore/dataset/frequentation-gares
    """
    return get_example('data/french_rail_passengers.csv')


@data_set
def swiss_rail_passengers():
    """Swiss railway passenger frequency of 724 stations in 2014.

    Source: `SBB`__, March 2016.

    __ https://data.sbb.ch/explore/dataset/passagierfrequenz/
    """
    return get_example('data/swiss_rail_passengers.csv')


@data_set
def swiss_public_transport_delays():
    """Delays of 14 million stops in minutes from April 4th trough
    May 2nd, 2017 in the Swiss public transport system.

    Source: `SBB`__, May 2017.

    __ https://opentransportdata.swiss/de/dataset/istdaten
    """
    return get_example('data/swiss_public_transport_delays.csv')


@data_set
def indian_trains_passing():
    """Number of Indian trains passing through 2,961 of 4,756 stations.

    Source: `Cleartrip`_, May 2017.

    .. _Cleartrip: https://www.cleartrip.com/trains/stations/list
    """
    return get_example('data/indian_trains_passing.csv')


@data_set
def us_power_plants():
    """Electric capacity in Megawatts of 7,610 US power plants.

    Source: `Energy Information Administration`_, December 2016.

    .. _Energy Information Administration: https://data.opendatasoft.com/explore/dataset/power-plants%40public/information/
    """
    return get_example('data/us_power_plants.csv')


@data_set
def exoplanets():
    """Mass and radius for 630 exoplanets.

    Source: `Exoplanet Team`_, February 2017.

    .. _Exoplanet Team: http://www.exoplanet.eu/catalog/
    """
    with open(resource_filename(__name__, 'data/exoplanets.json')) as f:
        return load(f, object_pairs_hook=OrderedDict)


@data_set
def titanic_fares():
    """Fares of 891 passengers of the Titanic.

    Source: `Xiamen Chen`_, November 2014.

    .. _Xiamen Chen: https://github.com/caesar0301/awesome-public-datasets/tree/master/Datasets
    """
    return get_example('data/titanic_fares.csv')


@data_set
def tree_vol():
    """Volume in cubic metres of 536,752 German trees in 2012.

    Source: Thünen-Institute, `Third National Forest Inventory`_, 2016.

    .. _Third National Forest Inventory: https://bwi.info
    """
    return get_example('data/tree_vol.csv')


@data_set
def lakes_level_1():
    """Volume in cubic kilometres and surface in square kilometres of 519 lakes and reservoirs.

        Subset from Level 1.

        Level 1 (GLWD-1) comprises the 3,067 largest lakes (area ≥ 50 km\ :sup:`2`) and 654 largest reservoirs (storage capacity ≥ 0.5 km\ :sup:`3`) worldwide, and includes extensive attribute data.

        Source: `World Wildlife Fund`_, July 1st, 2004.

        .. _World Wild Life Fund: https://www.worldwildlife.org/publications/global-lakes-and-wetlands-database-large-lake-polygons-level-1
    """
    with open(resource_filename(__name__, 'data/lakes_level_1.json')) as f:
        return load(f, object_pairs_hook=OrderedDict)


@data_set
def lakes_surface():
    # pragma pylint: disable=line-too-long
    """Surface in square kilometres of 248,613 lakes and reservoirs.

    This set combines GLWD-1 and GLWD-2 data sets.

    Level 1 (GLWD-1) comprises the 3,067 largest lakes (area ≥ 50 km\ :sup:`2`) and 654 largest reservoirs (storage capacity ≥ 0.5 km\ :sup:`3`) worldwide, and includes extensive attribute data.

    Level 2 (GLWD-2) comprises permanent open water bodies with a surface area ≥ 0.1 km\ :sup:`2` excluding the water bodies contained in GLWD-1. The approximately 250,000 polygons of GLWD-2 are attributed as lakes, reservoirs and rivers.

    Source: `World Wildlife Fund`_, July 1st, 2004.

    .. _World Wildlife Fund: https://www.worldwildlife.org/publications/global-lakes-and-wetlands-database-large-lake-polygons-level-1
    """
    return get_example('data/lakes_surface.csv')
    # pragma pylint: enable=line-too-long


@data_set
def forest_fires():
    """Size of 51,674 Canadian Forest Fires (1959-2015) in ha.

    Source: `Canadian National Fire Database`_, 2017.

    .. _Canadian National Fire Database: http://cwfis.cfs.nrcan.gc.ca/datamart/metadata/nfdbpnt
    """
    return get_example('data/forest_fires.csv')


@data_set
def stars_masses():
    """Masses of 168 stars within 75 light years distance in suns.

    Source: `Internet Stellar Database`_, 2017.

    .. _Internet Stellar Database: http://www.stellar-database.com
    """
    return get_example('data/stars_masses.csv')


@data_set
def stars_surfaces():
    """Surfaces of 1,112 stars within 75 light years distance in suns.

    Source: `Internet Stellar Database`_, 2017.

    .. _Internet Stellar Database: http://www.stellar-database.com
    """
    return get_example('data/stars_surfaces.csv')


@data_set
def stars():
    """Masses and radii of 211 stars within 75 light years distance in suns.

    Source: `Internet Stellar Database`_, 2017.

    .. _Internet Stellar Database: http://www.stellar-database.com
    """
    with open(resource_filename(__name__, 'data/stars.json')) as f:
        return load(f, object_pairs_hook=OrderedDict)


@data_set
def meteorites():
    """Masses of 46,038 meteorites found on earth.

    Source: `Meteoritical Bulletin Database`_, 2017.

    .. _Meteoritical Bulletin Database: https://www.lpi.usra.edu/meteor/metbull.php
    """
    return get_example('data/meteorites.csv')


@data_set
def debris_masses():
    """Masses of xxx debris.

    Source: Europe Space Agency, 2017.
    """
    return get_example('data/debris_masses.csv')
