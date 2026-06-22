using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/SpatialMath }
using { /UnrealEngine.com/Temporary/Diagnostics }
using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /Fortnite.com/Playspaces }

kill_floor_device := class(creative_device):

    OnBegin<override>()<suspends> : void =
        Print("KillFloor: started")
        for (Player : GetPlayspace().GetPlayers()):
            if (FortChar := Player.GetFortCharacter[]):
                spawn { WatchPlayer(FortChar) }

    WatchPlayer(FortChar : fort_character)<suspends> : void =
        FortChar.EliminatedEvent().Await()
        Z := FortChar.GetTransform().Translation.Z
        Print("Player died at Z = {Z}")
