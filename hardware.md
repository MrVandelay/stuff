

What does the different drivers do, what configuration do they support
How do the use DSM (Data safety manager) and DTH (Data transfer handler) for safety critical data handling

# SPA2

# SPA3
DIMD2.0 → SPA3 V436
DIMD2.5 → SPA3 V326
(SPA3/SA8255P platform)



## Drivers
### ALPNS_COMMON_S2_DIM_HUD
it's the SPA2 combined DIM (Driver Information Module) and HUD (Heads Up Display) display driver, running on QNX with Qualcomm 8155/8255 chipsets

### BSHALP_COMMON_S3_CSD_DIM
it's the SPA3 combined CSD/DIM display driver for the BSH ALP platform, running on the Qualcomm SA8255 chipset under QNX.
deserializer for the DIM is MAX96870B


### ALP_1600_2560_G2_CSD
It's the SPA2 CSD (Center Stack Display) driver for the 1600×2560 ALP panel, part of the QNX display driver stack.
Somehow this need the ALPNS_COMMON_S2_DIM_HUD driver as well, but I am not sure how they are related. Maybe the ALPNS_COMMON_S2_DIM_HUD is a wrapper around the ALP_1600_2560_G2_CSD to provide additional functionality or support for specific features of the HUD display.
Deserializer for the CSD is MAX6774


# Sw stack architecture

## DISCO
DISCO = Driver Information Safety COmponent.
It's an ASIL-B SEooC (Safety Element out of Context) that performs graphical and signal validation on the DIM display.
It ensures that safety-critical telltales (parking brake, child lock, etc.) are correctly rendered.
Maintained by Team Doozers (whereas DSM/DTH is Team Nebula's domain). DISCO Feature

## SAIL
 SAIL sits above DSM/DTH in the safety reporting chain (receiving aggregated status from SALSA and forwarding to HKP), but is not in the data path between DSM/DTH and the display hardware.

## SALSA (Safety Adaptation Layer for SPA Architecture)
Receives heartbeat from DSM

## DTH (Display Traffic Handler)
DTH is the communication layer that DSM uses to talk to hardware. Both are separate QNX processes that are part of the display safety architecture (ASIL-B, ISO 26262 compliant). They are both safety components
DTH exposes a QNX named channel (via name_attach) that its clients — DSM and the display drivers — connect to and send requests through

DSM (or a display driver) sends a request message to DTH's named channel
1. DTH receives the request, decodes the header, and routes it to the correct device (serializer, deserializer, MCU) via the UART bus (SPA2) or I2C bus (SPA3)
2. The hardware device responds
3. DTH forwards the response back to the client
4. The client is blocked between the request/reply pair — it's synchronous

## DSM (Display Safety Manager)
DSM uses DTH to:
Run startup routine tests — reading/writing serializer and deserializer registers to verify the display system is safe to use
Perform continuous health monitoring — periodically checking safety-critical registers (link status, error counters, ERRB)
Execute safe state transitions — when faults are detected, DSM reads/writes registers through DTH to disable backlights, report DTCs, etc.
Send a heartbeat to SALSA — DSM's heartbeat depends on the display state it monitors through DTH
DTH provides DSM with:
Arbitrated access to the GMSL2 control channel (serializer/deserializer registers) — so DSM and display drivers don't collide on the bus
Client prioritization — DSM as a safety process can get higher priority access than QM driver operations
A transport abstraction — DSM doesn't need to know whether the underlying bus is UART (SPA2) or I2C (SPA3)


Abbreviations:
- ALP:      Automotive Linux Platform
- ASIL:     Automotive Safety Integrity Level
- CSD:      Center Stack Display
- DTH:      Display Traffic Handler
- DSM:      Display Safety Manager
- DTC:      Diagnostic Trouble Code
- GMSL:     Gigabit Multimedia Serial Link
- HUD:      Heads Up Display
- I/O:      Input/Outputj
- Fusa:     Functional safety (FuSa) is a critical aspect of automotive software development,
            ensuring that systems operate safely even in the presence of faults.
            In the context of display drivers for automotive applications, FuSa involves
            implementing safety mechanisms to prevent hazardous situations caused by display failures.



Common:
The UXC communicates with the rest of the vehicle over Ethernet (SOME/IP,
used for receiving display signals from the CSP) and CAN (used between the
UXCH and the vehicle). Display power is controlled by the Zone Controller Right A (ZCRA).



Goal            G
Strategy        S
Solution        Sn
Context         C
Assumption      A
Justification   J

5.3.1  Software architecture satisfies the allocated software safety requirements.
    on just DSM and DTH?
    Where is the requirements located? Do I need access to Doors?




Claims
Jira                                        Headline                                                                                                                                    Status
1 Functional safety management             Functional safety Management
                                                Functional safety activities were planned and managed.
                                                Roles, responsibilities, and interfaces were defined.
                                                Required independence and confirmation measures were achieved.
                                                Safety-related anomalies and deviations were managed.

2 Safety requirements                       Safety Requiredments
                                                Safety requirements are correctly and completely specified
                                                Software safety requirements are derived from and traceable to the applicable VCC software safety requirements.
                                                Software safety requirements are traceable throughout the software development lifecycle.

3 Software architecture and design          Software architecture and design
                                                Software architecture satisfies the allocated software safety requirements.
                                                Test description available
                                                Traceability between FuSa Requirements and Test Procedures is available
                                                Test Results are available
                                                Safety Architecture confirmed via Safety Analyses
                                                Other Verification Methods of FuSa Requirments are covered

4 Implementation and coding DSM/DTH        Implementation and Coding
                                                Software implementation complies with the specified design and safety requirements                                                      Done
                                                The required safety mechanisms are present and identifiable in the implementation                                                       Done

5 Safety analysis DSM/DTH                   Safety Analysis
                                                Safety-related software failure modes were identified and analyzed.                                                                     Done
                                                FMEA findings are addressed in requirements, architecture, design, or verification.                                                     Done

6                                           Software Verification
                                                Software integration and testing verify that software safety mechanisms operate as intended.

7                                            Supporting Processes
                                                Configuration management and change control preserve safety-related work products and ensure changes are reviewed before integration.
                                                Documentation is complete, controlled, reviewed, and available as safety evidence
                                                Software tools are used with sufficient confidence for their intended safety-related use.

8                                           Supporting Processes ??
                                                Confirmation reviews were conducted and their findings support the safety argument.
                                                Functional safety audit confirms that planned safety processes were implemented and followed.
                                                Functional safety assessment supports acceptance of the software contribution for the defined release scope

 9                                          Safety Case Completeness
                                                The safety case presents a complete and structured argument for the software safety contribution.
                                                The safety case identifies assumptions, known limitations, open issues, and residual risks.




5.3 Development Management and 5.26 Safety Reviews.


