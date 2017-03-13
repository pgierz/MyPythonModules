from custom_io import get_remote_data, custom_io_constants
from parsing_tools import get_model_component_from_varname, lists
import os
from scipy.io import netcdf
import cdo

CDO = cdo.Cdo()

GLOBAL_DEBUG = False


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def debug(s):
    if GLOBAL_DEBUG:
        print((bcolors.FAIL + "DEBUG: "+s+bcolors.ENDC))


def header(s):
    # print((bcolors.HEADER+s+bcolors.ENDC))
    pass


def fix_mpiom_levels(fname):
    if CDO.nlevel(input=fname)[0] == "40":
        if not CDO.showlevel(input=fname)[0].split(" ")[0] == "6":
            os.system("cdo invertlev "+fname+" tmp")
            os.system("mv tmp "+fname)


def old_simulation_header(my_fn):
    def split_old_name_style(remote_address):
        user = remote_address.split(":")[0].split("@")[0]
        host = remote_address.split(":")[0].split("@")[1]
        path = remote_address.split(":")[1]
        expid = path.split("/")[-1]
        return my_fn(user, host, path, expid)
    return split_old_name_style


class _cosmos_simulation(object):
    """
    # TODO I need to write some documentation for this

    Paul J. Gierz, Sat Feb  6 13:37:00 2016
    """

    def __init__(self, user, host, path, expid):
        self._script_dir = "/Users/pgierz/Research/scripts/"
        self.fullpath = user+"@"+host+":"+path+"/"+expid
        self.user = user 
        self.host = host
        self.path = path
        self.expid = expid

    @classmethod
    def from_old_init(cls, remote_address):
        user = remote_address.split(":")[0].split("@")[0]
        host = remote_address.split(":")[0].split("@")[1]
        path = remote_address.split(":")[1]
        expid = path.split("/")[-1]       
        return cls(user, host, path, expid)

    def _deploy_script(self, script, args, needs_exp=False):
        """This private method takes a script given by the arg script and
        deploys it to the remote host to do cdo stuff

        args are EXTRA args to the script that are normally supplied via flags.

        Paul J. Gierz, Sat Feb  6 13:57:51 2016
        """

        # sendargs = []
        # if needs_exp:
        #     for a in range(len(args)):
        #         sendargs.append(self.path + "/" +
        #                         args[a].replace("@EXPID@", self.expid))
        # else:
        #     sendargs = args

        # If script is link, expand to the real thing:
        command = "ssh -T " + self.user + "@" + self.host + \
                  ' "mkdir -p ' + self.path + "/" + self.expid + '/analysis_scripts; cd ' + \
                  self.path + "/" + self.expid + '/analysis_scripts; bash -sl" < ' + \
                  os.path.realpath(script) 
        # print command
        if args is not None:
            sendargs = [self.path+"/"+self.expid+"/"+args[a].replace("@EXPID@", self.expid) if needs_exp else args for a in range(len(args))]
            command = command + " " + " ".join(sendargs)
        os.system(command)

    @classmethod
    def update_file(meth, *args):
        pass


