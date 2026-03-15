from random import choice
from random import randint
import curses

people = {}
afterlife = {}
generations = 0

law = False

def info(stdscr, action, people): # wip, not implemented yet
    global law
    
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

    stdscr.clear()

    title = 'PYTHON SOCIETY PROGRAM'

    height, width = stdscr.getmaxyx()
    x = (width - len(title)) // 2

    stdscr.addstr(0, x, title, curses.color_pair(1))
    
    stdscr.addstr(3, 0, action)
    
    if people:
        formatted = "\n".join(f"| {key}: {value}" for key, value in people.items())
        if len(formatted.splitlines()) > height:
            formatted = formatted.split('\n')[:-4+height]
    else:
        formatted = "| "

    stdscr.addstr(5, 0, f"""PEOPLE:
{formatted}
    
{'Laws are in action.' if law else 'There are no laws.'}
    
Press any key to continue. """)
    
    if not formatted is list:
        lines = formatted.splitlines()
    else:
        lines = formatted
    line_lengths = [len(line) for line in lines]
    max_length = max(line_lengths)

    for i in range(len(line_lengths)):
        stdscr.addstr(i+6, max_length, '|')

    stdscr.refresh()
    stdscr.getch()
    
def run_info(action, people):
    curses.wrapper(lambda stdscr: info(stdscr, action or 'No action.', people))

def free():
    return 'Nothing happened this generation.'

def kill(person):
    global people
    global afterlife
    
    afterlife[person] = people[person]
    people.pop(person)

def gen_name():
    options = ['ka', 're', 'ku', 'so', 'fa', 'si', 'di', 'to', 
'ne', 'ko', ' ']
    name = ''
    for i in range(randint(1, 10)):
        name = name + choice(options)
    
    return name     

def baby():
    global people
    global generations
    
    giver1 = choice(list(people.keys()))
    giver2 = choice(list(people.keys()))
    
    baby = gen_name()
    
    people[baby] = {
        'kills': 0,
        'born': generations
    }
    
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
        return f'{attacker} killed themself.'
        
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
        free
    ]
    return choice(actions)()

def main():
    global people
    global afterlife
    global generations

    print('python society program')
    number_of_people = int(input('number of people: '))
    for i in range(number_of_people):
        name = input(f'Name for founder {i+1}: ')
        people[name] = {
            "kills": 0,
            "born": 1
        }

    peak = number_of_people    

    while len(people) > 0:
        generations += 1
        peak = max(peak, len(people))
        run_info(generation(), people)
    
    run_info(f'Everybody died. It took {generations} generations for it to happen. The peak was {peak}.', afterlife)

if __name__ == '__main__':
    main()
