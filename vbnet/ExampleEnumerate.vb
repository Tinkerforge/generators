Imports Tinkerforge

Module ExampleEnumerate
    Const HOST As String = "localhost"
    Const PORT As Integer = 4223

    Sub EnumerateCB(ByVal sender As IPConnection, _
                    ByVal uid As String, _
                    ByVal connectedUid As String, _
                    ByVal position As Char, _
                    ByVal hardwareVersion() As Short, _
                    ByVal firmwareVersion() As Short, _
                    ByVal deviceIdentifier As Integer, _
                    ByVal enumerationType As Short)
        System.Console.WriteLine("UID:               {0}", uid)
        System.Console.WriteLine("Enumeration Type:  {0}", enumerationType)

        If enumerationType = IPConnection.ENUMERATION_TYPE_DISCONNECTED Then
            System.Console.WriteLine("")
            Return
        End If

        System.Console.WriteLine("Connected UID:     {0}", connectedUid)
        System.Console.WriteLine("Position:          {0}", position)
        System.Console.WriteLine("Hardware Version:  {0}.{1}.{2}", _
                                 hardwareVersion(0), hardwareVersion(1), hardwareVersion(2))
        System.Console.WriteLine("Firmware Version:  {0}.{1}.{2}", _
                                 firmwareVersion(0), firmwareVersion(1), firmwareVersion(2))
        System.Console.WriteLine("Device Identifier: {0}", deviceIdentifier)
        System.Console.WriteLine("")
    End Sub

    Sub Main()
        ' Create connection and connect to brickd
        Dim ipcon As New IPConnection()
        ipcon.Connect(HOST, PORT)

        ' Register Enumerate Callback
        AddHandler ipcon.EnumerateCallback, AddressOf EnumerateCB

        ' Trigger Enumerate
        ipcon.Enumerate()

        System.Console.WriteLine("Press key to exit")
        System.Console.ReadLine()
        ipcon.Disconnect()
    End Sub
End Module
