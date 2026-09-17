SPA2
Dim threads:


1                                                       Super thread
DimHudUnlogResmgr                                       logging for debug
McuResmgr                                               Device parameterResourceManager for MCU
ADC_debug                                               ADC (Analog to Digital Converter) debug
DoubleTaskBuffer                                        Two task at the same time ??
DimResmgr                                               Device parameterResourceManager for dim
DoubleTaskBuffer                                        Two task at the same time ??
HudDiagResmgr                                           Device parameterResourceManager diag for HUD
HudAmbillmnResmgr
HudResmgr                                               Device parameterResourceManager for HUD
pm_handler
DimHudResmgr                                           Device parameterResourceManager for HUD and DIM
HudEventLoop
DimHud-ErrbMonitor
GpioInterruptMonitor
DimHud-LinkLockMonitor
GpioInterruptMonitor
ADC Reading Loop
DimDriver::DeRating


SPA3
Dim threads:

CsdDimDMain
ADC_debug
DimResmgr
4
ErrorHandlerLoop
TouchManagerDispatch
TouchManagerReply
TouchManagerDispatch
TouchManagerReply
CsdResmgr
DoubleTaskBuffer
dim_state_resmgr
DoubleTaskBuffer
csd_state_resmgr
pm_handler
AdcMonitor
LinkWorkerA
GpioInterruptMonitor
LinkWorkerB
LinkMonitor
ADC Reading Loop
DIM: DeRating
TouchInit
TconMonitor
InterruptHandler(GPIO75)
GpioInterruptMonitor
InterruptHandler(GPIO6)
InterruptHandler(GPIO53)
InterruptHandler(GPIO103)
GpioInterruptMonitor
GpioInterruptMonitor
GpioInterruptMonitor
TouchController
34
