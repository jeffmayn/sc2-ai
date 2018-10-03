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
        await self.expandBase()

    async def buildSCVs(self):
        # declare command center cc as first one build.
        cc = self.units(COMMANDCENTER)
        cc = cc.first

        # train SCVs.
        if self.can_afford(SCV) and self.workers.amount < 22 and cc.noqueue:
            await self.do(cc.train(SCV))
            print(SCV)

    async def buildSupplyDepot(self):
        # build new supply depot when below threshold
        # TODO: make generic, and increase build-count as different types of units becomes available.
        if self.supply_left < 5 and not self.already_pending(SUPPLYDEPOT):
            scv = self.units(SCV).ready
            # check if we got the money to build it.
            if scv.exists and self.can_afford(SUPPLYDEPOT):
                    await self.build(SUPPLYDEPOT, near=scv.first)

    async def expandBase(self):
        # when only one command center, we expand if affordable.
        # TODO: make it generic, so more expansions happens due to volume of existing bases and current threat level.
        if self.units(COMMANDCENTER).amount < 2 and self.can_afford(COMMANDCENTER):
            await self.expand_now()

def main():
    sc2.run_game(sc2.maps.get("AcidPlantLE"),
    [Bot(Race.Terran, terranAI()),
    Computer(Race.Terran, Difficulty.Easy)],
    realtime=True)

if __name__ == '__main__':
    main()
