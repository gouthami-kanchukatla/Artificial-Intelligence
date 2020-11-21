# wumpus_kb.py
# ------------
# Licensing Information:
# Please DO NOT DISTRIBUTE OR PUBLISH solutions to this project.
# You are free to use and extend these projects for EDUCATIONAL PURPOSES ONLY.
# The Hunt The Wumpus AI project was developed at University of Arizona
# by Clay Morrison (clayton@sista.arizona.edu), spring 2013.
# This project extends the python code provided by Peter Norvig as part of
# the Artificial Intelligence: A Modern Approach (AIMA) book example code;
# see http://aima.cs.berkeley.edu/code.html
# In particular, the following files come directly from the AIMA python
# code: ['agents.py', 'logic.py', 'search.py', 'utils.py']
# ('logic.py' has been modified by Clay Morrison in locations with the
# comment 'CTM')
# The file ['minisat.py'] implements a slim system call wrapper to the minisat
# (see http://minisat.se) SAT solver, and is directly based on the satispy
# python project, see https://github.com/netom/satispy .

import utils

#-------------------------------------------------------------------------------
# Wumpus Propositions
#-------------------------------------------------------------------------------

### atemporal variables

proposition_bases_atemporal_location = ['P', 'W', 'S', 'B']

def pit_str(x, y):
    "There is a Pit at <x>,<y>"
    return 'P{0}_{1}'.format(x, y)
def wumpus_str(x, y):
    "There is a Wumpus at <x>,<y>"
    return 'W{0}_{1}'.format(x, y)
def stench_str(x, y):
    "There is a Stench at <x>,<y>"
    return 'S{0}_{1}'.format(x, y)
def breeze_str(x, y):
    "There is a Breeze at <x>,<y>"
    return 'B{0}_{1}'.format(x, y)

### fluents (every proposition who's truth depends on time)

proposition_bases_perceptual_fluents = ['Stench', 'Breeze', 'Glitter', 'Bump', 'Scream']

def percept_stench_str(t):
    "A Stench is perceived at time <t>"
    return 'Stench{0}'.format(t)
def percept_breeze_str(t):
    "A Breeze is perceived at time <t>"
    return 'Breeze{0}'.format(t)
def percept_glitter_str(t):
    "A Glitter is perceived at time <t>"
    return 'Glitter{0}'.format(t)
def percept_bump_str(t):
    "A Bump is perceived at time <t>"
    return 'Bump{0}'.format(t)
def percept_scream_str(t):
    "A Scream is perceived at time <t>"
    return 'Scream{0}'.format(t)

proposition_bases_location_fluents = ['OK', 'L']

def state_OK_str(x, y, t):
    "Location <x>,<y> is OK at time <t>"
    return 'OK{0}_{1}_{2}'.format(x, y, t)
def state_loc_str(x, y, t):
    "At Location <x>,<y> at time <t>"
    return 'L{0}_{1}_{2}'.format(x, y, t)

def loc_proposition_to_tuple(loc_prop):
    """
    Utility to convert location propositions to location (x,y) tuples
    Used by HybridWumpusAgent for internal bookkeeping.
    """
    parts = loc_prop.split('_')
    return (int(parts[0][1:]), int(parts[1]))

proposition_bases_state_fluents = ['HeadingNorth', 'HeadingEast',
                                   'HeadingSouth', 'HeadingWest',
                                   'HaveArrow', 'WumpusAlive']

def state_heading_north_str(t):
    "Heading North at time <t>"
    return 'HeadingNorth{0}'.format(t)
def state_heading_east_str(t):
    "Heading East at time <t>"
    return 'HeadingEast{0}'.format(t)
def state_heading_south_str(t):
    "Heading South at time <t>"
    return 'HeadingSouth{0}'.format(t)
def state_heading_west_str(t):
    "Heading West at time <t>"
    return 'HeadingWest{0}'.format(t)
def state_have_arrow_str(t):
    "Have Arrow at time <t>"
    return 'HaveArrow{0}'.format(t)
