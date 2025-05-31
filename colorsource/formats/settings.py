from dataclasses import dataclass
from typing import List, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Settings:
    art_net_universe_mapping: List[int]
    auto_select_channels: bool
    button_brightness: int
    default_cue_time: int
    default_move_dark_time: int
    default_move_time: int
    display_backlight: int
    dmx_speed: int
    external_monitor: bool
    fader_functions: List[str]
    language: str
    operating_mode: int
    rdm_enable: bool
    rubberband_mode: bool
    s_acn_priority: int
    s_acn_universe_mapping: List[int]
    show_stage_map_zones: bool
    sneak_time: int
    soft_button_functions: List[str]
    software_version: str
    user_passcode: str
    video_mode: str

    @staticmethod
    def from_dict(obj: Any) -> "Settings":
        assert isinstance(obj, dict)
        art_net_universe_mapping = from_list(from_int, obj.get("artNetUniverseMapping"))
        auto_select_channels = from_bool(obj.get("autoSelectChannels"))
        button_brightness = from_int(obj.get("buttonBrightness"))
        default_cue_time = from_int(obj.get("defaultCueTime"))
        default_move_dark_time = from_int(obj.get("defaultMoveDarkTime"))
        default_move_time = from_int(obj.get("defaultMoveTime"))
        display_backlight = from_int(obj.get("displayBacklight"))
        dmx_speed = from_int(obj.get("dmxSpeed"))
        external_monitor = from_bool(obj.get("externalMonitor"))
        fader_functions = from_list(from_str, obj.get("faderFunctions"))
        language = from_str(obj.get("language"))
        operating_mode = from_int(obj.get("operatingMode"))
        rdm_enable = from_bool(obj.get("rdmEnable"))
        rubberband_mode = from_bool(obj.get("rubberbandMode"))
        s_acn_priority = from_int(obj.get("sACNPriority"))
        s_acn_universe_mapping = from_list(from_int, obj.get("sAcnUniverseMapping"))
        show_stage_map_zones = from_bool(obj.get("showStageMapZones"))
        sneak_time = from_int(obj.get("sneakTime"))
        soft_button_functions = from_list(from_str, obj.get("softButtonFunctions"))
        software_version = from_str(obj.get("softwareVersion"))
        user_passcode = from_str(obj.get("userPasscode"))
        video_mode = from_str(obj.get("videoMode"))
        return Settings(
            art_net_universe_mapping,
            auto_select_channels,
            button_brightness,
            default_cue_time,
            default_move_dark_time,
            default_move_time,
            display_backlight,
            dmx_speed,
            external_monitor,
            fader_functions,
            language,
            operating_mode,
            rdm_enable,
            rubberband_mode,
            s_acn_priority,
            s_acn_universe_mapping,
            show_stage_map_zones,
            sneak_time,
            soft_button_functions,
            software_version,
            user_passcode,
            video_mode,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["artNetUniverseMapping"] = from_list(
            from_int, self.art_net_universe_mapping
        )
        result["autoSelectChannels"] = from_bool(self.auto_select_channels)
        result["buttonBrightness"] = from_int(self.button_brightness)
        result["defaultCueTime"] = from_int(self.default_cue_time)
        result["defaultMoveDarkTime"] = from_int(self.default_move_dark_time)
        result["defaultMoveTime"] = from_int(self.default_move_time)
        result["displayBacklight"] = from_int(self.display_backlight)
        result["dmxSpeed"] = from_int(self.dmx_speed)
        result["externalMonitor"] = from_bool(self.external_monitor)
        result["faderFunctions"] = from_list(from_str, self.fader_functions)
        result["language"] = from_str(self.language)
        result["operatingMode"] = from_int(self.operating_mode)
        result["rdmEnable"] = from_bool(self.rdm_enable)
        result["rubberbandMode"] = from_bool(self.rubberband_mode)
        result["sACNPriority"] = from_int(self.s_acn_priority)
        result["sAcnUniverseMapping"] = from_list(from_int, self.s_acn_universe_mapping)
        result["showStageMapZones"] = from_bool(self.show_stage_map_zones)
        result["sneakTime"] = from_int(self.sneak_time)
        result["softButtonFunctions"] = from_list(from_str, self.soft_button_functions)
        result["softwareVersion"] = from_str(self.software_version)
        result["userPasscode"] = from_str(self.user_passcode)
        result["videoMode"] = from_str(self.video_mode)
        return result


def settings_from_dict(s: Any) -> Settings:
    return Settings.from_dict(s)


def settings_to_dict(x: Settings) -> Any:
    return to_class(Settings, x)
