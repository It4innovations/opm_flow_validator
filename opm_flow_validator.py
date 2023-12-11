#
# Author: Georg Zitzlsberger (georg.zitzlsberger<ad>vsb.cz)
# Copyright (C) 2023 Georg Zitzlsberger, IT4Innovations,
#                    VSB-Technical University of Ostrava, Czech Republic
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
import os
import re
import io
import sys
import pandas as pd
import subprocess
from matplotlib import pyplot as plt

def usage():
    print("Usage:")
    print("{} summary_tool results_a results_b case_name".format(sys.argv[0]))
    print("")
    print("  summary_tool:  Path to opm-common's 'summary' tool")
    print("  results_[a|b]: Paths to OPM Flow results (A/B) to compare")
    print("  case_name:     Name of the case")

if len(sys.argv) != 5:
    usage()
    sys.exit(1)

summary_tool = sys.argv[1]
dir_a = sys.argv[2]
dir_b = sys.argv[3]
case = sys.argv[4]

if not os.access(summary_tool, os.X_OK):
    print("Error: summary_tool is not executable")
    print("")
    usage()
    sys.exit(1)

if not os.path.isdir(dir_a) or \
   not os.path.isdir(dir_b):
    print("Error: results_[a|b] have to be directories")
    print("")
    usage()
    sys.exit(1)

if not os.path.isfile(dir_a + "/" + case + ".UNSMRY") or \
   not os.path.isfile(dir_b + "/" + case + ".UNSMRY"):
    print("Error: case_name does not exist in results_[a|b]")
    print("")
    usage()
    sys.exit(1)

outs = subprocess.run([summary_tool, "-l", dir_a + "/" + case], shell=False, text=True, capture_output=True)
if outs.returncode != 0:
    print("Error: Cannot execute '{} -l {}'".format(summary_tool, dir_a + "/" + case))
    sys.exit(1)

# WBHP should always be there!
wells = re.findall('WBHP:([^ \t]+)', outs.stdout, re.DOTALL)
print("Found the following wells:")
for well in wells:
    print("\t" + well)

opts = re.findall("([^ \t]+):{}".format(wells[0]), outs.stdout, re.DOTALL)
print("Found the following options:")
for opt in opts:
    print("\t" + opt)

querys = []
for well in wells:
    for opt in opts:
        querys.append("{}:{}".format(opt, well))


def RRMSE(df_a, df_b):
        num = ((df_a - df_b)**2).mean(axis=0)
        den = (df_a**2).sum(axis=0)
        if den == 0:
            squared_error = float("nan")
        else:
            squared_error = num / den
        rrmse = squared_error**0.5
        return rrmse

print("RRMSE for...")
for query in querys:
    outs_a = subprocess.run([summary_tool, dir_a + "/" + case, "TIME", query], shell=False, text=True, capture_output=True)
    if outs_a.returncode != 0:
        print("Error: Cannot execute '{} {} TIME {}'".format(summary_tool, dir_a + "/" + case, query))
        sys.exit(1)
    outs_b = subprocess.run([summary_tool, dir_b + "/" + case, "TIME", query], shell=False, text=True, capture_output=True)
    if outs_b.returncode != 0:
        print("Error: Cannot execute '{} {} TIME {}'".format(summary_tool, dir_b + "/" + case, query))
        sys.exit(1)

    buffer_a = io.StringIO(outs_a.stdout)
    df_a = pd.read_csv(filepath_or_buffer = buffer_a, sep="\s+", index_col=0)#, names=['TIME', query])

    buffer_b = io.StringIO(outs_b.stdout)
    df_b = pd.read_csv(filepath_or_buffer = buffer_b, sep="\s+", index_col=0)

    df = pd.DataFrame({"{}_a".format(query): df_a[query], "{}_b".format(query): df_b[query]})
    df_int = df.interpolate(method='linear', axis=0)

    rrmse = RRMSE(df_int["{}_a".format(query)], df_int["{}_b".format(query)])
    print("\t{}: {}".format(query, rrmse))

    ax = df_a.plot(use_index=True, xlabel="TIME", ylabel=query, figsize=(15,8))
    df_b.plot(use_index=True, xlabel="TIME", ylabel=query, label=dir_b, ax=ax)
    ax.grid()
    ax.legend([dir_a, dir_b])
    plt.savefig("{}.pdf".format(query), bbox_inches='tight')
