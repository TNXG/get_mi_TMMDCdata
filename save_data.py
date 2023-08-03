import time
import asyncio
from loguru import logger
from bleak import BleakClient
import binascii

address = "A4:C1:38:40:0E:A2"  # 这个地方填写自己的蓝牙设备的地址
# 下面这个是特征
NOTIFICATION_UUID = "ebe0ccbc-7a0a-4b0c-8a1a-6ff2997da3a6"

async def run_ble_client(address: str, queue: asyncio.Queue):
    async def callback_handler(sender, data):
        await queue.put((time.time(), data))
    
    async with BleakClient(address) as client:
        logger.info(f"Connected: {client.is_connected}")
        await client.start_notify(NOTIFICATION_UUID, callback_handler)
        try:
            await asyncio.sleep(90.0)  # 修改这里的超时时间
        except asyncio.CancelledError:
            pass
        finally:
            await client.stop_notify(NOTIFICATION_UUID)
            logger.info("Disconnected from the device.")

            # Send an "exit command to the consumer"
            await queue.put((time.time(), None))

async def run_queue_consumer(queue: asyncio.Queue, data_List: list):
    while True:
        # Use await asyncio.wait_for(queue.get(), timeout=1.0) if you want a timeout for getting data.
        epoch, data = await queue.get()
        if data is None:
            logger.info("Got message from client about disconnection. Exiting consumer loop...")
            break
        else:
            data_List.append(str(binascii.hexlify(data)))
            logger.info(f"Received callback data via async queue at {epoch}: {data}")

def text_save(data):  # data为要写入数据列表.
    file = open('resieve_data.txt', 'w')
    for i in data:
        i = i[2:30] + '\n'
        file.write(i)
    file.close()
    print("==========保存成功===========")

async def main():
    queue = asyncio.Queue()
    data_store = []
    client_task = run_ble_client(address, queue)
    consumer_task = run_queue_consumer(queue, data_store)
    try:
        await asyncio.gather(client_task, consumer_task)
    except asyncio.CancelledError:
        pass

    text_save(data_store)
    logger.info("Main method done.")

if __name__ == "__main__":
    asyncio.run(main())
