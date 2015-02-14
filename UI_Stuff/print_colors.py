class my_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def format_s_in_color(s, c):
    return c+s+my_colors.ENDC

def HEADER(s):
    return format_s_in_color(s, my_colors.HEADER)

def OKBLUE(s):
    return format_s_in_color(s, my_colors.OKBLUE)

def OKGREEN(s):
    return format_s_in_color(s, my_colors.OKGREEN)

def WARNING(s):
    return format_s_in_color(s, my_colors.WARNING)

def FAIL(s):
    return format_s_in_color(s, my_colors.FAIL)


