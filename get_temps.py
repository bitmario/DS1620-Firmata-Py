import asyncio
import time

from pymata_aio import pymata_core
from pymata_aio.pymata_core import PymataCore
from pymata_aio.constants import Constants


DS1620_CONFIG = 0x30
DS1620_TEMP = 0x31
DS1620_TEMP_RESPONSE = 0x32


class MyPymata(PymataCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ds1620_configured = False
        self.ds1620_temperature = -9999
        self.command_dictionary[DS1620_TEMP_RESPONSE] = self._ds1620_message

    async def _ds1620_message(self, data):
        val = int(
            (data[pymata_core.PrivateConstants.MSB] << 7)
            + data[pymata_core.PrivateConstants.LSB]
        )
        self.ds1620_temperature = val / 100.0

    async def configure_ds1620(self, rst_pin, clk_pin, dq_pin):
        await self._send_sysex(DS1620_CONFIG, [rst_pin, clk_pin, dq_pin])
        await asyncio.sleep(0.75)

        self.ds1620_configured = True

    async def get_temp(self):
        """
        Read temperature from a DS1620 via firmata, returns the received temperature or
        -9999 on error.

        Should take less than 20ms if operating in continuous mode, or more than 750ms if
        operating in 1SHOT mode.
        """
        if not self.ds1620_configured:
            raise RuntimeError(
                "You must configure the DS1620 before trying to read the temperature"
            )

        await self._send_sysex(DS1620_TEMP, None)

        current_time = time.time()
        while self.ds1620_temperature == -9999:
            elapsed_time = time.time()
            if elapsed_time - current_time > 4:
                break
            await asyncio.sleep(self.sleep_tune)

        temp = self.ds1620_temperature
        self.ds1620_temperature = -9999

        return temp


RST_PIN = 4
CLK_PIN = 3
DQ_PIN = 2

loop = asyncio.get_event_loop()

dev = MyPymata()
dev.start()

loop.run_until_complete(dev.configure_ds1620(RST_PIN, CLK_PIN, DQ_PIN))

while True:
    print(loop.run_until_complete(dev.get_temp()))
