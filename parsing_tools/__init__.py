import socket
import os


def get_model_component_from_varname(varname):
    if "REFDIR" in os.environ.keys():
        REFDIR = os.environ["REFDIR"]
    else:
        if socket.gethostname() == "rayo3":
            REFDIR = "/csys/nobackup1_PALEO/pgierz/reference_stuff/"
        elif socket.gethostname() == "uv100":
            REFDIR = "/csys/nobackup1_PALEO/pgierz/reference_stuff/"
        elif socket.gethostname() == "stan1":
            REFDIR = "/home/ace/pgierz/reference_stuff"
        else:
            print "REFDIR not found, recloning..."
            os.system("git clone git@bitbucket.org:pgierz/reference_stuff.git")
            REFDIR = "./reference_stuff/"
    with open(REFDIR + "/echam5_variables.txt", "r") as f:
        echam5_main_varlist = f.readlines()
        for v in echam5_main_varlist:
            echam5_main_varlist[
                echam5_main_varlist.index(v)] = v.strip().split()[1]
    with open(REFDIR + "/echam5_wiso_variables.txt", "r") as f:
        echam5_wiso_varlist = f.readlines()
        for v in echam5_wiso_varlist:
            echam5_wiso_varlist[
                echam5_wiso_varlist.index(v)] = v.strip().split()[1]
    with open(REFDIR + "/mpiom_variables.txt", "r") as f:
        mpiom_main_varlist = f.readlines()
        for v in mpiom_main_varlist:
            mpiom_main_varlist[
                mpiom_main_varlist.index(v)] = v.strip().split()[1]
    with open(REFDIR + "/mpiom_wiso_variables.txt", "r") as f:
        mpiom_wiso_varlist = f.readlines()
        for v in mpiom_wiso_varlist:
            mpiom_wiso_varlist[
                mpiom_wiso_varlist.index(v)] = v.strip().split()[1]
    if varname in echam5_main_varlist:
        return "echam5_main"
    elif varname in echam5_wiso_varlist:
        return "echam5_wiso"
    elif varname in mpiom_main_varlist:
        return "mpiom_main"
    elif varname in mpiom_wiso_varlist:
        return "mpiom_wiso"
    else:
        return None

    
def make_required_data_pick_script(script, scriptargs=None):
    prevdir = os.getcwd()
    os.chdir("/Users/pgierz/Research/Eem_Hol_Wiso/")  # FIXME: See note
    # PG: NOTE This will not be smart if I want to generalize this to
    # multiple projects. Instead I should set a CURRENT_PROJ variable
    # that detects which project I am in based on the current working
    # directory.

    make_command_to_call = script + scriptargs
    os.system(make_command_to_call)
    os.chdir(prevdir)


def make_required_data_yearmean(varname):
    prevdir = os.getcwd()
    os.chdir("/Users/pgierz/Research/Eem_Hol_Wiso/")
    make_command_to_call = "./tools/deploy_script.py scripts/ANALYSIS_make_yearmean.sh "+varname
    os.system(make_command_to_call)
    os.chdir(prevdir)


def load_required_data(varname, exps, expids):
    from custom_io.get_remote_data import get_remote_data
    model_keys = {}
    sim_dict = {}
    for exp, eid in zip(exps, expids):
        mod_component = model_keys[get_model_component_from_varname(varname)]
        if "mpiom" in mod_component:
            remap_suff = "_remap"
        else:
            remap_suff = ""
        sim_dict[eid] = get_remote_data(exp+"/post/"+mod_component.split("_")[1]+"/"+eid+mod_component+varname+"_timmean"+remap_suff+".nc", copy_to_local=True)
     

def get_time_axis_from_netcdf(ncfile):
    ncfile
