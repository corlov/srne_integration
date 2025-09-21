

cmd_reset_settings = 0x78
cmd_clear_history = 0x79

addr_retedChargingCurrent = 0x000A
addr_ratedDischargeCurrent = 0x000B
addr_model = 0x000C
addr_softwareVersion = 0x0014
addr_hardwareVersion = 0x0016
addr_serialNumber = 0x0018

# 35 регистров с динамической информацией
addr_dynamic_info_registers_start_addr = 0x100

add_history_start_addr = 0xF000
addr_specialPowerControl = 0xE021
addr_boostchargingRecoveryVoltage = 0xE00A
addr_overDischargeRecoveryVoltage = 0xE00B
addr_underVoltageWarningLevel = 0xE00C
addr_overDischargeVoltage = 0xE00D
addr_dischargingLimitVoltage = 0xE00E
addr_overDischareTimeDelay = 0xE010
addr_equalizingChargingTime = 0xE011
addr_boostChargingTime = 0xE012
addr_equalizingChargingInterval = 0xE013
addr_temperatureCompensationFactor = 0xE014
addr_loadWorkingMode = 0xE01D
addr_nominalBatteryCapacity = 0xE002
addr_systemVoltageSetting = 0xE003
addr_recognizedVoltage = 0xE003
addr_batteryType = 0xE004
addr_overVoltageThreshold = 0xE005
addr_chargingVoltageLimit = 0xE006
addr_equalizingChargingVoltage = 0xE007
addr_boostchargingVoltage = 0xE008
addr_floatingChargingVoltage = 0xE009
addr_lightControlDelay = 0xE01E
addr_lightControlVoltage = 0xE01F

addr_loadOnOff = 0x010A
addr_chargeCurrent = 0xE001