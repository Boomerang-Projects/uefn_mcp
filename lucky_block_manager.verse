using { /Verse.org/Simulation }
using { /Verse.org/Random }
using { /UnrealEngine.com/Temporary/Diagnostics }
using { /UnrealEngine.com/Temporary/UI }
using { /UnrealEngine.com/Temporary/SpatialMath }
using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /Fortnite.com/Playspaces }
using { /Fortnite.com/UI }

lucky_block_manager := class(creative_device):

    @editable PillarTeleporters : []teleporter_device = array{}
    @editable StormController : storm_controller_device = storm_controller_device{}
    @editable EndGameDevice : end_game_device = end_game_device{}

    var GameRunning : logic = false

    OnBegin<override>()<suspends> : void =
        for (T : PillarTeleporters):
            T.Disable()
        loop:
            RunLobbyPhase()
            RunGamePhase()

    RunLobbyPhase()<suspends> : void =
        set GameRunning = false
        # Show ready prompt and wait for any player to hold E
        Playspace := GetPlayspace()
        race:
            WaitForReady(Playspace)
            loop:
                Sleep(1.0)

    WaitForReady(Playspace : fort_playspace)<suspends> : void =
        # Wait until at least 1 player is in the game then start
        loop:
            Players := Playspace.GetPlayers()
            if (Players.Length > 0):
                Sleep(5.0)  # Give players a moment in lobby
                return
            Sleep(1.0)

    RunGamePhase()<suspends> : void =
        set GameRunning = true
        Playspace := GetPlayspace()
        Players := Playspace.GetPlayers()

        # Shuffle teleporters and assign one per player
        var ShuffledTeleporters : []teleporter_device = PillarTeleporters
        var i : int = ShuffledTeleporters.Length - 1
        loop:
            if (i <= 0):
                break
            j := GetRandomInt(0, i)
            if (TI := ShuffledTeleporters[i], TJ := ShuffledTeleporters[j]):
                set ShuffledTeleporters = ShuffledTeleporters.ReplaceElement[i, TJ]
                set ShuffledTeleporters = ShuffledTeleporters.ReplaceElement[j, TI]
            set i = i - 1

        # Teleport each player to their assigned pillar
        for (Idx -> Player : Players):
            if (Teleporter := ShuffledTeleporters[Idx]):
                Teleporter.Enable()
                Teleporter.Teleport(Player)
                Teleporter.Disable()

        # Start the storm
        StormController.StartStorm()

        # Watch for last player standing
        WaitForGameEnd(Playspace)

    WaitForGameEnd(Playspace : fort_playspace)<suspends> : void =
        loop:
            Sleep(3.0)
            Players := Playspace.GetPlayers()
            AlivePlayers := Players.Filter(Player => if (FC := Player.GetFortCharacter[]) { not FC.IsEliminated() } else { false })
            if (AlivePlayers.Length <= 1):
                Sleep(3.0)
                if (Winner := AlivePlayers[0]):
                    EndGameDevice.Activate(Player := Winner)
                StormController.StopStorm()
                Sleep(5.0)
                return
