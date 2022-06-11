FROM jupyter/scipy-notebook:ubuntu-20.04

USER root
RUN mkdir /data

# GRASS GIS
RUN mkdir /data/grass
RUN wget -c https://geo.fsv.cvut.cz/geoharmonizer/odse_workshop_2022/grass/geodata.zip -O /data/grass/geodata.zip
RUN apt-get update
RUN apt-get --yes install software-properties-common
RUN add-apt-repository ppa:ubuntugis/ubuntugis-experimental
RUN add-apt-repository ppa:ubuntugis/ubuntugis-unstable
RUN apt-get update
RUN apt-get --yes install grass-core grass-dev
RUN apt-get --yes install python3-ply
RUN pip3 install folium gdal==3.4.3 

# eumap
# RUN pip3 install -e git+https://gitlab.com/geoharmonizer_inea/eumap.git#egg=eumap[full]

# ST_LUCAS
RUN pip3 install owslib==0.22
RUN pip3 install -e git+https://gitlab.com/geoharmonizer_inea/st_lucas/st_lucas-python-package.git@release-1_0#egg=st_lucas
