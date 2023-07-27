from datetime import datetime
import os
import urllib
import zlib
import requests
from tool import ToolUtil
from flask import Response
from .setup import *

try:
    if os.path.exists(os.path.join(os.path.dirname(__file__), "souce_nsports_handler.py")):
        from .souce_nsports_handler import NSPORTS_Handler

    else:
        from support import SupportSC

        NSPORTS_Handler = SupportSC.load_module_f(__file__, "souce_nsports_handler").NSPORTS_Handler
except:
    pass


class ModuleMain(PluginModuleBase):
    def __init__(self, P):
        super(ModuleMain, self).__init__(P, name="main", first_menu="setting", scheduler_desc="네이버스포츠")
        self.db_default = {
            f"{self.name}_db_version": "1",
            f"{self.name}_auto_start": "False",
            f"{self.name}_interval": "5",
            "plex_server_url": "http://localhost:32400",
            "plex_token": "",
            "plex_meta_item": "",
            "yaml_path": "",
            "use_sports": "True",
            "use_esports": "False",
            "use_quality": "1920x1080",
            "streaming_type": "redirect",
        }

    def process_menu(self, sub, req):
        arg = P.ModelSetting.to_dict()
        arg["api_m3u"] = ToolUtil.make_apikey_url(f"/{P.package_name}/api/m3u")
        arg["api_yaml"] = ToolUtil.make_apikey_url(f"/{P.package_name}/api/yaml")
        if sub == "setting":
            arg["is_include"] = F.scheduler.is_include(self.get_scheduler_name())
            arg["is_running"] = F.scheduler.is_running(self.get_scheduler_name())
        return render_template(f"{P.package_name}_{self.name}_{sub}.html", arg=arg)

    def process_command(self, command, arg1, arg2, arg3, req):
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if command == "broad_list":
            return jsonify({"list": NSPORTS_Handler.ch_list(), "updated_at": updated_at})
        elif command == "schedule_list":
            return jsonify({"list": NSPORTS_Handler.schedule_list(), "updated_at": updated_at})
        elif command == "schedule_esports_list":
            return jsonify({"list": NSPORTS_Handler.schedule_esports_list(), "updated_at": updated_at})
        elif command == "play_url":
            url = ToolUtil.make_apikey_url(f"/{P.package_name}/api/url.m3u8?ch_id={arg1}")
            ret = {"ret": "success", "data": url, "title": arg2}
        return jsonify(ret)

    def process_api(self, sub, req):
        try:
            if sub == "m3u":
                data = NSPORTS_Handler.make_m3u()
                return Response(data, headers={"Content-Type": "text/plain; charset=utf-8"})
            elif sub == "yaml":
                data = NSPORTS_Handler.make_yaml()
                return Response(data, headers={"Content-Type": "text/yaml; charset=utf-8"})
            elif sub == "url.m3u8":
                return NSPORTS_Handler.url_m3u8(req)
            elif sub == "play":
                return NSPORTS_Handler.play(req)
            elif sub == "segment":
                return NSPORTS_Handler.segment(req)

        except Exception as e:
            P.logger.error(f"Exception:{str(e)}")
            P.logger.error(traceback.format_exc())

    def scheduler_function(self):
        try:
            NSPORTS_Handler.sync_yaml_data()
        except Exception as e:
            P.logger.error(f"Exception:{str(e)}")
            P.logger.error(traceback.format_exc())
