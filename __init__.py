import os

try:
    import yaml
except:
    os.system("pip install pyyaml")
try:
    import bs4
except:
    os.system("pip install bs4")

# try:
#     if os.path.exists(os.path.join(os.path.dirname(__file__), "souce_nsports_handler.py")):
#         from .souce_nsports_handler import NSPORTS_Handler

#     else:
#         from support import SupportSC

#         NSPORTS_Handler = SupportSC.load_module_f(__file__, "souce_nsports_handler").NSPORTS_Handler
# except:
#     pass

# try:
#     if os.path.exists(os.path.join(os.path.dirname(__file__), "souce_nsports_service.py")):
#         from .souce_nsports_service import NSPORTS_Service
#     else:
#         from support import SupportSC

#         NSPORTS_Service = SupportSC.load_module_f(__file__, "souce_nsports_service").NSPORTS_Service
# except:
#     pass
