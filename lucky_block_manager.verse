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
    @editable LobbyTeleporter : teleporter_device = teleporter_device{}
    @editable ResetZones : []mutator_zone_device = array{}
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

        # Wipe player builds from last round before anyone lands on pillars
        for (Z : ResetZones):
            Z.Enable()
        Sleep(2.0)
        for (Z : ResetZones):
            Z.Disable()

        # Start the storm once — never reset it between rounds
        if (StormStarted = false):
            set StormStarted = true
            StormController.GenerateStorm()

        # Assign each player a unique pillar via random rotation
        Offset := GetRandomInt(0, PillarTeleporters.Length - 1)
        for (Idx -> Player : Players):
            var PillarIdx : int = Idx + Offset
            if (PillarIdx >= PillarTeleporters.Length):
                set PillarIdx = PillarIdx - PillarTeleporters.Length
            if (Teleporter := PillarTeleporters[PillarIdx]):
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
                # Send everyone back to the lobby to start the next round
                LobbyTeleporter.Enable()
                for (P : Players):
                    LobbyTeleporter.Teleport(P)
                LobbyTeleporter.Disable()
                for (T : PillarTeleporters):
                    T.Disable()
                Sleep(3.0)
                return
