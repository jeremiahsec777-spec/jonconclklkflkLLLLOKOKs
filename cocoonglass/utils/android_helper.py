from kivy.utils import platform
from kivy.logger import Logger

if platform == 'android':
    from jnius import autoclass, cast
    from android.permissions import request_permissions, Permission

    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Settings = autoclass('android.provider.Settings')
    Uri = autoclass('android.net.Uri')
    Context = autoclass('android.content.Context')
    PowerManager = autoclass('android.os.PowerManager')

class AndroidHelper:
    @staticmethod
    def request_miui_permissions():
        if platform != 'android':
            Logger.info("AndroidHelper: Not on Android, skipping permissions")
            return

        # Request basic recording permissions
        request_permissions([Permission.RECORD_AUDIO, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

    @staticmethod
    def disable_battery_optimization():
        if platform != 'android': return

        activity = PythonActivity.mActivity
        package_name = activity.getPackageName()
        pm = cast(PowerManager, activity.getSystemService(Context.POWER_SERVICE))

        if not pm.isIgnoringBatteryOptimizations(package_name):
            intent = Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)
            intent.setData(Uri.parse(f"package:{package_name}"))
            activity.startActivity(intent)

    @staticmethod
    def start_foreground_service():
        if platform != 'android': return
        Logger.info("AndroidHelper: Foreground service start requested (Stub)")
        # Implementation would involve starting a Kivy service defined in buildozer.spec
        pass
