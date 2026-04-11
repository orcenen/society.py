"""
a few notes:

1. when you look at this code i just want you to know that you should not change how the lines and formatted code works thanks :))
2. Lorus is the first sign that people can live past 60. His infuence is in this code.
3. on most runs it works so there arent any bugs that are just invalid python in places that run many times
4. i need minimal safety checks in the modding api because thats not fun
"""

from random import choice, randint, random
from pyperclip import copy
import curses, json

# .VARIABLES

people = {}
afterlife = {}
generations = 0
history = []

law = False

# .UTILITY

def u_info(stdscr, action, people):
    global law    

    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.curs_set(0)
    stdscr.erase()

    title = 'PYTHON SOCIETY PROGRAM'

    height, width = stdscr.getmaxyx()
    x = (width - len(title)) // 2

    stdscr.addstr(0, x, title, curses.color_pair(1))
    
    stdscr.addstr(3, 0, action)
    
    if people:
        formatted = "\n".join(
            f"| {key}: {'; '.join(f'{k}: {v}' for k, v in value.items())}"
            for key, value in people.items()
        )
        lines = formatted.splitlines()
        lines = lines[:max(0, height - 4)]
    else:
        formatted = "| "
    
    lines = formatted.splitlines() if isinstance(formatted, str) else formatted

    stdscr.addstr(5, 0, f"PEOPLE: {len(people)}")
    
    max_lines = height - 10
    lines = lines[:max_lines]
    
    for i, line in enumerate(lines):
        stdscr.addstr(6 + i, 0, line[:width-1])
    
    footer_y = 6 + len(lines) + 1
    stdscr.addstr(footer_y, 0, 'Laws are in action.' if law else 'There are no laws.')
    stdscr.addstr(footer_y + 2, 0, 'Press any key to continue.')

    stdscr.refresh()
    stdscr.getch()

def u_run_info(action, people): curses.wrapper(lambda stdscr: u_info(stdscr, action or 'No action.', people))

def u_preset():
    global generations
    
    return {
            'kills': 0,
            'born': generations,
            'money': 0,
            'died': None
        } 

# .ACTIONS

def a_cry():
    global people

    tear = choice(list(people.keys()))

    return f'{tear} cried.'

def a_poetry():
    global people
    global afterlife
    
    writer = choice(list(people.keys()))
    
    if random() >= 0.5:
        return f'{writer} wrote a poem.'
    else:
        if list(afterlife.keys()):
            honor = choice(list(afterlife.keys()))
            return f'{writer} wrote a poem in honor of {honor}.'
        else:
            return f'{writer} wrote a poem for the future.'

def a_breakdown():
    global people

    victim = choice(list(people.keys()))

    return f'{victim} had a psychotic breakdown.'

def a_journey():
    global people
    global generations

    if len(list(people.keys())) < 2:
        return a_free()

    traveler = choice(list(people.keys()))

    if random() >= 0.5:
        name = gen_name().strip()

        people[name] = u_preset()
        
        return f'{traveler} went on a journey and found a traveler named {name}.'

    else:
        kill(traveler)
        return f'{traveler} went on a journey and never came back.'    

def steal(stealer, victim):
    global people
    
    stolen = people[victim]["money"]
    people[stealer]["money"] += stolen
    people[victim]["money"] = 0
    
def a_work():
    worker = choice(list(people.keys()))
    money = 1
    people[worker]["money"] += money
    
    return f'{worker} made {money} currency working. (total {people[worker]["money"]})'

def a_wanderer():
    speaker = choice(list(people.keys()))

    return f'A wandering tribe went by, and {speaker} told them Folklore.'

def a_talk():
    global people
    topics = [
        'Lorus',
        'genocide',
        'war',
        'laws',
        'the current news',
        'religion',
        'hope',
        'suicide prevention',
        choice(list(people.keys()))
    ]

    speaker = choice(list(people.keys()))

    return f'{speaker} spoke publicly about {choice(topics)}.'

def a_settlers():
    global people
    global generations
        
    attacker = choice(list(people.keys()))
    amount = randint(2, 5)
    names = []        

    for _ in range(amount):
        baby = gen_name().strip()
        names.append(baby)
        people[baby] = u_preset()
    return f"{amount} settlers joined the society. ({', '.join(names)})"
            
def a_terror():
    global people
    
    attacker = choice(list(people.keys()))
    kills = randint(1, 10)
    victims = []    
    actual_kills = 0

    for _ in range(kills):
        if len(people) <= 1:
            break

        victim = choice(list(people.keys()))
        if victim != attacker:
            victims.append(victim)
            steal(attacker, victim)
            kill(victim)
            actual_kills += 1
    people[attacker]['kills'] += actual_kills
    
    return f"{attacker} killed {actual_kills} people. ({', '.join(victims)})"

