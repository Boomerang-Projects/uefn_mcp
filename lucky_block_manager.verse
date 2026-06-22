using { /Verse.org/Simulation }
using { /Verse.org/Random }
using { /UnrealEngine.com/Temporary/Diagnostics }
using { /UnrealEngine.com/Temporary/SpatialMath }
using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /Fortnite.com/Playspaces }

lucky_block_manager := class(creative_device):

    @editable PillarTeleporters : []teleporter_device = array{}
    @editable StormController : basic_storm_controller_device = basic_storm_controller_device{}
    @editable EndGameDevice : end_game_device = end_game_device{}
    @editable ItemSpawners : []item_spawner_device = array{}

    var GameRunning : logic = false
    var StormStarted : logic = false

    OnBegin<override>()<suspends> : void =
        for (T : PillarTeleporters):
            T.Disable()
        for (S : ItemSpawners):
            S.Disable()
        loop:
            RunLobbyPhase()
            RunGamePhase()

    RunLobbyPhase()<suspends> : void =
        set GameRunning = false
        for (S : ItemSpawners):
            S.Disable()
        var Seconds : int = 6
        loop:
            if (Seconds <= 0):
                break
            Print("Game starting in {Seconds}...")
            Sleep(1.0)
            set Seconds = Seconds - 1

    RunGamePhase()<suspends> : void =
        set GameRunning = true
        Playspace := GetPlayspace()
        Players := Playspace.GetPlayers()

        for (S : ItemSpawners):
            S.Enable()

        # Start the storm once — never reset it between rounds
        if (not StormStarted):
            set StormStarted = true
            StormController.GenerateStorm()

        # Shuffle teleporters so each player gets a random unique pillar
        var ShuffledTeleporters : []teleporter_device = PillarTeleporters
        var i : int = ShuffledTeleporters.Length - 1
        loop:
            if (i <= 0):
                break
            j := GetRandomInt(0, i)
            if (TI := ShuffledTeleporters[i], TJ := ShuffledTeleporters[j],
                Swapped1 := ShuffledTeleporters.ReplaceElement[i, TJ]):
                if (Swapped2 := Swapped1.ReplaceElement[j, TI]):
                    set ShuffledTeleporters = Swapped2
            set i = i - 1

        for (Idx -> Player : Players):
            if (Idx < ShuffledTeleporters.Length, Teleporter := ShuffledTeleporters[Idx]):
                Teleporter.Enable()
                Teleporter.Teleport(Player)
                Teleporter.Disable()

        WaitForGameEnd(Playspace)

        for (S : ItemSpawners):
            S.Disable()

    WaitForGameEnd(Playspace : fort_playspace)<suspends> : void =
        loop:
            Sleep(3.0)
            Players := Playspace.GetPlayers()
            var AliveCount : int = 0
            for (P : Players):
                if (FC := P.GetFortCharacter[]):
                    if (FC.IsActive[]):
                        set AliveCount = AliveCount + 1
            if (AliveCount <= 1):
                Sleep(3.0)
                for (P : Players):
                    if (FC := P.GetFortCharacter[]):
                        if (FC.IsActive[]):
                            EndGameDevice.Activate(Agent := P)
                for (T : PillarTeleporters):
                    T.Disable()
                Sleep(5.0)
                return
