# Copyright (c) 2013 Santosh Philip

# This file is part of pyclearsky.

# pyclearsky is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pyclearsky is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pyclearsky.  If not, see <http://www.gnu.org/licenses/>.

"""test ashraesky against weather file
compare outputs against weather data from clear sky days."""

import sys
# sys.path.append('/Users/santosh/Documents/coolshadow/sunpath/spapyrex')
sys.path.append('/Users/oompag/Documents/coolshadow/sunpath/spapyrex')

import spabase
import calendar
import clearskyrad
from datetime import datetime

# phoenix Arizona
spadict = {}
spadict['year'] = 1975 
spadict['month'] = 2
spadict['day'] = 16
spadict['hour'] = 14
spadict['minute'] = 00
spadict['second'] = 00
spadict['timezone'] = -7.0 # negative west of Greenwich
                           # -12   to   12 hours
spadict['delta_t'] = 67 # Difference between earth rotation time 
                        # and terrestrial time
spadict['longitude'] = -112.066 # negative west of Greenwich
                                # -180  to  180 degrees
spadict['latitude'] = 33.43 # N is +ve
spadict['elevation'] = 339.14 # meters
spadict['pressure'] = 820 # millibars
spadict['temperature'] = 11 # C
spadict['slope'] = 0
spadict['azm_rotation'] = 0
spadict['atmos_refract'] = 0.5667 # typical value

statfilename = './weatherfiles/USA_AZ_Phoenix/USA_AZ_Phoenix.722780_TMY2.stat'
taubs, tauds = clearskyrad.tau(open(statfilename))

# for m in range(1, 13):
for m in range(1, 13):
    for d in range(1, calendar.monthrange(spadict['year'], m)[1] + 1):
    # for d in range(1, 25):
        for h in range(1, 25):
            spadict['month'] = m
            spadict['day'] = d
            spadict['hour'] = h
            try:
                sun = spabase.spacalc(spadict)
                alt = 90 - sun['zenith']
                taub, taud = taubs[m -1], tauds[m -1]
                thedate = datetime(spadict['year'], m, d)
                if alt <= 0:
                    Eb = 0
                    Ed = 0
                else:
                    Eb = clearskyrad.directnormal(taub, taud, alt, thedate=thedate)
                    Ed = clearskyrad.diffusehorizontal(taub, taud, alt, thedate=thedate)
                print '%s, %s, %s, %s, %s, %s' % (m, d, h, alt, Eb, Ed)
                # print m, d, h, 90 - sun['zenith']
                # print sun
            except spabase.UnknownError:
                raise spabase.DataError
