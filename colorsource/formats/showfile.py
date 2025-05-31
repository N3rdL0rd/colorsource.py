from dataclasses import dataclass
from typing import List, Any, Optional, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except Exception:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


@dataclass
class Color:
    b: int
    channel: int
    emitters: List[int]
    g: int
    r: int

    @staticmethod
    def from_dict(obj: Any) -> "Color":
        assert isinstance(obj, dict)
        b = from_int(obj.get("b"))
        channel = from_int(obj.get("channel"))
        emitters = from_list(from_int, obj.get("emitters"))
        g = from_int(obj.get("g"))
        r = from_int(obj.get("r"))
        return Color(b, channel, emitters, g, r)

    def to_dict(self) -> dict:
        result: dict = {}
        result["b"] = from_int(self.b)
        result["channel"] = from_int(self.channel)
        result["emitters"] = from_list(from_int, self.emitters)
        result["g"] = from_int(self.g)
        result["r"] = from_int(self.r)
        return result


@dataclass
class Palette:
    display_color: str
    ltp_parameters: List[Any]
    palette: int
    text: str
    colors: Optional[List[Color]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Palette":
        assert isinstance(obj, dict)
        display_color = from_str(obj.get("displayColor"))
        ltp_parameters = from_list(lambda x: x, obj.get("ltpParameters"))
        palette = from_int(obj.get("palette"))
        text = from_str(obj.get("text"))
        colors = from_union(
            [lambda x: from_list(Color.from_dict, x), from_none], obj.get("colors")
        )
        return Palette(display_color, ltp_parameters, palette, text, colors)

    def to_dict(self) -> dict:
        result: dict = {}
        result["displayColor"] = from_str(self.display_color)
        result["ltpParameters"] = from_list(lambda x: x, self.ltp_parameters)
        result["palette"] = from_int(self.palette)
        result["text"] = from_str(self.text)
        if self.colors is not None:
            result["colors"] = from_union(
                [lambda x: from_list(lambda x: to_class(Color, x), x), from_none],
                self.colors,
            )
        return result


@dataclass
class Level:
    b: int
    channel: int
    colors: List[int]
    g: int
    level: int
    r: int

    @staticmethod
    def from_dict(obj: Any) -> "Level":
        assert isinstance(obj, dict)
        b = from_int(obj.get("b"))
        channel = from_int(obj.get("channel"))
        colors = from_list(from_int, obj.get("colors"))
        g = from_int(obj.get("g"))
        level = from_int(obj.get("level"))
        r = from_int(obj.get("r"))
        return Level(b, channel, colors, g, level, r)

    def to_dict(self) -> dict:
        result: dict = {}
        result["b"] = from_int(self.b)
        result["channel"] = from_int(self.channel)
        result["colors"] = from_list(from_int, self.colors)
        result["g"] = from_int(self.g)
        result["level"] = from_int(self.level)
        result["r"] = from_int(self.r)
        return result


@dataclass
class LtpParameter:
    channel: int
    is16_bit: bool
    palette: int
    parameter: int
    value: int

    @staticmethod
    def from_dict(obj: Any) -> "LtpParameter":
        assert isinstance(obj, dict)
        channel = from_int(obj.get("channel"))
        is16_bit = from_bool(obj.get("is16Bit"))
        palette = from_int(obj.get("palette"))
        parameter = from_int(obj.get("parameter"))
        value = from_int(obj.get("value"))
        return LtpParameter(channel, is16_bit, palette, parameter, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["channel"] = from_int(self.channel)
        result["is16Bit"] = from_bool(self.is16_bit)
        result["palette"] = from_int(self.palette)
        result["parameter"] = from_int(self.parameter)
        result["value"] = from_int(self.value)
        return result


@dataclass
class Content:
    assigned_ranges: List[Any]
    include_flags: int
    levels: List[Level]
    ltp_parameters: List[LtpParameter]

    @staticmethod
    def from_dict(obj: Any) -> "Content":
        assert isinstance(obj, dict)
        assigned_ranges = from_list(lambda x: x, obj.get("assignedRanges"))
        include_flags = from_int(obj.get("includeFlags"))
        levels = from_list(Level.from_dict, obj.get("levels"))
        ltp_parameters = from_list(LtpParameter.from_dict, obj.get("ltpParameters"))
        return Content(assigned_ranges, include_flags, levels, ltp_parameters)

    def to_dict(self) -> dict:
        result: dict = {}
        result["assignedRanges"] = from_list(lambda x: x, self.assigned_ranges)
        result["includeFlags"] = from_int(self.include_flags)
        result["levels"] = from_list(lambda x: to_class(Level, x), self.levels)
        result["ltpParameters"] = from_list(
            lambda x: to_class(LtpParameter, x), self.ltp_parameters
        )
        return result


@dataclass
class Step:
    content: Content
    cue: int
    down_time: int
    flag: bool
    text: str
    up_time: int
    wait_time: int

    @staticmethod
    def from_dict(obj: Any) -> "Step":
        assert isinstance(obj, dict)
        content = Content.from_dict(obj.get("content"))
        cue = from_int(obj.get("cue"))
        down_time = from_int(obj.get("downTime"))
        flag = from_bool(obj.get("flag"))
        text = from_str(obj.get("text"))
        up_time = from_int(obj.get("upTime"))
        wait_time = from_int(obj.get("waitTime"))
        return Step(content, cue, down_time, flag, text, up_time, wait_time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["content"] = to_class(Content, self.content)
        result["cue"] = from_int(self.cue)
        result["downTime"] = from_int(self.down_time)
        result["flag"] = from_bool(self.flag)
        result["text"] = from_str(self.text)
        result["upTime"] = from_int(self.up_time)
        result["waitTime"] = from_int(self.wait_time)
        return result


@dataclass
class CueList:
    col_text0: str
    col_text1: str
    col_text2: str
    col_text3: str
    col_text4: str
    col_text5: str
    steps: List[Step]
    text: str

    @staticmethod
    def from_dict(obj: Any) -> "CueList":
        assert isinstance(obj, dict)
        col_text0 = from_str(obj.get("colText0"))
        col_text1 = from_str(obj.get("colText1"))
        col_text2 = from_str(obj.get("colText2"))
        col_text3 = from_str(obj.get("colText3"))
        col_text4 = from_str(obj.get("colText4"))
        col_text5 = from_str(obj.get("colText5"))
        steps = from_list(Step.from_dict, obj.get("steps"))
        text = from_str(obj.get("text"))
        return CueList(
            col_text0,
            col_text1,
            col_text2,
            col_text3,
            col_text4,
            col_text5,
            steps,
            text,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["colText0"] = from_str(self.col_text0)
        result["colText1"] = from_str(self.col_text1)
        result["colText2"] = from_str(self.col_text2)
        result["colText3"] = from_str(self.col_text3)
        result["colText4"] = from_str(self.col_text4)
        result["colText5"] = from_str(self.col_text5)
        result["steps"] = from_list(lambda x: to_class(Step, x), self.steps)
        result["text"] = from_str(self.text)
        return result


@dataclass
class Independent:
    active: bool
    button_mode: int
    dmx: List[int]
    level: int
    master_mode: int

    @staticmethod
    def from_dict(obj: Any) -> "Independent":
        assert isinstance(obj, dict)
        active = from_bool(obj.get("active"))
        button_mode = from_int(obj.get("buttonMode"))
        dmx = from_list(from_int, obj.get("dmx"))
        level = from_int(obj.get("level"))
        master_mode = from_int(obj.get("masterMode"))
        return Independent(active, button_mode, dmx, level, master_mode)

    def to_dict(self) -> dict:
        result: dict = {}
        result["active"] = from_bool(self.active)
        result["buttonMode"] = from_int(self.button_mode)
        result["dmx"] = from_list(from_int, self.dmx)
        result["level"] = from_int(self.level)
        result["masterMode"] = from_int(self.master_mode)
        return result


@dataclass
class Memory:
    content: Content
    master: int
    memory_page: int
    move_time: int
    text: str

    @staticmethod
    def from_dict(obj: Any) -> "Memory":
        assert isinstance(obj, dict)
        content = Content.from_dict(obj.get("content"))
        master = from_int(obj.get("master"))
        memory_page = from_int(obj.get("memoryPage"))
        move_time = from_int(obj.get("moveTime"))
        text = from_str(obj.get("text"))
        return Memory(content, master, memory_page, move_time, text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["content"] = to_class(Content, self.content)
        result["master"] = from_int(self.master)
        result["memoryPage"] = from_int(self.memory_page)
        result["moveTime"] = from_int(self.move_time)
        result["text"] = from_str(self.text)
        return result


@dataclass
class Page:
    text: str

    @staticmethod
    def from_dict(obj: Any) -> "Page":
        assert isinstance(obj, dict)
        text = from_str(obj.get("text"))
        return Page(text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["text"] = from_str(self.text)
        return result


@dataclass
class Device:
    channel: int
    device_id: int
    dmx: int
    echo_address_range: bool
    echo_zone_only: bool
    footprint: int
    invert_pan: bool
    invert_tilt: bool
    manufacturer: str
    mode: str
    model: str
    personality_dcid: str
    space: int
    swap_pan_tilt: bool
    tag1: int
    tag2: int
    text: str
    zone: int

    @staticmethod
    def from_dict(obj: Any) -> "Device":
        assert isinstance(obj, dict)
        channel = from_int(obj.get("channel"))
        device_id = from_int(obj.get("deviceId"))
        dmx = from_int(obj.get("dmx"))
        echo_address_range = from_bool(obj.get("echoAddressRange"))
        echo_zone_only = from_bool(obj.get("echoZoneOnly"))
        footprint = from_int(obj.get("footprint"))
        invert_pan = from_bool(obj.get("invertPan"))
        invert_tilt = from_bool(obj.get("invertTilt"))
        manufacturer = from_str(obj.get("manufacturer"))
        mode = from_str(obj.get("mode"))
        model = from_str(obj.get("model"))
        personality_dcid = from_str(obj.get("personalityDcid"))
        space = from_int(obj.get("space"))
        swap_pan_tilt = from_bool(obj.get("swapPanTilt"))
        tag1 = from_int(obj.get("tag1"))
        tag2 = from_int(obj.get("tag2"))
        text = from_str(obj.get("text"))
        zone = from_int(obj.get("zone"))
        return Device(
            channel,
            device_id,
            dmx,
            echo_address_range,
            echo_zone_only,
            footprint,
            invert_pan,
            invert_tilt,
            manufacturer,
            mode,
            model,
            personality_dcid,
            space,
            swap_pan_tilt,
            tag1,
            tag2,
            text,
            zone,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["channel"] = from_int(self.channel)
        result["deviceId"] = from_int(self.device_id)
        result["dmx"] = from_int(self.dmx)
        result["echoAddressRange"] = from_bool(self.echo_address_range)
        result["echoZoneOnly"] = from_bool(self.echo_zone_only)
        result["footprint"] = from_int(self.footprint)
        result["invertPan"] = from_bool(self.invert_pan)
        result["invertTilt"] = from_bool(self.invert_tilt)
        result["manufacturer"] = from_str(self.manufacturer)
        result["mode"] = from_str(self.mode)
        result["model"] = from_str(self.model)
        result["personalityDcid"] = from_str(self.personality_dcid)
        result["space"] = from_int(self.space)
        result["swapPanTilt"] = from_bool(self.swap_pan_tilt)
        result["tag1"] = from_int(self.tag1)
        result["tag2"] = from_int(self.tag2)
        result["text"] = from_str(self.text)
        result["zone"] = from_int(self.zone)
        return result


@dataclass
class PatchParameter:
    name: str
    number: int
    type: int

    @staticmethod
    def from_dict(obj: Any) -> "PatchParameter":
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        number = from_int(obj.get("number"))
        type = from_int(obj.get("type"))
        return PatchParameter(name, number, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["number"] = from_int(self.number)
        result["type"] = from_int(self.type)
        return result


@dataclass
class Media:
    pass

    @staticmethod
    def from_dict(obj: Any) -> "Media":
        assert isinstance(obj, dict)
        return Media()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class Range:
    begin: int
    default: int
    end: int
    label: str
    media: Media

    @staticmethod
    def from_dict(obj: Any) -> "Range":
        assert isinstance(obj, dict)
        begin = from_int(obj.get("begin"))
        default = from_int(obj.get("default"))
        end = from_int(obj.get("end"))
        label = from_str(obj.get("label"))
        media = Media.from_dict(obj.get("media"))
        return Range(begin, default, end, label, media)

    def to_dict(self) -> dict:
        result: dict = {}
        result["begin"] = from_int(self.begin)
        result["default"] = from_int(self.default)
        result["end"] = from_int(self.end)
        result["label"] = from_str(self.label)
        result["media"] = to_class(Media, self.media)
        return result


@dataclass
class PersonalityParameter:
    coarse: int
    fade_with_intensity: bool
    fine: int
    home: int
    invert: bool
    name: str
    size: int
    snap: bool
    type: int
    ranges: Optional[List[Range]] = None
    emitter_definition: Optional[List[float]] = None

    @staticmethod
    def from_dict(obj: Any) -> "PersonalityParameter":
        assert isinstance(obj, dict)
        coarse = from_int(obj.get("coarse"))
        fade_with_intensity = from_bool(obj.get("fadeWithIntensity"))
        fine = from_int(obj.get("fine"))
        home = from_int(obj.get("home"))
        invert = from_bool(obj.get("invert"))
        name = from_str(obj.get("name"))
        size = from_int(obj.get("size"))
        snap = from_bool(obj.get("snap"))
        type = from_int(obj.get("type"))
        ranges = from_union(
            [lambda x: from_list(Range.from_dict, x), from_none], obj.get("ranges")
        )
        emitter_definition = from_union(
            [lambda x: from_list(from_float, x), from_none],
            obj.get("emitterDefinition"),
        )
        return PersonalityParameter(
            coarse,
            fade_with_intensity,
            fine,
            home,
            invert,
            name,
            size,
            snap,
            type,
            ranges,
            emitter_definition,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["coarse"] = from_int(self.coarse)
        result["fadeWithIntensity"] = from_bool(self.fade_with_intensity)
        result["fine"] = from_int(self.fine)
        result["home"] = from_int(self.home)
        result["invert"] = from_bool(self.invert)
        result["name"] = from_str(self.name)
        result["size"] = from_int(self.size)
        result["snap"] = from_bool(self.snap)
        result["type"] = from_int(self.type)
        if self.ranges is not None:
            result["ranges"] = from_union(
                [lambda x: from_list(lambda x: to_class(Range, x), x), from_none],
                self.ranges,
            )
        if self.emitter_definition is not None:
            result["emitterDefinition"] = from_union(
                [lambda x: from_list(to_float, x), from_none], self.emitter_definition
            )
        return result


@dataclass
class Personality:
    colortable: str
    commands: List[Any]
    dcid: str
    has_intensity: bool
    lib_date: str
    lib_ver: str
    manufacturer: int
    manufacturer_name: str
    max_offset: int
    mode: int
    mode_name: str
    model: int
    model_name: str
    parameters: List[PersonalityParameter]

    @staticmethod
    def from_dict(obj: Any) -> "Personality":
        assert isinstance(obj, dict)
        colortable = from_str(obj.get("colortable"))
        commands = from_list(lambda x: x, obj.get("commands"))
        dcid = from_str(obj.get("dcid"))
        has_intensity = from_bool(obj.get("hasIntensity"))
        lib_date = from_str(obj.get("libDate"))
        lib_ver = from_str(obj.get("libVer"))
        manufacturer = from_int(obj.get("manufacturer"))
        manufacturer_name = from_str(obj.get("manufacturerName"))
        max_offset = from_int(obj.get("maxOffset"))
        mode = from_int(obj.get("mode"))
        mode_name = from_str(obj.get("modeName"))
        model = from_int(obj.get("model"))
        model_name = from_str(obj.get("modelName"))
        parameters = from_list(PersonalityParameter.from_dict, obj.get("parameters"))
        return Personality(
            colortable,
            commands,
            dcid,
            has_intensity,
            lib_date,
            lib_ver,
            manufacturer,
            manufacturer_name,
            max_offset,
            mode,
            mode_name,
            model,
            model_name,
            parameters,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["colortable"] = from_str(self.colortable)
        result["commands"] = from_list(lambda x: x, self.commands)
        result["dcid"] = from_str(self.dcid)
        result["hasIntensity"] = from_bool(self.has_intensity)
        result["libDate"] = from_str(self.lib_date)
        result["libVer"] = from_str(self.lib_ver)
        result["manufacturer"] = from_int(self.manufacturer)
        result["manufacturerName"] = from_str(self.manufacturer_name)
        result["maxOffset"] = from_int(self.max_offset)
        result["mode"] = from_int(self.mode)
        result["modeName"] = from_str(self.mode_name)
        result["model"] = from_int(self.model)
        result["modelName"] = from_str(self.model_name)
        result["parameters"] = from_list(
            lambda x: to_class(PersonalityParameter, x), self.parameters
        )
        return result


@dataclass
class Topo:
    channel: int
    column: int
    device_id: int
    row: int

    @staticmethod
    def from_dict(obj: Any) -> "Topo":
        assert isinstance(obj, dict)
        channel = from_int(obj.get("channel"))
        column = from_int(obj.get("column"))
        device_id = from_int(obj.get("deviceId"))
        row = from_int(obj.get("row"))
        return Topo(channel, column, device_id, row)

    def to_dict(self) -> dict:
        result: dict = {}
        result["channel"] = from_int(self.channel)
        result["column"] = from_int(self.column)
        result["deviceId"] = from_int(self.device_id)
        result["row"] = from_int(self.row)
        return result


@dataclass
class Patch:
    devices: List[Device]
    parameters: List[PatchParameter]
    personalities: List[Personality]
    topo: List[Topo]
    user_arrangement: bool

    @staticmethod
    def from_dict(obj: Any) -> "Patch":
        assert isinstance(obj, dict)
        devices = from_list(Device.from_dict, obj.get("devices"))
        parameters = from_list(PatchParameter.from_dict, obj.get("parameters"))
        personalities = from_list(Personality.from_dict, obj.get("personalities"))
        topo = from_list(Topo.from_dict, obj.get("topo"))
        user_arrangement = from_bool(obj.get("userArrangement"))
        return Patch(devices, parameters, personalities, topo, user_arrangement)

    def to_dict(self) -> dict:
        result: dict = {}
        result["devices"] = from_list(lambda x: to_class(Device, x), self.devices)
        result["parameters"] = from_list(
            lambda x: to_class(PatchParameter, x), self.parameters
        )
        result["personalities"] = from_list(
            lambda x: to_class(Personality, x), self.personalities
        )
        result["topo"] = from_list(lambda x: to_class(Topo, x), self.topo)
        result["userArrangement"] = from_bool(self.user_arrangement)
        return result


@dataclass
class View:
    height: int
    scale: int
    x: int
    y: int

    @staticmethod
    def from_dict(obj: Any) -> "View":
        assert isinstance(obj, dict)
        height = from_int(obj.get("height"))
        scale = from_int(obj.get("scale"))
        x = from_int(obj.get("x"))
        y = from_int(obj.get("y"))
        return View(height, scale, x, y)

    def to_dict(self) -> dict:
        result: dict = {}
        result["height"] = from_int(self.height)
        result["scale"] = from_int(self.scale)
        result["x"] = from_int(self.x)
        result["y"] = from_int(self.y)
        return result


@dataclass
class Play:
    beam_palettes: List[Palette]
    color_palettes: List[Palette]
    console_model: str
    cue_list: CueList
    independents: List[Independent]
    input_volume: int
    memories: List[Memory]
    pages: List[Page]
    patch: Patch
    position_palettes: List[Palette]
    recent: List[Any]
    sequences: List[Any]
    show_file_name: str
    software_version: str
    tag_groups: List[Page]
    views: List[View]

    @staticmethod
    def from_dict(obj: Any) -> "Play":
        assert isinstance(obj, dict)
        beam_palettes = from_list(Palette.from_dict, obj.get("beamPalettes"))
        color_palettes = from_list(Palette.from_dict, obj.get("colorPalettes"))
        console_model = from_str(obj.get("consoleModel"))
        cue_list = CueList.from_dict(obj.get("cueList"))
        independents = from_list(Independent.from_dict, obj.get("independents"))
        input_volume = from_int(obj.get("inputVolume"))
        memories = from_list(Memory.from_dict, obj.get("memories"))
        pages = from_list(Page.from_dict, obj.get("pages"))
        patch = Patch.from_dict(obj.get("patch"))
        position_palettes = from_list(Palette.from_dict, obj.get("positionPalettes"))
        recent = from_list(lambda x: x, obj.get("recent"))
        sequences = from_list(lambda x: x, obj.get("sequences"))
        show_file_name = from_str(obj.get("showFileName"))
        software_version = from_str(obj.get("softwareVersion"))
        tag_groups = from_list(Page.from_dict, obj.get("tagGroups"))
        views = from_list(View.from_dict, obj.get("views"))
        return Play(
            beam_palettes,
            color_palettes,
            console_model,
            cue_list,
            independents,
            input_volume,
            memories,
            pages,
            patch,
            position_palettes,
            recent,
            sequences,
            show_file_name,
            software_version,
            tag_groups,
            views,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["beamPalettes"] = from_list(
            lambda x: to_class(Palette, x), self.beam_palettes
        )
        result["colorPalettes"] = from_list(
            lambda x: to_class(Palette, x), self.color_palettes
        )
        result["consoleModel"] = from_str(self.console_model)
        result["cueList"] = to_class(CueList, self.cue_list)
        result["independents"] = from_list(
            lambda x: to_class(Independent, x), self.independents
        )
        result["inputVolume"] = from_int(self.input_volume)
        result["memories"] = from_list(lambda x: to_class(Memory, x), self.memories)
        result["pages"] = from_list(lambda x: to_class(Page, x), self.pages)
        result["patch"] = to_class(Patch, self.patch)
        result["positionPalettes"] = from_list(
            lambda x: to_class(Palette, x), self.position_palettes
        )
        result["recent"] = from_list(lambda x: x, self.recent)
        result["sequences"] = from_list(lambda x: x, self.sequences)
        result["showFileName"] = from_str(self.show_file_name)
        result["softwareVersion"] = from_str(self.software_version)
        result["tagGroups"] = from_list(lambda x: to_class(Page, x), self.tag_groups)
        result["views"] = from_list(lambda x: to_class(View, x), self.views)
        return result


@dataclass
class ShowFile:
    play: Play

    @staticmethod
    def from_dict(obj: Any) -> "ShowFile":
        assert isinstance(obj, dict)
        play = Play.from_dict(obj.get("play"))
        return ShowFile(play)

    def to_dict(self) -> dict:
        result: dict = {}
        result["play"] = to_class(Play, self.play)
        return result


def showfile_from_dict(s: Any) -> ShowFile:
    return ShowFile.from_dict(s)


def showfile_to_dict(x: ShowFile) -> Any:
    return to_class(ShowFile, x)
