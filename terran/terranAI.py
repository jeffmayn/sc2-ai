import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.player import Human

class terranAI(sc2.BotAI):
    async def on_step(self, iteration):
        await self.distribute_workers()
        await self.buildSCVs()
        await self.buildSupplyDepot()

    async def buildSCVs(self):
        # declare command center cc as first one build
        cc = self.units(COMMANDCENTER)
        cc = cc.first

        # train SCVs
        if self.can_afford(SCV) and self.workers.amount < 22 and cc.noqueue:
            await self.do(cc.train(SCV))

    async def buildSupplyDepot(self):
        if self.supply_left < 10 and not self.already_pending(SUPPLYDEPOT):
            scv = self.units(SCV).ready
            if scv.exists:
                if self.can_afford(SUPPLYDEPOT):
                    await self.build(SUPPLYDEPOT, near=scv.first)

def main():
    sc2.run_game(sc2.maps.get("AcidPlantLE"),
    [Bot(Race.Terran, terranAI()),
    Computer(Race.Terran, Difficulty.Easy)],
    realtime=True)

if __name__ == '__main__':
    main()
