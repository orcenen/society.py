 # when you look at this code i just want you to know that you should not change how the lines and formatted code works thanks :))
# Lorus is the first sign that people can live past 60. His infuence is in this code.

from random import choice, randint, random
from pyperclip import copy
import curses, json

people = {}
afterlife = {}
generations = 0
history = []

law = False

color = True

def info(stdscr, action, people):
    global law
    global color    

    if color:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        
        color = not color
    
    stdscr.erase()

    title = 'PYTHON SOCIETY PROGRAM'

    height, width = stdscr.getmaxyx()
    x = (width - len(title)) // 2

    stdscr.addstr(0, x, title, curses.color_pair(1))
    
    stdscr.addstr(3, 0, action)
    
    if people:
        formatted = "\n".join(f"| {key}: {value}" for key, value in people.items())
        lines = formatted.splitlines()
        lines = lines[:max(0, height - 4)]
    else:
        formatted = "| "
    
    lines = formatted.splitlines() if isinstance(formatted, str) else formatted

    stdscr.addstr(5, 0, f"PEOPLE: {len(people)}")
    
    max_lines = height - 10
    lines = lines[:max_lines]
    
    for i, line in enumerate(lines):
        stdscr.addstr(6 + i, 0, line)
    
    footer_y = 6 + len(lines) + 1
    stdscr.addstr(footer_y, 0, 'Laws are in action.' if law else 'There are no laws.')
    stdscr.addstr(footer_y + 2, 0, 'Press any key to continue.')
    
    line_lengths = [len(line) for line in lines]
    max_length = max(line_lengths)

    stdscr.refresh()
    stdscr.getch()
    
def run_info(action, people):
    curses.wrapper(lambda stdscr: info(stdscr, action or 'No action.', people))

def wanderer():
    speaker = choice(list(people.keys()))

    return f'A wandering tribe went by, and {speaker} told them Folklore..'

def talk():
    global people
    topics = [
        'Lorus',
        'genocide',
        'war',
        'laws',
        'the current news',
        'religion'
    ]

    speaker = choice(list(people.keys()))

    return f'{speaker} spoke publicly about {choice(topics)}.'


def settlers():
    global people
    global generations
        
    attacker = choice(list(people.keys()))
    amount = randint(2, 5)
        
    for _ in range(amount):
        baby = gen_name().strip()
        people[baby] = {
            'kills': 0,
            'born': generations
        }
    return f'{amount} settlers joined the society.'
            
def terror():
    global people
    
    attacker = choice(list(people.keys()))
    kills = randint(1, 10)
    
    for _ in range(kills):
        victim = choice(list(people.keys()))
        if victim != attacker:
            kill(victim)
        else:
            kills -= 1
    people[attacker]['kills'] += kills
    return f'{attacker} killed {kills} people.'

def free():
    return 'Nothing happened this generation.'

def kill(person):
    global people
    global afterlife
    
    afterlife[person] = people[person]
    people.pop(person)

def gen_name():
    options = ['ka', 're', 'ku', 'so', 'fa', 'si', 'di', 'to', 
'ne', 'ko', 'shi', 'rok', 'knet', 'loru' ' ']
    name = ''
    for i in range(randint(1, 5)):
        name = name + choice(options)
    
    return name     

def baby():
    global people
    global generations
    
    giver1 = choice(list(people.keys()))
    giver2 = choice(list(people.keys()))
    
    baby = gen_name().strip()
    
    people[baby] = {
        'kills': 0,
        'born': generations
    }
    if random() <= 0.2:
        baby2 = gen_name().strip()
        people[baby2] = {
            'kills': 0,
            'born': generations
        }

        if giver1 == giver2:
            return f'{giver1} found two babies and named them {baby} and {baby2}.'
        else:
            return f'{giver1} and {giver2} had two babies together and named them {baby} and {baby2}.'
    
    if giver1 == giver2:
        return f'{giver1} found a baby and named it {baby}.'
    else:
        return f'{giver1} and {giver2} had a baby together and named it {baby}.'
    

def order():
    global law
    global people
    
    congress = choice(list(people.keys()))
    if law == False:
        law = True
        return f'{congress} reinstated laws.'
    else:
        law = False
        return f'{congress} revoked laws.'

def murder():
    global people
    global afterlife

    attacker = choice(list(people.keys()))
    victim = choice(list(people.keys()))

    if attacker == victim:
        kill(attacker)
        return f'{attacker} killed themselves.'
        
    elif law == True and len(people) <= 3:
        filtered = [x for x in people if x not in (attacker, victim)]
        if filtered: 
            cop = choice(filtered)
        
            people[attacker]['kills'] += 1
            people[cop]['kills'] += 1
            kill(attacker)
            kill(victim)
            return f'{attacker} killed {victim}, and {cop} executed them for it.'
        else:
            return free()
    else:
        kill(victim)
        people[attacker]['kills'] += 1
        return f'{attacker} killed {victim}.'
        

def generation():
    actions = [
        murder,
        order,
        baby,
        free,
        terror,
        settlers,
        talk,
        wanderer
    ]
    return choice(actions)()

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
        people[name] = {
            "kills": 0,
            "born": 1
        }

    peak = number_of_people    

    while len(people) > 0:
        generations += 1
        peak = max(peak, len(people))
        history.append(f'{generations}: {generation()}')
        run_info(history[-1], people)
    
    run_info(f'Everybody died. It took {generations} generations for it to happen. The peak was {peak}.', afterlife)
    
    print('\n' * 5)
    if input('Copy history to clipboard? (Y or N) ').upper() == 'Y':
        copy(json.dumps(afterlife, indent=4) + json.dumps(history, indent=4))

if __name__ == '__main__':
    main()
