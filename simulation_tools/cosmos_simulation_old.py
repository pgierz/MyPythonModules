from custom_io import get_remote_data
from scipy.io import netcdf
from parsing_tools import get_model_component_from_varname, valid_components
import os


class cosmos_simulation(object):
    """
    # TODO I need to write some documentation for this

    Paul J. Gierz, Sat Feb  6 13:37:00 2016
    """
    def __init__(self, path, tmp=False):
        super(cosmos_simulation, self).__init__()
        self._script_dir = "/Users/pgierz/Research/scripts/"
        self.fullpath = path
        self.user = path.split(":")[0].split("@")[0]
        self.host = path.split(":")[0].split("@")[1]
        self.path = path.split(":")[1]
        self.expid = path.split(":")[1].split("/")[-1]
        self.tmp = tmp
        if self.tmp:
            self.ctl = False
        else:
            self.ctl = True

    def _deploy_script(self, script, args, needs_exp=False):
        """This private method takes a script given by the arg script and
        deploys it to the remote host to do cdo stuff

        args are EXTRA args to the script that are normally supplied via flags.

        Paul J. Gierz, Sat Feb  6 13:57:51 2016
        """
        sendargs = []
        if needs_exp:
            for a in range(len(args)):
                sendargs.append(self.path + "/" + args[a].replace("@EXPID@", self.expid))
        else:
            sendargs = args

        # If script is link, expand to the real thing:
        if args is not None:
            command = 'ssh ' + self.user + "@" + self.host + ' "mkdir -p ' + self.path + '/analysis_scripts; cd ' + \
                      self.path + '/analysis_scripts; bash -sl" < ' + \
                      os.path.realpath(script) + " " + " ".join(sendargs)
        else:
            command = 'ssh ' + self.user + "@" + self.host + ' "mkdir -p ' + self.path + '/analysis_scripts; cd ' + \
                      self.path + '/analysis_scripts; bash -sl" < ' + \
                      os.path.realpath(script)    
        os.system(command)

    def analysis_timmean(self, varname, sfc=False):
        component = get_model_component_from_varname(varname)
        # print component
        if "mpiom" in component:
            suffix = "_remap.nc"
        else:
            suffix = ".nc"
        self._deploy_script(self._script_dir+"/ANALYSIS_make_timmean.sh "+varname, None)
        # print self.fullpath+"/post/"+component+"/"+self.expid+"_"+component+"_"+varname+"_timmean"+suffix
        if sfc and "mpiom" in component:
            self._deploy_script(self._script_dir+"/ANALYSIS_select_sfc.sh timmean "+varname+" "+component, None)
            suffix = suffix.replace(".nc", "_sfc.nc")
        data = get_remote_data(self.fullpath+"/post/"+component.split("_")[0]+"/"+self.expid+"_"+component+"_"+varname+"_timmean"+suffix,
                               copy_to_local=self.ctl)
        return netcdf.netcdf_file(data)

    def analysis_AMOC_spatial(self):
        self._deploy_script(self._script_dir+"/ANALYSIS_make_amoc.sh ", None)
        # print self.fullpath+"/post/"+component+"/"+self.expid+"_"+component+"_"+varname+"_timmean"+suffix
        data = get_remote_data(self.fullpath+"/post/mpiom/"+self.expid+"_mpiom_MOC_complete_180x40_Sv_timmean.nc",
                               copy_to_local=self.ctl)
        return netcdf.netcdf_file(data)
    
    def analysis_yearmean(self, varname):
        component = get_model_component_from_varname(varname)
        # print component
        if "mpiom" in component:
            suffix = "_remap.nc"
        else:
            suffix = ".nc"
        if "wiso" in component:
            raise Exception("Please use method wiso_yearmean_echam5 or wiso_yearmean_mpiom instead!")
        self._deploy_script(self._script_dir+"/ANALYSIS_make_yearmean.sh "+varname, None)
        # print self.fullpath+"/post/"+component+"/"+self.expid+"_"+component+"_"+varname+"_yearmean"+suffix
        data = get_remote_data(self.fullpath+"/post/"+component.split("_")[0]+"/"+self.expid+"_"+component+"_"+varname+"_yearmean"+suffix,
                               copy_to_local=self.ctl)
        return netcdf.netcdf_file(data)

    def analysis_ymonmean(self, varname):
        component = get_model_component_from_varname(varname)
        # print component
        if "mpiom" in component:
            suffix = "_remap.nc"
        else:
            suffix = ".nc"
        self._deploy_script(self._script_dir+"/ANALYSIS_make_ymonmean.sh "+varname, None)
        # print self.fullpath+"/post/"+component+"/"+self.expid+"_"+component+"_"+varname+"_ymonmean"+suffix
        data = get_remote_data(self.fullpath+"/post/"+component.split("_")[0]+"/"+self.expid+"_"+component+"_"+varname+"_ymonmean"+suffix,
                               copy_to_local=self.ctl)
        return netcdf.netcdf_file(data)

    def analysis_yseasmean(self, varname):
        component = get_model_component_from_varname(varname)
        # print component
        if "mpiom" in component:
            suffix = "_remap.nc"
        else:
            suffix = ".nc"
        self._deploy_script(self._script_dir+"/ANALYSIS_make_yseasmean.sh "+varname, None)
        # print self.fullpath+"/post/"+component+"/"+self.expid+"_"+component+"_"+varname+"_yseasmean"+suffix
        data = get_remote_data(self.fullpath+"/post/"+component.split("_")[0]+"/"+self.expid+"_"+component+"_"+varname+"_yseasmean"+suffix,
                               copy_to_local=self.ctl)
        return netcdf.netcdf_file(data)

    def analysis_seasmean(self, varname):
        component = get_model_component_from_varname(varname)
        # print component
        if "mpiom" in component:
            suffix = "_remap.nc"
        else:
            suffix = ".nc"
        self._deploy_script(self._script_dir+"/ANALYSIS_make_seasmean.sh "+varname, None)
        # print self.fullpath+"/post/"+component+"/"+self.expid+"_"+component+"_"+varname+"_seasmean"+suffix
        data = get_remote_data(self.fullpath+"/post/"+component.split("_")[0]+"/"+self.expid+"_"+component+"_"+varname+"_seasmean"+suffix,
                               copy_to_local=self.ctl)
        return netcdf.netcdf_file(data)

    def analysis_insolation(self):
        self._deploy_script(self._script_dir+"/ANALYSIS_insolation.sh", None)
        data = get_remote_data(self.fullpath+"/post/echam5/"+self.expid+"_echam5_main_srad0d_ymonmean_zonmean.nc",
                               copy_to_local=self.ctl)
        return netcdf.netcdf_file(data)
                               
    def _make_wiso_yearmean_echam5(self):
        self._deploy_script(self._script_dir+"/ANALYSIS_calc_wiso_yearmean.sh", None)

    def _make_wiso_ymonmean_mpiom(self):
        self._deploy_script(self._script_dir+"/ANALYSIS_calc_wiso_mpiom_delta18O_ymonmean.sh", None)

    def wiso_yearmean_echam5(self, varname):
        self._make_wiso_yearmean_echam5(self)
        if get_model_component_from_varname(varname) is not "echam5_wiso":
            raise Exception(varname+" is not a echam5_wiso variable!")
        self._deploy_script(self._script_dir+"/WISO_select_yearmean_echam5.sh", varname)
        data = get_remote_data(self.fullpath+"/post/echam5/"+self.expid+"_echam5_wiso_"+varname+"_yearmean.nc",
                               copy_to_local=self.ctl)
        return netcdf.netcdf_file(data)

    def _make_wiso_timmean_echam5(self):
        self._deploy_script(self._script_dir+"/ANALYSIS_calc_wiso_timmean.sh", None)

    def wiso_timmean_echam5(self, varname):
        if get_model_component_from_varname(varname) is not "echam5_wiso":
            raise Exception(varname+" is not a echam5_wiso variable!")
        self._make_wiso_timmean_echam5()
        self._deploy_script(self._script_dir+"/WISO_select_timmean_echam5.sh "+varname, None)
        data = get_remote_data(self.fullpath+"/post/echam5/"+self.expid+"_echam5_wiso_"+varname+"_timmean.nc",
                               copy_to_local=self.ctl)
        return netcdf.netcdf_file(data)

    def wiso_ymonmean_mpiom(self):
        self._make_wiso_ymonmean_mpiom()
        data = get_remote_data(self.fullpath+"/post/mpiom/"+self.expid+"_mpiom_wiso_delta18O_ymonmean_remap.nc",
                               copy_to_local=self.ctl)
        return netcdf.netcdf_file(data)

    def wiso_ymonmean_mpiom_sfc(self):
        self._make_wiso_ymonmean_mpiom()
        data = get_remote_data(self.fullpath+"/post/mpiom/"+self.expid+"_mpiom_wiso_delta18O_lev6_ymonmean_remap.nc",
                               copy_to_local=self.ctl)
        return netcdf.netcdf_file(data)
