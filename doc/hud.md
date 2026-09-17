
From uds-toolkit

Is sent to dut and received by doip router

That is then forward to hud_proxy echo /dev/display/hud/diag

Hud proxy send the message to hud driver (/dev/display/hud/diag)


Hud driver

    common_driver
            dim_hud_d
                HErer is the binary
                It includes the  DiimHudCommonDriver from lib_dim_hud library and the more specific HudDriver from lib_hud library.
                It creates a instnce of HudDriver (Specific one) and then a DimHudCommonDriver (common one) and forwards the specific HudDriver to the DimHudCommonDriver.


            lib_dim_hud
                DimHudCommonDriver
                    It is the common driver for all hud drivers. It has the common functionality for all hud drivers.

    hud/
        lib_hud
            HudDriver
                It is the specific driver for the hud. It has the specific functionality for the hud.


                In here we create a HudDiagnosticResourceManager
                    And in that one we create the /dev/display/hud/diag resource and register it
                    So here we have the receiver from hud_proxy and the sender to the hud driver. So when we receive a message from hud_proxy,
                    So for the message above from uds-toolkit it arrives in io_write, io write calls HandleDiagWrite (wihch releays in HudDriver) The message looks like this: 22, f1, 86
                    HandleDiagWrite sends the message to  the thread  (HudEventLooop) which looks like it calls
                            MsgReceive (Get first part)
                            MsgRead (Get more of the mesage)
                            And then mcu->SendDiagnosticRequest Not sure what is being sent here of the original message ( 0 , 3, 22, f1, 86)
                                There is some  addon that tells it's a diagnostic request

                                The MCU  sends it to register device
                                    register device is DthRegisterDevice that sends it with MsgSend_r wich I think is sending to another process
                                    (/dev/name/local/dth)  Where the name is a server
                                    I{t must be the dth server

                             1