def state_wumpus_alive_str(t):
    "Wumpus is Alive at time <t>"
    return 'WumpusAlive{0}'.format(t)

proposition_bases_actions = ['Forward', 'Grab', 'Shoot', 'Climb',
                             'TurnLeft', 'TurnRight', 'Wait']

def action_forward_str(t=None):
    "Action Forward executed at time <t>"
    return ('Forward{0}'.format(t) if t != None else 'Forward')
def action_grab_str(t=None):
    "Action Grab executed at time <t>"
    return ('Grab{0}'.format(t) if t != None else 'Grab')
def action_shoot_str(t=None):
    "Action Shoot executed at time <t>"
    return ('Shoot{0}'.format(t) if t != None else 'Shoot')
def action_climb_str(t=None):
    "Action Climb executed at time <t>"
    return ('Climb{0}'.format(t) if t != None else 'Climb')
def action_turn_left_str(t=None):
    "Action Turn Left executed at time <t>"
    return ('TurnLeft{0}'.format(t) if t != None else 'TurnLeft')
def action_turn_right_str(t=None):
    "Action Turn Right executed at time <t>"
    return ('TurnRight{0}'.format(t) if t != None else 'TurnRight')
def action_wait_str(t=None):
    "Action Wait executed at time <t>"
    return ('Wait{0}'.format(t) if t != None else 'Wait')


def add_time_stamp(prop, t): return '{0}{1}'.format(prop, t)

proposition_bases_all = [proposition_bases_atemporal_location,
                         proposition_bases_perceptual_fluents,
                         proposition_bases_location_fluents,
                         proposition_bases_state_fluents,
                         proposition_bases_actions]


#-------------------------------------------------------------------------------
# Axiom Generator: Current Percept Sentence
#-------------------------------------------------------------------------------

#def make_percept_sentence(t, tvec):
def axiom_generator_percept_sentence(t, tvec):

    """
    Asserts that each percept proposition is True or False at time t.

    t := time
    tvec := a boolean (True/False) vector with entries corresponding to
            percept propositions, in this order:
                (<stench>,<breeze>,<glitter>,<bump>,<scream>)

    Example:
        Input:  [False, True, False, False, True]
        Output: '~Stench0 & Breeze0 & ~Glitter0 & ~Bump0 & Scream0'
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"###############################################################################
    
    # default percepts
    percepts_list = ['Stench','Breeze','Glitter','Bump','Scream']         
    
    percept_status = []


    for ele in range(len(tvec)):

        # upon percept is true
        if tvec[ele] == True:
            percept_status.append(percepts_list[ele]+str(t))  
        else:                 
            #add conditions with negation
            percept_status.append('~'+percepts_list[ele]+str(t))  
    
    axiom_str = ' & '.join( percept_status ) 
                                       
    return axiom_str                                             


#-------------------------------------------------------------------------------
# Axiom Generators: Initial Axioms
#-----------------------------------


#-------------------------------------------------------------------------------
# Axiom Generator: Current Percept Sentence
#-------------------------------------------------------------------------------

#def make_percept_sentence(t, tvec):
def axiom_generator_percept_sentence(t, tvec):
    """
    Asserts that each percept proposition is True or False at time t.

    t := time
    tvec := a boolean (True/False) vector with entries corresponding to
            percept propositions, in this order:
                (<stench>,<breeze>,<glitter>,<bump>,<scream>)

    Example:
        Input:  [False, True, False, False, True]
        Output: '~Stench0 & Breeze0 & ~Glitter0 & ~Bump0 & Scream0'
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"###############################################################################



    # default percepts
    percepts_list = ['Stench','Breeze','Glitter','Bump','Scream']         

    percept_status = []


    for ele in range(len(tvec)):

    # upon percept is true
        if tvec[ele] == True:
            percept_status.append(percepts_list[ele]+str(t))  
        else:                 
        #add conditions with negation
            percept_status.append('~'+percepts_list[ele]+str(t))  

    axiom_str = ' & '.join( percept_status ) 
                   
    return axiom_str                                             


