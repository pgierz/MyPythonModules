from custom_io import get_remote_data, custom_io_constants
from parsing_tools import get_model_component_from_varname, lists
import os
from scipy.io import netcdf
import cdo

CDO = cdo.Cdo()


def fix_mpiom_levels(fname):
    if CDO.nlevel(input=fname)[0] == "40":
        if not CDO.showlevel(input=fname)[0].split(" ")[0] == "6":
            os.system("cdo invertlev "+fname+" tmp")
            os.system("mv tmp "+fname)

            
class _cosmos_simulation(object):
    """
    # TODO I need to write some documentation for this

    Paul J. Gierz, Sat Feb  6 13:37:00 2016
    """

    def __init__(self, path):
        super(_cosmos_simulation, self).__init__()
        self._script_dir = "/Users/pgierz/Research/scripts/"
        self.fullpath = path
        self.user = path.split(":")[0].split("@")[0]
        self.host = path.split(":")[0].split("@")[1]
        self.path = path.split(":")[1]
        self.expid = path.split(":")[1].split("/")[-1]

    def _deploy_script(self, script, args, needs_exp=False):
        """This private method takes a script given by the arg script and
        deploys it to the remote host to do cdo stuff

        args are EXTRA args to the script that are normally supplied via flags.

        Paul J. Gierz, Sat Feb  6 13:57:51 2016
        """
        sendargs = []
        if needs_exp:
            for a in range(len(args)):
                sendargs.append(self.path + "/" +
                                args[a].replace("@EXPID@", self.expid))
        else:
            sendargs = args

        # If script is link, expand to the real thing:
        if args is not None:
            command = 'ssh ' + self.user + "@" + self.host + \
                      ' "mkdir -p ' + self.path + '/analysis_scripts; cd ' + \
                      self.path + '/analysis_scripts; bash -sl" < ' + \
                      os.path.realpath(script) + " " + " ".join(sendargs)
        else:
            command = 'ssh ' + self.user + "@" + self.host + \
                      ' "mkdir -p ' + self.path + '/analysis_scripts; cd ' + \
                      self.path + '/analysis_scripts; bash -sl" < ' + \
                      os.path.realpath(script)
        os.system(command)


class cosmos_standard_analysis(_cosmos_simulation):
    """
    docstring
    """

    def __init__(self, path):
        _cosmos_simulation.__init__(self, path)
        self.suffix = ""

    def _check_mpiom(self, varname):
        component = get_model_component_from_varname(varname)
        # print component
        if "mpiom" in component:
            self.suffix = "_remap.nc"
        else:
            self.suffix = ".nc"
        return True

    def _time_analysis(self, varname, time_operator):
        mpiom_var = self._check_mpiom(varname)
        component = get_model_component_from_varname(varname)
        # What would this file be called on the remote host?
        rfile = self.path + "/post/" + component.split("_")[0] + "/" + self.expid + "_" + component + "_" + varname + "_" + time_operator + self.suffix
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
            self._deploy_script(self._script_dir +
                                "/ANALYSIS_make_" + time_operator + ".sh " + varname, None)
            # Load
            return netcdf.netcdf_file(get_remote_data(self.user+"@"+self.host+":"+rfile, copy_to_local=True))

    # Start of standard time dependence analysis (monmean, seasmean, etc)
    def monmean(self, varname):
        print "Doing monmean of %s for %s" % (self.expid, varname)
        return self._time_analysis(varname, "monmean")

    def seasmean(self, varname):
        print "Doing seasmean of %s for %s" % (self.expid, varname)
        return self._time_analysis(varname, "seasmean")

    def yearmean(self, varname):
        print "Doing yearmean of %s for %s" % (self.expid, varname)
        return self._time_analysis(varname, "yearmean")

    def timmean(self, varname):
        print "Doing timmean of %s for %s" % (self.expid, varname)
        return self._time_analysis(varname, "timmean")

    def ymonmean(self, varname):
        print "Doing ymonmean of %s for %s" % (self.expid, varname)
        return self._time_analysis(varname, "ymonmean")

    def yseasmean(self, varname):
        print "Doing yseasmean of %s for %s" % (self.expid, varname)
        return self._time_analysis(varname, "yseasmean")
    # End of standard analysis toolkit

    # extras:
    def AMOC_spatial_timmean(self):
        self._deploy_script(self._script_dir + "/ANALYSIS_make_amoc.sh ", None)
        return netcdf.netcdf_file(get_remote_data(self.fullpath + "/post/mpiom/" + self.expid + "_mpiom_MOC_complete_180x40_Sv_timmean.nc",
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

    def _wiso_analysis(self, varname, time_operator):
        component = get_model_component_from_varname(varname)
        mpiom_var = self._check_mpiom(varname)
        rfile = self.path + "/post/" + component.split("_")[0] + "/" + self.expid + "_" + component + "_" + varname + "_" + time_operator + self.suffix
        lfile = rfile.replace(custom_io_constants.replace_path_dict[self.host],
                              custom_io_constants.local_experiment_storehouse)
        if os.path.exists(lfile):
            if mpiom_var:
                fix_mpiom_levels(lfile)
            return netcdf.netcdf_file(lfile)
        else:
            if mpiom_var:
                if varname is "delta18Osw":
                    self._deploy_script(self._script_dir+"/ANALYSIS_calc_wiso_mpiom_delta18O_"+time_operator+".sh", None)
                else:
                    self._time_analysis(varname, time_operator)
                return netcdf.netcdf_file(get_remote_data(self.user+"@"+self.host+":"+rfile, copy_to_local=True))
            else:
                # Some other code that does the appropriate echam analysis
                self._deploy_script(self._script_dir+"/ANALYSIS_calc_wiso_echam5_"+time_operator+".sh "+varname, None)
                return netcdf.netcdf_file(get_remote_data(self.user+"@"+self.host+":"+rfile, copy_to_local=True))

    def monmean(self, varname):
        print "Doing monmean of %s for %s" % (self.expid, varname)
        if self._check_wiso(varname):
            return self._wiso_analysis(varname, "monmean")
        else:
            return self._time_analysis(varname, "monmean")

    def seasmean(self, varname):
        print "Doing seasmean of %s for %s" % (self.expid, varname)
        if self._check_wiso(varname):
            return self._wiso_analysis(varname, "seasmean")
        else:
            return self._time_analysis(varname, "seasmean")

    def yearmean(self, varname):
        print "Doing yearmean of %s for %s" % (self.expid, varname)
        if self._check_wiso(varname):
            return self._wiso_analysis(varname, "yearmean")
        else:       
            return self._time_analysis(varname, "yearmean")

    def timmean(self, varname):
        print "Doing timmean of %s for %s" % (self.expid, varname)
        if self._check_wiso(varname):
            return self._wiso_analysis(varname, "timmean")
        else:       
            return self._time_analysis(varname, "timmean")

    def ymonmean(self, varname):
        print "Doing ymonmean of %s for %s" % (self.expid, varname)
        if self._check_wiso(varname):
            return self._wiso_analysis(varname, "ymonmean")
        else:       
            return self._time_analysis(varname, "ymonmean")

    def yseasmean(self, varname):
        print "Doing yseasmean of %s for %s" % (self.expid, varname)
        if self._check_wiso(varname):
            return self._wiso_analysis(varname, "yseasmean")
        else:       
            return self._time_analysis(varname, "yseasmean")
