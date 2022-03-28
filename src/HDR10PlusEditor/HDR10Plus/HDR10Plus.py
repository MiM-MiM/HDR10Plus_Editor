"""HDR10Plus
Contains the class for the HDR10Plus Object
"""
# pylint: disable=invalid-name,line-too-long

try:
    import HDR10PlusEditor.HDR10Plus.json as HDR10PlusJSON
except ModuleNotFoundError:
    import HDR10Plus.json as HDR10PlusJSON


class HDR10Plus:
    """HDR10Plus Object
    Able to export to json, verify, and edit scenes (add/remove frames)
    """

    HDR10Plus_DCT = None

    def __init__(self, data):
        """Initalize HDR10Plus object.
        Keyword arguments:
        data -- a dictionary of the HDR10+ JSON
        """
        if not isinstance(data, dict):
            pass
        self.HDR10Plus_DCT = data

    def export_as_json(self, saveName):
        """Export the HDR10Plus object to a file.
        Keyword arguments:
        saveName -- The path to save the new JSON.
        """
        if not isinstance(saveName, str):
            raise RuntimeError(
                f"{__name__ }.export_as_json() expected a string filepath."
            )

        HDR10PlusJSON.export(dct=self.HDR10Plus_DCT, saveName=saveName)

    def verify(self):
        """Verify the object to contain a valid HDR10+ JSON/dct.
        Keyword arguments:
        """
        missing = []
        # Required JSONInfo, SceneInfo, SceneInfoSummary
        if not self.get_JSONInfo:
            missing.append("JSONInfo")
        if not self.get_SceneInfo:
            missing.append("SceneInfo")
        if not self.get_SceneInfoSummary:
            missing.append("SceneInfoSummary")
        if missing:
            raise ValueError(
                f"HDR10Plus requires 'JSONInfo, SceneInfo, and SceneInfoSummary'.\tMissing: {missing}"
            )
        SceneInfoSummary = self.get_SceneInfoSummary()
        if not SceneInfoSummary.get("SceneFirstFrameIndex"):
            missing.append("SceneFirstFrameIndex")
        if not SceneInfoSummary.get("SceneFrameNumbers"):
            missing.append("SceneFrameNumbers")
        if missing:
            raise ValueError(
                f"HDR10Plus requires 'SceneInfoSummary' to have 'SceneFirstFrameIndex' and 'SceneFrameNumbers'.\tMissing: {missing}"
            )
        SceneInfo = self.get_SceneInfo()
        SceneInfo_frame_count = len(SceneInfo)
        SceneInfoSummary_frame_count = sum(SceneInfoSummary.get("SceneFrameNumbers"))
        if SceneInfo_frame_count != SceneInfoSummary_frame_count:
            raise ValueError(
                f"HDR10Plus frame count error...\tFrame count in SceneInfo ({SceneInfo_frame_count}) does not match SceneInfoSummary ({SceneInfoSummary_frame_count})"
            )
        return True

    def summary(self):
        """View a summary of the HDR10+ parsed.
        Keyword arguments:
        """
        summary = None
        JSONInfo = self.get_JSONInfo()
        profile = JSONInfo.get("HDR10plusProfile")
        version = JSONInfo.get("Version")
        SceneInfo = self.get_SceneInfo()
        SceneInfoSummary = self.get_SceneInfoSummary().get("SceneFirstFrameIndex", [])
        TitleInfo = self.get_TitleInfo().get("Title")
        ToolInfo = self.get_ToolInfo().get("Tool")
        if TitleInfo:
            summary = f"{TitleInfo}" if not summary else f"{summary} | {TitleInfo}"
        if profile and version:
            profile_version = f"HDR10+ Profile {profile} Version {version}"
            summary = (
                f"{summary} | {profile_version}" if summary else f"{profile_version}"
            )
        if SceneInfo:
            frame_count = f"{len(SceneInfo)} Frames"
            summary = f"{summary} | {frame_count}" if summary else f"{frame_count}"
        if SceneInfoSummary:
            scene_count = f"{len(SceneInfoSummary)} Scenes"
            summary = f"{summary} | {scene_count}" if summary else f"{scene_count}"
        if ToolInfo:
            summary = f"{summary} | {ToolInfo}" if summary else f"{ToolInfo}"
        return summary

    def get_JSONInfo(self):
        """Return the JSONInfo or an empty dct.
        Keyword arguments:
        """
        return self.HDR10Plus_DCT.get("JSONInfo", {})

    def get_SceneInfo(self):
        """Return the SceneInfo or an empty list.
        Keyword arguments:
        """
        # SceneInfo is a list of frames.
        return self.HDR10Plus_DCT.get("SceneInfo", [])

    def get_SceneInfoSummary(self):
        """Return the SceneInfoSummary or an empty dct.
        Keyword arguments:
        """
        return self.HDR10Plus_DCT.get("SceneInfoSummary", {})

    def get_TitleInfo(self):
        """Return the TitleInfo or an empty dct.
        Keyword arguments:
        """
        return self.HDR10Plus_DCT.get("TitleInfo", {})

    def get_ToolInfo(self):
        """Return the ToolInfo or an empty dct.
        Keyword arguments:
        """
        return self.HDR10Plus_DCT.get("ToolInfo", {})

    def modify_scene_frames(self, sceneID, frames):
        #  pylint: disable=too-many-locals
        """Add or remove frames from a given scene.
        Keyword arguments:
        sceneID -- The scene ID to be modified, starting at 0.
        frames -- The amount of frames to add/remove.
        """
        scene_frames = self.get_SceneInfoSummary().get("SceneFrameNumbers")
        total_scenes = len(scene_frames)
        if -1 >= sceneID >= total_scenes:
            raise ValueError(
                f"Invalid SceneID given, recieved ({sceneID}). Valid range (inclusive): 0-{scene_frames-1}."
            )
        scene_frame_count = scene_frames[sceneID]
        new_SceneInfoSummary = self.get_SceneInfoSummary()
        new_SceneInfo = self.get_SceneInfo()
        scene_start = new_SceneInfoSummary["SceneFirstFrameIndex"][sceneID]
        scene_end = new_SceneInfoSummary["SceneFirstFrameIndex"][sceneID + 1]
        if frames < 0:
            if scene_frame_count <= abs(frames):
                raise ValueError(
                    f"Invalid modification, attempted to remove '{abs(frames)}' frames from scene '{sceneID}', which only has {scene_frame_count} frames."
                )
            if sceneID == 0:
                new_SceneInfo = new_SceneInfo[abs(frames) :]
            elif sceneID == total_scenes - 1:
                new_SceneInfo = new_SceneInfo[0 : len(new_SceneInfo) - 1 + frames]
            else:
                scene_start = new_SceneInfoSummary["SceneFirstFrameIndex"][sceneID]
                scene_end = new_SceneInfoSummary["SceneFirstFrameIndex"][sceneID + 1]
                SceneInfo_start = new_SceneInfo[0:scene_start]
                SceneInfo_mid = new_SceneInfo[scene_start : scene_end - 1]
                SceneInfo_mid = SceneInfo_mid[abs(frames) :]
                SceneInfo_end = new_SceneInfo[scene_end - 1 :]
                new_SceneInfo = SceneInfo_start + SceneInfo_mid + SceneInfo_end
        else:
            if sceneID == 0:
                new_SceneInfo = [new_SceneInfo[0]] * frames + new_SceneInfo
            elif sceneID == total_scenes - 1:
                new_SceneInfo = (
                    new_SceneInfo + [new_SceneInfo[0 : len(new_SceneInfo) - 1]] * frames
                )
            else:
                SceneInfo_start = new_SceneInfo[0:scene_start]
                SceneInfo_mid = new_SceneInfo[scene_start : scene_end - 1]
                SceneInfo_mid = SceneInfo_mid + [SceneInfo_mid[0]] * frames
                SceneInfo_end = new_SceneInfo[scene_end - 1 :]
                new_SceneInfo = SceneInfo_start + SceneInfo_mid + SceneInfo_end
        # Update the SceneFirstFrameIndex
        for i in range(sceneID + 1, total_scenes):
            new_SceneInfoSummary["SceneFirstFrameIndex"][i] = (
                new_SceneInfoSummary["SceneFirstFrameIndex"][i] + frames
            )
        # Update the SceneFrameNumbers (curent scene only)
        new_SceneInfoSummary["SceneFrameNumbers"][sceneID] = (
            new_SceneInfoSummary["SceneFrameNumbers"][sceneID] + frames
        )
        self.HDR10Plus_DCT["SceneInfoSummary"] = new_SceneInfoSummary
        self.HDR10Plus_DCT["SceneInfo"] = new_SceneInfo
        r = list(
            range(
                new_SceneInfoSummary["SceneFirstFrameIndex"][sceneID],
                new_SceneInfoSummary["SceneFirstFrameIndex"][sceneID + 1],
            )
        )
        r.reverse()
        sceneFrameNumber = len(r) - 1
        for i in r:
            self.HDR10Plus_DCT["SceneInfo"][i]["SceneFrameIndex"] = sceneFrameNumber
            sceneFrameNumber -= 1

        # Update the SequenceFrameIndex frame numbers.
        for i in range(0, len(new_SceneInfo)):
            self.HDR10Plus_DCT["SceneInfo"][i]["SequenceFrameIndex"] = i
        # Set the scene changed to start at 0, some reason it would not set it correctly, all other scene frames seemed fine.
        self.HDR10Plus_DCT["SceneInfo"][scene_start]["SequenceFrameIndex"] = 0