#-------------------------------------------------------------------------------
# Axiom Generators: Initial Axioms
#-------------------------------------------------------------------------------

def axiom_generator_initial_location_assertions(x, y):
    """
    Assert that there is no Pit and no Wumpus in the location

    x,y := the location
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"###################################################################################

    # storing not pit and not wumpus: ( not pit(x,y) ) and ( not wumpus(x,y) )
    str_pit = pit_str(x, y)
    str_wumpus  = wumpus_str(x, y)

    axiom_str =  axiom_str + '(~' + str_pit + ')' + ' & (~' + str_wumpus + ')'

    return axiom_str


def axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax):
    """
    Assert that Breezes (atemporal) are only found in locations where
    there are one or more Pits in a neighboring location (or the same location!)

    x,y := the location
    xmin, xmax, ymin, ymax := the bounds of the environment; you use these
           variables to 'prune' any neighboring locations that are outside
           of the environment (and therefore are walls, so can't have Pits).
    """
    axiom_str = ''

    "*** YOUR CODE HERE ***"#####################################################################################

    adjacent_to_pit = []

    #check  the  pits in the enivornment :
    # applying  Breeze (x , y)  <=>  Pit( x+1,y ) or Pit( x-1,y ) | Pit( x,y+1 ) | Pit( x,y-1 ) | Pit( x,y )

    for (m,n) in [ ((x-1),y), (x,(y-1)), ((x+1),y),(x,(y+1)) ]:   

        if ( (n <= ymax) and (n >= ymin)  and ( m >= xmin ) and ( m <= xmax )) : adjacent_to_pit.append(pit_str(m,n))
            
    adjacent_to_pit.append('P'+str(x)+'_'+str(y))

    i = '{0} <=> ({1})'
    j = ' | '

    # merge the locations of pits  and breeze
    axiom_str = i.format( breeze_str(x,y),  j.join(adjacent_to_pit) )  

    return (axiom_str)

def generate_pit_and_breeze_axioms(xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_pits_and_breezes')
    return axioms

def axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax):
    """
    Assert that Stenches (atemporal) are only found in locations where
    there are one or more Wumpi in a neighboring location (or the same location!)

    (Don't try to assert here that there is only one Wumpus;
    we'll handle that separately)

    x,y := the location
    xmin, xmax, ymin, ymax := the bounds of the environment; you use these
           variables to 'prune' any neighboring locations that are outside
           of the environment (and therefore are walls, so can't have Wumpi).
    """
    axiom_str = ''

    "*** YOUR CODE HERE ***"
    # Stench(x,y) <=> Wumpus(x+1,y) or Wumpus(x-1,y) | Wumpus(x,y+1) | Wumpus(x,y-1) | Wumpus(x,y)
    
    if  x >  xmax or x < xmin:
        return axiom_str

    if  y > ymax or y < ymin:
        return axiom_str

    axiom_str =  stench_str( x , y )  +  " <=> ( "
    special_char = ' | '

    #Going through all the negihbouring tiles
    if (  ( xmin <=  x + 1 <= xmax ) and ( ymin  <= y  <= ymax ) ):
        axiom_str =  axiom_str + wumpus_str(x + 1, y) + special_char

    if ((  xmin <= x - 1 <= xmax ) and ( ymin <= y <= ymax )):
        axiom_str = axiom_str + wumpus_str( x - 1, y) + special_char

    if (( xmin <= x <= xmax) and (ymin <= y - 1 <= ymax)):
        axiom_str = axiom_str + wumpus_str( x, y - 1) + special_char

    if ((xmin <= x <= xmax) and (ymin <= y + 1 <= ymax)):
        axiom_str = axiom_str  + wumpus_str( x, y + 1) + special_char

    axiom_str = axiom_str +  wumpus_str(x, y)
    axiom_str = axiom_str  + ' ) '
    return axiom_str

def generate_wumpus_and_stench_axioms(xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_wumpus_and_stench')
    return axioms

def axiom_generator_at_least_one_wumpus(xmin, xmax, ymin, ymax):
    """
    Assert that there is at least one Wumpus.

    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
   
    "*** YOUR CODE HERE ***"######################################################################################

    squares = [ wumpus_str( x_val , y_val ) for x_val in range( xmin, xmax + 1) for y_val in range( ymin , ymax + 1)]  #checking the boundary conditions

    axiom_str = ' | '.join(  squares )   #merging the wumpus locations

    return(axiom_str)


def axiom_generator_at_most_one_wumpus(xmin, xmax, ymin, ymax):
    """
    Assert that there is at at most one Wumpus.

    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    
    "*** YOUR CODE HERE ***"########################################################################################
    
    max_pos =   max(xmax,ymax)
    mul = xmax*ymax
    for num in range(0, mul):
        for ele in range(num+1, mul):  
            x =    int(num/max_pos) + 1
            y =    int(num%max_pos) + 1
            i =    int(ele/max_pos) + 1
            j =    int(ele%max_pos) + 1
            
            statement = "(~" + wumpus_str(x, y) + " | " + "~" + wumpus_str(i,j) + ")" #iterating the loop to go through all the different combinations
            if axiom_str == '':
                axiom_str = statement
            else:
                axiom_str = axiom_str + '&' + statement
    return(axiom_str)     #returning the merged condition

def axiom_generator_only_in_one_location(xi, yi, xmin, xmax, ymin, ymax, t = 0):
    """
    Assert that the Agent can only be in one (the current xi,yi) location at time t.

    xi,yi := the current location.
    xmin, xmax, ymin, ymax := the bounds of the environment.
    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"#############################################################################################

    not_squares  = ['~' +  state_loc_str( x_val, y_val, t) for x_val in range( xmin, xmax+1 ) for y_val in range(ymin,ymax+1)]
    curr_square = ( '~L'+str(xi)+'_'+str(yi)+'_'+str(t) )                           #
    not_squares.remove(curr_square)

    st_1 = 'L{0}_{1}_{2}'.format( xi, yi, t )

    #if the agent is  in one location => the  agent  is  not available in other location
    st_2 = '{0}'.format(' & '.join(not_squares))  
    axiom_str = st_1 + " & " + st_2
    return(axiom_str) 

def axiom_generator_only_one_heading(heading = 'north', t = 0):
    """
    Assert that Agent can only head in one direction at a time.

    heading := string indicating heading; default='north';
               will be one of: 'north', 'east', 'south', 'west'
    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"#############################################################################

    not_headings = []
    all_headings = [ 'North','South','East','West']

    for header in all_headings:

        if header.upper() == heading.upper():
            axiom_str =  axiom_str+'Heading{0}{1} & ('.format(header,str(t))
        else:
            not_headings.append( '~Heading' + header + str(t))
    
    axiom_str += '{0} )'.format('&'.join(not_headings))
    return axiom_str

def axiom_generator_have_arrow_and_wumpus_alive(t = 0):
    """
    Assert that Agent has the arrow and the Wumpus is alive at time t.

    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"#####################################################################

    #merging the state_have_arrow_str and  state_wumpus_alive_str outputs of logical conditions
    axiom_str =' {0} & {1} '.format(state_have_arrow_str(t),state_wumpus_alive_str(t))  

    return(axiom_str)


def initial_wumpus_axioms(xi, yi, width, height, heading='east'):
    """
    Generate all of the initial wumpus axioms
    
    xi,yi = initial location
    width,height = dimensions of world
    heading = str representation of the initial agent heading
    """
    axioms = [axiom_generator_initial_location_assertions(xi, yi)]
    axioms.extend(generate_pit_and_breeze_axioms(1, width, 1, height))
    axioms.extend(generate_wumpus_and_stench_axioms(1, width, 1, height))
    
    axioms.append(axiom_generator_at_least_one_wumpus(1, width, 1, height))
    axioms.append(axiom_generator_at_most_one_wumpus(1, width, 1, height))

    axioms.append(axiom_generator_only_in_one_location(xi, yi, 1, width, 1, height))
    axioms.append(axiom_generator_only_one_heading(heading))

    axioms.append(axiom_generator_have_arrow_and_wumpus_alive())
    
    return axioms


#-------------------------------------------------------------------------------
# Axiom Generators: Temporal Axioms (added at each time step)
#-------------------------------------------------------------------------------

def axiom_generator_location_OK(x, y, t):
    """
    Assert the conditions under which a location is safe for the Agent.
    (Hint: Are Wumpi always dangerous?)

    x,y := location
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"#######################################################################################changesss
    

    #status of wumpus being alive 
    wum_status = state_wumpus_alive_str(t) 

    # position  of the wumpus
    wum_pos = wumpus_str(x,y)  

     # condition  of the state        
    state_status = state_OK_str(x,y,t) 

    #condition of the pit 
    pit_status  = pit_str(x,y)           

    axiom_str =  '{0} <=> (~{1} & ({3} >> ~{2}))'.format(state_status,pit_status,wum_status,wum_pos)      #merging the conditions
    return(axiom_str)


def generate_square_OK_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_location_OK(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_location_OK')
    return filter(lambda s: s != '', axioms)


#-------------------------------------------------------------------------------
# Connection between breeze / stench percepts and atemporal location properties

def axiom_generator_breeze_percept_and_location_property(x, y, t):
    """
    Assert that when in a location at time t, then perceiving a breeze
    at that time (a percept) means that the location is breezy (atemporal)

    x,y := location
    t := time
    """
    axiom_str = ''

    "*** YOUR CODE HERE ***"

    axiom_str =  '{0} >> ({1} <=> {2})'.format( state_loc_str(x,y,t) , percept_breeze_str(t) , breeze_str(x,y) )

    return axiom_str


def generate_breeze_percept_and_location_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_breeze_percept_and_location_property(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_breeze_percept_and_location_property')
    return filter(lambda s: s != '', axioms)

def axiom_generator_stench_percept_and_location_property(x, y, t):
    """
    Assert that when in a location at time t, then perceiving a stench
    at that time (a percept) means that the location has a stench (atemporal)

    x,y := location
    t := time
    """
    axiom_str = ''

    #stench Percept
    stench_percept=percept_stench_str(t)       
    
    #stench Location
    str_stench=stench_str(x,y)             
    
    #State  Location
    state_loc=state_loc_str(x,y,t)        
    
    axiom_str = '{0} >> ({1} <=> {2})'.format(state_loc,stench_percept,str_stench) #merging the conditions 

    return(axiom_str)

def generate_stench_percept_and_location_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_stench_percept_and_location_property(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_stench_percept_and_location_property')
    return filter(lambda s: s != '', axioms)


#-------------------------------------------------------------------------------
# Transition model: Successor-State Axioms (SSA's)
# Avoid the frame problem(s): don't write axioms about actions, write axioms about
# fluents!  That is, write successor-state axioms as opposed to effect and frame
# axioms
#
# The general successor-state axioms pattern (where F is a fluent):
#   F^{t+1} <=> (Action(s)ThatCause_F^t) | (F^t & ~Action(s)ThatCauseNot_F^t)

# NOTE: this is very expensive in terms of generating many (~170 per axiom) CNF clauses!
def axiom_generator_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax):
    """
    Assert the condidtions at time t under which the agent is in
    a particular location (state_loc_str: L) at time t+1, following
    the successor-state axiom pattern.

    See Section 7. of AIMA.  However...
    NOTE: the book's version of this class of axioms is not complete
          for the version in Project 3.
    
    x,y := location
    t := time
    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    moves = ['({0} & (~{1} | {2} | {3} | {4} | {5} | {6}))'.format( state_loc_str(x,y,t),  action_forward_str(t),  percept_bump_str(t+1), 
        action_grab_str(t), action_shoot_str(t), action_turn_left_str(t),  action_turn_right_str(t))]

    # evalute the location, direction of the  previous percepts
    for ((x_val,y_val), direction ) in [(((x-1),y),'E'),((x,(y-1)),'N'),(((x+1),y),'W'),((x,(y+1)),'S')]: 
        
        if  x_val >= xmin  and  y_val >= ymin and x_val <= xmax  and y_val <= ymax:

            #North
            if direction == 'N': moves.append('({0} & ({1} & {2}))'.format(state_loc_str(x,y-1,t),state_heading_north_str(t),action_forward_str(t)))
            #South  
            if direction == 'S': moves.append('({0} & ({1} & {2}))'.format(state_loc_str(x,y+1,t),state_heading_south_str(t),action_forward_str(t)))
            #East   
            if direction == 'E': moves.append('({0} & ({1} & {2}))'.format(state_loc_str(x - 1, y, t), state_heading_east_str(t), action_forward_str(t)))
            #West 
            if direction == 'W': moves.append('({0} & ({1} & {2}))'.format(state_loc_str(x + 1, y, t), state_heading_west_str(t), action_forward_str(t)))  
            
    
    statement =  state_loc_str(x,y,t+1)
    axiom_str = '{0} <=> ({1})'.format(statement,' | '.join(moves))
    return axiom_str

def generate_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax, heading):
    """
    The full at_location SSA converts to a fairly large CNF, which in
    turn causes the KB to grow very fast, slowing overall inference.
    We therefore need to restric generating these axioms as much as possible.
    This fn generates the at_location SSA only for the current location and
    the location the agent is currently facing (in case the agent moves
    forward on the next turn).
    This is sufficient for tracking the current location, which will be the
    single L location that evaluates to True; however, the other locations
    may be False or Unknown.
    """
    axioms = [axiom_generator_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax)]
    if heading == 'west' and x - 1 >= xmin:
        axioms.append(axiom_generator_at_location_ssa(t, x-1, y, xmin, xmax, ymin, ymax))
    if heading == 'east' and x + 1 <= xmax:
        axioms.append(axiom_generator_at_location_ssa(t, x+1, y, xmin, xmax, ymin, ymax))
    if heading == 'south' and y - 1 >= ymin:
        axioms.append(axiom_generator_at_location_ssa(t, x, y-1, xmin, xmax, ymin, ymax))
    if heading == 'north' and y + 1 <= ymax:
        axioms.append(axiom_generator_at_location_ssa(t, x, y+1, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_at_location_ssa')
    return filter(lambda s: s != '', axioms)

#----------------------------------

def axiom_generator_have_arrow_ssa(t):
    """
    Assert the conditions at time t under which the Agent
    has the arrow at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    arrow_state_1 =  state_have_arrow_str(t)
    arrow_state_2 = state_have_arrow_str(t+1)

    shoot_action = action_shoot_str(t)


    axiom_str = '{0} <=> ({1} & ~{2})'.format(arrow_state_2,arrow_state_1,shoot_action)
    return(axiom_str)

def axiom_generator_wumpus_alive_ssa(t):
    """
    Assert the conditions at time t under which the Wumpus
    is known to be alive at time t+1

    (NOTE: If this axiom is implemented in the standard way, it is expected
    that it will take one time step after the Wumpus dies before the Agent
    can infer that the Wumpus is actually dead.)

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    # wumpus being alive state at previous percepts
    w_state_1=state_wumpus_alive_str(t)         
    w_state_2=state_wumpus_alive_str(t+1) 
    # wumpus scream  state   
    scream_status=percept_scream_str(t+1)          
    axiom_str = '{0} <=> ({1} & ~{2})'.format(w_state_2,w_state_1,scream_status) 
    return(axiom_str)


#----------------------------------


def axiom_generator_heading_north_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be North at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

   

    #wait action
    a_1 = action_wait_str(t)
    #grab the gold
    a_2 = action_grab_str(t) 
    #shoot the arrow         
    a_3 = action_shoot_str(t)
    #forward action
    a_4 = action_forward_str(t)        
    #heading to north
    s_1 = state_heading_north_str(t)
    #checking the bump   
    p_1 = percept_bump_str(t+1)        


    # action heading  to the  east and turn left
    e=state_heading_east_str(t)
    l=action_turn_left_str(t)
    left = '({0} & {1})'.format(e,l)

    # action heading  to the  west and turn right
    w =state_heading_west_str(t)
    r=action_turn_right_str(t)
    right = '({0} & {1})'.format(w,r)
    
    no_move = '({0} & ({1} | {2} | {3} | {4} | {5}))'.format(s_1,a_1,a_2,a_3,p_1,a_4) 
    axiom_str = '{0} <=> ({1} | {2} | {3})'.format(state_heading_north_str(t+1),no_move,left,right)
    return(axiom_str)

def axiom_generator_heading_east_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be East at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    #wait action
    a_1=action_wait_str(t) 
    #grab the gold
    a_2=action_grab_str(t)
    #shoot the arrow         
    a_3=action_shoot_str(t)
    #forward action
    a_4=action_forward_str(t) 

    #heading east
    s_1=state_heading_east_str(t) 

    #checking the bump   
    p_1=percept_bump_str(t+1) 


    # action heading  to the  north and turn right

    n=state_heading_north_str(t)
    r=action_turn_right_str(t)
    right = '({0} & {1})'.format(n,r) 

    # action heading  to the south and turn left

    s=state_heading_south_str(t)
    l=action_turn_left_str(t)
    left = '({0} & {1})'.format(s,l)
    
    no_move = '({0} & ({1} | {2} | {3} | {4} | {5}))'.format(s_1,a_1,a_2,a_3,p_1,a_4) #merging all the conditions as it moved to north
    axiom_str = '{0} <=> ({1} | {2} | {3})'.format(state_heading_east_str(t+1),no_move,left,right) #merging the conditions
    return(axiom_str)

def axiom_generator_heading_south_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be South at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    #wait action
    a_1=action_wait_str(t) 
    #grab the gold
    a_2=action_grab_str(t)
    #shoot the arrow         
    a_3=action_shoot_str(t)
    #forward action
    a_4=action_forward_str(t) 

    #heading south
    s_1=state_heading_south_str(t)
    #bump percept
    p_1=percept_bump_str(t+1) 

    # action heading  to the  east and turn right

    e=state_heading_east_str(t)
    r=action_turn_right_str(t)
    right = '({0} & {1})'.format(e,r) 

    # action heading  to the  west and turn left

    w=state_heading_west_str(t)
    l=action_turn_left_str(t)
    left = '({0} & {1})'.format(w,l) 
    

    no_move = '({0} & ({1} | {2} | {3} | {4} | {5}))'.format(s_1,a_1,a_2,a_3,p_1,a_4) 
    axiom_str = '{0} <=> ({1} | {2} | {3})'.format(state_heading_south_str(t+1),no_move,left,right) 
    return(axiom_str)

def axiom_generator_heading_west_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be West at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
     #wait action
    a_1=action_wait_str(t) 
    #grab the gold
    a_2=action_grab_str(t)
    #shoot the arrow         
    a_3=action_shoot_str(t)
    #forward action
    a_4=action_forward_str(t) 

    #heading west
    s_1=state_heading_west_str(t) 
    #bump percept
    p_1=percept_bump_str(t+1)

    # action heading  to the  south and turn right

    s=state_heading_south_str(t)
    r=action_turn_right_str(t)
    right = '({0} & {1})'.format(s,r) 

    # action heading  to the  north and turn left

    n=state_heading_north_str(t)
    l=action_turn_left_str(t)
    left = '({0} & {1})'.format(n,l) 
    

    no_move = '({0} & ({1} | {2} | {3} | {4} | {5}))'.format(s_1,a_1,a_2,a_3,p_1,a_4) 
    axiom_str = '{0} <=> ({1} | {2} | {3})'.format(state_heading_west_str(t+1),no_move,left,right) 
    return(axiom_str)

def generate_heading_ssa(t):
    """
    Generates all of the heading SSAs.
    """
    return [axiom_generator_heading_north_ssa(t),
            axiom_generator_heading_east_ssa(t),
            axiom_generator_heading_south_ssa(t),
            axiom_generator_heading_west_ssa(t)]

def generate_non_location_ssa(t):
    """
    Generate all non-location-based SSAs
    """
    axioms = [] # all_state_loc_ssa(t, xmin, xmax, ymin, ymax)
    axioms.append(axiom_generator_have_arrow_ssa(t))
    axioms.append(axiom_generator_wumpus_alive_ssa(t))
    axioms.extend(generate_heading_ssa(t))
    return filter(lambda s: s != '', axioms)

#----------------------------------

def axiom_generator_heading_only_north(t):
    """
    Assert that when heading is North, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    n=state_heading_north_str(t) #heading north
    s=state_heading_south_str(t) #heading south
    e=state_heading_east_str(t) #heading east
    w=state_heading_west_str(t) #heading west
    
    axiom_str =  '{0} <=> (~{1} & ~{2} & ~{3})'.format( n, s, e, w) #merging the conditions
    return(axiom_str)

def axiom_generator_heading_only_east(t):
    """
    Assert that when heading is East, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"


    #heading to the  north
    n=state_heading_north_str(t)
    #heading to the  south 
    s=state_heading_south_str(t)
    #heading to the  east 
    e=state_heading_east_str(t) 
    #heading to the west
    w=state_heading_west_str(t) 

    axiom_str = '{0} <=> (~{1} & ~{2} & ~{3})'.format(e,s,n,w) 
    return(axiom_str)

def axiom_generator_heading_only_south(t):
    """
    Assert that when heading is South, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    #heading to the  north
    n=state_heading_north_str(t)
    #heading to the  south 
    s=state_heading_south_str(t)
    #heading to the  east 
    e=state_heading_east_str(t) 
    #heading to the west
    w=state_heading_west_str(t) 

    axiom_str = '{0} <=> (~{1} & ~{2} & ~{3})'.format(s,n,e,w) #merging the conditions
    return(axiom_str)
    

def axiom_generator_heading_only_west(t):
    """
    Assert that when heading is West, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    #heading to the  north
    n=state_heading_north_str(t)
    #heading to the  south 
    s=state_heading_south_str(t)
    #heading to the  east 
    e=state_heading_east_str(t) 
    #heading to the west
    w=state_heading_west_str(t) 

    axiom_str = '{0} <=> (~{1} & ~{2} & ~{3})'.format(w,s,e,n) #merging the conditions
    return(axiom_str)
    
def generate_heading_only_one_direction_axioms(t):
    return [axiom_generator_heading_only_north(t),
            axiom_generator_heading_only_east(t),
            axiom_generator_heading_only_south(t),
            axiom_generator_heading_only_west(t)]


def axiom_generator_only_one_action_axioms(t):
    """
    Assert that only one axion can be executed at a time.
    
    t := time
    """
    axiom_str = ''
   
    "*** YOUR CODE HERE ***"

    axioms_list = []

    #possible actions
    defined_actions= [action_forward_str(t), action_grab_str(t), action_shoot_str(t), action_climb_str(t), action_turn_left_str(t), action_turn_right_str(t), action_wait_str(t)]
    
    for i in range(0, len(defined_actions)):
        for j in range(i+1, len(defined_actions)):
            #append the logical statements
            axioms_list.append("(~" + defined_actions[i] + "|~" + defined_actions[j] + ")") 

    axiom_str = "("+ '|'.join(defined_actions) + ")&"
    axiom_str = axiom_str+ "(" + ' & '.join(axioms_list) + ")"
    return(axiom_str) 


def generate_mutually_exclusive_axioms(t):
    """
    Generate all time-based mutually exclusive axioms.
    """
    axioms = []
    
    # must be t+1 to constrain which direction could be heading _next_
    axioms.extend(generate_heading_only_one_direction_axioms(t + 1))

    # actions occur in current time, after percept
    axioms.append(axiom_generator_only_one_action_axioms(t))

    return filter(lambda s: s != '', axioms)

#-------------------------------------------------------------------------------