class cosmos_standard_analysis(_cosmos_simulation):
    """
    docstring
    """

    # def __init__(self, path):
    #     _cosmos_simulation.__init__(self, path)
    #     self.suffix = ""

    def _check_mpiom(self, varname):
        component = get_model_component_from_varname(varname)
        # print component
        if "mpiom" in component:
            self.suffix = "_remap.nc"
            return True
        else:
            self.suffix = ".nc"
            return False

    def _time_analysis(self, varname, time_operator, sfc=False):
        mpiom_var = self._check_mpiom(varname)
        component = get_model_component_from_varname(varname)
        # What would this file be called on the remote host?
        # print self.suffix
        if sfc and "_sfc.nc" not in self.suffix:
            self.suffix = self.suffix.replace(".nc", "_sfc.nc")
        # print self.suffix
        rfile = self.path + "/" + self.expid + "/post/" + component.split("_")[0] + "/" + self.expid + "_" + component + "_" + varname + "_" + time_operator + self.suffix

        # What would this file be called locally?
        lfile = rfile.replace(custom_io_constants.replace_path_dict[self.host],
                              custom_io_constants.local_experiment_storehouse)
        # Try to load from local first:
        if os.path.exists(lfile):
            if mpiom_var:
                fix_mpiom_levels(lfile)
            return netcdf.netcdf_file(lfile)
        # Otherwise, make and load:
        else:
            # Make
            # print("Making file!")
            self._deploy_script(self._script_dir +
                                "/ANALYSIS_make_" + time_operator + ".sh " + varname, None)
            if sfc and "_sfc.nc" not in self.suffix:
                self._deploy_script(self._script_dir +
                                    "/ANALYSIS_select_sfc.sh "+rfile.replace("_sfc", ""), None)
                rfile = rfile.replace(".nc", "_sfc.nc")
            # print("Done!")
            # Load
            # print(rfile)
            return netcdf.netcdf_file(get_remote_data(self.user+"@"+self.host+":"+rfile, copy_to_local=True))

    # Start of standard time dependence analysis (monmean, seasmean, etc)
    def monmean(self, varname, sfc=False):
        header("Doing monmean of %s for %s" % (self.expid, varname))
        return self._time_analysis(varname, "monmean", sfc)

    def seasmean(self, varname, sfc=False):
        header("Doing seasmean of %s for %s" % (self.expid, varname))
        return self._time_analysis(varname, "seasmean", sfc)

    def yearmean(self, varname, sfc=False):
        header("Doing yearmean of %s for %s" % (self.expid, varname))
        return self._time_analysis(varname, "yearmean", sfc)

    def timmean(self, varname, sfc=False):
        header("Doing timmean of %s for %s" % (self.expid, varname))
        return self._time_analysis(varname, "timmean", sfc)

    def ymonmean(self, varname, sfc=False):
        header("Doing ymonmean of %s for %s" % (self.expid, varname))
        return self._time_analysis(varname, "ymonmean", sfc)

    def yseasmean(self, varname, sfc=False):
        header("Doing yseasmean of %s for %s" % (self.expid, varname))
        return self._time_analysis(varname, "yseasmean", sfc)
    # End of standard analysis toolkit

    # extras:
    def AMOC_spatial_timmean(self):
        self._deploy_script(self._script_dir + "/ANALYSIS_make_amoc.sh ", None)
        return netcdf.netcdf_file(get_remote_data(self.fullpath + "/post/mpiom/" + self.expid + "_mpiom_MOC_complete_180x40_Sv_timmean.nc",
                                                  copy_to_local=True))

    def AMOC_timeseries_45N(self):
        self._deploy_script(self._script_dir + "/ANALYSIS_make_amoc.sh ", None)
        return netcdf.netcdf_file(get_remote_data(self.fullpath + "/post/mpiom/" + self.expid + "_mpiom_MOC_complete_180x40_Sv_index_45-60N.nc",
                                                  copy_to_local=True))

    def insolation(self):
        self._deploy_script(self._script_dir + "/ANALYSIS_insolation.sh", None)
        return netcdf.netcdf_file(get_remote_data(self.fullpath + "/post/echam5/" + self.expid + "_echam5_main_srad0d_ymonmean_zonmean.nc",
                                                  copy_to_local=True))


