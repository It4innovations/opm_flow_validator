# Validate OPM Flow Results

This tool computes the RRMSE (Relative Root Mean Square Error) for the individual options and wells from the [OPM Flow](https://opm-project.org/) results. It helps to quickly assess whether changes produce similar results.

# Usage

    $ python opm_flow_validator.py ../opm-common/build/bin/summary ../orig_sleip_n1_np8_omp2 ../sleip_n1_np8_omp2 SLEIPNER
    Found the following wells:
        Injector
    Found the following options:
        WBHP
        WGIR
        WGIT
        WGOR
        WOPR
        WOPT
    RRMSE for...
        WBHP:Injector: 0.00012067214186583837
        WGIR:Injector: 0.0
        WGIT:Injector: 0.000883134044815037
        WGOR:Injector: nan
        WOPR:Injector: nan
        WOPT:Injector: nan

In addition, to the RRMSE metrics, it generates plots in the local work directory to compare (e.g., WBHP:Injector.pdf). View with a PDF viewer.

# Contact
Should you have any feedback or questions, please contact the main author: Georg Zitzlsberger (georg.zitzlsberger(a)vsb.cz).

# Acknowledgments
This work was supported by the ACROSS project. This project has received funding from the European High- Performance Computing Joint Undertaking (JU) under grant agreement No 955648. The JU receives support from the European Union's Horizon 2020 research and innovation programme and Italy, France, the Czech Republic, the United Kingdom, Greece, the Netherlands, Germany, Norway. This project has received funding from the Ministry of Education, Youth and Sports of the Czech Republic (ID: MC2104).

# License
This project is made available under the GNU General Public License, version 3 (GPLv3).