def a_free():
    return 'Nothing happened this generation.'

def kill(person):
    global people
    global afterlife
    
    people[person]['died'] = generations
    afterlife[person] = people[person]
    people.pop(person)

def gen_name():
    options = ['ka', 're', 'ku', 'so', 'fa', 'si', 'di', 'to', 
'ne', 'ko', 'shi', 'rok', 'knet', 'loru', 'ca', 'me', ' ']
    name = ''
    for i in range(randint(1, 5)):
        name = name + choice(options)
    
    return name     

def a_baby():
    global people
    global generations
    
    giver1 = choice(list(people.keys()))
    giver2 = choice(list(people.keys()))
    
    baby = gen_name().strip()
    
    people[baby] = u_preset()
    if random() <= 0.2:
        baby2 = gen_name().strip()
        people[baby2] = u_preset()

        if giver1 == giver2:
            return f'{giver1} found two babies and named them {baby} and {baby2}.'
        else:
            return f'{giver1} and {giver2} had two babies together and named them {baby} and {baby2}.'
    
    if giver1 == giver2:
        return f'{giver1} found a baby and named it {baby}.'
    else:
        return f'{giver1} and {giver2} had a baby together and named it {baby}.' 

def a_order():
    global law
    global people
    
    congress = choice(list(people.keys()))
    if not law:
        law = True
        return f'{congress} reinstated laws.'
    else:
        law = False
        return f'{congress} revoked laws.'

def a_murder():
    global people
    global afterlife

    attacker = choice(list(people.keys()))
    victim = choice(list(people.keys()))

    if attacker == victim:
        kill(attacker)
        return f'{attacker} killed themselves.'
        
    elif law and len(people) <= 3:
        filtered = [x for x in people if x not in (attacker, victim)]
        if filtered: 
            cop = choice(filtered)
        
            people[attacker]['kills'] += 1
            steal(attacker, victim)
            people[cop]['kills'] += 1
            steal(cop, attacker)
            kill(attacker)
            kill(victim)
            return f'{attacker} killed {victim}, and {cop} executed them for it.'
        else:
            return a_free()
    else:
        steal(attacker, victim)
        kill(victim)
        people[attacker]['kills'] += 1
        return f'{attacker} killed {victim}.'

# .ACTIONS
 
actions = [
    a_murder,
    a_order,
    a_baby,
    a_free,
    a_terror,
    a_settlers,
    a_talk,
    a_wanderer,
    a_work,
    a_journey,
    a_breakdown,
    a_poetry,
    a_cry
]        

# .GENERATION

def generation():
    global actions
    
    return choice(actions)()

# .MAIN

def main():
    global people
    global afterlife
    global generations
    global history

    print('\n' * 5)

    print('PYTHON SOCIETY PROGRAM\n')
    number_of_people = int(input('# of people: '))
    for i in range(number_of_people):
        name = input(f'name #{i+1}: ')
        people[name] = u_preset()

    peak = number_of_people    

    while len(people) > 0:
        if Mod.enabled:
            [i() for i in Mod.before]
        
        generations += 1
        peak = max(peak, len(people))
        
        history.append(f'{generations}: {generation()}')
        u_run_info(history[-1], people)
        
        if Mod.enabled:
            [i() for i in Mod.after]
    
    u_run_info(f'Everybody died. It took {generations} generations for it to happen. The peak was {peak}.', afterlife)
    
    print('\n' * 5)
    if input('Copy history to clipboard? (Y or N) ').upper() == 'Y':
        copy(json.dumps(afterlife, indent=4) + json.dumps(history, indent=4))

# .MODS

class Mod:
    before = []
    after = []
    enabled = False
    
    @classmethod
    def action(cls, func):
        global actions
        actions.append(func)
        return func
    @classmethod
    def mod_after(cls, func):
        cls.after.append(func)
        return func
    @classmethod
    def mod_before(cls, func):
        cls.before.append(func)
        return func
    @classmethod
    def clear_actions(cls):
        global actions
        actions = []
    @classmethod
    def replace_action(cls, func, func2):
        global actions
        for i in range(len(actions)):
            if actions[i] == func:
                actions[i] = func2
    @classmethod
    def change_person(cls, new_stats):
        global u_preset
        def u_preset():
            global generations
            
            return new_stats
    @classmethod
    def safety():
        return len(people) > 0

if __name__ == '__main__':
    main()