class cosmos_wiso_analysis(cosmos_standard_analysis):
    """
    docstring
    """
    def _check_wiso(self, varname):
        if varname in lists.echam5_wiso_list + lists.mpiom_wiso_list:
            return True
        else:
            return False

    def _wiso_analysis(self, varname, time_operator, sfc=False):
        component = get_model_component_from_varname(varname)
        debug(component)
        mpiom_var = self._check_mpiom(varname)
        if sfc:
            self.suffix = self.suffix.replace(".nc", "_sfc.nc")
        rfile = self.path + "/" + self.expid + "/post/" + component.split("_")[0] + "/" + self.expid + "_" + component + "_" + varname + "_" + time_operator + self.suffix
        # print(rfile)
        lfile = rfile.replace(custom_io_constants.replace_path_dict[self.host],
                              custom_io_constants.local_experiment_storehouse)
        debug(lfile)
        if os.path.exists(lfile):
            if mpiom_var:
                fix_mpiom_levels(lfile)
            return netcdf.netcdf_file(lfile)
        else:
            debug("In first else")
            if mpiom_var:
                debug("in mpiom_var")
                if varname is "delta18Osw":
                    self._deploy_script(self._script_dir+"/ANALYSIS_calc_wiso_mpiom_delta18O_"+time_operator+".sh", None)
                    if sfc:
                        self._deploy_script(self._script_dir + "/ANALYSIS_select_sfc.sh "+rfile.replace("_sfc", ""), None)
                        rfile.replace(".nc", "_sfc.nc")
                if varname is "delta18Oc":
                    self._deploy_script(self._script_dir+"/ANALYSIS_calc_wiso_mpiom_calcite_"+time_operator+".sh", None)
                    if sfc:
                        self._deploy_script(self._script_dir + "/ANALYSIS_select_sfc.sh "+rfile.replace("_sfc", ""), None)
                        rfile.replace(".nc", "_sfc.nc")
                if varname is "delta18Oshackleton":
                    self._deploy_script(self._script_dir+"/ANALYSIS_calc_wiso_mpiom_shakleton_"+time_operator+".sh", None)
                    if sfc:
                        self._deploy_script(self._script_dir + "/ANALYSIS_select_sfc.sh "+rfile.replace("_sfc", ""), None)
                        rfile.replace(".nc", "_sfc.nc")

                else:
                    self._time_analysis(varname, time_operator, sfc=sfc)
                # print(("PG:", self.user+"@"+self.host+":"+rfile))
                return netcdf.netcdf_file(get_remote_data(self.user+"@"+self.host+":"+rfile, copy_to_local=True))
            else:
                debug ("Standard analysis for echam")
                # some other code that does the appropriate echam analysis
                self._deploy_script(self._script_dir+"/ANALYSIS_calc_wiso_echam5_"+time_operator+".sh "+varname, None)
                return netcdf.netcdf_file(get_remote_data(self.user+"@"+self.host+":"+rfile, copy_to_local=True))

    def monmean(self, varname, sfc=False):
        header("Doing monmean of %s for %s" % (self.expid, varname))
        if self._check_wiso(varname):
            return self._wiso_analysis(varname, "monmean", sfc)
        else:
            return self._time_analysis(varname, "monmean", sfc)

    def seasmean(self, varname, sfc=False):
        header("Doing seasmean of %s for %s" % (self.expid, varname))
        if self._check_wiso(varname):
            return self._wiso_analysis(varname, "seasmean", sfc)
        else:
            return self._time_analysis(varname, "seasmean", sfc)

    def yearmean(self, varname, sfc=False):
        header("Doing yearmean of %s for %s" % (self.expid, varname))
        if self._check_wiso(varname):
            return self._wiso_analysis(varname, "yearmean", sfc)
        else:       
            return self._time_analysis(varname, "yearmean", sfc)

    def timmean(self, varname, sfc=False):
        header("Doing timmean of %s for %s" % (self.expid, varname))
        if self._check_wiso(varname):
            return self._wiso_analysis(varname, "timmean", sfc)
        else:       
            return self._time_analysis(varname, "timmean", sfc)

    def ymonmean(self, varname, sfc=False):
        header("Doing ymonmean of %s for %s" % (self.expid, varname))
        if self._check_wiso(varname):
            return self._wiso_analysis(varname, "ymonmean", sfc)
        else:       
            return self._time_analysis(varname, "ymonmean", sfc)

    def yseasmean(self, varname, sfc=False):
        header("Doing yseasmean of %s for %s" % (self.expid, varname))
        if self._check_wiso(varname):
            return self._wiso_analysis(varname, "yseasmean", sfc)
        else:       
            return self._time_analysis(varname, "yseasmean", sfc)
