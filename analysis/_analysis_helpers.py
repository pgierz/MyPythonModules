#!/usr/bin/python
"""
    _analysis_helpers.py
Lives: /Users/pgierz/Code/MyPythonModules/analysis/_analysis_helpers.py

contains some helper functions for the python based analysis routines

Paul J. Gierz Sun Jul 19 20:06:23 2015
"""
# Local Variables:
# number_of_prints: 0
# End:
import Pyro4
import os
import sys
import socket




def _set_up_host_connection(host):
    # set up remote daemon
    # Commands that need to be run:
    # $ python ~/Code/MyPythonModules/analysis/Remote_Functions_server.py
    daemon = some_command_that_starts_daemon(host)
    ns = 




def _exec_function_on_remote_host(host, fn, **kwargs):
    rapply = _set_up_host_connection( host ) # Set up a connection
    result = rapply( fn, args, kwargs ) # Remotely call the function
    assert result == fn( *args, **kwargs ) #Just as a test, verify that it has the expected value.




def _find_on_all_hosts(RUN):
    for host in [line.strip() for line in open(os.path.expanduser("/Users/pgierz/Research/.searchable_hosts.dat"), 'r') if "#" not in line]:
        user, host =  host.split(":")[0].split("@")[:]
        


class Remote_Functions(object):
    def evaluate(self, func, args):
        return self.func(*args)

    def square(self, x):
        return x**2


    def _find_full_run_path(self, RUN):
        import os
        import sys
        import socket
        # If we only give an expid, we need to see where that run might be located:
        if "/" not in RUN:
            expid = RUN
        else:
            expid = RUN.split("/")[-1]
        # Look for local .all_runs file:
        if os.path.exists(os.path.expanduser("~/.all_runs.dat")):
            exps = [line.strip() for line in open(os.path.expanduser("~/.all_runs.dat"), 'r') if "#" not in line]
            list1 = exps
            list2 = [s for s in exps if expid in s]
            if any(expid in s for s in exps):
                path = exps[exps.index(*[s for s in exps if expid in s])]
                return path
            else:
                print "ERROR: Couldn't find ", expid, " on",  socket.gethostname()
                return "remote_trigger"
        else:
            print "ERROR: Couldn't find $HOME/.all_runs on ", socket.gethostname()
            return "fail_trigger"

def main():
    server = Remote_Functions()
    Pyro4.Daemon.serverSimple(
        {
            server: "server"
        },
        ns=True)

if __name__ == '__main__':
    main()
    
