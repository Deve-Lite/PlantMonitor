
from machine import Pin
from asyncio import sleep_ms

async def blink(led: Pin, n=1):
    for i in range(n):
        led.value(1)
        sleep_ms(300)
        led.value(0)
        sleep_ms(300)
        