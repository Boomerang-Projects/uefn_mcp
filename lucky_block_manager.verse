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
    @editable ReadyButton : conditional_button_device = conditional_button_device{}

    var GameRunning : logic = false

    OnBegin<override>()<suspends> : void =
        for (T : PillarTeleporters):
            T.Disable()
        loop:
            RunLobbyPhase()
            RunGamePhase()

    RunLobbyPhase()<suspends> : void =
        set GameRunning = false
        ReadyButton.Enable()
        ReadyButton.ActivatedEvent.Await()
        ReadyButton.Disable()

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
            if (TI := ShuffledTeleporters[i], TJ := ShuffledTeleporters[j],
                Swapped1 := ShuffledTeleporters.ReplaceElement[i, TJ]):
                if (Swapped2 := Swapped1.ReplaceElement[j, TI]):
                    set ShuffledTeleporters = Swapped2
            set i = i - 1

        # Teleport each player to their assigned pillar
        for (Idx -> Player : Players):
            if (Idx < PillarTeleporters.Length, Teleporter := ShuffledTeleporters[Idx]):
                Teleporter.Enable()
                Teleporter.Teleport(Player)
                Teleporter.Disable()

        Sleep(30.0)
        StormController.GenerateStorm()

        WaitForGameEnd(Playspace)

    WaitForGameEnd(Playspace : fort_playspace)<suspends> : void =
        loop:
            Sleep(3.0)
            Players := Playspace.GetPlayers()
            var AliveCount : int = 0
            var LastAlive : agent = agent{}
            for (P : Players):
                if (FC := P.GetFortCharacter[]):
                    if (FC.IsActive[]):
                        set AliveCount = AliveCount + 1
                        set LastAlive = P
            if (AliveCount <= 1):
                Sleep(3.0)
                if (AliveCount = 1):
                    EndGameDevice.Activate(Agent := LastAlive)
                StormController.DestroyStorm()
                for (T : PillarTeleporters):
                    T.Disable()
                Sleep(5.0)
                return
