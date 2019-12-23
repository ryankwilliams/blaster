from blaster import Blaster

from tests.examples.valid import ValidCar

blaster = Blaster(
    tasks=[
        {
            'name': 'car',
            'task': ValidCar,
            'methods': ['exterior', 'interior']
        }
    ]
)
rdata = blaster.blastoff(serial=False)
print(rdata)