Imports Tinkerforge

Module ExampleAuthenticate
    Const HOST As String = "localhost"
    Const PORT As Integer = 4223
    Const SECRET As String = "My Authentication Secret!"

    Sub ConnectedCB(ByVal sender As IPConnection, _
                    ByVal connectReason As Short)
        Select Case connectReason
            Case IPConnection.CONNECT_REASON_REQUEST
                System.Console.WriteLine("Connected by request")
            Case IPConnection.CONNECT_REASON_AUTO_RECONNECT
                System.Console.WriteLine("Auto-Reconnect")
        End Select

        ' Authenticate first...
        Try
            sender.Authenticate(SECRET)
            System.Console.WriteLine("Authentication succeeded")
        catch
            System.Console.WriteLine("Could not authenticate")
            Exit Sub
        End Try

        ' ...reenable auto reconnect mechanism, as described below...
        sender.SetAutoReconnect(true)

        ' ...then trigger enumerate
        sender.Enumerate()
    End Sub

    Sub EnumerateCB(ByVal sender As IPConnection, _
                    ByVal uid As String, _
                    ByVal connectedUid As String, _
                    ByVal position As Char, _
                    ByVal hardwareVersion() As Short, _
                    ByVal firmwareVersion() As Short, _
                    ByVal deviceIdentifier As Integer, _
                    ByVal enumerationType As Short)
        System.Console.WriteLine("UID: {0}, Enumeration Type: {1}", uid, enumerationType)
    End Sub

    Sub Main()
        ' Create IPConnection and connect to brickd
        Dim ipcon As New IPConnection()

        ' Register Connected Callback
        AddHandler ipcon.Connected, AddressOf ConnectedCB

        ' Register Enumerate Callback
        AddHandler ipcon.EnumerateCallback, AddressOf EnumerateCB

        ' Disable auto reconnect mechanism, in case we have the wrong secret.
        ' If the authentication is successful, reenable it.
        ipcon.SetAutoReconnect(false)

        ' Connect to brickd
        ipcon.Connect(HOST, PORT)

        System.Console.WriteLine("Press key to exit")
        System.Console.ReadLine()
        ipcon.Disconnect()
    End Sub
End Module
