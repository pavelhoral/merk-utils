# ------------------------------------------------------------------
#
# PROJECT REALITY SERVER INIT
#
# This file can be edited by any server (public or private).
#

# Import namehack module - initialize before realityinit!
import bf2.namehack
bf2.namehack.init()

import realityinit

realityinit.init(False)  # Switch to True if using debugger executables (PRLauncher.exe will automatically modify this value accordingly)

# ------------------------------------------------------------------
# Add your custom script's initilization bellow

