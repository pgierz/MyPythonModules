from custom_io import get_remote_data
from parsing_tools import get_model_component_from_varname
import os


class cosmos_simulation(object):
    """
    # TODO I need to write some documentation for this

    Paul J. Gierz, Sat Feb  6 13:37:00 2016
    """
    def __init__(self, path):
        super(cosmos_simulation, self).__init__()
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
        # print command
        os.system(command)

    def analysis_timmean(self, varname):
        component = get_model_component_from_varname(varname)
        # print component
        if "mpiom" in component:
            suffix = "_remap.nc"
        else:
            suffix = ".nc"
        self._deploy_script(self._script_dir+"/ANALYSIS_make_timmean.sh "+varname, None)
        # print self.fullpath+"/post/"+component+"/"+self.expid+"_"+component+"_"+varname+"_timmean"+suffix
        data = get_remote_data(self.fullpath+"/post/"+component.split("_")[0]+"/"+self.expid+"_"+component+"_"+varname+"_timmean"+suffix,
                               copy_to_local=True)
        return data

    def analysis_yearmean(self, varname):
        component = get_model_component_from_varname(varname)
        # print component
        if "mpiom" in component:
            suffix = "_remap.nc"
        else:
            suffix = ".nc"
        self._deploy_script(self._script_dir+"/ANALYSIS_make_yearmean.sh "+varname, None)
        # print self.fullpath+"/post/"+component+"/"+self.expid+"_"+component+"_"+varname+"_yearmean"+suffix
        data = get_remote_data(self.fullpath+"/post/"+component.split("_")[0]+"/"+self.expid+"_"+component+"_"+varname+"_yearmean"+suffix,
                               copy_to_local=True)
        return data

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
                               copy_to_local=True)
        return data

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
                               copy_to_local=True)
        return data

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
                               copy_to_local=True)
        return data
