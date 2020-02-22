from random  import randint
from Team import *

printActionDescription = True

def dprint(s):
    if printActionDescription:
        print(s)

def teamAlive(team):
    count = 0
    for i in team:
        if i.alive == True:
            count += 1
    return count

def teamDead(team):
    count = 0
    for i in team:
        if i.alive == False:
            count += 1
    return count

#Constants for Mage Type        
manaCost = 20
manaRecovery = 30


class Character(object):
    def __init__(self):
        self.name = ''
        self.maxhp = 1000
        self.hp = 1000
        self.str = 0
        self.maxmana = 0
        self.mana = 0
        self.cost = 9999999999
        self.alive = True

    def act(self,myTeam,enemy):
        return

    def gotHurt(self,damage):
        if damage >= self.hp:
            self.hp = 0
            self.alive = False
            dprint(self.name + ' died!')
        else:
            self.hp -= damage
            dprint(self.name +
                   f' hurt with remaining hp {self.hp}.')

class Fighter(Character):
    def __init__(self):
        super().__init__()
        self.name = 'Fighter'
        self.maxhp = 1200
        self.hp = 1200
        self.str = 100
        self.cost = 100

    def act(self,myTeam,enemy):
        target = randAlive(enemy)
        dprint(f'Hurt enemy {target} by damage {self.str}.')
        enemy[target].gotHurt(self.str)

class Berserker(Fighter):
    def __init__(self):
        super().__init__()
        self.name = 'Berserker'
        self.cost = 200

    def berserk(self, enemy):
        self.str = self.str * 2
        dprint(f'Berserk mode! Attack double!')
        
    def act(self,myTeam,enemy):
        target = randAlive(enemy)
        if self.hp <= (self.maxhp/2):
            self.berserk(enemy)
            dprint(f'Hurt enemy {target} by damage {self.str}.')
            enemy[target].gotHurt(self.str)        
        else:
            dprint(f'Hurt enemy {target} by damage {self.str}.')
            enemy[target].gotHurt(self.str)        
            
class Mage(Character):
    def __init__(self):
        super().__init__()
        self.name = 'Mage'
        self.maxmana = 50
        self.mana = 50
        self.hp = 800
        self.cost = 200
        self.int = 400

    def cast(self,myTeam,enemy):
        self.mana -= manaCost
        target = randAlive(enemy)
        dprint(f'Strike enemy {target} with spell')
        enemy[target].gotHurt(self.int)
        
    def act(self,myTeam,enemy):
        if self.mana < manaCost:
            self.mana += manaRecovery
            dprint(f'Mana recover to {self.mana}.')
        else:
            self.cast(myTeam,enemy)

class ArchMage(Mage):
    def __init__(self):
        super().__init__()
        self.name = 'ArchMage'
        self.cost = 600

    def kaboom(self,myTeam,enemy):
        self.mana -= manaCost
        extraDamage = self.int * 2
        for i in enemy:
            if i.alive == True:
                i.gotHurt(extraDamage)
        dprint(f'Cast KABOOOOM! (Damage {extraDamage}) to every enemy!')
        enemy

    def cast(self,myTeam,enemy):
        self.mana -= manaCost
        target = randAlive(enemy)
        dprint(f'Strike enemy {target} with spell')
        enemy[target].gotHurt(self.int)

    def act(self,myTeam,enemy):
        if self.mana < manaCost:
            self.mana += manaRecovery
            dprint(f'Mana recover to {self.mana}.')
        elif (teamAlive(myTeam) == 1 and self.alive == True):
            self.kaboom(myTeam, enemy)            
        else:
            self.cast(myTeam,enemy)
   
class Necromancer(Mage):
    def __init__(self):
        super().__init__()
        self.name = 'Necromancer'
        self.maxmana = 50
        self.mana = 50
        self.hp = 800
        self.cost = 400

    def revive(self, myTeam):
        self.mana -= manaCost
        target = randDeath(myTeam)
        myTeam[target].alive == True
        myTeam[target].hp = (myTeam[target].maxhp)//2
        dprint(f'Reviving member {target} with hp {myTeam[target].hp}.')

    def cast(self,myTeam,enemy):
        self.mana -= manaCost
        target = randAlive(enemy)
        dprint(f'Strike enemy {target} with spell')
        enemy[target].gotHurt(self.int)
        
    def act(self,myTeam,enemy):
        if self.mana < manaCost:
            self.mana += manaRecovery
            dprint(f'Mana recover to {self.mana}.')
        elif teamDead(myTeam) > 0:
            self.revive(myTeam)
        else:
            self.cast(myTeam,enemy)
   
